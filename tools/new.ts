/**
 * Scaffolds content so nobody has to remember the file layout.
 *
 *   npm run new:lesson -- <module> <chapter> <lesson-id> "Title" [code|cards|table|exercise]
 *   npm run new:module -- <module-id> "Title" "Short title"
 *
 * Lessons are created with example text and added at the end of the chapter. Replace the text,
 * then run `npm run check`. Modules are created in content/_drafts/<id>/ (ignored by the site)
 * with one chapter and one lesson; move the folder to content/modules/ and list it in
 * content/manifest.yaml when it is ready.
 */
import { existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const CONTENT_DIRECTORY = fileURLToPath(new URL("../content/", import.meta.url));

type LessonType = "code" | "cards" | "table" | "exercise";

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

/** A double-quoted string is always valid YAML. */
const quote = (text: string): string => JSON.stringify(text);

const LESSON_TEMPLATES: Record<LessonType, (id: string, title: string) => string> = {
  code: (id, title) =>
    `id: ${id}\ntitle: ${quote(title)}\ntype: code\nlanguage: cs\ncodeFile: code/${id}.cs\nkeyPoints:\n  - Primeira ideia, numa frase curta.\n  - Segunda ideia, numa frase curta.\nlearnMore:\n  explanation: Explicação em dois a quatro parágrafos.\n  tryIt: Algo para o aluno experimentar.\n`,
  cards: (id, title) =>
    `id: ${id}\ntitle: ${quote(title)}\ntype: cards\ncards:\n  - title: Conceito A\n    lines:\n      - Uma frase.\n  - title: Conceito B\n    lines:\n      - Uma frase.\n`,
  table: (id, title) =>
    `id: ${id}\ntitle: ${quote(title)}\ntype: table\nrows:\n  - [Coluna 1, Coluna 2]\n  - [Valor, Descrição]\n  - [Valor, Descrição]\n`,
  exercise: (id, title) =>
    `id: ${id}\ntitle: ${quote(title)}\ntype: exercise\nsteps:\n  - keyword: Primeiro\n    text: Instrução do primeiro passo.\n  - keyword: Segundo\n    text: Instrução do segundo passo.\nexpectedOutput: null\nhint: Uma pista curta.\n`,
};

async function createLesson([moduleId, chapterId, lessonId, title, type = "code"]: string[]): Promise<void> {
  if (!moduleId || !chapterId || !lessonId || !title || !(type in LESSON_TEMPLATES)) {
    fail('usage: npm run new:lesson -- <module> <chapter> <lesson-id> "Title" [code|cards|table|exercise]');
  }
  const chapterDirectory = join(CONTENT_DIRECTORY, "modules", moduleId, "chapters", chapterId);
  const chapterFile = join(chapterDirectory, "chapter.yaml");
  if (!existsSync(chapterFile)) fail(`${chapterFile} does not exist`);
  if (existsSync(join(chapterDirectory, `${lessonId}.yaml`))) fail(`lesson ${lessonId} already exists`);

  await writeFile(join(chapterDirectory, `${lessonId}.yaml`), LESSON_TEMPLATES[type as LessonType](lessonId, title));
  if (type === "code") {
    await mkdir(join(chapterDirectory, "code"), { recursive: true });
    await writeFile(
      join(chapterDirectory, "code", `${lessonId}.cs`),
      '// Replace with a runnable example (max 24 lines, English).\nConsole.WriteLine("Hello");\n',
    );
  }

  // add the reference after the last existing lesson of the chapter
  const lines = (await readFile(chapterFile, "utf8")).split("\n");
  const lessonsLine = lines.findIndex((line) => line.startsWith("lessons:"));
  let lastLessonLine = lessonsLine;
  for (let index = lessonsLine + 1; index < lines.length && /^\s+- \$ref:/.test(lines[index]); index++) {
    lastLessonLine = index;
  }
  lines.splice(lastLessonLine + 1, 0, `  - $ref: ${lessonId}.yaml`);
  await writeFile(chapterFile, lines.join("\n"));
  console.log(`created ${lessonId} in ${chapterId}. Edit it, then run: npm run check`);
}

async function createModule([moduleId, title, shortTitle]: string[]): Promise<void> {
  if (!moduleId || !title || !shortTitle) fail('usage: npm run new:module -- <module-id> "Title" "Short title"');
  if (!/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/.test(moduleId)) fail("module id must be kebab-case");

  const moduleDirectory = join(CONTENT_DIRECTORY, "_drafts", moduleId);
  if (existsSync(moduleDirectory)) fail(`${moduleDirectory} already exists`);

  const chapterId = `${moduleId}-1`;
  const lessonId = `${chapterId}-1`;
  const chapterDirectory = join(moduleDirectory, "chapters", chapterId);
  await mkdir(join(chapterDirectory, "code"), { recursive: true });

  await writeFile(
    join(moduleDirectory, "module.yaml"),
    `id: ${moduleId}\nkind: course\ntitle: ${quote(title)}\nshortTitle: ${quote(shortTitle)}\ntagline: Uma ou duas frases sobre o que o aluno aprende neste módulo.\nchapters:\n  - $ref: chapters/${chapterId}/chapter.yaml\n` +
      `wrapUp:\n  learned:\n    - O que o aluno já sabe fazer\n  practiceIdeas:\n    - Uma ideia para praticar\n  docs:\n    - title: Documentação oficial\n      url: https://learn.microsoft.com/dotnet/\n`,
  );
  await writeFile(
    join(chapterDirectory, "chapter.yaml"),
    `id: ${chapterId}\ntitle: Primeiro capítulo\nintro: O que o aluno vai aprender neste capítulo.\nlessons:\n  - $ref: ${lessonId}.yaml\nquiz: []\n`,
  );
  await writeFile(join(chapterDirectory, `${lessonId}.yaml`), LESSON_TEMPLATES.code(lessonId, "Primeira lição"));
  await writeFile(
    join(chapterDirectory, "code", `${lessonId}.cs`),
    '// Replace with a runnable example.\nConsole.WriteLine("Hello");\n',
  );
  console.log(
    `created content/_drafts/${moduleId}/. Check it with: npm run check -- content/_drafts/${moduleId}/module.yaml`,
  );
}

const [command, ...commandArguments] = process.argv.slice(2);
if (command === "lesson") await createLesson(commandArguments);
else if (command === "module") await createModule(commandArguments);
else fail("usage: npm run new:lesson|new:module -- ...");
