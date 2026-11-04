/**
 * Final project: the details of a user story shown in the drawer, and the HTML copied to Azure DevOps.
 */
import type { StoryDetails, UserStory } from "../../../content/schema";
import { escapeHtml, renderEach } from "../../html";

const PRIORITY_BY_VALUE: Record<string, string> = { Alto: "Must have", Médio: "Should have", Baixo: "Could have" };

const listItems = (items: readonly string[]) => renderEach(items, (item) => `<li>${escapeHtml(item)}</li>`);

/** "Dado", "E", "E"...: the first line of a Given/When/Then group has the keyword, the rest "E". */
function givenWhenThenLines(keyword: string, lines: readonly string[], wrap: (line: string) => string): string[] {
  return lines.map((line, index) => wrap(`<b>${index ? "E" : keyword}</b> ${escapeHtml(line)}`));
}

function renderScenarioLines(scenario: StoryDetails["scenarios"][number], wrap: (line: string) => string): string {
  return [
    ...givenWhenThenLines("Dado", scenario.given, wrap),
    ...givenWhenThenLines("Quando", scenario.when, wrap),
    ...givenWhenThenLines("Então", scenario.then, wrap),
  ].join("");
}

const keepLine = (line: string) => line;

/* ------------------------------------------------- drawer content */

export function renderStoryDetails(userStory: UserStory): string {
  const story = userStory.details;
  if (!story) return "";
  const priority = PRIORITY_BY_VALUE[userStory.businessValue ?? ""] ?? "";
  const scenarios = renderEach(
    story.scenarios,
    (scenario, index) =>
      `<div class="gk"><h4>Cenário ${index + 1}: ${escapeHtml(scenario.title)}</h4>` +
      renderScenarioLines(scenario, (line) => `<p>${line}</p>`) +
      `</div>`,
  );
  return (
    `<div class="uscopy" role="group" aria-label="Copiar para o Azure DevOps"><span>Copiar para o Azure DevOps</span>` +
    `<button data-action="copy-story" data-key="title">Título</button><button data-action="copy-story" data-key="description">Descrição</button>` +
    `<button data-action="copy-story" data-key="criteria">Acceptance Criteria</button></div>` +
    `<p class="usline"><b>Como</b> ${escapeHtml(story.persona)}, <b>quero</b> ${escapeHtml(story.want)}, <b>para</b> ${escapeHtml(story.purpose)}.</p>` +
    `<div class="usmeta"><span><i>Feature</i>${escapeHtml(userStory.feature)}</span><span><i>Prioridade</i>${escapeHtml(priority)}</span>` +
    `<span><i>Estimativa</i>${story.storyPoints} pontos</span>` +
    (userStory.dependsOn ? `<span><i>Depende de</i>${escapeHtml(userStory.dependsOn)}</span>` : "") +
    `</div><h3>Descrição</h3><p>${escapeHtml(story.description)}</p>` +
    `<h3>Regras de negócio</h3><ul class="usl">${listItems(userStory.rules)}</ul>` +
    `<h3>Critérios de aceitação</h3>${scenarios}` +
    `<h3>Fora do âmbito</h3><ul class="usl">${listItems(story.outOfScope)}</ul>` +
    `<h3>Definition of Done</h3><ul class="usl dod"><li>Regras de negócio no Domain ou no handler, com testes unitários</li>` +
    `<li>Migration criada e aplicada, quando há alterações ao modelo</li><li>Todos os cenários acima verificados, pelo menos num pedido no Bruno</li>` +
    `<li>Erros devolvidos como Response com o code correto (sempre HTTP 200)</li>` +
    `<li>Código revisto: uma classe por ficheiro, sem lógica de negócio no controller</li></ul>`
  );
}

/* ------------------------------------------- copy to Azure DevOps */

export type StoryPart = "title" | "description" | "criteria";

function descriptionForCopy(userStory: UserStory, story: StoryDetails): string {
  return (
    `<p><b>Como</b> ${escapeHtml(story.persona)}, <b>quero</b> ${escapeHtml(story.want)}, <b>para</b> ${escapeHtml(story.purpose)}.</p>` +
    `<p>${escapeHtml(story.description)}</p><p><b>Regras de negócio</b></p><ul>${listItems(userStory.rules)}</ul>` +
    `<p><b>Fora do âmbito</b></p><ul>${listItems(story.outOfScope)}</ul>`
  );
}

function criteriaForCopy(story: StoryDetails): string {
  return renderEach(
    story.scenarios,
    (scenario, index) =>
      `<p><b>Cenário ${index + 1}: ${escapeHtml(scenario.title)}</b><br>` +
      [
        givenWhenThenLines("Dado", scenario.given, keepLine).join("<br>"),
        givenWhenThenLines("Quando", scenario.when, keepLine).join("<br>"),
        givenWhenThenLines("Então", scenario.then, keepLine).join("<br>"),
      ].join("<br>") +
      `</p>`,
  );
}

/** HTML for the clipboard: pasted into Azure DevOps it keeps its bold text and lists. */
export function renderStoryForCopy(userStory: UserStory, part: StoryPart): string {
  const story = userStory.details;
  if (part === "title") return escapeHtml(`${userStory.id} · ${userStory.title}`);
  if (!story) return "";
  return part === "description" ? descriptionForCopy(userStory, story) : criteriaForCopy(story);
}
