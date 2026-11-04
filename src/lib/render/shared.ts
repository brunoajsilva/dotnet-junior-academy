/**
 * Pieces shared by the pages: progress bar, previous/next links, breadcrumb and the "Saber mais" card.
 */
import type { AcademyModule, SummaryCard } from "../../content/schema";
import { ARROW_ICON, escapeHtml } from "../html";
import type { Percentage } from "../progress";
import { registerDrawer, type RenderContext } from "./context";

export function renderProgressBar(progress: Percentage): string {
  return (
    `<div class="barrow"><div class="bar"><i style="width:${progress.percent}%"></i></div>` +
    `<span>${progress.done} de ${progress.total}</span></div>`
  );
}

/** Links to the previous and next page, in reading order. */
export function renderPager(context: RenderContext, routeId: string): string {
  const { routes } = context.site;
  const index = routes.findIndex((route) => route.id === routeId);
  const previous = routes[index - 1];
  const next = routes[index + 1];

  let links = "";
  if (!previous) links += '<a href="#"><small>Anterior</small><span>Início</span></a>';
  if (previous) {
    links += `<a href="#${previous.id}"><small>Anterior</small><span>${escapeHtml(previous.title)}</span></a>`;
  }
  if (next) {
    links += `<a class="nx" href="#${next.id}"><small>Seguinte</small><span>${escapeHtml(next.title)}</span></a>`;
  }
  return `<nav class="pager" aria-label="Navegação entre páginas">${links}</nav>`;
}

export function renderBreadcrumb(context: RenderContext, module: AcademyModule, lastLabel?: string): string {
  const moduleLink = `<a href="#${context.site.firstRouteId(module)}">Módulo ${module.number}</a>`;
  const last = lastLabel ? `<span>/</span><span>${escapeHtml(lastLabel)}</span>` : "";
  return `<div class="crumb"><a href="#">Início</a><span>/</span>${moduleLink}${last}</div>`;
}

/** A card whose button opens its "Saber mais" drawer. */
export function renderSummaryCard(context: RenderContext, card: SummaryCard, drawerKey: string): string {
  registerDrawer(context, drawerKey, card.title, card.learnMore && { learnMore: card.learnMore });
  return (
    `<button class="cardbtn" data-action="open-drawer" data-key="${escapeHtml(drawerKey)}">` +
    `<h4>${escapeHtml(card.title)}</h4><p>${escapeHtml(card.summary)}</p>` +
    `<span class="go">Saber mais${ARROW_ICON}</span></button>`
  );
}

/** Opening of every module page: the coloured header with title, lead and progress. */
export function moduleColour(module: AcademyModule): string {
  return `--mc:var(--c-${module.id})`;
}
