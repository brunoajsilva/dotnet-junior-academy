/** Small DOM helpers for the browser code. */

export function queryOptional<T extends Element = HTMLElement>(selector: string, root: ParentNode = document): T | null {
  return root.querySelector<T>(selector);
}

export function query<T extends Element = HTMLElement>(selector: string, root: ParentNode = document): T {
  const element = root.querySelector<T>(selector);
  if (!element) throw new Error(`element not found: ${selector}`);
  return element;
}

export function queryAll<T extends Element = HTMLElement>(selector: string, root: ParentNode = document): T[] {
  return Array.from(root.querySelectorAll<T>(selector));
}

/** `data-key` of an element, which every action button has. */
export function dataKey(element: HTMLElement): string {
  return element.dataset.key ?? "";
}
