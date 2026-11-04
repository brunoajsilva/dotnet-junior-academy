/**
 * Small helpers shared by every renderer: escaping, icons and internal links.
 *
 * The renderers return HTML strings, so they run unchanged in the static build (Node) and in the
 * browser. Internal links are written as `href="#route-id"` and turned into real URLs by
 * `rewriteHashLinks()` once the whole page is assembled.
 */

export function escapeHtml(value: unknown): string {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/** Renders every item and concatenates the results. */
export function renderEach<T>(items: readonly T[], render: (item: T, index: number) => string): string {
  return items.map(render).join("");
}

/** Plain text with blank lines between paragraphs, as written in the content files. */
export function renderParagraphs(text: string): string {
  return text
    .split(/\n\n+/)
    .map((paragraph) => `<p class="pre">${escapeHtml(paragraph)}</p>`)
    .join("");
}

export const ARROW_ICON =
  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';

export const TICK_ICON =
  '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7"/></svg>';

/** "1" becomes "01": the number shown next to lessons and sections. */
export function twoDigits(number: number): string {
  return number < 10 ? `0${number}` : String(number);
}

/* ------------------------------------------------------------ internal links */

let baseUrl = "/";

/** Where the site is served from (Astro's BASE_URL), e.g. "/dotnet-junior-academy/". */
export function setBaseUrl(url: string): void {
  baseUrl = url.endsWith("/") ? url : `${url}/`;
}

/** URL of a page. The home page has the empty route id. */
export function routeUrl(routeId: string): string {
  return routeId ? `${baseUrl}${routeId}/` : baseUrl;
}

export function rewriteHashLinks(html: string): string {
  return html.replace(/href="#([^"]*)"/g, (_match, routeId: string) => `href="${routeUrl(routeId)}"`);
}

/**
 * The academy's logo mark: three rising bars in a rounded square. It is the same for every academy;
 * only the name next to it changes. The colour follows the theme through `--accent`.
 */
export const LOGO_MARK =
  '<svg class="logo" viewBox="0 0 40 40" width="28" height="28" aria-hidden="true" focusable="false">' +
  '<rect width="40" height="40" rx="11" fill="var(--accent)"/>' +
  '<rect x="9.5" y="21" width="5.5" height="9" rx="2.75" fill="#fff" fill-opacity=".5"/>' +
  '<rect x="17.25" y="15" width="5.5" height="15" rx="2.75" fill="#fff" fill-opacity=".78"/>' +
  '<rect x="25" y="9" width="5.5" height="21" rx="2.75" fill="#fff"/></svg>';
