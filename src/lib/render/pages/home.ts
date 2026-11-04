import type { AcademyModule } from "../../../content/schema";
import { ARROW_ICON, escapeHtml, renderEach } from "../../html";
import { moduleProgress } from "../../progress";
import type { RenderContext } from "../context";
import { moduleColour } from "../shared";

function describeContents(module: AcademyModule): string {
  switch (module.kind) {
    case "course": {
      const lessonCount = module.chapters.reduce((total, chapter) => total + chapter.lessons.length, 0);
      return `${module.chapters.length} capítulos · ${lessonCount} temas`;
    }
    case "intro":
      return `${module.sections.length} secções · checklist de software`;
    case "project":
      return `${module.phases.length} fases · 6 dias`;
  }
}

function renderModuleCard(context: RenderContext, module: AcademyModule): string {
  const { percent } = moduleProgress(context.progress, module);
  return (
    `<a class="mcard" href="#${context.site.firstRouteId(module)}" style="${moduleColour(module)}">` +
    `<span class="k">Módulo ${module.number}</span><h3>${escapeHtml(module.title)}</h3><p>${escapeHtml(module.tagline)}</p>` +
    `<span class="meta">${describeContents(module)}</span>` +
    `<span class="go"><span class="bar"><i style="width:${percent}%;background:var(--mc)"></i></span><span>${percent}%</span></span></a>`
  );
}

export function renderHomePage(context: RenderContext): string {
  const { site, progress } = context;
  const lastRoute = progress.lastRoute ? site.routeById(progress.lastRoute) : undefined;
  const continueLink = lastRoute
    ? `<a class="btn" href="#${lastRoute.id}">Continuar: ${escapeHtml(lastRoute.title)}</a>`
    : "";
  const firstModule = site.modules[0];

  const hero =
    `<section class="hero"><p class="eyebrow">Backend · .NET 10</p><h1>Aprende .NET a escrever código.</h1>` +
    `<p>Cinco módulos, do primeiro programa em C# a uma API segura com Clean Architecture. Cada tema abre mais detalhe quando precisares dele.</p>` +
    `<div class="cta"><a class="btn pri" href="#${site.firstRouteId(firstModule)}">Começar pela Academia${ARROW_ICON}</a>${continueLink}</div></section>`;

  return hero + `<div class="mods">${renderEach(site.modules, (module) => renderModuleCard(context, module))}</div>`;
}
