/**
 * Smoke test of the built site (run `npm run build` first; `npm test` does both).
 *
 * Serves dist/ the way GitHub Pages would, opens every page on desktop and mobile and checks:
 * no script errors, one h1, no sideways scroll, the page finished loading, and the main interactions
 * (mark as seen, quiz, "Saber mais" drawer, progress surviving a reload, architecture layers).
 */
import { createReadStream, existsSync, statSync } from "node:fs";
import { readdir } from "node:fs/promises";
import { createServer } from "node:http";
import type { AddressInfo } from "node:net";
import { extname, join, normalize } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium, type Page } from "playwright";
import { base } from "../site.config.mjs";

const DIST_DIRECTORY = fileURLToPath(new URL("../dist/", import.meta.url));
if (!existsSync(join(DIST_DIRECTORY, "index.html"))) {
  console.error("dist/ not found: run `npm run build` first.");
  process.exit(1);
}

const CONTENT_TYPES: Record<string, string> = {
  ".html": "text/html",
  ".js": "text/javascript",
  ".css": "text/css",
  ".json": "application/json",
};
const IGNORED_CONSOLE_ERRORS = /fonts\.(googleapis|gstatic)|ERR_(TUNNEL|NAME|INTERNET)|Failed to load resource/;
const NOT_COURSE_PAGES = new Set(["_astro", "pagefind", "data"]);

const server = createServer((request, response) => {
  const path = decodeURIComponent(new URL(request.url ?? "/", "http://localhost").pathname);
  if (!path.startsWith(base)) return void response.writeHead(404).end();
  let file = normalize(join(DIST_DIRECTORY, path.slice(base.length)));
  if (!file.startsWith(DIST_DIRECTORY)) return void response.writeHead(403).end();
  if (existsSync(file) && statSync(file).isDirectory()) file = join(file, "index.html");
  if (!existsSync(file)) return void response.writeHead(404).end("not found");
  response.writeHead(200, { "Content-Type": CONTENT_TYPES[extname(file)] ?? "application/octet-stream" });
  createReadStream(file).pipe(response);
});
await new Promise<void>((resolve) => server.listen(0, resolve));
const origin = `http://localhost:${(server.address() as AddressInfo).port}${base}`;

async function listRoutes(): Promise<string[]> {
  const routes = [""];
  for (const entry of await readdir(DIST_DIRECTORY, { withFileTypes: true })) {
    const isPage = entry.isDirectory() && existsSync(join(DIST_DIRECTORY, entry.name, "index.html"));
    if (isPage && !NOT_COURSE_PAGES.has(entry.name)) routes.push(entry.name);
  }
  return routes;
}

const problems: string[] = [];
const fail = (message: string): void => void problems.push(message);

async function waitUntilReady(page: Page, description: string): Promise<void> {
  await page
    .waitForFunction(() => document.documentElement.dataset.ready, null, { timeout: 8000 })
    .catch(() => fail(`${description}: did not finish loading`));
  if ((await page.evaluate(() => document.documentElement.dataset.ready)) === "error") {
    fail(`${description}: script failed while loading`);
  }
}

async function checkStoryModal(page: Page): Promise<void> {
  await page.goto(`${origin}projeto-p3/`);
  await waitUntilReady(page, "projeto-p3");
  const isOpen = () => page.evaluate(() => document.querySelector(".smodal:not([hidden])") !== null);

  await page.click('[data-action="open-story"]');
  if (!(await isOpen())) fail("the user story modal did not open");

  // a click on the dimmed area closes it
  await page.mouse.click(4, 4);
  if (await isOpen()) fail("clicking outside the user story modal did not close it");

  // the details drawer opens above the modal, and Esc closes the top one first
  await page.click('[data-action="open-story"]');
  await page.click('.smodal:not([hidden]) [data-action="open-drawer"]');
  await page.keyboard.press("Escape");
  if (!(await isOpen())) fail("Esc closed the modal together with the drawer");
  await page.keyboard.press("Escape");
  if (await isOpen()) fail("Esc did not close the user story modal");
}

async function checkInteractions(page: Page): Promise<void> {
  await page.goto(`${origin}csharp-1/`);
  await waitUntilReady(page, "csharp-1");
  await page.click('.lesson [data-action="toggle-seen"]');
  await page.click('[data-action="answer"][data-question="0"][data-option="1"]');
  await page.click('[data-action="open-drawer"]');
  if (!(await page.evaluate(() => document.querySelector("#drawer")?.classList.contains("on")))) {
    fail("the drawer did not open");
  }
  await page.keyboard.press("Escape");

  await page.reload();
  await waitUntilReady(page, "csharp-1 after reload");
  const kept = await page.evaluate(() => ({
    seenLessons: document.querySelectorAll(".lesson.seen").length,
    rightAnswers: document.querySelectorAll(".opt.right").length,
  }));
  if (kept.seenLessons < 1) fail("progress (seen) did not survive a reload");
  if (kept.rightAnswers < 1) fail("the quiz answer did not survive a reload");

  await checkStoryModal(page);

  await page.goto(`${origin}projeto/`);
  await waitUntilReady(page, "projeto");
  if (await page.$('[data-action="select-layer"]')) {
    const before = await page.innerHTML("#arch");
    await page.click('[data-action="select-layer"]:not([aria-pressed="true"])');
    if (before === (await page.innerHTML("#arch"))) fail("clicking an architecture layer had no effect");
  }
}

const browser = await chromium.launch();
const routes = await listRoutes();
let pagesChecked = 0;

for (const [deviceName, width] of [["desktop", 1280], ["mobile", 400]] as const) {
  const context = await browser.newContext({ viewport: { width, height: 900 } });
  const page = await context.newPage();
  page.on("pageerror", (error) => fail(`${deviceName}: script error: ${error.message}`));
  page.on("console", (message) => {
    if (message.type() === "error" && !IGNORED_CONSOLE_ERRORS.test(message.text())) {
      fail(`${deviceName}: console error: ${message.text()}`);
    }
  });

  for (const route of routes) {
    const description = `${deviceName} ${route || "home"}`;
    await page.goto(origin + (route ? `${route}/` : ""));
    await waitUntilReady(page, description);
    pagesChecked++;

    const measurements = await page.evaluate(() => ({
      horizontalOverflow: document.documentElement.scrollWidth - innerWidth,
      headingCount: document.querySelectorAll("#main h1").length,
      hashLinks: document.querySelectorAll('#main a[href^="#"], #side a[href^="#"]').length,
    }));
    if (measurements.headingCount !== 1) fail(`${description}: expected one h1, found ${measurements.headingCount}`);
    if (measurements.horizontalOverflow > 1) fail(`${description}: horizontal overflow ${measurements.horizontalOverflow}px`);
    if (measurements.hashLinks > 0) fail(`${description}: ${measurements.hashLinks} link(s) still use #hash`);
  }

  if (deviceName === "desktop") await checkInteractions(page);
  await context.close();
}

if (!existsSync(join(DIST_DIRECTORY, "pagefind", "pagefind.js"))) {
  fail("pagefind index is missing (run the full build)");
}

await browser.close();
server.close();
console.log(`${pagesChecked} pages checked`);
if (problems.length > 0) {
  console.error([...new Set(problems)].join("\n"));
  process.exit(1);
}
console.log("OK");
