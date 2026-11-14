// Transforma cada <FileTree> do Starlight numa árvore de ficheiros clicável: à esquerda a árvore,
// à direita o contexto do item escolhido (descrição, caminho, etiqueta e o código do ficheiro). Sem JavaScript, fica a árvore normal.
// O Markdown não muda: `- **Account.cs** (novo) Descrição` e `- Pasta/ Descrição`.

type Badge = "novo" | "alterado" | "apagar";
interface Entry {
  kind: "dir" | "file";
  name: string;
  desc: string;
  badge?: Badge;
  children: Entry[];
  parent?: Entry;
}

const BADGES: Record<Badge, { label: string; plural: string; mark: string }> = {
  novo: { label: "Novo", plural: "novos", mark: "+" },
  alterado: { label: "Alterado", plural: "alterados", mark: "~" },
  apagar: { label: "A apagar", plural: "a apagar", mark: "−" },
};

function clean(text: string | null | undefined): string {
  return (text ?? "").replace(/\s+/g, " ").trim();
}

function parse(li: Element, parent?: Entry): Entry {
  const isDir = li.classList.contains("directory");
  const entry = li.querySelector(":scope > details > summary > .tree-entry, :scope > .tree-entry");
  const first = entry?.firstElementChild?.cloneNode(true) as HTMLElement | undefined;
  first?.querySelectorAll(".sr-only, svg").forEach((node) => node.remove());
  let name = clean(first?.textContent);
  let desc = clean(entry?.querySelector(".comment")?.textContent);

  let badge: Badge | undefined;
  const match = desc.match(/^\((novo|alterado|a apagar|apagar)\)\s*/i);
  if (match) {
    badge = match[1].toLowerCase().includes("apagar") ? "apagar" : (match[1].toLowerCase() as Badge);
    desc = desc.slice(match[0].length);
  }
  // Linhas do género «(apagar) (a apagar) A, B e C»: o nome é a lista de ficheiros.
  if (/^\(.*\)$/.test(name)) {
    if (badge === "apagar" && desc) {
      name = desc;
      desc = "Estes ficheiros são apagados neste passo.";
    } else {
      name = name.slice(1, -1);
    }
  }

  const result: Entry = { kind: isDir ? "dir" : "file", name, desc, badge, children: [], parent };
  if (isDir) {
    for (const child of li.querySelectorAll(":scope > details > ul > li")) result.children.push(parse(child, result));
  }
  return result;
}

const FOLDER = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M2 5.5A1.5 1.5 0 0 1 3.5 4h5.2c.4 0 .8.2 1.1.5L11.3 6H20.5A1.5 1.5 0 0 1 22 7.5v11a1.5 1.5 0 0 1-1.5 1.5h-17A1.5 1.5 0 0 1 2 18.5z" fill="currentColor"/></svg>';
const CHEVRON = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M6 3l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

const EXTENSIONS: Record<string, string> = { cs: "C#", json: "JSON", sln: "SLN", md: "MD", csproj: "PRJ", http: "HTTP", bru: "BRU" };

function extension(name: string): string {
  const ext = name.split(".").pop()?.toLowerCase() ?? "";
  return name.includes(".") ? (EXTENSIONS[ext] ?? ext.slice(0, 4).toUpperCase()) : "";
}

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string, html?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (html !== undefined) node.innerHTML = html;
  return node;
}

function pathOf(entry: Entry): string[] {
  const parts: string[] = [];
  for (let current: Entry | undefined = entry.parent; current; current = current.parent) parts.unshift(current.name.replace(/\/$/, ""));
  return parts;
}

function files(entry: Entry): Entry[] {
  return entry.kind === "file" ? [entry] : entry.children.flatMap(files);
}

/** Os blocos de código da página com um caminho no título (ex.: BankingApp.Domain/Customers/Customer.cs). */
function codeBlocks(): Map<string, HTMLElement> {
  const blocks = new Map<string, HTMLElement>();
  for (const frame of document.querySelectorAll<HTMLElement>(".sl-markdown-content figure.frame.has-title")) {
    const title = clean(frame.querySelector("figcaption .title")?.textContent);
    const wrapper = frame.closest<HTMLElement>(".expressive-code");
    if (title.includes("/") && wrapper && !wrapper.closest(".ptree")) blocks.set(title, wrapper);
  }
  return blocks;
}

/** Procura o bloco cujo caminho é o fim do caminho do ficheiro na árvore. */
function findCode(entry: Entry, blocks: Map<string, HTMLElement>): HTMLElement | undefined {
  const full = [...pathOf(entry), entry.name].join("/");
  let best: string | undefined;
  for (const title of blocks.keys()) {
    if (full === title || full.endsWith(`/${title}`)) if (!best || title.length > best.length) best = title;
  }
  return best ? blocks.get(best) : undefined;
}

function copyable(wrapper: HTMLElement): HTMLElement {
  const clone = wrapper.cloneNode(true) as HTMLElement;
  clone.querySelectorAll("link, script").forEach((node) => node.remove());
  clone.classList.add("ptree__code");
  const button = clone.querySelector<HTMLButtonElement>(".copy button");
  button?.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.code ?? "");
      button.dataset.state = "copied";
      setTimeout(() => delete button.dataset.state, 1600);
    } catch {}
  });
  return clone;
}

function enhance(source: HTMLElement) {
  const rootList = source.querySelector(":scope > ul");
  if (!rootList) return;
  const roots = [...rootList.children].map((li) => parse(li));
  const all = roots.flatMap((root) => [root, ...flat(root)]);
  const rows = new Map<Entry, HTMLButtonElement>();
  const blocks = codeBlocks();

  const widget = el("div", "ptree not-content");
  widget.classList.toggle("ptree--code", blocks.size > 0);
  const toolbar = el("div", "ptree__bar");
  const tree = el("div", "ptree__tree");
  const detail = el("aside", "ptree__detail");
  detail.setAttribute("aria-live", "polite");

  const counts = (Object.keys(BADGES) as Badge[]).map((badge) => ({ badge, n: all.filter((e) => e.badge === badge && e.kind === "file").length }));
  toolbar.append(el("span", "ptree__title", "Estrutura do projeto"));
  for (const { badge, n } of counts) {
    if (n) toolbar.append(el("span", `ptree__tag ptree__tag--${badge}`, `<b>${BADGES[badge].mark}</b> ${n} ${BADGES[badge].plural}`));
  }

  function select(entry: Entry) {
    for (const [other, row] of rows) {
      if (other === entry) row.setAttribute("aria-current", "true");
      else row.removeAttribute("aria-current");
    }
    detail.replaceChildren();
    const path = pathOf(entry);
    if (path.length) detail.append(el("p", "ptree__path", path.map((part) => `<span>${part}</span>`).join('<i aria-hidden="true">/</i>')));
    const head = el("div", "ptree__head");
    head.append(el("span", entry.kind === "dir" ? "ptree__icon ptree__icon--dir" : "ptree__icon", entry.kind === "dir" ? FOLDER : extension(entry.name) || "·"));
    head.append(el("h4", "ptree__name", ""));
    head.lastElementChild!.textContent = entry.name;
    detail.append(head);
    const meta = el("p", "ptree__meta");
    meta.append(el("span", "ptree__kind", entry.kind === "dir" ? "Pasta" : "Ficheiro"));
    if (entry.badge) meta.append(el("span", `ptree__tag ptree__tag--${entry.badge}`, `<b>${BADGES[entry.badge].mark}</b> ${BADGES[entry.badge].label}`));
    detail.append(meta);
    const text = el("p", "ptree__desc");
    text.textContent = entry.desc || (entry.kind === "dir" ? "Pasta do projeto." : "Sem descrição.");
    detail.append(text);
    const code = entry.kind === "file" ? findCode(entry, blocks) : undefined;
    if (code) detail.append(copyable(code));
    if (entry.kind === "dir") {
      const inside = files(entry);
      const changed = (Object.keys(BADGES) as Badge[]).map((badge) => ({ badge, n: inside.filter((f) => f.badge === badge).length })).filter((c) => c.n);
      if (changed.length) {
        const summary = el("p", "ptree__summary");
        for (const { badge, n } of changed) summary.append(el("span", `ptree__tag ptree__tag--${badge}`, `<b>${BADGES[badge].mark}</b> ${n} ${BADGES[badge].plural}`));
        detail.append(summary);
      }
    }
  }

  function build(entry: Entry): HTMLElement {
    const item = el("li", `ptree__item ptree__item--${entry.kind}`);
    const row = el("button", `ptree__row${entry.badge ? ` ptree__row--${entry.badge}` : ""}`);
    row.type = "button";
    rows.set(entry, row);
    if (entry.kind === "dir") {
      row.append(el("span", "ptree__chevron", CHEVRON), el("span", "ptree__glyph ptree__glyph--dir", FOLDER));
    } else {
      row.append(el("span", "ptree__chevron ptree__chevron--empty"), el("span", "ptree__glyph", extension(entry.name) || "·"));
    }
    const label = el("span", "ptree__label");
    label.textContent = entry.name;
    row.append(label);
    if (entry.badge) row.append(el("span", `ptree__tag ptree__tag--${entry.badge}`, `<b>${BADGES[entry.badge].mark}</b> ${BADGES[entry.badge].label}`));
    item.append(row);

    let list: HTMLUListElement | undefined;
    if (entry.kind === "dir" && entry.children.length) {
      list = el("ul", "ptree__list");
      for (const child of entry.children) list.append(build(child));
      item.append(list);
      row.setAttribute("aria-expanded", "true");
    }
    row.addEventListener("click", () => {
      select(entry);
      if (list) {
        const open = row.getAttribute("aria-expanded") !== "true";
        row.setAttribute("aria-expanded", String(open));
        list.hidden = !open;
      }
    });
    return item;
  }

  const top = el("ul", "ptree__list ptree__list--top");
  for (const root of roots) top.append(build(root));
  tree.append(top);

  widget.append(toolbar, tree, detail);
  source.after(widget);
  source.classList.add("ptree-source");
  select(all.find((entry) => entry.badge && entry.kind === "file") ?? roots[0]);
}

function flat(entry: Entry): Entry[] {
  return entry.children.flatMap((child) => [child, ...flat(child)]);
}

for (const tree of document.querySelectorAll<HTMLElement>("starlight-file-tree")) enhance(tree);
