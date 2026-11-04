/**
 * Everything a page render needs besides the content: the learner's progress, the current page and
 * the small pieces of state the renderers fill in (drawer texts, code block ids, tree nodes...).
 * The static build makes one context per page; the browser keeps one and updates it.
 */
import type { LearnMore, PhaseFile, TreeNode, UserStory } from "../../content/schema";
import type { LearnerProgress } from "../progress";
import type { Site } from "../site";

/** What the "Saber mais" drawer shows: an explanation, or the details of a user story. */
export type DrawerContent = { learnMore: LearnMore } | { storyDetails: UserStory };

export interface DrawerEntry {
  title: string;
  content: DrawerContent;
}

export interface RenderContext {
  site: Site;
  progress: LearnerProgress;
  /** Route id of the page being drawn; "" is the home page. */
  currentRouteId: string;
  /** Drawer texts registered while rendering, by the key of the button that opens them. */
  drawerEntries: Map<string, DrawerEntry>;
  /** Counters that give every code block, tab group and tree node an id on the page. */
  idCounters: { codeBlocks: number; codeTabGroups: number; treeNodes: number };
  /** File tree nodes by id, so a click can show the node's description and code. */
  treeNodesById: Map<string, TreeNode>;
  /** Code files of the current project phase, by file name. */
  phaseFilesByName: Map<string, PhaseFile>;
  /** Selected layer of the architecture diagram and current step of the request flow. */
  architecture: { selectedLayerId: string; flowStepIndex: number };
  /** The user story currently open in the drawer (the copy buttons use it). */
  openStoryDetails: UserStory | null;
}

export function createRenderContext(
  site: Site,
  progress: LearnerProgress,
  currentRouteId: string,
): RenderContext {
  return {
    site,
    progress,
    currentRouteId,
    drawerEntries: new Map(),
    idCounters: { codeBlocks: 0, codeTabGroups: 0, treeNodes: 0 },
    treeNodesById: new Map(),
    phaseFilesByName: new Map(),
    architecture: { selectedLayerId: "domain", flowStepIndex: 0 },
    openStoryDetails: null,
  };
}

/** Registers the text of a "Saber mais" drawer and returns its key. */
export function registerDrawer(
  context: RenderContext,
  key: string,
  title: string,
  content: DrawerContent | undefined,
): string {
  if (content) context.drawerEntries.set(key, { title, content });
  return key;
}

/** Forgets what the previous page registered, before a page is drawn again in the browser. */
export function resetPageState(context: RenderContext): void {
  context.drawerEntries.clear();
  context.idCounters = { codeBlocks: 0, codeTabGroups: 0, treeNodes: 0 };
  context.treeNodesById.clear();
  context.phaseFilesByName.clear();
  context.architecture = { selectedLayerId: "domain", flowStepIndex: 0 };
  context.openStoryDetails = null;
}
