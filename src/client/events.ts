/**
 * Clicks and keys. Every button in the page carries `data-action="<name>"` (and usually `data-key`),
 * and one listener on the document runs the matching handler below.
 */
import type { Chapter } from "../content/schema";
import { rewriteHashLinks, routeUrl } from "../lib/html";
import {
  chapterProgress,
  phaseSeenKey,
  saveProgress,
  toggleFlag,
} from "../lib/progress";
import type { RenderContext } from "../lib/render/context";
import { renderQuiz } from "../lib/render/pages/course";
import { renderArchitecture, renderRequestFlow } from "../lib/render/project/architecture";
import { renderTreePanel } from "../lib/render/project/files";
import { renderPlanBar } from "../lib/render/project/plan";
import type { StoryPart } from "../lib/render/project/story-details";
import { copyText, copyStoryDetailsPart } from "./clipboard";
import { closeDrawer, closeSideMenu, isDrawerOpen, openDrawer, toggleSideMenu } from "./drawer";
import { closeStoryModal, openStoryModal } from "./story-modal";
import { dataKey, query, queryAll, queryOptional } from "./dom";
import { renderMenus } from "./render";

type ActionHandler = (context: RenderContext, element: HTMLElement) => void;

function findChapter(context: RenderContext, chapterId: string): Chapter | undefined {
  for (const module of context.site.modules) {
    if (module.kind !== "course") continue;
    const chapter = module.chapters.find((candidate) => candidate.id === chapterId);
    if (chapter) return chapter;
  }
  return undefined;
}

/** Keeps the progress bar in a chapter's header in step with the lessons marked as seen. */
function updateChapterProgressBar(context: RenderContext): void {
  const target = context.site.routeById(context.currentRouteId)?.target;
  if (target?.kind !== "chapter") return;
  const { done, total, percent } = chapterProgress(context.progress, target.module.chapters[target.chapterIndex]);
  const bar = queryOptional(".ph .barrow");
  if (!bar) return;
  query("i", bar).style.width = `${percent}%`;
  query("span", bar).textContent = `${done} de ${total}`;
}

function persist(context: RenderContext): void {
  saveProgress(context.progress);
}

function replaceQuiz(context: RenderContext, chapterId: string): void {
  const chapter = findChapter(context, chapterId);
  if (chapter) query(`#quiz-${chapterId}`).outerHTML = renderQuiz(context, chapter);
}

const ACTIONS: Record<string, ActionHandler> = {
  "open-drawer": (context, element) => openDrawer(context, dataKey(element)),

  "open-story": (_context, element) => openStoryModal(dataKey(element)),

  "close-story": () => closeStoryModal(),

  "copy-code": (_context, element) => {
    const code = document.getElementById(element.dataset.target ?? "");
    if (code) copyText(code.textContent ?? "", element);
  },

  "copy-text": (_context, element) => copyText(element.dataset.value ?? "", element),

  "select-tab": (_context, element) => {
    const group = element.dataset.tabGroup;
    const index = element.dataset.index;
    queryAll(`[data-action="select-tab"][data-tab-group="${group}"]`).forEach((tab) =>
      tab.setAttribute("aria-selected", String(tab === element)),
    );
    queryAll(`[data-pane^="${group}-"]`).forEach((pane) => {
      pane.hidden = pane.dataset.pane !== `${group}-${index}`;
    });
  },

  "toggle-reveal": (_context, element) => {
    const panel = element.nextElementSibling as HTMLElement;
    const opening = panel.hidden;
    element.dataset.label ??= element.textContent ?? "";
    panel.hidden = !opening;
    element.setAttribute("aria-expanded", String(opening));
    element.textContent = opening ? "Esconder" : element.dataset.label;
  },

  "toggle-seen": (context, element) => {
    const seen = toggleFlag(context.progress.seen, dataKey(element));
    persist(context);
    element.setAttribute("aria-pressed", String(seen));
    query("span", element).textContent = seen ? "Visto" : "Marcar como visto";
    element.closest(".lesson")?.classList.toggle("seen", seen);
    renderMenus(context);
    updateChapterProgressBar(context);
  },

  "toggle-phase": (context, element) => {
    const done = toggleFlag(context.progress.seen, phaseSeenKey(dataKey(element)));
    persist(context);
    element.setAttribute("aria-pressed", String(done));
    query("span", element).textContent = done ? "Fase concluída" : "Marcar como concluída";
    renderMenus(context);
  },

  "toggle-step": (context, element) => {
    const ticked = toggleFlag(context.progress.tickedSteps, dataKey(element));
    persist(context);
    element.setAttribute("aria-checked", String(ticked));
  },

  "toggle-criterion": (context, element) => {
    const ticked = toggleFlag(context.progress.acceptedCriteria, dataKey(element));
    persist(context);
    element.setAttribute("aria-checked", String(ticked));
    renderMenus(context);
  },

  "toggle-tool": (context, element) => {
    const installed = toggleFlag(context.progress.installedTools, dataKey(element));
    persist(context);
    element.setAttribute("aria-pressed", String(installed));
    element.closest(".swi")?.classList.toggle("ok", installed);
    renderMenus(context);
  },

  answer: (context, element) => {
    const chapterId = element.dataset.chapter ?? "";
    const answers = (context.progress.quizAnswers[chapterId] ??= []);
    answers[Number(element.dataset.question)] = Number(element.dataset.option);
    persist(context);
    replaceQuiz(context, chapterId);
  },

  "reset-quiz": (context, element) => {
    const chapterId = element.dataset.chapter ?? "";
    delete context.progress.quizAnswers[chapterId];
    persist(context);
    replaceQuiz(context, chapterId);
  },

  "select-file": (context, element) => showTreeNode(context, element, true),
  "select-directory": (context, element) => showTreeNode(context, element, false),

  "copy-story": (context, element) => copyStoryDetailsPart(context, dataKey(element) as StoryPart, element),

  "toggle-pick": (context, element) => {
    const picked = toggleFlag(context.progress.pickedStories, dataKey(element));
    persist(context);
    element.setAttribute("aria-pressed", String(picked));
    element.textContent = picked ? "No meu plano" : "Adicionar ao meu plano";
    const planBar = queryOptional("#planbar");
    const project = context.site.projectModule();
    if (planBar && project) planBar.outerHTML = renderPlanBar(context, project);
  },

  "select-layer": (context, element) => {
    context.architecture.selectedLayerId = dataKey(element);
    redrawArchitecture(context);
  },

  "go-to-step": (context, element) => {
    context.architecture.flowStepIndex = Number(element.dataset.index);
    redrawRequestFlow(context);
  },

  "next-step": (context) => {
    const lastStep = (context.site.projectModule()?.flow.length ?? 1) - 1;
    context.architecture.flowStepIndex = Math.min(context.architecture.flowStepIndex + 1, lastStep);
    redrawRequestFlow(context);
  },

  "previous-step": (context) => {
    context.architecture.flowStepIndex = Math.max(context.architecture.flowStepIndex - 1, 0);
    redrawRequestFlow(context);
  },
};

function showTreeNode(context: RenderContext, element: HTMLElement, isFile: boolean): void {
  const treeBox = element.closest(".treebox");
  const node = context.treeNodesById.get(dataKey(element));
  if (!treeBox || !node) return;
  if (isFile) {
    queryAll(".tfile", treeBox).forEach((file) => file.setAttribute("aria-pressed", String(file === element)));
  }
  query(".tpanel", treeBox).innerHTML = renderTreePanel(context, node);
}

function redrawArchitecture(context: RenderContext): void {
  const project = context.site.projectModule();
  if (project) query("#arch").innerHTML = rewriteHashLinks(renderArchitecture(context, project));
}

function redrawRequestFlow(context: RenderContext): void {
  const project = context.site.projectModule();
  if (project) query("#flowbox").innerHTML = renderRequestFlow(context, project);
}

export function bindEvents(context: RenderContext): void {
  document.addEventListener("click", (event) => {
    const target = event.target as Element;

    // links written as href="#route-id" navigate to the real page
    const hashLink = target.closest<HTMLAnchorElement>('a[href^="#"]');
    if (hashLink && !event.defaultPrevented && !event.metaKey && !event.ctrlKey) {
      event.preventDefault();
      location.assign(routeUrl(hashLink.getAttribute("href")?.slice(1) ?? ""));
      return;
    }

    const goTo = target.closest<HTMLElement>("[data-go-to-route]");
    if (goTo) {
      location.assign(routeUrl(goTo.dataset.goToRoute ?? ""));
      return;
    }

    const actionElement = target.closest<HTMLElement>("[data-action]");
    const action = actionElement?.dataset.action;
    if (actionElement && action && ACTIONS[action]) ACTIONS[action](context, actionElement);
  });

  query("#drClose").addEventListener("click", closeDrawer);
  query("#drScrim").addEventListener("click", closeDrawer);
  query("#menuBtn").addEventListener("click", toggleSideMenu);
  query("#scrim").addEventListener("click", closeSideMenu);
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    // the drawer opens above the story modal, so Esc closes the one on top first
    if (isDrawerOpen()) closeDrawer();
    else {
      closeStoryModal();
      closeSideMenu();
    }
  });
}
