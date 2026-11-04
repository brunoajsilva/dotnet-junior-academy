/**
 * Course pages: module overview, chapters, quizzes and the module wrap-up.
 */
import type { Chapter, CourseModule } from "../../../content/schema";
import { escapeHtml, renderEach } from "../../html";
import { chapterProgress, moduleProgress } from "../../progress";
import { isExercise, renderLesson } from "../blocks";
import type { RenderContext } from "../context";
import { moduleColour, renderBreadcrumb, renderPager, renderProgressBar } from "../shared";

function pageHeader(module: CourseModule, eyebrow: string, title: string, lead: string, progressBar: string): string {
  return (
    `<header class="ph" style="${moduleColour(module)}"><p class="eyebrow">${eyebrow}</p>` +
    `<h1>${escapeHtml(title)}</h1><p class="lead">${escapeHtml(lead)}</p>${progressBar}</header>`
  );
}

function renderChapterCard(context: RenderContext, chapter: Chapter, index: number): string {
  const { done, total } = chapterProgress(context.progress, chapter);
  const exerciseTag = chapter.lessons.some(isExercise) ? '<span class="tag ex">exercício</span>' : "";
  const quizTag = chapter.quiz.length ? '<span class="tag qz">quiz</span>' : "";
  return (
    `<a class="chcard" href="#${chapter.id}"><span class="num">${index + 1}</span><div><h3>${escapeHtml(chapter.title)}</h3>` +
    `<p>${escapeHtml(chapter.intro)}</p><div style="margin-top:8px"><span class="tag">${chapter.lessons.length} temas</span>` +
    `${exerciseTag}${quizTag}</div></div><span class="st">${done}/${total} vistos</span></a>`
  );
}

export function renderModuleOverview(context: RenderContext, module: CourseModule): string {
  const header = pageHeader(
    module,
    `Módulo ${module.number}`,
    module.title,
    module.tagline,
    renderProgressBar(moduleProgress(context.progress, module)),
  );
  const chapters = renderEach(module.chapters, (chapter, index) => renderChapterCard(context, chapter, index));
  return (
    renderBreadcrumb(context, module) +
    header +
    `<div class="chlist" style="${moduleColour(module)}">${chapters}</div>` +
    renderPager(context, module.id)
  );
}

/* ------------------------------------------------------------------ quiz */

export function renderQuiz(context: RenderContext, chapter: Chapter): string {
  if (!chapter.quiz.length) return "";
  const answers = context.progress.quizAnswers[chapter.id] ?? [];
  const finished = chapter.quiz.every((_question, index) => answers[index] != null);
  const score = chapter.quiz.filter((question, index) => answers[index] === question.correctIndex).length;

  const questions = renderEach(chapter.quiz, (question, questionIndex) => {
    const chosen = answers[questionIndex];
    const answered = chosen != null;
    const options = renderEach(question.options, (option, optionIndex) => {
      const state = !answered ? "" : optionIndex === question.correctIndex ? " right" : optionIndex === chosen ? " wrong" : "";
      return (
        `<button class="opt${state}" ${answered ? "disabled" : ""} data-action="answer" data-chapter="${chapter.id}" ` +
        `data-question="${questionIndex}" data-option="${optionIndex}">${escapeHtml(option)}</button>`
      );
    });
    const feedback = answered
      ? `<p class="why"><b>${chosen === question.correctIndex ? "Certo. " : "Não é bem assim. "}</b>${escapeHtml(question.explanation)}</p>`
      : "";
    return `<div class="q"><p class="qt">${questionIndex + 1}. ${escapeHtml(question.question)}</p><div class="opts">${options}</div>${feedback}</div>`;
  });

  const result = finished
    ? `<div class="score"><span>Resultado: ${score} de ${chapter.quiz.length}</span><button class="btn" data-action="reset-quiz" data-chapter="${chapter.id}">Repetir</button></div>`
    : "";
  return (
    `<section class="quiz" id="quiz-${chapter.id}"><h2>Verifica o que aprendeste</h2>` +
    `<p class="sub2">${chapter.quiz.length} perguntas. Escolhe uma resposta para veres a explicação.</p>${questions}${result}</section>`
  );
}

/* --------------------------------------------------------------- wrap-up */

function renderWrapUp(module: CourseModule): string {
  const { learned, practiceIdeas, docs } = module.wrapUp;
  const list = (items: readonly string[]) => `<ul>${renderEach(items, (item) => `<li>${escapeHtml(item)}</li>`)}</ul>`;
  const docLinks = renderEach(
    docs,
    (doc) => `<li><a href="${doc.url}" target="_blank" rel="noopener">${escapeHtml(doc.title)}</a></li>`,
  );
  return (
    `<section class="outro"><h2>Para continuar a aprender</h2><div class="cgrid">` +
    `<div class="icard"><h4>Já sabes</h4>${list(learned)}</div>` +
    `<div class="icard"><h4>Documentação</h4><ul>${docLinks}</ul></div>` +
    `<div class="icard"><h4>Para praticar</h4>${list(practiceIdeas)}</div></div></section>`
  );
}

/* --------------------------------------------------------------- chapter */

export function renderChapter(context: RenderContext, module: CourseModule, chapterIndex: number): string {
  const chapter = module.chapters[chapterIndex];
  const header = pageHeader(
    module,
    `Módulo ${module.number} · Capítulo ${chapterIndex + 1}`,
    chapter.title,
    chapter.intro,
    renderProgressBar(chapterProgress(context.progress, chapter)),
  );
  const lessons = renderEach(chapter.lessons, (lesson, index) => renderLesson(context, lesson, index));
  const isLastChapter = chapterIndex === module.chapters.length - 1;
  return (
    renderBreadcrumb(context, module, chapter.title) +
    header +
    `<div class="lessons" style="${moduleColour(module)}">${lessons}</div>` +
    renderQuiz(context, chapter) +
    (isLastChapter ? renderWrapUp(module) : "") +
    renderPager(context, chapter.id)
  );
}
