/**
 * Final project: the learner's plan (picked user stories) and the grouping of user stories by feature.
 */
import type { Phase, ProjectModule } from "../../../content/schema";
import { escapeHtml, renderEach } from "../../html";
import type { RenderContext } from "../context";
import { renderUserStoryCard } from "./user-story";

function pickedStoryIds(context: RenderContext, module: ProjectModule): string[] {
  return module.phases
    .flatMap((phase) => phase.userStories ?? [])
    .filter((story) => context.progress.pickedStories[story.id])
    .map((story) => story.id);
}

export function renderPlanBar(context: RenderContext, module: ProjectModule): string {
  const totalStories = module.phases.reduce((total, phase) => total + (phase.userStories ?? []).length, 0);
  const picked = pickedStoryIds(context, module);
  const summary = picked.length
    ? `<span class="planlist">${picked.join(" ")}</span>`
    : "<span>Marca as user stories que escolhes em cada feature.</span>";
  return `<div class="planbar" id="planbar"><span>No meu plano: <b>${picked.length}</b> de ${totalStories}</span>${summary}</div>`;
}

/** The user stories of a phase, grouped by feature when the phase has features. */
export function renderFeatureGroups(context: RenderContext, phase: Phase): string {
  const stories = phase.userStories ?? [];
  const storyList = (list: typeof stories) =>
    `<div class="feats">${renderEach(list, (story) => renderUserStoryCard(context, story))}</div>`;

  if (!phase.features) return storyList(stories);

  return renderEach(phase.features, (feature) => {
    const featureStories = stories.filter((story) => story.feature === feature.id);
    if (!featureStories.length) return "";
    const count = `${featureStories.length} user ${featureStories.length === 1 ? "story" : "stories"}`;
    return (
      `<section class="epic" aria-labelledby="ep-${feature.id}"><header><span class="eid">${feature.id}</span>` +
      `<div><h4 id="ep-${feature.id}">${escapeHtml(feature.title)}</h4><p>${escapeHtml(feature.description)}</p></div>` +
      `<span class="ecount">${count}</span></header>${storyList(featureStories)}</section>`
    );
  });
}
