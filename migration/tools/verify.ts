/**
 * Checks that the conversion kept everything. Compares the current content (content/, read with the
 * current loader) with the generated pages (site/src/content/docs) and the built site (site/dist).
 *
 *   cd site && npm run build && cd .. && npx tsx migration/tools/verify.ts
 *
 * Exit code 1 when a count differs, a code block is missing or an internal link is broken.
 */
import { readdir, readFile, stat } from "node:fs/promises";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type { AcademyModule } from "../../src/content/schema";
import { loadContent } from "../../src/lib/content-loader";

const ROOT = resolve(fileURLToPath(new URL("../..", import.meta.url)));
const DOCS = join(ROOT, "site/src/content/docs");
const DIST = join(ROOT, "site/dist");

const problems: string[] = [];

async function listFiles(directory: string, extensions: string[]): Promise<string[]> {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(
    entries.map((entry) => {
      const path = join(directory, entry.name);
      if (entry.isDirectory()) return listFiles(path, extensions);
      return Promise.resolve(extensions.some((extension) => entry.name.endsWith(extension)) ? [path] : []);
    }),
  );
  return nested.flat();
}

const occurrences = (text: string, pattern: RegExp) => (text.match(pattern) ?? []).length;

function expect(name: string, expected: number, actual: number): void {
  const status = expected === actual ? "OK  " : "FAIL";
  console.log(`${status} ${name}: esperado ${expected}, encontrado ${actual}`);
  if (expected !== actual) problems.push(name);
}

/** What the current content holds, counted straight from the loaded YAML. */
function sourceCounts(modules: AcademyModule[]) {
  const result = { pages: 1, lessons: 0, quiz: 0, learnMore: 0, hints: 0, stories: 0, codeBlocks: [] as string[] };
  for (const module of modules) {
    if (module.kind === "intro") {
      result.pages += module.sections.length;
      for (const section of module.sections)
        for (const block of section.blocks) {
          if (block.type === "cards") result.learnMore += block.cards.filter((card) => card.learnMore).length;
          if (block.type === "steps") result.learnMore += block.steps.filter((step) => step.learnMore).length;
          if (block.type === "outcomes") result.learnMore += block.outcomes.filter((item) => item.learnMore).length;
          if (block.type === "software") result.learnMore += block.tools.filter((tool) => tool.learnMore).length;
        }
    } else if (module.kind === "course") {
      result.pages += 1 + module.chapters.length;
      for (const chapter of module.chapters) {
        result.quiz += chapter.quiz.length;
        for (const lesson of chapter.lessons) {
          result.lessons++;
          if (lesson.learnMore) result.learnMore++;
          if (lesson.type === "code") result.codeBlocks.push(lesson.code);
        }
      }
    } else {
      result.pages += 1 + module.phases.length + 1;
      result.learnMore += module.brief.cards.filter((card) => card.learnMore).length;
      for (const phase of module.phases) {
        if (phase.learnMore) result.learnMore++;
        for (const story of phase.userStories ?? []) {
          result.stories++;
          if (story.hint) result.hints++;
        }
      }
    }
  }
  return result;
}

async function checkLinks(): Promise<void> {
  const exists = await stat(DIST).then(() => true, () => false);
  if (!exists) {
    problems.push("site/dist não existe: corre `npm run build` em site/ antes");
    return;
  }
  let checked = 0;
  for (const file of await listFiles(DIST, [".html"])) {
    const html = await readFile(file, "utf8");
    for (const [, href] of html.matchAll(/<a[^>]+href="([^"#?]+)/g)) {
      if (/^(https?:|mailto:|\/\/)/.test(href)) continue;
      const base = href.startsWith("/") ? DIST : resolve(file, "..");
      const target = resolve(base, `.${href.startsWith("/") ? href : `/${href}`}`);
      const candidates = [target, join(target, "index.html")];
      const found = (await Promise.all(candidates.map((path) => stat(path).then((s) => s.isFile(), () => false)))).some(Boolean);
      checked++;
      if (!found) problems.push(`link partido em ${file.slice(DIST.length)}: ${href}`);
    }
  }
  console.log(`OK   ${checked} links internos verificados (os partidos aparecem abaixo)`);
}

async function main(): Promise<void> {
  const content = await loadContent(join(ROOT, "content"));
  const source = sourceCounts(content.modules as unknown as AcademyModule[]);

  const files = await listFiles(DOCS, [".md", ".mdx"]);
  const texts = await Promise.all(files.map((file) => readFile(file, "utf8")));
  const all = texts.join("\n");

  expect("páginas", source.pages, files.length);
  const chapterTexts = texts.filter((_, index) => /\/(csharp|dotnet|auth)\/(?!index\.)/.test(files[index]));
  const lessonHeadings = chapterTexts.reduce((total, text) => total + occurrences(text, /^## (?!Quiz$)/gm), 0);
  expect("lições", source.lessons, lessonHeadings);
  expect("perguntas de quiz", source.quiz, occurrences(all, /^### Pergunta \d+$/gm));
  expect("respostas de quiz", source.quiz, occurrences(all, /<summary>Ver resposta<\/summary>/g));
  expect("«Saber mais»", source.learnMore, occurrences(all, /<summary>Saber mais<\/summary>/g));
  expect("pistas das user stories", source.hints, occurrences(all, /<summary>Pista de abordagem<\/summary>/g));
  expect("user stories", source.stories, occurrences(all, /^### US\d+ · /gm));

  const missingCode = source.codeBlocks.filter((code) => !all.includes(code));
  expect("exemplos de código das lições presentes palavra a palavra", source.codeBlocks.length, source.codeBlocks.length - missingCode.length);

  await checkLinks();

  if (problems.length) {
    console.error(`\n${problems.length} problema(s):`);
    for (const problem of problems) console.error(`- ${problem}`);
    process.exit(1);
  }
  console.log("\nTudo certo.");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
