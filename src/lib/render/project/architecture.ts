/**
 * Final project: architecture diagram, request flow and the day-by-day overview.
 */
import type { Layer, ProjectModule } from "../../../content/schema";
import { escapeHtml, renderEach } from "../../html";
import type { RenderContext } from "../context";

function findLayer(module: ProjectModule, layerId: string): Layer {
  const layer = module.layers.find((candidate) => candidate.id === layerId);
  if (!layer) throw new Error(`unknown layer '${layerId}'`);
  return layer;
}

/** Layers from the outside in, as drawn in the diagram. */
const LAYER_STACK = ["api", "infrastructure", "application", "domain"];
const TESTS_LAYER = "tests";
const REFERENCES_ARROW = '<div class="arr">↓ referencia</div>';

function renderLayerButton(context: RenderContext, module: ProjectModule, layerId: string): string {
  const layer = findLayer(module, layerId);
  const selected = findLayer(module, context.architecture.selectedLayerId);
  const isReferenced = selected.references.some((reference) => reference.startsWith(layer.name));
  return (
    `<button class="lay${isReferenced ? " ref" : ""}" aria-pressed="${layerId === selected.id}" data-action="select-layer" ` +
    `data-key="${layerId}" style="--lc:var(--l-${layer.color})"><span class="dot"></span>` +
    `<span><b>${escapeHtml(layer.name)}</b><small>${escapeHtml(layer.role)}</small></span></button>`
  );
}

function renderLayerPanel(layer: Layer): string {
  const contains = renderEach(layer.contains, (item) => `<li>${escapeHtml(item)}</li>`);
  const references = layer.references.length
    ? `<ul>${renderEach(layer.references, (reference) => `<li><code>${escapeHtml(reference)}</code></li>`)}</ul>`
    : '<p style="font-size:.92rem">Nada. É o centro.</p>';
  return (
    `<div class="lpanel" style="--lc:var(--l-${layer.color})"><h4>${escapeHtml(layer.name)}</h4>` +
    `<p class="role">${escapeHtml(layer.role)}</p><p>${escapeHtml(layer.rationale)}</p>` +
    `<h5>Contém</h5><ul>${contains}</ul><h5>Referencia</h5>${references}` +
    `<h5>Nunca conhece</h5><p class="never">${escapeHtml(layer.neverKnows)}</p></div>`
  );
}

export function renderArchitecture(context: RenderContext, module: ProjectModule): string {
  const button = (layerId: string) => renderLayerButton(context, module, layerId);
  const stack =
    LAYER_STACK.map(button).join(REFERENCES_ARROW) +
    `<div class="arr" style="margin-top:6px">Verificação</div>${button(TESTS_LAYER)}`;
  const selectedLayer = findLayer(module, context.architecture.selectedLayerId);
  return `<div class="arch"><div class="stack">${stack}</div>${renderLayerPanel(selectedLayer)}</div>`;
}

export function renderRequestFlow(context: RenderContext, module: ProjectModule): string {
  const stepIndex = context.architecture.flowStepIndex;
  const step = module.flow[stepIndex];
  const layer = findLayer(module, step.layer);

  const dots = renderEach(module.flow, (_step, index) => {
    const state = index === stepIndex ? "on" : index < stepIndex ? "done" : "";
    return `<button class="${state}" data-action="go-to-step" data-index="${index}" aria-label="Passo ${index + 1}"></button>`;
  });
  const isFirst = stepIndex === 0;
  const isLast = stepIndex === module.flow.length - 1;
  return (
    `<div class="stepper" id="flow"><div class="dots">${dots}</div>` +
    `<span class="lchip" style="--lc:var(--l-${layer.color})">${escapeHtml(layer.name.replace("BankingApp.", ""))}</span>` +
    `<h4>${stepIndex + 1}. ${escapeHtml(step.title)}</h4><p>${escapeHtml(step.description)}</p>` +
    `<div class="ctl"><button class="btn" data-action="previous-step" ${isFirst ? "disabled" : ""}>Anterior</button>` +
    `<button class="btn pri" data-action="next-step" ${isLast ? "disabled" : ""}>Seguinte</button></div></div>`
  );
}

export function renderDays(module: ProjectModule): string {
  const days = renderEach(
    module.days,
    (day) =>
      `<a class="day" href="#${day.route}"><small>${escapeHtml(day.label)}</small><h4>${escapeHtml(day.title)}</h4><p>${escapeHtml(day.goal)}</p></a>`,
  );
  return `<div class="days">${days}</div>`;
}
