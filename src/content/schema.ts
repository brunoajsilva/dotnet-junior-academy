/**
 * Shape of everything under content/. The same schemas validate the content at build time
 * (see ../content.config.ts) and give the renderers their types, so a field that is missing,
 * misspelled or out of range fails the build with the path of the problem.
 */
import { z } from "astro/zod";

const text = z.string().min(1);
const textList = z.array(z.string());
const kebabCase = z.string().regex(/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/, "kebab-case, e.g. 'efcore'");

const codeLanguage = z.enum(["cs", "sh", "json", "xml", "http", "txt", "bru"]);

/** The longer explanation shown in the "Saber mais" drawer. */
const learnMoreSchema = z
  .object({ explanation: text, pitfall: text.optional(), tryIt: text.optional() })
  .strict();

/** A titled card with one summary sentence and an optional "Saber mais" drawer. */
const summaryCardSchema = z
  .object({ title: text, summary: z.string(), learnMore: learnMoreSchema.optional() })
  .strict();

/* ------------------------------------------------------------------ lessons */

const lessonBase = { id: text, title: text, learnMore: learnMoreSchema.optional(), tryItCommand: text.optional() };

const exerciseStepSchema = z.object({ keyword: z.string(), text }).strict();
const tableRowsSchema = z.array(textList).min(2);

const exerciseFields = {
  steps: z.array(exerciseStepSchema).min(2).max(8),
  expectedOutput: z.string().nullable().optional(),
  hint: text.optional(),
  challenge: text.optional(),
  table: tableRowsSchema.optional(),
};

const lessonCardSchema = z
  .object({
    title: z.string(),
    lines: textList,
    codeFile: text.optional(),
    code: text.optional(),
    asChecklist: z.boolean().optional(),
    isNote: z.boolean().optional(),
  })
  .strict();

const levelSchema = z.object({ name: text, description: text }).strict();

const codeLessonSchema = z
  .object({
    ...lessonBase,
    type: z.literal("code"),
    language: codeLanguage,
    codeFile: text,
    code: text,
    keyPoints: z.array(text).min(2).max(4),
  })
  .strict();

const cardsLessonSchema = z
  .object({
    ...lessonBase,
    type: z.literal("cards"),
    /** How many of the first cards are drawn as a left-to-right flow of steps. */
    flowSteps: z.number().int().optional(),
    cards: z.array(lessonCardSchema).min(2).max(8),
  })
  .strict();

const tableLessonSchema = z
  .object({ ...lessonBase, type: z.literal("table"), rows: tableRowsSchema, note: z.string().optional() })
  .strict();

const exerciseLessonSchema = z.object({ ...lessonBase, type: z.literal("exercise"), ...exerciseFields }).strict();

/** Shipped lessons with their own drawings. New modules should use "cards" instead. */
const domainLessonSchema = z
  .object({
    ...lessonBase,
    type: z.literal("domain"),
    entities: z.array(z.object({ name: text, fields: text }).strict()).length(3),
    relations: z.array(text).length(2),
    ...exerciseFields,
  })
  .strict();

const pyramidLessonSchema = z
  .object({
    ...lessonBase,
    type: z.literal("pyramid"),
    levels: z.array(levelSchema),
    cards: z.array(z.object({ title: text, lines: textList }).strict()),
  })
  .strict();

const layersLessonSchema = z
  .object({ ...lessonBase, type: z.literal("layers"), levels: z.array(levelSchema).length(3), rules: textList })
  .strict();

const lessonSchema = z.discriminatedUnion("type", [
  codeLessonSchema,
  cardsLessonSchema,
  tableLessonSchema,
  exerciseLessonSchema,
  domainLessonSchema,
  pyramidLessonSchema,
  layersLessonSchema,
]);

const quizQuestionSchema = z
  .object({
    question: text,
    options: z.array(text).min(3).max(5),
    /** Index (from 0) of the correct option. */
    correctIndex: z.number().int().min(0),
    explanation: text,
  })
  .strict()
  .refine((q) => q.correctIndex < q.options.length, "'correctIndex' must point to one of the options");

const chapterSchema = z
  .object({
    id: text,
    title: text,
    intro: text,
    lessons: z.array(lessonSchema).min(1).max(14),
    quiz: z.array(quizQuestionSchema).max(6),
  })
  .strict();

/* ------------------------------------------------------------------ modules */

const moduleHead = {
  /** Position in the manifest, starting at 1 (set by the loader). */
  number: z.number().int(),
  id: kebabCase,
  title: text,
  shortTitle: z.string().max(28),
  tagline: text.max(260),
};

const wrapUpSchema = z
  .object({
    learned: z.array(text).min(1),
    practiceIdeas: z.array(text).min(1),
    docs: z.array(z.object({ title: text, url: z.string().url() }).strict()),
  })
  .strict();

const courseModuleSchema = z
  .object({ ...moduleHead, kind: z.literal("course"), chapters: z.array(chapterSchema).min(1), wrapUp: wrapUpSchema })
  .strict();

/* Introduction module ("academia") */

const toolSchema = z
  .object({
    id: text,
    name: text,
    requirement: z.enum(["required", "optional", "later"]),
    reason: text,
    checkCommand: z.string(),
    expectedResult: z.string(),
    installation: text,
    learnMore: learnMoreSchema.optional(),
  })
  .strict();

const introBlockSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("paragraph"), text }).strict(),
  z.object({ type: z.literal("cards"), title: text.optional(), cards: z.array(summaryCardSchema) }).strict(),
  z.object({ type: z.literal("steps"), steps: z.array(summaryCardSchema) }).strict(),
  z
    .object({
      type: z.literal("outcomes"),
      outcomes: z.array(summaryCardSchema.extend({ moduleId: text }).strict()),
    })
    .strict(),
  z.object({ type: z.literal("plan") }).strict(),
  z
    .object({
      type: z.literal("schedule"),
      weeks: z
        .array(
          z
            .object({
              title: text,
              days: z
                .array(
                  z
                    .object({
                      /** Working day of the academy, starting at 1. */
                      day: z.number().int().min(1),
                      items: z
                        .array(
                          z
                            .object({
                              moduleId: text,
                              title: text,
                              detail: z.string().optional(),
                              /** Route the item links to, for example "csharp-2". */
                              routeId: text.optional(),
                            })
                            .strict(),
                        )
                        .min(1),
                    })
                    .strict(),
                )
                .min(1),
            })
            .strict(),
        )
        .min(1),
    })
    .strict(),
  z.object({ type: z.literal("software"), tools: z.array(toolSchema) }).strict(),
]);

const introSectionSchema = z.object({ id: text, title: text, blocks: z.array(introBlockSchema) }).strict();

const introModuleSchema = z
  .object({ ...moduleHead, kind: z.literal("intro"), sections: z.array(introSectionSchema).min(1) })
  .strict();

/* Final project module */

const scenarioSchema = z
  .object({ title: text, given: textList, when: textList, then: textList })
  .strict();

const storyDetailsSchema = z
  .object({
    persona: text,
    want: text,
    purpose: text,
    description: text,
    scenarios: z.array(scenarioSchema),
    outOfScope: textList,
    storyPoints: z.number(),
  })
  .strict();

/** A user story of the project brief. */
const userStorySchema = z
  .object({
    id: text,
    kind: z.string().optional(),
    title: text,
    story: text,
    /** Id of the feature (group of user stories) this story belongs to. */
    feature: text.optional(),
    endpoint: z.string().nullable(),
    body: z.string().nullable(),
    rules: textList,
    responses: z.array(z.object({ result: text, when: text }).strict()),
    criteria: z.array(text),
    uses: textList.optional(),
    hint: learnMoreSchema.optional(),
    /** "Alto", "Médio" or "Baixo". */
    businessValue: z.string().optional(),
    dependsOn: z.string().optional(),
    /** The formal story (persona, scenarios, story points) shown in the drawer and copied to Azure DevOps. */
    details: storyDetailsSchema.optional(),
  })
  .strict();

export interface TreeNode {
  name: string;
  description: string;
  /** Name of the code file shown for this node (matches `files[].name` of a phase section). */
  file?: string | null;
  tag?: string | null;
  children?: TreeNode[];
}

const treeNodeSchema: z.ZodType<TreeNode> = z.lazy(() =>
  z
    .object({
      name: text,
      description: z.string(),
      file: z.string().nullable().optional(),
      tag: z.string().nullable().optional(),
      children: z.array(treeNodeSchema).optional(),
    })
    .strict(),
);

const phaseFileSchema = z.object({ name: text, language: codeLanguage, codeFile: text, code: text }).strict();

const phaseSectionSchema = z
  .object({
    title: text,
    intro: text.optional(),
    steps: z.array(text).optional(),
    brunoRequests: z.array(z.object({ title: text, description: text }).strict()).optional(),
    files: z.array(phaseFileSchema).optional(),
    expectedOutcome: text.optional(),
  })
  .strict();

/** A group of related user stories (what is usually called an epic). */
const featureSchema = z.object({ id: text, title: text, description: text }).strict();

const phaseSchema = z
  .object({
    id: text,
    /** "Dia 1"..., empty for the session with the trainer. */
    day: z.string(),
    kind: z.string(),
    title: text,
    goal: text,
    uses: textList.optional(),
    trees: z.array(z.object({ title: text, note: text, root: treeNodeSchema }).strict()).optional(),
    rules: textList.optional(),
    features: z.array(featureSchema).optional(),
    userStories: z.array(userStorySchema).optional(),
    sections: z.array(phaseSectionSchema).optional(),
    learnMore: learnMoreSchema.optional(),
  })
  .strict();

const layerSchema = z
  .object({
    id: text,
    name: text,
    role: text,
    color: text,
    contains: textList,
    references: textList,
    neverKnows: text,
    rationale: text,
  })
  .strict();

const projectModuleSchema = z
  .object({
    ...moduleHead,
    kind: z.literal("project"),
    brief: z.object({ context: text, cards: z.array(summaryCardSchema) }).strict(),
    days: z
      .array(z.object({ label: text, title: text, goal: text, route: text }).strict())
      .min(1),
    layers: z.array(layerSchema).min(1),
    flow: z.array(z.object({ layer: text, title: text, description: text }).strict()).min(1),
    finalDelivery: z
      .object({
        title: text,
        intro: text,
        deliverables: z.array(z.object({ title: text, description: text }).strict()).min(1),
        reviewSteps: z.array(z.object({ title: text, description: text }).strict()).min(1),
        planVersusReality: textList,
        reviewQuestions: textList,
      })
      .strict(),
    endpoints: tableRowsSchema,
    acceptanceCriteria: textList,
    extras: textList,
    phases: z.array(phaseSchema).min(1),
  })
  .strict();

export const moduleSchema = z.discriminatedUnion("kind", [
  courseModuleSchema,
  introModuleSchema,
  projectModuleSchema,
]);

/* ------------------------------------------------------------------ types */

export type LearnMore = z.infer<typeof learnMoreSchema>;
export type SummaryCard = z.infer<typeof summaryCardSchema>;
export type Lesson = z.infer<typeof lessonSchema>;
export type CodeLesson = z.infer<typeof codeLessonSchema>;
export type CardsLesson = z.infer<typeof cardsLessonSchema>;
export type LessonCard = z.infer<typeof lessonCardSchema>;
export type ExerciseLike = z.infer<typeof exerciseLessonSchema> | z.infer<typeof domainLessonSchema>;
export type QuizQuestion = z.infer<typeof quizQuestionSchema>;
export type Chapter = z.infer<typeof chapterSchema>;
export type CourseModule = z.infer<typeof courseModuleSchema>;
export type IntroModule = z.infer<typeof introModuleSchema>;
export type IntroSection = z.infer<typeof introSectionSchema>;
export type IntroBlock = z.infer<typeof introBlockSchema>;
export type Tool = z.infer<typeof toolSchema>;
export type ProjectModule = z.infer<typeof projectModuleSchema>;
export type Phase = z.infer<typeof phaseSchema>;
export type PhaseSection = z.infer<typeof phaseSectionSchema>;
export type PhaseFile = z.infer<typeof phaseFileSchema>;
export type Feature = z.infer<typeof featureSchema>;
export type UserStory = z.infer<typeof userStorySchema>;
export type StoryDetails = z.infer<typeof storyDetailsSchema>;
export type Layer = z.infer<typeof layerSchema>;
export type AcademyModule = z.infer<typeof moduleSchema>;
