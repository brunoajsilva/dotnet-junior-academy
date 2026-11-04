/**
 * Draws the page in the browser. The server already rendered the same HTML without the learner's
 * progress; drawing it again here adds what is saved in localStorage.
 */
import { rewriteHashLinks } from "../lib/html";
import { saveProgress, sectionSeenKey } from "../lib/progress";
import { resetPageState, type RenderContext } from "../lib/render/context";
import {
  renderModuleSwitcher,
  renderProgressPill,
  renderSideMenu,
} from "../lib/render/navigation";
import { renderPage } from "../lib/render/page";
import { query } from "./dom";

export function renderMenus(context: RenderContext): void {
  query("#side").innerHTML = rewriteHashLinks(renderSideMenu(context));
  query("#modnav").innerHTML = rewriteHashLinks(renderModuleSwitcher(context));
  query("#pill").innerHTML = renderProgressPill(context);
}

/** Opening an introduction section counts as having read it. */
function markIntroSectionAsSeen(context: RenderContext): void {
  const target = context.site.routeById(context.currentRouteId)?.target;
  if (target?.kind === "section") context.progress.seen[sectionSeenKey(target.section.id)] = 1;
}

export function renderCurrentPage(context: RenderContext): void {
  resetPageState(context);
  markIntroSectionAsSeen(context);
  query("#main").innerHTML = rewriteHashLinks(renderPage(context));
  if (context.currentRouteId) context.progress.lastRoute = context.currentRouteId;
  saveProgress(context.progress);
  renderMenus(context);
}
