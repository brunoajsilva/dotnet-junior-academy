/**
 * Building blocks of a lesson: cards, tables, steps, exercises and the lesson article itself.
 */
import type {
  CardsLesson,
  Lesson,
  LearnMore,
  LessonCard,
} from "../../content/schema";
import { ARROW_ICON, TICK_ICON, escapeHtml, renderEach, twoDigits } from "../html";
import { renderCodeBlock } from "./code";
import { registerDrawer, type RenderContext } from "./context";

export function renderMoreButton(drawerKey: string, label = "Saber mais"): string {
  return `<button class="more" data-action="open-drawer" data-key="${escapeHtml(drawerKey)}">${label}${ARROW_ICON}</button>`;
}

/** One sentence as a paragraph, several as a bullet list. */
function renderParagraphOrList(lines: readonly string[]): string {
  if (!lines.length) return "";
  if (lines.length === 1) return `<p>${escapeHtml(lines[0])}</p>`;
  return `<ul>${renderEach(lines, (line) => `<li>${escapeHtml(line)}</li>`)}</ul>`;
}

/* ---------------------------------------------------------------- cards */

function renderFlowSteps(cards: readonly LessonCard[]): string {
  const steps = renderEach(
    cards,
    (card) =>
      `<div class="fstep"><b>${escapeHtml(card.title.replace(/\s+/g, " "))}</b><span>${escapeHtml(card.lines.join(" "))}</span></div>`,
  );
  return `<div class="flow">${steps}</div>`;
}

function renderCard(context: RenderContext, card: LessonCard): string {
  const body = card.asChecklist
    ? `<ul>${renderEach(card.lines, (line) => `<li>${escapeHtml(line)}</li>`)}</ul>`
    : renderParagraphOrList(card.lines);
  const code = card.code
    ? renderCodeBlock(context, { code: card.code, language: "cs", fileName: "", small: true })
    : "";
  return `<div class="icard"><h4>${escapeHtml(card.title)}</h4>${body}${code}</div>`;
}

function renderNote(card: LessonCard): string {
  return `<div class="note">${renderEach(card.lines, (line) => `<span>${escapeHtml(line)}</span>`)}</div>`;
}

export function renderCards(context: RenderContext, lesson: CardsLesson): string {
  const flowCount = lesson.flowSteps ?? 0;
  const flow = flowCount ? renderFlowSteps(lesson.cards.slice(0, flowCount)) : "";
  const remaining = lesson.cards.slice(flowCount);
  const notes = remaining.filter((card) => card.isNote);
  const cards = remaining.filter((card) => !card.isNote);

  let html = flow;
  if (cards.length) {
    const columns = cards.some((card) => card.code) ? " two" : "";
    html += `<div class="cgrid${columns}">${renderEach(cards, (card) => renderCard(context, card))}</div>`;
  }
  return html + renderEach(notes, renderNote);
}

/* ---------------------------------------------------------------- table */

export function renderTable(rows: readonly (readonly string[])[]): string {
  const [header, ...body] = rows;
  const headerCells = renderEach(header, (cell) => `<th>${escapeHtml(cell)}</th>`);
  const bodyRows = renderEach(
    body,
    (row) => `<tr>${renderEach(row, (cell) => `<td>${escapeHtml(cell)}</td>`)}</tr>`,
  );
  return `<div class="tbl"><table><thead><tr>${headerCells}</tr></thead><tbody>${bodyRows}</tbody></table></div>`;
}

/* ---------------------------------------------------------------- steps */

export interface StepList {
  /** Prefix of the progress key of each step: "<id>:<index>". */
  id: string;
  steps: readonly { keyword: string; text: string }[];
}

export function renderSteps(context: RenderContext, list: StepList): string {
  const items = renderEach(list.steps, (step, index) => {
    const key = `${list.id}:${index}`;
    const ticked = Boolean(context.progress.tickedSteps[key]);
    const keyword = step.keyword ? `<b>${escapeHtml(step.keyword)}.</b> ` : "";
    return (
      `<li><button class="step" role="checkbox" aria-checked="${ticked}" data-action="toggle-step" data-key="${key}">` +
      `<span class="bx">${TICK_ICON}</span><span class="tx">${keyword}${escapeHtml(step.text)}</span></button></li>`
    );
  });
  return `<ul class="steps">${items}</ul>`;
}

/** Steps that have no bold keyword, e.g. the criteria of a feature. */
export function plainSteps(texts: readonly string[]): StepList["steps"] {
  return texts.map((text) => ({ keyword: "", text }));
}

/* ------------------------------------------------------------- exercise */

type ExerciseContent = Extract<Lesson, { type: "exercise" | "domain" }>;

function renderExercise(context: RenderContext, lesson: ExerciseContent): string {
  let html = renderSteps(context, { id: lesson.id, steps: lesson.steps });
  if (lesson.hint) html += `<div class="note">${escapeHtml(lesson.hint)}</div>`;
  if (lesson.table) html += `<div class="blk" style="margin-top:14px">${renderTable(lesson.table)}</div>`;
  if (lesson.expectedOutput) {
    html +=
      `<div class="reveal"><button data-action="toggle-reveal" aria-expanded="false">Ver resultado esperado</button>` +
      `<div class="panel" hidden><pre class="term">${escapeHtml(lesson.expectedOutput)}</pre></div></div>`;
  }
  if (lesson.challenge) html += `<div class="extra"><b>Extra.</b> ${escapeHtml(lesson.challenge)}</div>`;
  return html;
}

function renderDomain(context: RenderContext, lesson: Extract<Lesson, { type: "domain" }>): string {
  const [first, second, third] = lesson.entities;
  const entity = (item: typeof first) =>
    `<div class="ent"><b>${item.name}</b><span>${escapeHtml(item.fields)}</span></div>`;
  const relation = (text: string) => `<span class="rel">${text} →</span>`;
  return (
    `<div class="ents">${entity(first)}${relation(lesson.relations[0])}${entity(second)}` +
    `${relation(lesson.relations[1])}${entity(third)}</div>` +
    renderExercise(context, lesson)
  );
}

/* --------------------------------------------------------- legacy drawings */

function renderPyramid(lesson: Extract<Lesson, { type: "pyramid" }>): string {
  const levels = renderEach(
    lesson.levels,
    (level) => `<div><b>${escapeHtml(level.name)}</b>${escapeHtml(level.description)}</div>`,
  );
  const cards = renderEach(
    lesson.cards,
    (card) => `<div class="icard"><h4>${escapeHtml(card.title)}</h4>${renderParagraphOrList(card.lines)}</div>`,
  );
  return `<div class="pyr">${levels}</div><div class="cgrid">${cards}</div>`;
}

function renderLayers(lesson: Extract<Lesson, { type: "layers" }>): string {
  const [outer, middle, inner] = lesson.levels;
  const rules = renderEach(lesson.rules, (rule) => `<li>${escapeHtml(rule)}</li>`);
  return (
    `<div class="lbody"><div class="rings"><div class="ring r1"><span class="lb">${escapeHtml(outer.name)}</span>` +
    `<div class="ring r2" style="margin-top:6px"><span class="lb">${escapeHtml(middle.name)}</span>` +
    `<div class="ring r3" style="margin-top:6px;padding-top:34px"><b>${escapeHtml(inner.name)}</b><br>${escapeHtml(inner.description)}</div>` +
    `</div></div></div><ul class="pts">${rules}</ul></div>`
  );
}

/* --------------------------------------------------------------- lesson */

function renderLessonBody(context: RenderContext, lesson: Lesson): string {
  switch (lesson.type) {
    case "code": {
      const points = renderEach(lesson.keyPoints, (point) => `<li>${escapeHtml(point)}</li>`);
      const code = renderCodeBlock(context, { code: lesson.code, language: lesson.language });
      return `<div class="lbody"><ul class="pts">${points}</ul>${code}</div>`;
    }
    case "cards":
      return renderCards(context, lesson);
    case "table":
      return renderTable(lesson.rows) + (lesson.note ? `<div class="note warn">${escapeHtml(lesson.note)}</div>` : "");
    case "pyramid":
      return renderPyramid(lesson);
    case "layers":
      return renderLayers(lesson);
    case "domain":
      return renderDomain(context, lesson);
    case "exercise":
      return renderExercise(context, lesson);
  }
}

export function isExercise(lesson: Lesson): boolean {
  return lesson.type === "exercise" || lesson.type === "domain";
}

export function renderLesson(context: RenderContext, lesson: Lesson, index: number): string {
  const drawerKey = registerDrawer(context, `l:${lesson.id}`, lesson.title, lesson.learnMore && { learnMore: lesson.learnMore });
  const seen = Boolean(context.progress.seen[lesson.id]);
  const exercise = isExercise(lesson);
  const classes = `lesson${seen ? " seen" : ""}${exercise ? " exercise" : ""}`;
  const badge = exercise ? '<span class="ex-badge">Exercício prático</span>' : "";

  return (
    `<article class="${classes}" id="${lesson.id}">${badge}` +
    `<div class="lh"><span class="ix">${twoDigits(index + 1)}</span><h3>${escapeHtml(lesson.title)}</h3>` +
    `<button class="seenbtn" data-action="toggle-seen" data-key="${lesson.id}" aria-pressed="${seen}">${TICK_ICON}` +
    `<span>${seen ? "Visto" : "Marcar como visto"}</span></button></div>` +
    renderLessonBody(context, lesson) +
    (lesson.learnMore ? `<div class="lfoot">${renderMoreButton(drawerKey)}</div>` : "") +
    `</article>`
  );
}

export type { LearnMore };
