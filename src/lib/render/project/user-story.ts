/**
 * Final project: one user story: a row in the list and a modal (endpoint, rules, responses, criteria, hints).
 */
import type { UserStory } from "../../../content/schema";
import { ARROW_ICON, escapeHtml, renderEach } from "../../html";
import { plainSteps, renderMoreButton, renderSteps, renderTable } from "../blocks";
import { renderCodeBlock } from "../code";
import { registerDrawer, type RenderContext } from "../context";

/** The "Usa:" / "Rever:" line with links to the lessons a phase or user story builds on. */
export function renderRelatedLessons(context: RenderContext, lessonIds: readonly string[], label: string, style = ""): string {
  const links = renderEach(lessonIds, (id) => {
    const route = context.site.routeById(id);
    return `<a href="#${id}">${escapeHtml(route ? route.title : id)}</a>`;
  });
  return `<div class="uses"${style}><span>${label}</span>${links}</div>`;
}

function renderStoryMeta(story: UserStory): string {
  const value = story.businessValue
    ? `<span class="val ${story.businessValue}">Valor ${story.businessValue.toLowerCase()}</span>`
    : "";
  const dependency = story.dependsOn ? `<span class="val">depende de ${escapeHtml(story.dependsOn)}</span>` : "";
  return `<span class="meta">${value}${dependency}</span>`;
}

/** The row in the list: clicking it opens the story in a modal. */
function renderStoryRow(story: UserStory): string {
  return (
    `<button class="feat-row" type="button" data-action="open-story" data-key="${story.id}" aria-haspopup="dialog" aria-controls="story-${story.id}">` +
    `<span class="fid">${story.id}</span><div><h3>${escapeHtml(story.title)}</h3><p class="st">${escapeHtml(story.story)}</p></div>` +
    `${renderStoryMeta(story)}</button>`
  );
}

function renderUserStoryFooter(context: RenderContext, story: UserStory, hintKey: string): string {
  const picked = Boolean(context.progress.pickedStories[story.id]);
  let detailsButton = "";
  if (story.details) {
    const detailsKey = registerDrawer(context, `us:${story.id}`, `${story.id} · ${story.title}`, {
      storyDetails: story,
    });
    detailsButton = `<button class="more story" data-action="open-drawer" data-key="${escapeHtml(detailsKey)}">Detalhe${ARROW_ICON}</button>`;
  }
  const pickButton = story.businessValue
    ? `<button class="pickbtn" data-action="toggle-pick" data-key="${story.id}" aria-pressed="${picked}">${picked ? "No meu plano" : "Adicionar ao meu plano"}</button>`
    : "";
  return `<div class="lfoot" style="margin-top:0">${detailsButton}${renderMoreButton(hintKey, "Pista")}${pickButton}</div>`;
}

export function renderUserStoryCard(context: RenderContext, story: UserStory): string {
  const hintKey = registerDrawer(
    context,
    `ft:${story.id}`,
    `${story.id} · ${story.title}`,
    story.hint && { learnMore: story.hint },
  );

  let body = "";
  if (story.endpoint) body += `<div><h5>Pedido</h5><p class="ep">${escapeHtml(story.endpoint)}</p></div>`;
  if (story.body) {
    body += `<div>${renderCodeBlock(context, { code: story.body, language: "json", fileName: "Corpo do pedido", small: true })}</div>`;
  }
  body += `<div><h5>Regras</h5><ul class="rl">${renderEach(story.rules, (rule) => `<li>${escapeHtml(rule)}</li>`)}</ul></div>`;
  if (story.responses.length) {
    const rows = [["Resultado (code)", "Quando"], ...story.responses.map((response) => [response.result, response.when])];
    body += `<div><h5>Resultados (sempre HTTP 200)</h5>${renderTable(rows)}</div>`;
  }
  body += `<div><h5>Critérios de aceitação</h5>${renderSteps(context, { id: `ft-${story.id}`, steps: plainSteps(story.criteria) })}</div>`;
  if (story.uses?.length) body += renderRelatedLessons(context, story.uses, "Rever:", ' style="margin-top:0"');

  const modal =
    `<div class="smodal" id="story-${story.id}" hidden>` +
    `<div class="smodal-scrim" data-action="close-story"></div>` +
    `<section class="smodal-card" role="dialog" aria-modal="true" aria-labelledby="story-${story.id}-title">` +
    `<header class="smodal-head"><span class="fid">${story.id}</span>` +
    `<div><h3 id="story-${story.id}-title">${escapeHtml(story.title)}</h3><p class="st">${escapeHtml(story.story)}</p>${renderStoryMeta(story)}</div>` +
    `<button class="ibtn" type="button" data-action="close-story" aria-label="Fechar">Fechar <kbd>Esc</kbd></button></header>` +
    `<div class="fbody">${body}${renderUserStoryFooter(context, story, hintKey)}</div></section></div>`;

  return `<article class="feat" id="f-${story.id}">${renderStoryRow(story)}${modal}</article>`;
}
