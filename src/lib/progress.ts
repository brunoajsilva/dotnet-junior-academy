/**
 * What the learner has done, kept in localStorage, and the percentages derived from it.
 *
 * The stored JSON keeps its original short keys (seen, steps, sw, acc, ans, pick, last) so progress
 * saved by earlier versions of the site is still read; inside the code the fields have full names.
 */
import type { Chapter, AcademyModule } from "../content/schema";
import type { Site } from "./site";
import { phaseRouteId, sectionRouteId } from "./site";

export const PROGRESS_STORAGE_KEY = "academia-dotnet-v1";

type Flags = Record<string, 1>;

export interface LearnerProgress {
  /** Lessons by id, introduction sections as "sec:<id>" and project phases as "ph:<id>". */
  seen: Flags;
  /** Ticked steps, keyed "<lesson id>:<step index>". */
  tickedSteps: Flags;
  /** Software tools marked as installed, by tool id. */
  installedTools: Flags;
  /** Acceptance criteria of the project that are ticked, by index. */
  acceptedCriteria: Flags;
  /** Quiz answers: chapter id, then the chosen option index per question. */
  quizAnswers: Record<string, number[]>;
  /** User stories added to the learner's plan, by user story id. */
  pickedStories: Flags;
  lastRoute: string;
}

export interface Percentage {
  done: number;
  total: number;
  percent: number;
}

export function emptyProgress(): LearnerProgress {
  return {
    seen: {},
    tickedSteps: {},
    installedTools: {},
    acceptedCriteria: {},
    quizAnswers: {},
    pickedStories: {},
    lastRoute: "",
  };
}

/** Stored names, from before the fields had readable names. */
interface StoredProgress {
  seen?: Flags;
  steps?: Flags;
  sw?: Flags;
  acc?: Flags;
  ans?: Record<string, number[]>;
  pick?: Flags;
  last?: string;
}

/** Plans saved before the rename used "F1" for what is now "US1". */
function migrateStoryIds(picked: Flags | undefined): Flags | undefined {
  if (!picked) return undefined;
  const migrated: Flags = {};
  for (const [id, value] of Object.entries(picked)) migrated[id.replace(/^F(\d+)$/, "US$1")] = value;
  return migrated;
}

export function loadProgress(): LearnerProgress {
  const progress = emptyProgress();
  try {
    const raw = localStorage.getItem(PROGRESS_STORAGE_KEY);
    if (!raw) return progress;
    const stored = JSON.parse(raw) as StoredProgress;
    progress.seen = stored.seen ?? progress.seen;
    progress.tickedSteps = stored.steps ?? progress.tickedSteps;
    progress.installedTools = stored.sw ?? progress.installedTools;
    progress.acceptedCriteria = stored.acc ?? progress.acceptedCriteria;
    progress.quizAnswers = stored.ans ?? progress.quizAnswers;
    progress.pickedStories = migrateStoryIds(stored.pick) ?? progress.pickedStories;
    progress.lastRoute = stored.last ?? progress.lastRoute;
  } catch {
    // no storage, or unreadable content: start from scratch
  }
  return progress;
}

export function saveProgress(progress: LearnerProgress): void {
  const stored: StoredProgress & { quiz: object } = {
    seen: progress.seen,
    steps: progress.tickedSteps,
    quiz: {},
    sw: progress.installedTools,
    acc: progress.acceptedCriteria,
    ans: progress.quizAnswers,
    pick: progress.pickedStories,
    last: progress.lastRoute,
  };
  try {
    localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(stored));
  } catch {
    // storage is full or blocked: progress just is not kept
  }
}

/** Switches a flag on or off and returns the new state. */
export function toggleFlag(flags: Flags, key: string): boolean {
  if (flags[key]) {
    delete flags[key];
    return false;
  }
  flags[key] = 1;
  return true;
}

export const sectionSeenKey = (sectionId: string) => `sec:${sectionId}`;
export const phaseSeenKey = (phaseId: string) => `ph:${phaseId}`;

function toPercentage(done: number, total: number): Percentage {
  return { done, total, percent: total ? Math.round((100 * done) / total) : 0 };
}

export function chapterProgress(progress: LearnerProgress, chapter: Chapter): Percentage {
  const done = chapter.lessons.filter((lesson) => progress.seen[lesson.id]).length;
  return toPercentage(done, chapter.lessons.length);
}

export function moduleProgress(progress: LearnerProgress, module: AcademyModule): Percentage {
  let done = 0;
  let total = 0;
  const count = (isDone: boolean) => {
    total++;
    if (isDone) done++;
  };

  switch (module.kind) {
    case "course":
      for (const chapter of module.chapters) {
        const chapterTotals = chapterProgress(progress, chapter);
        done += chapterTotals.done;
        total += chapterTotals.total;
      }
      break;
    case "intro":
      for (const section of module.sections) {
        count(Boolean(progress.seen[sectionSeenKey(section.id)]));
        for (const block of section.blocks) {
          if (block.type !== "software") continue;
          for (const tool of block.tools) {
            if (tool.requirement === "required") count(Boolean(progress.installedTools[tool.id]));
          }
        }
      }
      break;
    case "project":
      module.phases.forEach((phase) => count(Boolean(progress.seen[phaseSeenKey(phase.id)])));
      module.acceptanceCriteria.forEach((_criterion, index) =>
        count(Boolean(progress.acceptedCriteria[index])),
      );
      break;
  }
  return toPercentage(done, total);
}

export function overallPercent(progress: LearnerProgress, site: Site): number {
  let done = 0;
  let total = 0;
  for (const module of site.modules) {
    const totals = moduleProgress(progress, module);
    done += totals.done;
    total += totals.total;
  }
  return Math.round((100 * done) / total);
}

/** 0 = nothing done, 1 = started, 2 = finished: the dot next to a menu entry. */
export function routeStatus(progress: LearnerProgress, site: Site, routeId: string): 0 | 1 | 2 {
  const target = site.routeById(routeId)?.target;
  if (!target) return 0;

  if (target.kind === "chapter") {
    const { done, total } = chapterProgress(progress, target.module.chapters[target.chapterIndex]);
    return done === 0 ? 0 : done === total ? 2 : 1;
  }
  if (target.kind === "phase") {
    const phase = target.module.phases[target.phaseIndex];
    return progress.seen[phaseSeenKey(phase.id)] ? 2 : 0;
  }
  if (target.kind === "section") {
    return progress.seen[sectionSeenKey(target.section.id)] ? 2 : 0;
  }
  return 0;
}

export { phaseRouteId, sectionRouteId };
