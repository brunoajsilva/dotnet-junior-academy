/**
 * Navigation: the module switcher in the top bar and the side menu (modules, chapters, project days).
 */
import type { AcademyModule } from "../../content/schema";
import { escapeHtml, renderEach, LOGO_MARK } from "../html";
import { moduleProgress, overallPercent, routeStatus } from "../progress";
import type { Route } from "../site";
import type { RenderContext } from "./context";
import { moduleColour } from "./shared";

const STATUS_CLASS = ["", "part", "full"] as const;

function renderMenuItem(context: RenderContext, route: Route, label = route.title, nested = false): string {
  const status = STATUS_CLASS[routeStatus(context.progress, context.site, route.id)];
  const current = route.id === context.currentRouteId ? "cur" : "";
  return (
    `<li${nested ? ' class="nest"' : ""}><a href="#${route.id}" class="${current}">` +
    `<span class="d ${status}"></span><span>${escapeHtml(label)}</span></a></li>`
  );
}

/** Routes titled "Dia 2 · User stories" are listed under a "Dia 2" heading. */
function renderRoutesGroupedByDay(context: RenderContext, routes: Route[]): string {
  let html = "";
  let lastDay = "";
  for (const route of routes) {
    const match = /^(Dias? [^·]+?) · (.+)$/.exec(route.title);
    if (match) {
      const [, day, label] = match;
      if (day !== lastDay) {
        html += `<li class="dgh">${escapeHtml(day)}</li>`;
        lastDay = day;
      }
      html += renderMenuItem(context, route, label, true);
    } else {
      html += renderMenuItem(context, route);
      lastDay = "";
    }
  }
  return html;
}

const isTrainerSession = (route: Route) =>
  route.target.kind === "phase" && !route.target.module.phases[route.target.phaseIndex].day;

function renderModuleMenu(context: RenderContext, module: AcademyModule): string {
  const routes = context.site.menuRoutes(module);
  const trainerRoutes = routes.filter(isTrainerSession);
  const otherRoutes = routes.filter((route) => !isTrainerSession(route));

  if (!trainerRoutes.length) return renderEach(otherRoutes, (route) => renderMenuItem(context, route));
  return (
    `<li class="gh">Com o formador</li>${renderEach(trainerRoutes, (route) => renderMenuItem(context, route))}` +
    `<li class="gsep"></li>${renderRoutesGroupedByDay(context, otherRoutes)}`
  );
}

function currentModule(context: RenderContext): AcademyModule | undefined {
  const route = context.site.routeById(context.currentRouteId);
  return route && context.site.moduleById(route.moduleId);
}

function renderCurrentModuleContext(context: RenderContext, current: AcademyModule | undefined): string {
  const { site, progress } = context;
  if (current) {
    const { done, total, percent } = moduleProgress(progress, current);
    return (
      `<div class="ctx" style="${moduleColour(current)}"><p class="eyebrow">Módulo ${current.number}</p>` +
      `<h2 class="ctitle"><a href="#${site.firstRouteId(current)}">${escapeHtml(current.shortTitle)}</a></h2>` +
      `<div class="cbar"><i style="width:${percent}%"></i></div><p class="cmeta">${done} de ${total} concluídos</p>` +
      `<ul class="sub">${renderModuleMenu(context, current)}</ul></div>`
    );
  }
  const modules = renderEach(
    site.modules,
    (module) =>
      `<li><a href="#${site.firstRouteId(module)}" style="${moduleColour(module)}"><span class="n">${module.number}</span>` +
      `<span>${escapeHtml(module.shortTitle)}</span><span class="pc">${moduleProgress(progress, module).percent}%</span></a></li>`,
  );
  return `<div class="ctx"><p class="eyebrow">Módulos</p><ul class="mlist">${modules}</ul></div>`;
}

function renderAllModules(context: RenderContext, current: AcademyModule | undefined): string {
  const { site, progress } = context;
  const overall = overallPercent(progress, site);
  const header =
    `<div class="nav-head"><button class="brand" data-go-to-route="" aria-label=".NET Backend Academy, página inicial">` +
    `${LOGO_MARK}<span class="wm"><b>.NET</b> Backend Academy</span></button><div class="nav-prog"><div class="bar"><i style="width:${overall}%"></i></div>` +
    `<span>${overall}%</span></div><a class="side-search" href="#pesquisa">Pesquisar</a></div>`;
  const modules = renderEach(site.modules, (module) => {
    const isCurrent = module === current;
    const submenu = isCurrent ? `<ul class="sub">${renderModuleMenu(context, module)}</ul>` : "";
    return (
      `<div class="mod${isCurrent ? " cur" : ""}" style="${moduleColour(module)}"><a href="#${site.firstRouteId(module)}">` +
      `<span class="n">${module.number}</span><span class="t">${escapeHtml(module.shortTitle)}</span>` +
      `<span class="pc">${moduleProgress(progress, module).percent}%</span></a>${submenu}</div>`
    );
  });
  return header + modules;
}

export function renderSideMenu(context: RenderContext): string {
  const current = currentModule(context);
  return `<div class="side-ctx">${renderCurrentModuleContext(context, current)}</div><div class="side-all">${renderAllModules(context, current)}</div>`;
}

/** The module buttons at the top of the page, with a thin progress line each. */
export function renderModuleSwitcher(context: RenderContext): string {
  const current = currentModule(context);
  return renderEach(context.site.modules, (module) => {
    const { percent } = moduleProgress(context.progress, module);
    return (
      `<a href="#${context.site.firstRouteId(module)}" class="${module === current ? "cur" : ""}" ` +
      `style="${moduleColour(module)};--p:${percent / 100}" title="${escapeHtml(module.shortTitle)} · ${percent}%">` +
      `<span class="n">${module.number}</span><span class="t">${escapeHtml(module.shortTitle)}</span><i></i></a>`
    );
  });
}

export function renderProgressPill(context: RenderContext): string {
  return `Progresso <b>${overallPercent(context.progress, context.site)}%</b>`;
}
