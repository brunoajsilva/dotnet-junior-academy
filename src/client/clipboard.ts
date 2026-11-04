/** Copying text and rich text, with a short confirmation on the button. */
import type { RenderContext } from "../lib/render/context";
import { renderStoryForCopy, type StoryPart } from "../lib/render/project/story-details";

function flashLabel(button: HTMLElement, label: string, milliseconds = 1400): void {
  const original = button.textContent;
  button.textContent = label;
  setTimeout(() => (button.textContent = original), milliseconds);
}

function copyWithHiddenTextarea(text: string, button: HTMLElement): void {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  try {
    document.execCommand("copy");
    flashLabel(button, "Copiado");
  } catch {
    flashLabel(button, "Seleciona e copia");
  }
  textarea.remove();
}

export function copyText(text: string, button: HTMLElement): void {
  if (!navigator.clipboard?.writeText) {
    copyWithHiddenTextarea(text, button);
    return;
  }
  navigator.clipboard.writeText(text).then(
    () => flashLabel(button, "Copiado"),
    () => copyWithHiddenTextarea(text, button),
  );
}

/** Copies HTML so that pasting it into Azure DevOps keeps bold text and lists. */
function copyRichText(html: string, onDone: (copied: boolean) => void): void {
  const holder = document.createElement("div");
  holder.innerHTML = html;
  holder.style.cssText =
    "position:fixed;left:-9999px;top:0;font:14px/1.4 Segoe UI,Arial,sans-serif;color:#000;background:#fff;letter-spacing:0";
  document.body.appendChild(holder);

  const selection = getSelection();
  const range = document.createRange();
  range.selectNodeContents(holder);
  selection?.removeAllRanges();
  selection?.addRange(range);
  let copied = false;
  try {
    copied = document.execCommand("copy");
  } catch {
    // falls back to plain text below
  }
  selection?.removeAllRanges();
  document.body.removeChild(holder);

  if (!copied && navigator.clipboard) {
    navigator.clipboard.writeText(holder.textContent ?? "").then(
      () => onDone(true),
      () => onDone(false),
    );
    return;
  }
  onDone(copied);
}

export function copyStoryDetailsPart(context: RenderContext, part: StoryPart, button: HTMLElement): void {
  const userStory = context.openStoryDetails;
  if (!userStory) return;
  const original = button.textContent;
  copyRichText(renderStoryForCopy(userStory, part), (copied) => {
    button.textContent = copied ? "Copiado ✓" : "Não foi possível copiar";
    setTimeout(() => (button.textContent = original), 1600);
  });
}
