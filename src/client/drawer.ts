/** The "Saber mais" drawer (explanations and user stories) and the mobile menu. */
import { escapeHtml, renderParagraphs, rewriteHashLinks } from "../lib/html";
import type { DrawerContent, RenderContext } from "../lib/render/context";
import { renderStoryDetails } from "../lib/render/project/story-details";
import { query } from "./dom";

let elementThatOpenedDrawer: Element | null = null;

function renderDrawerContent(context: RenderContext, content: DrawerContent): string {
  if ("storyDetails" in content) {
    context.openStoryDetails = content.storyDetails;
    return renderStoryDetails(content.storyDetails);
  }
  const { explanation, pitfall, tryIt } = content.learnMore;
  return (
    renderParagraphs(explanation) +
    (pitfall ? `<div class="callout pit"><b>Armadilha frequente</b>${escapeHtml(pitfall)}</div>` : "") +
    (tryIt ? `<div class="callout try"><b>Experimenta</b>${escapeHtml(tryIt)}</div>` : "")
  );
}

export function openDrawer(context: RenderContext, key: string): void {
  const entry = context.drawerEntries.get(key);
  if (!entry) return;

  query("#drBody").innerHTML = rewriteHashLinks(
    `<h2 id="drTitle">${escapeHtml(entry.title)}</h2>${renderDrawerContent(context, entry.content)}`,
  );
  query("#drawer").classList.add("on");
  query("#drScrim").classList.add("on");
  query("#drawer").setAttribute("aria-hidden", "false");
  elementThatOpenedDrawer = document.activeElement;
  query("#drClose").focus();
  query("#drBody").scrollTop = 0;
}

export function isDrawerOpen(): boolean {
  return query("#drawer").classList.contains("on");
}

export function closeDrawer(): void {
  if (!query("#drawer").classList.contains("on")) return;
  query("#drawer").classList.remove("on");
  query("#drScrim").classList.remove("on");
  query("#drawer").setAttribute("aria-hidden", "true");
  if (elementThatOpenedDrawer instanceof HTMLElement && document.contains(elementThatOpenedDrawer)) {
    elementThatOpenedDrawer.focus();
  }
}

export function closeSideMenu(): void {
  query("#side").classList.remove("on");
  query("#scrim").classList.remove("on");
  query("#menuBtn").setAttribute("aria-expanded", "false");
}

export function toggleSideMenu(): void {
  const opening = !query("#side").classList.contains("on");
  query("#side").classList.toggle("on", opening);
  query("#scrim").classList.toggle("on", opening);
  query("#menuBtn").setAttribute("aria-expanded", String(opening));
}
