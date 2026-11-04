/**
 * Syntax highlighting and the code block components (single block and tabbed files).
 */
import type { PhaseFile } from "../../content/schema";
import { escapeHtml, renderEach } from "../html";
import type { RenderContext } from "./context";

const CSHARP_KEYWORDS = new Set(
  (
    "abstract as async await base bool break case catch char class const continue decimal default do double " +
    "else enum false finally float for foreach if in init int interface internal is long namespace new null " +
    "object out override private protected public readonly record ref return sealed short static string struct " +
    "switch this throw true try using var virtual void while and or not when with get set required global " +
    "args yield"
  ).split(" "),
);

const span = (cssClass: string, text: string) => `<span class="${cssClass}">${text}</span>`;
const COMMENT = "c";
const STRING = "s";
const NUMBER = "n";
const KEYWORD = "k";
const TYPE_NAME = "t";

/* Groups: 1 comment, 2 string, 3 number, 4 identifier. */
const CSHARP_TOKEN =
  /(\/\/[^\n]*)|("""[\s\S]*?"""|\$?@?"(?:[^"\\\n]|\\.)*")|(\b\d[\d_]*(?:\.\d+)?[mMfFdDlLuU]?\b)|(\b[A-Za-z_]\w*\b)/g;

function highlightCsharp(code: string): string {
  let html = "";
  let lastEnd = 0;
  for (const match of code.matchAll(CSHARP_TOKEN)) {
    const [, comment, string, number, identifier] = match;
    const start = match.index ?? 0;
    html += escapeHtml(code.slice(lastEnd, start));
    lastEnd = start + match[0].length;

    if (comment) html += span(COMMENT, escapeHtml(comment));
    else if (string) html += span(STRING, escapeHtml(string));
    else if (number) html += span(NUMBER, escapeHtml(number));
    else if (CSHARP_KEYWORDS.has(identifier)) html += span(KEYWORD, identifier);
    else if (/^[A-Z]/.test(identifier) && code.charAt(lastEnd) !== "(") html += span(TYPE_NAME, identifier);
    else html += identifier;
  }
  return html + escapeHtml(code.slice(lastEnd));
}

const isCommentLine = (line: string) => /^\s*#/.test(line);

function highlightShell(code: string): string {
  return code
    .split("\n")
    .map((line) => {
      if (isCommentLine(line)) return span(COMMENT, escapeHtml(line));
      const commentStart = line.indexOf("   #");
      let trailingComment = "";
      if (commentStart > 0) {
        trailingComment = span(COMMENT, escapeHtml(line.slice(commentStart)));
        line = line.slice(0, commentStart);
      }
      const command = escapeHtml(line)
        .replace(/^(\s*)([\w.-]+)/, `$1${span(KEYWORD, "$2")}`)
        .replace(/(\s)(--?[a-zA-Z][\w-]*)/g, `$1${span(NUMBER, "$2")}`);
      return command + trailingComment;
    })
    .join("\n");
}

function highlightJson(code: string): string {
  return escapeHtml(code)
    .replace(/(&quot;(?:[^&]|&(?!quot;))*?&quot;)(\s*:)?/g, (_match, text: string, colon?: string) =>
      colon ? span(TYPE_NAME, text) + colon : span(STRING, text),
    )
    .replace(/\b(\d+(?:\.\d+)?)\b/g, span(NUMBER, "$1"));
}

function highlightXml(code: string): string {
  return escapeHtml(code)
    .replace(/(&lt;\/?[\w.:]+)/g, span(KEYWORD, "$1"))
    .replace(/(&quot;[^&]*?&quot;)/g, span(STRING, "$1"));
}

function highlightHttp(code: string): string {
  return code
    .split("\n")
    .map((line) => {
      if (isCommentLine(line)) return span(COMMENT, escapeHtml(line));
      return escapeHtml(line)
        .replace(/^(GET|POST|PUT|DELETE|PATCH)\b/, span(KEYWORD, "$1"))
        .replace(/^([\w-]+)(:)/, `${span(TYPE_NAME, "$1")}$2`)
        .replace(/(&quot;[^&]*?&quot;)(\s*:)?/g, (_match, text: string, colon?: string) =>
          colon ? span(TYPE_NAME, text) + colon : span(STRING, text),
        );
    })
    .join("\n");
}

export function highlight(code: string, language: string): string {
  switch (language) {
    case "sh":
      return highlightShell(code);
    case "json":
      return highlightJson(code);
    case "xml":
      return highlightXml(code);
    case "http":
      return highlightHttp(code);
    case "txt":
    case "bru":
      return escapeHtml(code);
    default:
      return highlightCsharp(code);
  }
}

const DEFAULT_FILE_LABELS: Record<string, string> = { sh: "Terminal", cs: "C#", xml: ".csproj" };

interface CodeBlockOptions {
  code: string;
  language: string;
  /** Label in the header; defaults to the language. */
  fileName?: string;
  small?: boolean;
}

const copyButton = (targetId: string) =>
  `<button class="copy" data-action="copy-code" data-target="${targetId}">Copiar</button>`;

export function renderCodeBlock(context: RenderContext, options: CodeBlockOptions): string {
  const { code, language, fileName, small } = options;
  const id = `cb${++context.idCounters.codeBlocks}`;
  const label = fileName || DEFAULT_FILE_LABELS[language] || language;
  return (
    `<div class="code"><div class="ch"><span class="fn">${escapeHtml(label)}</span>${copyButton(id)}</div>` +
    `<pre class="${small ? "sm" : ""}" id="${id}"><code>${highlight(code, language)}</code></pre></div>`
  );
}

/** One file as a code block, several files as tabs. */
export function renderCodeFiles(context: RenderContext, files: PhaseFile[], tabGroupId: string): string {
  if (files.length === 1) {
    const [file] = files;
    return renderCodeBlock(context, { code: file.code, language: file.language, fileName: file.name });
  }

  const tabs = renderEach(
    files,
    (file, index) =>
      `<button role="tab" aria-selected="${index === 0}" data-action="select-tab" data-tab-group="${tabGroupId}" data-index="${index}">${escapeHtml(file.name.split("/").pop())}</button>`,
  );
  const panes = renderEach(files, (file, index) => {
    const id = `cb${++context.idCounters.codeBlocks}`;
    return (
      `<div data-pane="${tabGroupId}-${index}" ${index ? "hidden" : ""}>` +
      `<div class="ch"><span class="fn">${escapeHtml(file.name)}</span>${copyButton(id)}</div>` +
      `<pre id="${id}"><code>${highlight(file.code, file.language)}</code></pre></div>`
    );
  });
  return `<div class="code"><div class="tabs" role="tablist">${tabs}</div>${panes}</div>`;
}
