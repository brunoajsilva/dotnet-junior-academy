/**
 * One-off migration: converts the current academy (content/, read with the current loader) into
 *
 *   site/src/content/docs/**          Starlight pages, one per page of the current site
 *   reference/01-solucao-base/**      BankingApp code after "Montar a solução" (phase p1)
 *   reference/02-autenticacao-jwt/**  BankingApp code after "Autenticação JWT" (p1 with p2 on top)
 *   migration/out/routes.json         old route id -> new URL path
 *   migration/out/report.md           counts and the list of things to review by hand
 *
 * Run from the repository root, after `site/` exists (copied from migration/templates/site):
 *
 *   npx tsx migration/tools/convert.ts            refuses to overwrite existing output
 *   npx tsx migration/tools/convert.ts --force    deletes and regenerates the output
 *
 * It only reads content/. It never changes the current site.
 */
import { mkdir, readdir, rm, stat, writeFile } from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type {
  AcademyModule,
  Chapter,
  CourseModule,
  IntroModule,
  IntroSection,
  LearnMore,
  Lesson,
  Phase,
  PhaseFile,
  ProjectModule,
  SummaryCard,
  TreeNode,
  UserStory,
} from "../../src/content/schema";
import { loadContent } from "../../src/lib/content-loader";

const ROOT = resolve(fileURLToPath(new URL("../..", import.meta.url)));
const DOCS = join(ROOT, "site/src/content/docs");
const REFERENCE = join(ROOT, "reference");
const OUT = join(ROOT, "migration/out");

/** Code snapshots of the final project: the phase whose code is the base, and the phases laid on top. */
const SNAPSHOTS = [
  { folder: "01-solucao-base", phases: ["p1"] },
  { folder: "02-autenticacao-jwt", phases: ["p1", "p2"] },
] as const;

const LANGUAGE: Record<string, string> = {
  cs: "csharp",
  sh: "bash",
  json: "json",
  xml: "xml",
  http: "http",
  txt: "text",
  bru: "text",
};

const REQUIREMENT_LABEL = { required: "Necessário", optional: "Opcional", later: "Mais tarde" } as const;

/* ------------------------------------------------------------------ text helpers */

/** Escapes plain text so Markdown and MDX show it exactly as written. */
function md(text: string): string {
  return text
    .replace(/([\\`*_[\]<>{}|&])/g, "\\$1")
    .replace(/^(\s*)([#>+-]|\d+\.)(?=\s)/gm, "$1\\$2");
}

/** Plain text with blank lines between paragraphs, as written in the YAML. */
function paragraphs(text: string): string {
  return text
    .split(/\n\n+/)
    .map((paragraph) => md(paragraph.trim()))
    .join("\n\n");
}

function bullets(items: readonly string[]): string {
  return items.map((item) => `- ${md(item)}`).join("\n");
}

function numbered(items: readonly string[]): string {
  return items.map((item, index) => `${index + 1}. ${md(item)}`).join("\n");
}

function table(rows: readonly (readonly string[])[]): string {
  const [header, ...body] = rows;
  const line = (cells: readonly string[]) => `| ${cells.map((cell) => md(cell).replace(/\n+/g, " ")).join(" | ")} |`;
  return [line(header), `| ${header.map(() => "---").join(" | ")} |`, ...body.map(line)].join("\n");
}

function fence(code: string, language: string, title?: string): string {
  const longestRun = Math.max(2, ...(code.match(/`+/g) ?? []).map((run) => run.length));
  const ticks = "`".repeat(longestRun + 1);
  const meta = title ? ` title=${JSON.stringify(title)}` : "";
  return `${ticks}${LANGUAGE[language] ?? language}${meta}\n${code}\n${ticks}`;
}

function aside(kind: "note" | "tip" | "caution" | "danger", title: string, text: string): string {
  return `:::${kind}[${md(title)}]\n${paragraphs(text)}\n:::`;
}

function details(summary: string, body: string): string {
  return `<details>\n<summary>${summary}</summary>\n\n${body}\n\n</details>`;
}

function learnMoreBlock(learnMore: LearnMore | undefined, summary = "Saber mais"): string {
  if (!learnMore) return "";
  const parts = [paragraphs(learnMore.explanation)];
  if (learnMore.pitfall) parts.push(aside("caution", "Armadilha", learnMore.pitfall));
  if (learnMore.tryIt) parts.push(aside("tip", "Experimenta", learnMore.tryIt));
  return details(summary, parts.join("\n\n"));
}

function frontmatter(title: string, description: string | undefined, order: number, label?: string): string {
  const lines = ["---", `title: ${JSON.stringify(title)}`];
  if (description) lines.push(`description: ${JSON.stringify(description.replace(/\s+/g, " ").trim())}`);
  lines.push("sidebar:", `  order: ${order}`);
  if (label) lines.push(`  label: ${JSON.stringify(label)}`);
  lines.push("---");
  return lines.join("\n");
}

function slugify(text: string): string {
  return text
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/#/g, "sharp")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

const join2 = (...blocks: string[]) => blocks.filter((block) => block.trim() !== "").join("\n\n");

/* ------------------------------------------------------------------ routes */

interface Page {
  /** Path under site/src/content/docs, without extension: "csharp/fundamentos-da-linguagem". */
  path: string;
  extension: "md" | "mdx";
  title: string;
}

/** Old route id ("csharp-1", "academia-what", "projeto-p1"...) -> new page. */
const pages = new Map<string, Page>();

function urlOf(path: string): string {
  return path === "index" ? "/" : `/${path.replace(/\/index$/, "")}/`;
}

/** Relative link from one page to another, so the site works under any base path. */
function linkFrom(fromPath: string, toRouteId: string): string {
  const target = pages.get(toRouteId);
  if (!target) throw new Error(`unknown route "${toRouteId}"`);
  const fromDirectory = urlOf(fromPath);
  const relativePath = relative(fromDirectory, urlOf(target.path)) || ".";
  return `${relativePath}/`;
}

function registerPages(modules: AcademyModule[]): void {
  for (const module of modules) {
    if (module.kind === "intro") {
      for (const section of module.sections)
        pages.set(`${module.id}-${section.id}`, { path: `${module.id}/${slugify(section.title)}`, extension: "md", title: section.title });
    } else if (module.kind === "course") {
      pages.set(module.id, { path: `${module.id}/index`, extension: "md", title: module.title });
      for (const chapter of module.chapters)
        pages.set(chapter.id, { path: `${module.id}/${slugify(chapter.title)}`, extension: "md", title: chapter.title });
    } else {
      pages.set(module.id, { path: `${module.id}/index`, extension: "md", title: module.title });
      for (const phase of module.phases)
        pages.set(`${module.id}-${phase.id}`, { path: `${module.id}/${slugify(phase.title)}`, extension: "mdx", title: phase.title });
      pages.set(`${module.id}-check`, { path: `${module.id}/entrega-final`, extension: "md", title: module.finalDelivery.title });
    }
  }
}

/** The page a module link opens (an introduction module has no overview page). */
function moduleRouteId(module: AcademyModule): string {
  return module.kind === "intro" ? `${module.id}-${module.sections[0].id}` : module.id;
}

/* ------------------------------------------------------------------ report */

const counts = {
  pages: 0,
  lessons: 0,
  quizQuestions: 0,
  learnMore: 0,
  userStories: 0,
  referenceFiles: 0,
};
const toReview: string[] = [];

/**
 * Texts that describe features of the current site that Starlight does not have (progress, drawer,
 * clickable file tree, personal plan). Every match goes to the report, to be rewritten by hand.
 */
const OBSOLETE_TEXT = [
  /marca(r)?( os temas| cada um)? como vist/i,
  /progresso/i,
  /painel/i,
  /gaveta/i,
  /escolhe um ficheiro/i,
  /carrega num/i,
  /no meu plano|adicionar ao meu plano/i,
  /neste browser/i,
  /marca cada um/i,
  /podes ir marcando/i,
];

async function writePage(routeId: string, content: string): Promise<void> {
  const page = pages.get(routeId);
  if (!page) throw new Error(`no page for route "${routeId}"`);
  for (const [index, line] of content.split("\n").entries()) {
    const match = OBSOLETE_TEXT.find((pattern) => pattern.test(line));
    if (match) toReview.push(`${page.path}.${page.extension}, linha ${index + 1}: fala de uma funcionalidade do site antigo («${line.match(match)![0]}»).`);
  }
  const file = join(DOCS, `${page.path}.${page.extension}`);
  await mkdir(dirname(file), { recursive: true });
  await writeFile(file, `${content.trim()}\n`);
  counts.pages++;
}

/* ------------------------------------------------------------------ course */

function lessonBody(lesson: Lesson): string {
  switch (lesson.type) {
    case "code":
      return join2(fence(lesson.code, lesson.language), bullets(lesson.keyPoints));
    case "cards": {
      const flowCount = lesson.flowSteps ?? 0;
      const flow = lesson.cards.slice(0, flowCount);
      const rest = lesson.cards.slice(flowCount);
      const flowList = flow.length
        ? flow.map((card, index) => `${index + 1}. **${md(card.title.replace(/\s+/g, " "))}** ${md(card.lines.join(" "))}`).join("\n")
        : "";
      const cards = rest.map((card) => {
        if (card.isNote) return aside("note", card.title || "Nota", card.lines.join("\n\n"));
        const body = card.asChecklist || card.lines.length > 1 ? bullets(card.lines) : paragraphs(card.lines.join(""));
        return join2(`#### ${md(card.title)}`, body, card.code ? fence(card.code, "cs") : "");
      });
      return join2(flowList, ...cards);
    }
    case "table":
      return join2(table(lesson.rows), lesson.note ? aside("caution", "Atenção", lesson.note) : "");
    case "exercise":
    case "domain": {
      const domain =
        lesson.type === "domain"
          ? join2(
              table([["Entidade", "Campos"], ...lesson.entities.map((entity) => [entity.name, entity.fields])]),
              `Relações: ${md(lesson.entities[0].name)} ${md(lesson.relations[0])} ${md(lesson.entities[1].name)}; ${md(lesson.entities[1].name)} ${md(lesson.relations[1])} ${md(lesson.entities[2].name)}.`,
            )
          : "";
      const steps = lesson.steps
        .map((step, index) => `${index + 1}. ${step.keyword ? `**${md(step.keyword)}.** ` : ""}${md(step.text)}`)
        .join("\n");
      return join2(
        ":::note[Exercício prático]\nResolve no teu IDE antes de abrires a solução ou o resultado esperado.\n:::",
        domain,
        steps,
        lesson.hint ? aside("tip", "Dica", lesson.hint) : "",
        lesson.table ? table(lesson.table) : "",
        lesson.expectedOutput ? details("Ver resultado esperado", fence(lesson.expectedOutput, "txt")) : "",
        lesson.challenge ? aside("note", "Extra", lesson.challenge) : "",
      );
    }
    case "pyramid":
      return join2(
        lesson.levels.map((level) => `- **${md(level.name)}**: ${md(level.description)}`).join("\n"),
        ...lesson.cards.map((card) => join2(`#### ${md(card.title)}`, bullets(card.lines))),
      );
    case "layers":
      return join2(
        lesson.levels.map((level) => `- **${md(level.name)}**: ${md(level.description)}`).join("\n"),
        bullets(lesson.rules),
      );
  }
}

function renderLesson(lesson: Lesson): string {
  counts.lessons++;
  if (lesson.learnMore) counts.learnMore++;
  return join2(
    `## ${md(lesson.title)}`,
    lessonBody(lesson),
    lesson.tryItCommand ? join2("Experimenta no terminal:", fence(lesson.tryItCommand, "sh")) : "",
    learnMoreBlock(lesson.learnMore),
  );
}

function renderQuiz(chapter: Chapter): string {
  if (!chapter.quiz.length) return "";
  const letters = "ABCDE";
  const questions = chapter.quiz.map((question, index) => {
    counts.quizQuestions++;
    const options = question.options.map((option, optionIndex) => `- **${letters[optionIndex]}.** ${md(option)}`).join("\n");
    const answer = `**${letters[question.correctIndex]}. ${md(question.options[question.correctIndex])}**\n\n${paragraphs(question.explanation)}`;
    return join2(`### Pergunta ${index + 1}`, md(question.question), options, details("Ver resposta", answer));
  });
  return join2("## Quiz", "Responde de cabeça antes de abrires cada resposta.", ...questions);
}

async function writeCourse(module: CourseModule): Promise<void> {
  const overviewPath = pages.get(module.id)!.path;
  const chapterLinks = module.chapters
    .map((chapter) => `- [${md(chapter.title)}](${linkFrom(overviewPath, chapter.id)}): ${md(chapter.intro)}`)
    .join("\n");
  await writePage(
    module.id,
    join2(
      frontmatter(module.title, module.tagline, 0, "Visão geral"),
      paragraphs(module.tagline),
      "## Capítulos",
      chapterLinks,
      "## O que vais aprender",
      bullets(module.wrapUp.learned),
      "## Ideias para praticar",
      bullets(module.wrapUp.practiceIdeas),
      "## Documentação",
      module.wrapUp.docs.map((doc) => `- [${md(doc.title)}](${doc.url})`).join("\n"),
    ),
  );

  for (const [index, chapter] of module.chapters.entries()) {
    if (!chapter.quiz.length) toReview.push(`${pages.get(chapter.id)!.path}: o capítulo não tem quiz (também não tinha no site atual).`);
    await writePage(
      chapter.id,
      join2(
        frontmatter(chapter.title, chapter.intro, index + 1),
        paragraphs(chapter.intro),
        ...chapter.lessons.map(renderLesson),
        renderQuiz(chapter),
      ),
    );
  }
}

/* ------------------------------------------------------------------ introduction */

function summaryCard(card: SummaryCard, extra = ""): string {
  if (card.learnMore) counts.learnMore++;
  return join2(`### ${md(card.title)}`, paragraphs(card.summary), extra, learnMoreBlock(card.learnMore));
}

function renderIntroSection(module: IntroModule, section: IntroSection, modules: AcademyModule[]): string {
  const path = pages.get(`${module.id}-${section.id}`)!.path;
  const blocks = section.blocks.map((block) => {
    switch (block.type) {
      case "paragraph":
        return paragraphs(block.text);
      case "cards":
        return join2(block.title ? `## ${md(block.title)}` : "", ...block.cards.map((card) => summaryCard(card)));
      case "steps":
        return block.steps
          .map((step, index) => summaryCard({ ...step, title: `${index + 1}. ${step.title}` }))
          .join("\n\n");
      case "outcomes":
        return block.outcomes
          .map((outcome) => {
            const target = modules.find((candidate) => candidate.id === outcome.moduleId);
            const link = target ? `Módulo: [${md(target.title)}](${linkFrom(path, moduleRouteId(target))})` : "";
            return summaryCard(outcome, link);
          })
          .join("\n\n");
      case "plan":
        return modules
          .filter((candidate) => candidate.id !== module.id)
          .map((candidate) => {
            const heading = `### [${md(candidate.title)}](${linkFrom(path, moduleRouteId(candidate))})`;
            const children =
              candidate.kind === "course"
                ? candidate.chapters.map((chapter) => `- [${md(chapter.title)}](${linkFrom(path, chapter.id)})`).join("\n")
                : candidate.kind === "project"
                  ? candidate.phases.map((phase) => `- [${md(phase.title)}](${linkFrom(path, `${candidate.id}-${phase.id}`)})`).join("\n")
                  : "";
            return join2(heading, paragraphs(candidate.tagline), children);
          })
          .join("\n\n");
      case "schedule":
        return block.weeks
          .map((week) => {
            const rows = week.days.flatMap((day) =>
              day.items.map((item, itemIndex) => {
                const module = modules.find((candidate) => candidate.id === item.moduleId);
                const title = item.routeId ? `[${md(item.title)}](${linkFrom(path, item.routeId)})` : md(item.title);
                return `| ${itemIndex === 0 ? `Dia ${day.day}` : ""} | ${md(module?.shortTitle ?? item.moduleId)} | ${title} | ${md(item.detail ?? "")} |`;
              }),
            );
            return join2(`## ${md(week.title)}`, ["| Dia | Módulo | Tema | Detalhe |", "| --- | --- | --- | --- |", ...rows].join("\n"));
          })
          .join("\n\n");
      case "software":
        return block.tools
          .map((tool) => {
            if (tool.learnMore) counts.learnMore++;
            return join2(
              `## ${md(tool.name)}`,
              `**${REQUIREMENT_LABEL[tool.requirement]}.** ${md(tool.reason)}`,
              tool.checkCommand ? join2("Para verificar:", fence(tool.checkCommand, "sh")) : "",
              `Resultado esperado: ${md(tool.expectedResult)}`,
              `Instalação: ${md(tool.installation)}`,
              learnMoreBlock(tool.learnMore),
            );
          })
          .join("\n\n");
    }
  });
  return join2(...blocks);
}

async function writeIntro(module: IntroModule, modules: AcademyModule[]): Promise<void> {
  for (const [index, section] of module.sections.entries()) {
    const description = index === 0 ? module.tagline : undefined;
    await writePage(
      `${module.id}-${section.id}`,
      join2(frontmatter(section.title, description, index + 1), renderIntroSection(module, section, modules)),
    );
  }
}

/* ------------------------------------------------------------------ project */

const TAG_LABEL: Record<string, string> = { novo: "novo", alterado: "alterado", apagar: "a apagar" };

function fileTreeLines(node: TreeNode, depth: number): string[] {
  const tag = node.tag ? TAG_LABEL[node.tag] ?? node.tag : "";
  const name = tag ? `**${node.name}**` : node.name;
  const comment = [tag ? `(${tag})` : "", md(node.description)].filter(Boolean).join(" ");
  const line = `${"  ".repeat(depth)}- ${name}${comment ? ` ${comment}` : ""}`;
  return [line, ...(node.children ?? []).flatMap((child) => fileTreeLines(child, depth + 1))];
}

/** Where a code file of a phase lives in the reference solution, or null when it is not part of it. */
function referencePath(fileName: string): string | null {
  if (fileName.startsWith("BankingApp.Tests/")) return `tests/${fileName}`;
  if (/^BankingApp\.[A-Za-z]+\//.test(fileName)) return `src/${fileName}`;
  if (fileName.startsWith("docs/bruno/")) return fileName;
  return null;
}

function snapshotOf(phaseId: string): (typeof SNAPSHOTS)[number] | undefined {
  // The page of a phase shows the code as it is at the end of that phase.
  return [...SNAPSHOTS].reverse().find((snapshot) => snapshot.phases.at(-1) === phaseId);
}

interface MdxImports {
  lines: string[];
  next: number;
}

function renderPhaseFile(file: PhaseFile, phase: Phase, pagePath: string, imports: MdxImports): string {
  const snapshot = snapshotOf(phase.id);
  const target = referencePath(file.name);
  if (snapshot && target) {
    const absolute = join(REFERENCE, snapshot.folder, target);
    const from = join(DOCS, dirname(pagePath));
    const name = `code${imports.next++}`;
    imports.lines.push(`import ${name} from ${JSON.stringify(`${relative(from, absolute)}?raw`)};`);
    return `<Code code={${name}} lang=${JSON.stringify(LANGUAGE[file.language] ?? file.language)} title=${JSON.stringify(file.name)} />`;
  }
  return fence(file.code, file.language, file.name);
}

function renderStory(story: UserStory): string {
  counts.userStories++;
  const facts = [
    story.endpoint ? `**Pedido:** \`${story.endpoint}\`` : "",
    story.businessValue ? `**Valor de negócio:** ${md(story.businessValue)}` : "",
    story.details ? `**Estimativa:** ${story.details.storyPoints} pontos` : "",
    story.dependsOn ? `**Depende de:** ${md(story.dependsOn)}` : "",
  ].filter(Boolean);
  const responses = story.responses.length
    ? table([["Resultado", "Quando"], ...story.responses.map((response) => [response.result, response.when])])
    : "";
  if (story.hint) counts.learnMore++;

  let formal = "";
  if (story.details) {
    const detail = story.details;
    const scenarioText = (scenario: (typeof detail.scenarios)[number], index: number) =>
      [
        `Cenário ${index + 1}: ${scenario.title}`,
        ...scenario.given.map((line, lineIndex) => `${lineIndex ? "E" : "Dado"} ${line}`),
        ...scenario.when.map((line, lineIndex) => `${lineIndex ? "E" : "Quando"} ${line}`),
        ...scenario.then.map((line, lineIndex) => `${lineIndex ? "E" : "Então"} ${line}`),
      ].join("\n");
    const description = [
      `Como ${detail.persona}, quero ${detail.want}, para ${detail.purpose}.`,
      "",
      detail.description,
      "",
      "Regras de negócio",
      ...story.rules.map((rule) => `- ${rule}`),
      "",
      "Fora do âmbito",
      ...detail.outOfScope.map((item) => `- ${item}`),
    ].join("\n");
    formal = details(
      "User story completa para o Azure DevOps",
      join2(
        fence(`${story.id} · ${story.title}`, "txt", "Título"),
        fence(description, "txt", "Descrição"),
        fence(detail.scenarios.map(scenarioText).join("\n\n"), "txt", "Acceptance Criteria"),
      ),
    );
  }

  return join2(
    `### ${md(story.id)} · ${md(story.title)}`,
    paragraphs(story.story),
    facts.join("  \n"),
    story.body ? fence(story.body, "json", "Corpo do pedido") : "",
    story.rules.length ? join2("**Regras**", bullets(story.rules)) : "",
    responses,
    story.criteria.length ? join2("**Critérios de aceitação**", story.criteria.map((item) => `- [ ] ${md(item)}`).join("\n")) : "",
    learnMoreBlock(story.hint, "Pista de abordagem"),
    formal,
  );
}

function renderPhase(module: ProjectModule, phase: Phase): string {
  const page = pages.get(`${module.id}-${phase.id}`)!;
  const imports: MdxImports = { lines: [], next: 1 };
  const parts: string[] = [];

  parts.push(`**${md(phase.day || "Sessão com o formador")}.** ${paragraphs(phase.goal)}`);
  if (phase.uses?.length) {
    const links = phase.uses.filter((routeId) => pages.has(routeId)).map((routeId) => `[${md(pages.get(routeId)!.title)}](${linkFrom(page.path, routeId)})`);
    parts.push(`Usa o que aprendeste em: ${links.join(", ")}.`);
  }
  if (phase.rules?.length) parts.push("## Regras", bullets(phase.rules));

  for (const tree of phase.trees ?? []) {
    parts.push(`## ${md(tree.title)}`, paragraphs(tree.note), `<FileTree>\n\n${fileTreeLines(tree.root, 0).join("\n")}\n\n</FileTree>`);
  }

  for (const section of phase.sections ?? []) {
    parts.push(
      `## ${md(section.title)}`,
      section.intro ? paragraphs(section.intro) : "",
      section.steps?.length ? numbered(section.steps) : "",
      section.brunoRequests?.length
        ? section.brunoRequests.map((request) => `- **${md(request.title)}**: ${md(request.description)}`).join("\n")
        : "",
      ...(section.files ?? []).map((file) => renderPhaseFile(file, phase, page.path, imports)),
      section.expectedOutcome ? aside("tip", "Resultado esperado", section.expectedOutcome) : "",
    );
  }

  const stories = phase.userStories ?? [];
  if (stories.length) {
    const features = phase.features ?? [];
    for (const feature of features) {
      parts.push(`## ${md(feature.id)} · ${md(feature.title)}`, paragraphs(feature.description));
      parts.push(...stories.filter((story) => story.feature === feature.id).map(renderStory));
    }
    const loose = stories.filter((story) => !features.some((feature) => feature.id === story.feature));
    if (loose.length) parts.push("## Outras user stories", ...loose.map(renderStory));
  }

  if (phase.learnMore) {
    counts.learnMore++;
    parts.push(learnMoreBlock(phase.learnMore));
  }

  const components = ["Code", "FileTree"].filter((component) =>
    component === "Code" ? imports.lines.length > 0 : (phase.trees ?? []).length > 0,
  );
  const header = [
    components.length ? `import { ${components.join(", ")} } from "@astrojs/starlight/components";` : "",
    ...imports.lines,
  ].filter(Boolean);
  return join2(header.join("\n"), ...parts);
}

async function writeProject(module: ProjectModule): Promise<void> {
  const overviewPath = pages.get(module.id)!.path;
  const days = table([
    ["Dia", "Tema", "Objetivo"],
    ...module.days.map((day) => [day.label, day.title, day.goal]),
  ]).split("\n");
  // Links in the second column of the days table.
  module.days.forEach((day, index) => {
    if (pages.has(day.route)) days[index + 2] = days[index + 2].replace(md(day.title), `[${md(day.title)}](${linkFrom(overviewPath, day.route)})`);
  });

  const layers = module.layers.map((layer) =>
    join2(
      `### ${md(layer.name)}: ${md(layer.role)}`,
      `**Contém:**\n\n${bullets(layer.contains)}`,
      `**Referencia:** ${layer.references.length ? layer.references.map(md).join(", ") : "nenhum projeto"}.`,
      `**Nunca conhece:** ${md(layer.neverKnows)}`,
      paragraphs(layer.rationale),
    ),
  );

  await writePage(
    module.id,
    join2(
      frontmatter(module.title, module.tagline, 0, "Visão geral"),
      paragraphs(module.tagline),
      paragraphs(module.brief.context),
      ...module.brief.cards.map((card) => summaryCard(card)),
      "## Os dias do projeto",
      days.join("\n"),
      "## Arquitetura",
      ...layers,
      "## O percurso de um pedido",
      module.flow.map((step, index) => `${index + 1}. **${md(step.title)}** (${md(step.layer)}): ${md(step.description)}`).join("\n"),
      "## Endpoints",
      table(module.endpoints),
      "## Critérios de aceitação",
      module.acceptanceCriteria.map((item) => `- [ ] ${md(item)}`).join("\n"),
      "## Extras",
      bullets(module.extras),
    ),
  );

  for (const [index, phase] of module.phases.entries()) {
    await writePage(`${module.id}-${phase.id}`, join2(frontmatter(phase.title, phase.goal, index + 1), renderPhase(module, phase)));
  }

  const delivery = module.finalDelivery;
  await writePage(
    `${module.id}-check`,
    join2(
      frontmatter(delivery.title, delivery.intro, module.phases.length + 1),
      paragraphs(delivery.intro),
      "## O que entregas",
      ...delivery.deliverables.map((item) => join2(`### ${md(item.title)}`, paragraphs(item.description))),
      "## Como corre a review",
      delivery.reviewSteps.map((step, index) => `${index + 1}. **${md(step.title)}** ${md(step.description)}`).join("\n"),
      "## Plano contra realidade",
      numbered(delivery.planVersusReality),
      "## Perguntas que podem surgir na review",
      numbered(delivery.reviewQuestions),
    ),
  );
}

/* ------------------------------------------------------------------ reference solution */

async function listFiles(directory: string): Promise<string[]> {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = await Promise.all(
    entries.map((entry) => {
      const path = join(directory, entry.name);
      return entry.isDirectory() ? listFiles(path) : Promise.resolve([path]);
    }),
  );
  return files.flat();
}

async function writeReference(module: ProjectModule): Promise<void> {
  for (const snapshot of SNAPSHOTS) {
    const written = new Set<string>();
    for (const phaseId of snapshot.phases) {
      const phase = module.phases.find((candidate) => candidate.id === phaseId);
      if (!phase) throw new Error(`phase ${phaseId} not found`);
      for (const file of (phase.sections ?? []).flatMap((section) => section.files ?? [])) {
        const target = referencePath(file.name);
        if (!target) continue;
        const absolute = join(REFERENCE, snapshot.folder, target);
        await mkdir(dirname(absolute), { recursive: true });
        await writeFile(absolute, `${file.code}\n`);
        written.add(target);
      }
    }
    counts.referenceFiles += written.size;
  }
  // Code files of the project that no page shows would be lost: list them for review.
  for (const phase of module.phases) {
    const codeDirectory = join(ROOT, "content/modules", module.id, "phases", phase.id, "code");
    const exists = await stat(codeDirectory).then(() => true, () => false);
    if (!exists) continue;
    const shown = new Set((phase.sections ?? []).flatMap((section) => section.files ?? []).map((file) => file.codeFile));
    for (const file of await listFiles(codeDirectory)) {
      if (!shown.has(file)) toReview.push(`content/${relative(join(ROOT, "content"), file)}: ficheiro de código que nenhuma página mostra.`);
    }
  }
}

/* ------------------------------------------------------------------ home and main */

async function writeHome(title: string, modules: AcademyModule[]): Promise<void> {
  pages.set("", { path: "index", extension: "md", title });
  const list = modules
    .map((module) => `## [${md(module.title)}](${linkFrom("index", moduleRouteId(module))})\n\n${paragraphs(module.tagline)}`)
    .join("\n\n");
  await writePage(
    "",
    join2(
      frontmatter(title, "Academia de .NET para programadores de backend.", 0),
      "A Academia dura 15 dias úteis: C#, .NET, autenticação e um projeto final com Clean Architecture. Começa pela introdução e segue os módulos por ordem.",
      list,
    ),
  );
}

async function main(): Promise<void> {
  const force = process.argv.includes("--force");
  const siteExists = await stat(join(ROOT, "site/astro.config.mjs")).then(() => true, () => false);
  if (!siteExists) throw new Error("site/ não existe. Copia primeiro migration/templates/site para site/ (ver migration/PLAN.md, fase 1).");

  for (const output of [DOCS, REFERENCE]) {
    const exists = await stat(output).then(() => true, () => false);
    if (exists && !force) throw new Error(`${relative(ROOT, output)} já existe. Corre com --force para o apagar e gerar de novo.`);
    if (exists) await rm(output, { recursive: true });
  }

  const content = await loadContent(join(ROOT, "content"));
  const modules = content.modules as unknown as AcademyModule[];
  registerPages(modules);

  await writeHome(content.title, modules);
  for (const module of modules) {
    if (module.kind === "intro") await writeIntro(module, modules);
    else if (module.kind === "course") await writeCourse(module);
    else {
      await writeReference(module);
      await writeProject(module);
    }
  }

  await mkdir(OUT, { recursive: true });
  const routes = Object.fromEntries([...pages].map(([routeId, page]) => [routeId || "(início)", urlOf(page.path)]));
  await writeFile(join(OUT, "routes.json"), `${JSON.stringify(routes, null, 2)}\n`);
  const report = [
    "# Relatório da conversão",
    "",
    `Gerado por migration/tools/convert.ts a ${new Date().toISOString().slice(0, 10)}.`,
    "",
    "| O quê | Quantidade |",
    "| --- | --- |",
    ...Object.entries(counts).map(([name, value]) => `| ${name} | ${value} |`),
    "",
    "## A rever à mão",
    "",
    ...(toReview.length ? toReview.map((item) => `- ${item}`) : ["- Nada."]),
    "",
  ].join("\n");
  await writeFile(join(OUT, "report.md"), report);
  console.log(report);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exit(1);
});
