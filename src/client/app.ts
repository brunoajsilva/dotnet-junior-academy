/**
 * Browser entry point. The page arrives fully rendered (Astro); this script loads the module data,
 * draws the page again with the learner's progress and wires up the interactions.
 */
import type { AcademyModule } from "../content/schema";
import { routeUrl, setBaseUrl } from "../lib/html";
import { loadProgress } from "../lib/progress";
import { createRenderContext } from "../lib/render/context";
import { buildSite } from "../lib/site";
import { bindEvents } from "./events";
import { renderCurrentPage, renderMenus } from "./render";

async function start(): Promise<void> {
  const baseUrl = document.documentElement.dataset.base ?? "/";
  setBaseUrl(baseUrl);
  const routeId = document.body.dataset.route ?? "";

  const response = await fetch(`${baseUrl}data/modules.json`);
  if (!response.ok) throw new Error(`data/modules.json: HTTP ${response.status}`);
  const site = buildSite((await response.json()) as AcademyModule[]);

  // old bookmarks used #route-id on a single page
  const legacyRouteId = location.hash.replace(/^#/, "");
  if (!routeId && legacyRouteId && site.routeById(legacyRouteId)) {
    location.replace(routeUrl(legacyRouteId));
    return;
  }

  const context = createRenderContext(site, loadProgress(), routeId);
  bindEvents(context);
  // pages that are not part of the course (search) keep the content they came with
  if (!routeId || site.routeById(routeId)) renderCurrentPage(context);
  else renderMenus(context);
  document.documentElement.dataset.ready = "1";
}

start().catch((error) => {
  console.error(error);
  document.documentElement.dataset.ready = "error";
});
