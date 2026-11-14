// Na página «Enunciado: user stories», cada user story (### USn · Título) fica reduzida a uma linha com o título.
// Ao clicar, o conteúdo abre numa janela (modal) com tudo: regras, resultados, critérios, pista e história para o Azure DevOps.
// Sem JavaScript, as user stories aparecem por extenso na página.

interface Story {
  id: string;
  title: string;
  group: string;
  holder: HTMLElement;
}

const content = document.querySelector<HTMLElement>(".sl-markdown-content");
const wrappers = content ? [...content.querySelectorAll<HTMLElement>(":scope > .sl-heading-wrapper.level-h3")] : [];
const stories: Story[] = [];
let open: (index: number) => void = () => {};

function create<K extends keyof HTMLElementTagNameMap>(tag: K, className: string, text?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function groupOf(wrapper: HTMLElement): string {
  for (let node = wrapper.previousElementSibling; node; node = node.previousElementSibling) {
    if (node.classList.contains("level-h2")) return node.querySelector("h2")?.textContent?.trim() ?? "";
  }
  return "";
}

for (const wrapper of wrappers) {
  const heading = wrapper.querySelector("h3");
  const match = heading?.textContent?.trim().match(/^(US\d+)\s*·\s*(.+)$/);
  if (!heading || !match) continue;

  // Tudo o que vem a seguir, até ao próximo título de nível 2 ou 3, é o conteúdo da user story.
  const holder = create("div", "us__content");
  holder.hidden = true;
  let next = wrapper.nextElementSibling;
  while (next && !next.classList.contains("level-h2") && !next.classList.contains("level-h3")) {
    const following = next.nextElementSibling;
    holder.append(next);
    next = following;
  }

  const story: Story = { id: match[1], title: match[2], group: groupOf(wrapper), holder };
  const row = create("button", "us__row");
  row.type = "button";
  row.append(create("span", "us__id", story.id), create("span", "us__title", story.title), create("span", "us__go", "Abrir"));
  row.addEventListener("click", () => open(stories.indexOf(story)));
  wrapper.before(row);
  wrapper.after(holder);
  wrapper.hidden = true;
  stories.push(story);
}

if (stories.length) {
  const dialog = create("dialog", "us__dialog");
  dialog.setAttribute("aria-labelledby", "us-title");
  const head = create("header", "us__head");
  const heading = create("div", "us__heading");
  const kicker = create("p", "us__kicker");
  const title = create("h2", "us__dialog-title");
  title.id = "us-title";
  heading.append(kicker, title);
  const close = create("button", "us__close");
  close.type = "button";
  close.setAttribute("aria-label", "Fechar");
  close.innerHTML = '<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
  head.append(heading, close);
  const body = create("div", "us__body sl-markdown-content");
  const foot = create("footer", "us__foot");
  const prev = create("button", "us__nav us__nav--prev");
  const nextButton = create("button", "us__nav us__nav--next");
  prev.type = nextButton.type = "button";
  foot.append(prev, nextButton);
  dialog.append(head, body, foot);
  document.body.append(dialog);

  let current = -1;

  function show(index: number) {
    if (current >= 0) stories[current].holder.append(...body.childNodes);
    current = index;
    const story = stories[index];
    kicker.textContent = story.group;
    title.textContent = `${story.id} · ${story.title}`;
    body.append(...story.holder.childNodes);
    body.scrollTop = 0;
    const before = stories[index - 1];
    const after = stories[index + 1];
    prev.hidden = !before;
    nextButton.hidden = !after;
    if (before) prev.textContent = `‹ ${before.id} ${before.title}`;
    if (after) nextButton.textContent = `${after.id} ${after.title} ›`;
  }

  open = (index: number) => {
    show(index);
    dialog.showModal();
  };

  prev.addEventListener("click", () => show(current - 1));
  nextButton.addEventListener("click", () => show(current + 1));
  close.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener("close", () => {
    if (current >= 0) stories[current].holder.append(...body.childNodes);
    current = -1;
  });
}
