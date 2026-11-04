/**
 * Final project pages: overview, guided phases and the final delivery page.
 */
import type { Phase, ProjectModule } from "../../../content/schema";
import { TICK_ICON, escapeHtml, renderEach } from "../../html";
import { phaseSeenKey } from "../../progress";
import { finalDeliveryRouteId, phaseRouteId } from "../../site";
import { renderMoreButton, renderTable } from "../blocks";
import { registerDrawer, type RenderContext } from "../context";
import {
  moduleColour,
  renderBreadcrumb,
  renderPager,
  renderProgressBar,
  renderSummaryCard,
} from "../shared";
import { moduleProgress } from "../../progress";
import { renderArchitecture, renderDays, renderRequestFlow } from "./architecture";
import { renderRelatedLessons } from "./user-story";
import { renderPhaseSection, renderPhaseTrees } from "./files";
import { renderFeatureGroups, renderPlanBar } from "./plan";

const pageHeader = (module: ProjectModule, eyebrow: string, title: string, lead: string, extra = "") =>
  `<header class="ph" style="${moduleColour(module)}"><p class="eyebrow">${eyebrow}</p><h1>${escapeHtml(title)}</h1>` +
  `<p class="lead">${escapeHtml(lead)}</p>${extra}</header><div style="${moduleColour(module)}">`;

const numberedList = (items: readonly string[]) =>
  `<ol class="ol">${renderEach(items, (item) => `<li><span>${escapeHtml(item)}</span></li>`)}</ol>`;

/* -------------------------------------------------------------- overview */

function renderPhaseCard(context: RenderContext, module: ProjectModule, phase: Phase): string {
  const done = Boolean(context.progress.seen[phaseSeenKey(phase.id)]);
  return (
    `<a class="ph-card" href="#${phaseRouteId(module, phase.id)}"><span class="num">${escapeHtml(phase.day || "Formador")}</span>` +
    `<div><h3>${escapeHtml(phase.title)}</h3><p>${escapeHtml(phase.goal)}</p></div>` +
    `<span class="st tag">${done ? "concluída" : "por fazer"}</span></a>`
  );
}

export function renderProjectOverview(context: RenderContext, module: ProjectModule): string {
  const header = pageHeader(
    module,
    `Módulo ${module.number}`,
    module.title,
    module.tagline,
    renderProgressBar(moduleProgress(context.progress, module)),
  );
  const briefCards = renderEach(module.brief.cards, (card, index) => renderSummaryCard(context, card, `pb${index}`));
  const finalDeliveryCard =
    `<a class="ph-card" href="#${finalDeliveryRouteId(module)}"><span class="num">Dia 6</span><div><h3>Entrega final</h3>` +
    `<p>Entregas o projeto e fazemos a review em conjunto, com os critérios de aceitação para saberes que estás pronto.</p></div><span class="st"></span></a>`;

  return (
    renderBreadcrumb(context, module) +
    header +
    `<p class="blk prose">${escapeHtml(module.brief.context)}</p><div class="blk"><div class="cgrid">${briefCards}</div></div>` +
    `<div class="blk"><h3>Seis dias</h3>${renderDays(module)}</div>` +
    `<div class="blk"><h3>Arquitetura</h3><div id="arch">${renderArchitecture(context, module)}</div></div>` +
    `<div class="blk"><h3>Percurso de um pedido</h3><div id="flowbox">${renderRequestFlow(context, module)}</div></div>` +
    `<div class="blk"><h3>Fases</h3><div class="phases">${renderEach(module.phases, (phase) => renderPhaseCard(context, module, phase))}${finalDeliveryCard}</div></div></div>` +
    renderPager(context, module.id)
  );
}

/* ----------------------------------------------------------------- phase */

function phaseEyebrow(module: ProjectModule, phaseIndex: number): string {
  const phase = module.phases[phaseIndex];
  if (!phase.day) return "Sessão com o formador";
  const daysWithPhase = module.phases.filter((candidate) => candidate.day);
  const position = module.phases.slice(0, phaseIndex).filter((candidate) => candidate.day).length + 1;
  return `${escapeHtml(phase.day)} · Fase ${position} de ${daysWithPhase.length}`;
}

export function renderPhase(context: RenderContext, module: ProjectModule, phaseIndex: number): string {
  const phase = module.phases[phaseIndex];
  const drawerKey = registerDrawer(context, `ph:${phase.id}`, phase.title, phase.learnMore && { learnMore: phase.learnMore });
  const completed = Boolean(context.progress.seen[phaseSeenKey(phase.id)]);

  context.phaseFilesByName.clear();
  for (const section of phase.sections ?? []) {
    for (const file of section.files ?? []) context.phaseFilesByName.set(file.name, file);
  }

  let html = renderBreadcrumb(context, module, phase.day ? `${phase.day} · ${phase.title}` : phase.title);
  html += pageHeader(module, phaseEyebrow(module, phaseIndex), phase.title, phase.goal);
  if (phase.uses?.length) html += renderRelatedLessons(context, phase.uses, "Usa:");
  html += renderPhaseTrees(context, phase);
  if (phase.rules) html += `<div class="blk"><h3>Regras do jogo</h3>${numberedList(phase.rules)}</div>`;
  if (phase.userStories) {
    html += `<div class="blk"><h3>User stories (${phase.userStories.length})</h3>${renderPlanBar(context, module)}${renderFeatureGroups(context, phase)}</div>`;
  }
  if (phase.kind === "plan") html += `<div class="blk">${renderPlanBar(context, module)}</div>`;
  (phase.sections ?? []).forEach((section, index) => {
    html += renderPhaseSection(context, phase, section, index);
  });
  html +=
    `<div class="lfoot" style="margin-top:44px">${renderMoreButton(drawerKey, "Saber mais sobre esta fase")}` +
    `<button class="seenbtn" data-action="toggle-phase" data-key="${phase.id}" aria-pressed="${completed}">${TICK_ICON}` +
    `<span>${completed ? "Fase concluída" : "Marcar como concluída"}</span></button></div></div>`;
  return html + renderPager(context, phaseRouteId(module, phase.id));
}

/* --------------------------------------------------------- final delivery */

function renderTitledList(items: ReadonlyArray<{ title: string; description: string }>): string {
  return (
    `<ol class="ol">` +
    renderEach(
      items,
      (item) => `<li><span><b>${escapeHtml(item.title)}.</b> ${escapeHtml(item.description)}</span></li>`,
    ) +
    `</ol>`
  );
}

export function renderFinalDelivery(context: RenderContext, module: ProjectModule): string {
  const { finalDelivery } = module;
  const criteria = renderEach(module.acceptanceCriteria, (criterion, index) => {
    const ticked = Boolean(context.progress.acceptedCriteria[index]);
    return (
      `<li><button class="step" role="checkbox" aria-checked="${ticked}" data-action="toggle-criterion" data-key="${index}">` +
      `<span class="bx">${TICK_ICON}</span><span class="tx">${escapeHtml(criterion)}</span></button></li>`
    );
  });
  const extras = renderEach(module.extras, (extra) => `<span>${escapeHtml(extra)}</span>`);

  return (
    renderBreadcrumb(context, module, "Entrega final") +
    pageHeader(module, "Dia 6 · Entrega final", finalDelivery.title, finalDelivery.intro) +
    `<div class="blk"><h3>O que entregas</h3>${renderTitledList(finalDelivery.deliverables)}</div>` +
    `<div class="blk"><h3>Como corre a review</h3>${renderTitledList(finalDelivery.reviewSteps)}</div>` +
    `<div class="blk"><h3>Antes de entregar</h3><p class="prose">Marca cada critério quando o conseguires demonstrar.</p>` +
    `<ul class="steps" style="margin-top:12px">${criteria}</ul></div>` +
    `<div class="blk"><h3>Plano contra realidade</h3>${numberedList(finalDelivery.planVersusReality)}</div>` +
    `<div class="blk"><h3>Perguntas que podem surgir na review</h3>${numberedList(finalDelivery.reviewQuestions)}</div>` +
    `<div class="blk"><h3>Todos os endpoints do enunciado</h3>${renderTable(module.endpoints)}</div>` +
    `<div class="blk"><h3>Extras (opcional)</h3><div class="note">${extras}</div></div></div>` +
    renderPager(context, finalDeliveryRouteId(module))
  );
}
