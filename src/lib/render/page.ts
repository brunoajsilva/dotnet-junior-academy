/**
 * Page builder shared by the static build and the browser: given a route it returns the HTML of
 * the main column. Internal links are written as "#route-id" (see html.ts).
 */
import { renderChapter, renderModuleOverview } from "./pages/course";
import { renderHomePage } from "./pages/home";
import { renderIntroSection } from "./pages/intro";
import type { RenderContext } from "./context";
import { renderFinalDelivery, renderPhase, renderProjectOverview } from "./project/pages";

export function renderPage(context: RenderContext): string {
  const route = context.site.routeById(context.currentRouteId);
  if (!route) return renderHomePage(context);

  const { target } = route;
  switch (target.kind) {
    case "section":
      return renderIntroSection(context, target.module, target.section);
    case "chapter":
      return renderChapter(context, target.module, target.chapterIndex);
    case "phase":
      return renderPhase(context, target.module, target.phaseIndex);
    case "finalDelivery":
      return renderFinalDelivery(context, target.module);
    case "moduleOverview":
      return target.module.kind === "course"
        ? renderModuleOverview(context, target.module)
        : renderProjectOverview(context, target.module);
  }
}

export function pageTitle(context: RenderContext): string {
  const route = context.site.routeById(context.currentRouteId);
  return `${route ? `${route.title} · ` : ""}.NET Backend Academy`;
}
