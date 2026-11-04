/**
 * Validates the content folder.
 *
 *   npm run check                                          everything listed in content/manifest.yaml
 *   npm run check -- content/_examples/logging/module.yaml one module (for example before adding it)
 *   npm run check -- --update-ids                          records new lesson/quiz ids in content/ids.lock
 *
 * It checks the shape of every module (the Zod schemas in src/content/schema.ts), that every referenced
 * file exists, that no file is orphaned, that ids are unique and never removed, and the writing rules
 * (no company names, no emoji). Modules you add get the authoring limits of docs/CONTENT-SCHEMA.md as well.
 * The exit code is 1 when something is wrong.
 */
import { readdir, readFile, writeFile } from "node:fs/promises";
import { dirname, basename } from "node:path";
import { join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { moduleSchema, type AcademyModule, type CourseModule } from "../src/content/schema";
import { loadContent, loadModule } from "../src/lib/content-loader";

const PROJECT_ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const CONTENT_DIRECTORY = join(PROJECT_ROOT, "content");

/** Modules shipped with the academy: structural checks only, not the limits for new modules. */
const SHIPPED_MODULE_IDS = new Set(["academia", "csharp", "dotnet", "auth", "projeto"]);

const MAX_CODE_LINES_IN_NEW_LESSON = 25;
const MAX_CHAPTERS_IN_NEW_MODULE = 8;
const MIN_LESSONS_IN_NEW_CHAPTER = 3;
const MIN_QUIZ_QUESTIONS_IN_NEW_CHAPTER = 3;

const FORBIDDEN_TEXT: Array<[RegExp, string]> = [
  [/\bITSector\b/i, "no company names or logos"],
  [/\bPostman\b/i, "the academy uses Bruno only"],
  [/\bTODO\b/, "unfinished text"],
  [/\blorem ipsum\b/i, "placeholder text"],
];
const EMOJI = /[\u{1F300}-\u{1FAFF}\u2600-\u27BF]/u;

type ReportProblem = (message: string) => void;

function* allTexts(node: unknown): Generator<string> {
  if (typeof node === "string") yield node;
  else if (Array.isArray(node)) for (const item of node) yield* allTexts(item);
  else if (node && typeof node === "object") {
    for (const [key, value] of Object.entries(node)) if (key !== "code") yield* allTexts(value);
  }
}

function checkWritingRules(academyModule: AcademyModule, report: ReportProblem): void {
  for (const text of allTexts(academyModule)) {
    for (const [pattern, reason] of FORBIDDEN_TEXT) {
      if (pattern.test(text)) report(`forbidden text ${pattern} (${reason}): ${text.slice(0, 60)}`);
    }
    if (EMOJI.test(text)) report(`emoji are not allowed: ${text.slice(0, 60)}`);
  }
}

function checkNewCourseLimits(course: CourseModule, report: ReportProblem): void {
  if (course.chapters.length > MAX_CHAPTERS_IN_NEW_MODULE) {
    report(`at most ${MAX_CHAPTERS_IN_NEW_MODULE} chapters`);
  }
  course.chapters.forEach((chapter, chapterIndex) => {
    const where = `chapter ${chapterIndex + 1}`;
    if (!chapter.id.startsWith(`${course.id}-`)) report(`${where}: id must start with '${course.id}-'`);
    if (chapter.lessons.length < MIN_LESSONS_IN_NEW_CHAPTER) {
      report(`${where}: needs at least ${MIN_LESSONS_IN_NEW_CHAPTER} lessons`);
    }
    if (chapter.quiz.length < MIN_QUIZ_QUESTIONS_IN_NEW_CHAPTER) {
      report(`${where}: the quiz needs at least ${MIN_QUIZ_QUESTIONS_IN_NEW_CHAPTER} questions`);
    }
    chapter.lessons.forEach((lesson, lessonIndex) => {
      const lessonWhere = `${where}, lesson ${lessonIndex + 1}`;
      if (!lesson.id.startsWith(`${course.id}-`)) report(`${lessonWhere}: id must start with '${course.id}-'`);
      if (lesson.type === "code" && lesson.code.split("\n").length > MAX_CODE_LINES_IN_NEW_LESSON) {
        report(`${lessonWhere}: code longer than ${MAX_CODE_LINES_IN_NEW_LESSON} lines, split the lesson`);
      }
    });
  });
}

function checkProjectReferences(academyModule: AcademyModule, report: ReportProblem): void {
  if (academyModule.kind !== "project") return;
  const phaseIds = new Set<string>();
  for (const phase of academyModule.phases) {
    if (phaseIds.has(phase.id)) report(`duplicate phase id '${phase.id}'`);
    phaseIds.add(phase.id);

    const userStories = phase.userStories ?? [];
    const storyIds = new Set<string>();
    for (const story of userStories) {
      if (storyIds.has(story.id)) report(`phase ${phase.id}: duplicate user story id '${story.id}'`);
      storyIds.add(story.id);
    }
    for (const story of userStories) {
      const dependencies = (story.dependsOn ?? "").split(",").map((id) => id.trim()).filter(Boolean);
      for (const dependency of dependencies) {
        if (!storyIds.has(dependency)) report(`user story ${story.id}: depends on unknown user story '${dependency}'`);
      }
      if (phase.features && !phase.features.some((feature) => feature.id === story.feature)) {
        report(`user story ${story.id}: unknown feature '${story.feature}'`);
      }
    }
  }
}

/** Every id under which learner progress is stored. Published ids must never change or disappear. */
function collectProgressIds(modules: AcademyModule[]): string[] {
  const ids: string[] = [];
  for (const academyModule of modules) {
    if (academyModule.kind === "course") {
      for (const chapter of academyModule.chapters) {
        ids.push(chapter.id, ...chapter.lessons.map((lesson) => lesson.id));
      }
    } else if (academyModule.kind === "intro") {
      ids.push(...academyModule.sections.map((section) => `sec:${section.id}`));
    } else {
      ids.push(...academyModule.phases.map((phase) => `ph:${phase.id}`));
    }
  }
  return ids;
}

function checkUniqueIds(modules: AcademyModule[], report: ReportProblem): void {
  const seen = new Set<string>();
  for (const id of collectProgressIds(modules)) {
    if (seen.has(id)) report(`duplicate id '${id}'`);
    seen.add(id);
  }
}

/** Returns the problems found in one module (already parsed from YAML). */
export function checkModule(rawModule: unknown, moduleNumber = 1): string[] {
  const problems: string[] = [];
  const parsed = moduleSchema.safeParse({ ...(rawModule as object), number: moduleNumber });
  if (!parsed.success) {
    const id = (rawModule as { id?: string }).id ?? "module";
    for (const issue of parsed.error.issues) problems.push(`${id}: ${issue.path.join(".")}: ${issue.message}`);
    return problems;
  }

  const academyModule = parsed.data;
  const report: ReportProblem = (message) => problems.push(`${academyModule.id}: ${message}`);
  const isShipped = SHIPPED_MODULE_IDS.has(academyModule.id);

  if (!isShipped) checkWritingRules(academyModule, report);
  if (academyModule.kind === "course" && !isShipped) checkNewCourseLimits(academyModule, report);
  checkProjectReferences(academyModule, report);
  return problems;
}

async function listFilesRecursively(directory: string): Promise<string[]> {
  const files: string[] = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...(await listFilesRecursively(path)));
    else files.push(path);
  }
  return files;
}

/**
 * A reference such as "code/bankingapp/x.cs" opens a file named "BankingApp/x.cs" on macOS and Windows
 * (case-insensitive) but not on the Linux machine that publishes the site. Every file the content
 * refers to must be written with exactly the case it has on disk.
 */
async function findWrongCaseReferences(files: string[]): Promise<string[]> {
  const problems: string[] = [];
  const listings = new Map<string, string[]>();
  for (const file of files) {
    let current = file;
    while (current.startsWith(CONTENT_DIRECTORY) && current !== CONTENT_DIRECTORY) {
      const parent = dirname(current);
      if (!listings.has(parent)) listings.set(parent, await readdir(parent));
      if (!listings.get(parent)!.includes(basename(current))) {
        problems.push(`${relative(CONTENT_DIRECTORY, file)}: the name does not match the case of the file on disk (Linux would not find it)`);
        break;
      }
      current = parent;
    }
  }
  return problems;
}

async function findOrphanFiles(referencedFiles: string[]): Promise<string[]> {
  const referenced = new Set(referencedFiles);
  const orphans: string[] = [];
  for (const file of await listFilesRecursively(CONTENT_DIRECTORY)) {
    const relativePath = relative(CONTENT_DIRECTORY, file).split("\\").join("/");
    const isDraftOrExample = relativePath.split("/").some((part) => part.startsWith("_"));
    if (isDraftOrExample || relativePath === "ids.lock") continue;
    if (!referenced.has(file)) {
      orphans.push(`${relativePath}: file is not referenced by any module (delete it, or prefix a folder with _ for drafts)`);
    }
  }
  return orphans;
}

async function checkLockedIds(modules: AcademyModule[], updateLockFile: boolean): Promise<string[]> {
  const lockPath = join(CONTENT_DIRECTORY, "ids.lock");
  const currentIds = collectProgressIds(modules);
  let lockedIds: string[] = [];
  try {
    lockedIds = (await readFile(lockPath, "utf8")).split("\n").filter(Boolean);
  } catch {
    // no lock file yet
  }

  const removedIds = lockedIds.filter((id) => !currentIds.includes(id));
  const problems = removedIds.map(
    (id) => `ids.lock: '${id}' was published but no longer exists (never rename or delete published ids)`,
  );

  const newIds = currentIds.filter((id) => !lockedIds.includes(id));
  if (updateLockFile && removedIds.length === 0) {
    await writeFile(lockPath, [...lockedIds, ...newIds].join("\n") + "\n");
    console.log(`ids.lock updated (${newIds.length} new ids)`);
  } else if (newIds.length > 0 && !updateLockFile) {
    console.log(
      `note: ${newIds.length} id(s) not in content/ids.lock yet (run: npm run check -- --update-ids once they are published)`,
    );
  }
  return problems;
}

async function main(): Promise<void> {
  const arguments_ = process.argv.slice(2);
  const updateLockFile = arguments_.includes("--update-ids");
  const singleModulePath = arguments_.find((argument) => !argument.startsWith("--"));
  const problems: string[] = [];
  let checkedFileCount: number;

  if (singleModulePath) {
    const { module, files } = await loadModule(resolve(singleModulePath));
    checkedFileCount = files.length;
    problems.push(...checkModule(module));
  } else {
    const content = await loadContent(CONTENT_DIRECTORY);
    checkedFileCount = content.files.length;
    content.modules.forEach((module, index) => problems.push(...checkModule(module, index + 1)));

    const parsedModules = content.modules.flatMap((module, index) => {
      const parsed = moduleSchema.safeParse({ ...module, number: index + 1 });
      return parsed.success ? [parsed.data] : [];
    });
    checkUniqueIds(parsedModules, (message) => problems.push(message));
    problems.push(...(await findWrongCaseReferences(content.files)));
    problems.push(...(await findOrphanFiles(content.files)));
    problems.push(...(await checkLockedIds(parsedModules, updateLockFile)));
  }

  if (problems.length > 0) {
    console.error(problems.join("\n"));
    console.error(`\n${problems.length} problem(s) found.`);
    process.exit(1);
  }
  console.log(`OK  ${singleModulePath ?? "content"} (${checkedFileCount} files)`);
}

main().catch((error: Error) => {
  console.error(error.message);
  process.exit(1);
});
