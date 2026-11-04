/**
 * Introduction module: its sections and the content blocks inside them.
 */
import type { IntroBlock, IntroModule, IntroSection, Tool } from "../../../content/schema";
import { ARROW_ICON, TICK_ICON, escapeHtml, renderEach } from "../../html";
import { moduleProgress } from "../../progress";
import { sectionRouteId } from "../../site";
import { renderMoreButton } from "../blocks";
import { registerDrawer, type RenderContext } from "../context";
import {
  moduleColour,
  renderBreadcrumb,
  renderPager,
  renderProgressBar,
  renderSummaryCard,
} from "../shared";

const REQUIREMENT_LABELS: Record<Tool["requirement"], string> = {
  required: "necessário",
  optional: "opcional",
  later: "mais tarde",
};

function renderCardGrid(context: RenderContext, cards: readonly IntroCardLike[], idPrefix: string): string {
  const cardsHtml = renderEach(cards, (card, index) => renderSummaryCard(context, card, `${idPrefix}${index}`));
  return `<div class="cgrid">${cardsHtml}</div>`;
}

type IntroCardLike = Parameters<typeof renderSummaryCard>[1];

function renderOutcomes(context: RenderContext, outcomes: Extract<IntroBlock, { type: "outcomes" }>["outcomes"], idPrefix: string): string {
  return renderEach(outcomes, (outcome, index) => {
    const target = context.site.moduleById(outcome.moduleId);
    if (!target) throw new Error(`outcome '${outcome.title}': unknown module '${outcome.moduleId}'`);
    const drawerKey = `${idPrefix}${index}`;
    registerDrawer(context, drawerKey, outcome.title, outcome.learnMore && { learnMore: outcome.learnMore });
    return (
      `<div class="outc" style="--mc:var(--c-${outcome.moduleId})"><span class="n">${target.number}</span><div>` +
      `<h4>${escapeHtml(outcome.title)}</h4><p>${escapeHtml(outcome.summary)}</p>` +
      `<button class="more" data-action="open-drawer" data-key="${drawerKey}">Saber mais${ARROW_ICON}</button> ` +
      `<a class="minibtn" style="display:inline-flex;align-items:center;margin-top:10px;text-decoration:none" href="#${context.site.firstRouteId(target)}">Ir para o módulo</a>` +
      `</div></div>`
    );
  });
}

function renderCoursePlan(context: RenderContext): string {
  const moduleLinks = (module: (typeof context.site.modules)[number]): string[] => {
    switch (module.kind) {
      case "intro":
        return module.sections.map(
          (section) => `<li><a href="#${sectionRouteId(module, section.id)}">${escapeHtml(section.title)}</a></li>`,
        );
      case "course":
        return module.chapters.map(
          (chapter, index) => `<li><a href="#${chapter.id}">${index + 1} · ${escapeHtml(chapter.title)}</a></li>`,
        );
      case "project":
        return module.phases.map(
          (phase, index) => `<li><a href="#${module.id}-${phase.id}">${index + 1} · ${escapeHtml(phase.title)}</a></li>`,
        );
    }
  };
  const modules = renderEach(
    context.site.modules,
    (module) =>
      `<div class="pm" style="--mc:var(--c-${module.id})"><h4><span class="n">${module.number}</span>${escapeHtml(module.title)}</h4>` +
      `<ul>${moduleLinks(module).join("")}</ul></div>`,
  );
  return `<div class="plan blk">${modules}</div>`;
}

function renderSchedule(context: RenderContext, weeks: Extract<IntroBlock, { type: "schedule" }>["weeks"]): string {
  const totalDays = weeks.reduce((total, week) => total + week.days.length, 0);
  const renderItem = (item: (typeof weeks)[number]["days"][number]["items"][number]): string => {
    if (!context.site.moduleById(item.moduleId)) throw new Error(`schedule '${item.title}': unknown module '${item.moduleId}'`);
    if (item.routeId && !context.site.routeById(item.routeId)) throw new Error(`schedule '${item.title}': unknown route '${item.routeId}'`);
    const title = item.routeId ? `<a href="#${item.routeId}">${escapeHtml(item.title)}</a>` : escapeHtml(item.title);
    const detail = item.detail ? `<p>${escapeHtml(item.detail)}</p>` : "";
    return `<li style="--mc:var(--c-${item.moduleId})"><span class="dot"></span><div><b>${title}</b>${detail}</div></li>`;
  };
  const renderDay = (day: (typeof weeks)[number]["days"][number]): string =>
    `<div class="sday"><span class="sd"><small>Dia</small>${day.day}</span><ul>${renderEach(day.items, renderItem)}</ul></div>`;
  const renderWeek = (week: (typeof weeks)[number]): string =>
    `<section class="sweek"><h3>${escapeHtml(week.title)}<span>${week.days.length} dias úteis</span></h3>${renderEach(week.days, renderDay)}</section>`;
  return `<div class="blk schedule" aria-label="Cronograma de ${totalDays} dias úteis">${renderEach(weeks, renderWeek)}</div>`;
}

function renderToolVerification(tool: Tool): string {
  if (tool.checkCommand) {
    return (
      `<div class="cmd"><code>${escapeHtml(tool.checkCommand)}</code>` +
      `<button class="minibtn" data-action="copy-text" data-value="${escapeHtml(tool.checkCommand)}">Copiar</button>` +
      `<span class="exp">→ ${escapeHtml(tool.expectedResult)}</span></div>`
    );
  }
  if (tool.expectedResult) {
    return `<div class="cmd"><span class="exp">Verificar: ${escapeHtml(tool.expectedResult)}</span></div>`;
  }
  return "";
}

function renderSoftwareChecklist(context: RenderContext, tools: readonly Tool[]): string {
  const items = renderEach(tools, (tool) => {
    const drawerKey = `sw:${tool.id}`;
    const installed = Boolean(context.progress.installedTools[tool.id]);
    registerDrawer(context, drawerKey, tool.name, tool.learnMore && { learnMore: tool.learnMore });
    return (
      `<div class="swi${installed ? " ok" : ""}"><button class="chk" data-action="toggle-tool" data-key="${tool.id}" ` +
      `aria-pressed="${installed}" aria-label="Marcar ${escapeHtml(tool.name)} como instalado">${TICK_ICON}</button><div>` +
      `<h4>${escapeHtml(tool.name)} <span class="chip ${tool.requirement}">${REQUIREMENT_LABELS[tool.requirement]}</span></h4>` +
      `<p>${escapeHtml(tool.reason)}</p>${renderToolVerification(tool)}` +
      `<p style="margin-top:6px"><b>Instalar:</b> ${escapeHtml(tool.installation)}</p>` +
      `<div class="acts">${renderMoreButton(drawerKey, "Saber mais")}</div></div></div>`
    );
  });
  return `<div class="blk sw">${items}</div>`;
}

function renderIntroBlock(context: RenderContext, block: IntroBlock, blockId: string): string {
  switch (block.type) {
    case "paragraph":
      return `<p class="blk prose">${escapeHtml(block.text)}</p>`;
    case "cards": {
      const title = block.title ? `<h3>${escapeHtml(block.title)}</h3>` : "";
      return `<div class="blk">${title}${renderCardGrid(context, block.cards, `b:${blockId}`)}</div>`;
    }
    case "steps":
      return `<div class="blk">${renderCardGrid(context, block.steps, `b:${blockId}`)}</div>`;
    case "outcomes":
      return `<div class="blk">${renderOutcomes(context, block.outcomes, `b:${blockId}`)}</div>`;
    case "plan":
      return renderCoursePlan(context);
    case "schedule":
      return renderSchedule(context, block.weeks);
    case "software":
      return renderSoftwareChecklist(context, block.tools);
  }
}

export function renderIntroSection(context: RenderContext, module: IntroModule, section: IntroSection): string {
  const isFirstSection = section === module.sections[0];
  const header =
    `<header class="ph" style="${moduleColour(module)}"><p class="eyebrow">Módulo ${module.number} · ${escapeHtml(module.title)}</p>` +
    `<h1>${escapeHtml(section.title)}</h1>` +
    (isFirstSection ? `<p class="lead">${escapeHtml(module.tagline)}</p>` : "") +
    `${renderProgressBar(moduleProgress(context.progress, module))}</header>`;
  const blocks = renderEach(section.blocks, (block, index) =>
    renderIntroBlock(context, block, `${section.id}${index}`),
  );
  return (
    renderBreadcrumb(context, module, section.title) +
    header +
    `<div style="${moduleColour(module)}">${blocks}</div>` +
    renderPager(context, sectionRouteId(module, section.id))
  );
}
