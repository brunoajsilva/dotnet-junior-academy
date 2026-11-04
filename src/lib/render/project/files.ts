/**
 * Final project: file trees and the guided sections that show code files.
 */
import type { Phase, PhaseSection, TreeNode } from "../../../content/schema";
import { escapeHtml, renderEach, twoDigits } from "../../html";
import { plainSteps, renderSteps } from "../blocks";
import { renderCodeBlock, renderCodeFiles } from "../code";
import type { RenderContext } from "../context";

/** Folder name to the architecture layer colour used for its left border. */
const PROJECT_FOLDER = /^BankingApp\.(Domain|Application|Infrastructure|Api|Tests)\/$/;
const LAYER_COLOUR: Record<string, string> = {
  Domain: "domain",
  Application: "application",
  Infrastructure: "infra",
  Api: "api",
  Tests: "tests",
};

const isGroupFolder = (node: TreeNode) => node.name === "src/" || node.name === "tests/";

function renderTag(node: TreeNode): string {
  return node.tag ? ` <span class="ttag ${node.tag}">${node.tag}</span>` : "";
}

function renderDirectory(context: RenderContext, node: TreeNode, children: TreeNode[]): string {
  const id = `td${++context.idCounters.treeNodes}`;
  context.treeNodesById.set(id, node);
  const project = PROJECT_FOLDER.exec(node.name);
  const projectAttributes = project ? ` class="proj" style="--lc:var(--l-${LAYER_COLOUR[project[1]]})"` : "";
  const groupClass = isGroupFolder(node) ? " grp" : "";
  return (
    `<li${projectAttributes}><details open><summary class="tdir${groupClass}" data-action="select-directory" data-key="${id}">` +
    `${escapeHtml(node.name)}</summary><ul>${renderEach(children, (child) => renderTreeNode(context, child))}</ul></details></li>`
  );
}

export function renderTreeNode(context: RenderContext, node: TreeNode): string {
  if (node.children) return renderDirectory(context, node, node.children);

  const id = `tf${++context.idCounters.treeNodes}`;
  context.treeNodesById.set(id, node);
  const hasCode = node.file && context.phaseFilesByName.has(node.file);
  return (
    `<li><button class="tfile${hasCode ? " has" : ""}" data-action="select-file" data-key="${id}" aria-pressed="false">` +
    `${escapeHtml(node.name)}${renderTag(node)}</button></li>`
  );
}

/** Description and code of the selected tree node. */
export function renderTreePanel(context: RenderContext, node: TreeNode): string {
  const file = node.file ? context.phaseFilesByName.get(node.file) : undefined;
  let body: string;
  if (file) body = renderCodeBlock(context, { code: file.code, language: file.language, fileName: node.file ?? "" });
  else if (node.children) body = '<p class="empty">Pasta. Abre os ficheiros para veres o que contêm.</p>';
  else body = '<p class="empty">Este ficheiro não tem código nesta página.</p>';
  return `<h4>${escapeHtml(node.name)}${renderTag(node)}</h4><p>${escapeHtml(node.description)}</p>${body}`;
}

export function renderPhaseTrees(context: RenderContext, phase: Phase): string {
  return renderEach(phase.trees ?? [], (tree) => {
    const list = renderTreeNode(context, tree.root);
    return (
      `<div class="blk"><h3>${escapeHtml(tree.title)}</h3><p style="color:var(--muted);font-size:.95rem">${escapeHtml(tree.note)}</p>` +
      `<div class="treebox"><div class="tree"><ul>${list}</ul></div><div class="tpanel">${renderTreePanel(context, tree.root)}</div></div></div>`
    );
  });
}

export function renderPhaseSection(context: RenderContext, phase: Phase, section: PhaseSection, index: number): string {
  let html = `<section class="sec"><h2><span class="ix">${twoDigits(index + 1)}</span>${escapeHtml(section.title)}</h2>`;
  if (section.intro) html += `<p class="intro">${escapeHtml(section.intro)}</p>`;
  if (section.steps?.length) {
    html += renderSteps(context, { id: `ph-${phase.id}-${index}`, steps: plainSteps(section.steps) });
  }
  if (section.brunoRequests) {
    const requests = renderEach(
      section.brunoRequests,
      (request) => `<li><div><h4>${escapeHtml(request.title)}</h4><p>${escapeHtml(request.description)}</p></div></li>`,
    );
    html += `<ol class="bruno">${requests}</ol>`;
  }
  if (section.files?.length) html += renderCodeFiles(context, section.files, `u${++context.idCounters.codeTabGroups}`);
  if (section.expectedOutcome) {
    html +=
      `<div class="reveal"><button data-action="toggle-reveal" aria-expanded="false">Ver o que deve acontecer</button>` +
      `<div class="panel" hidden><pre class="term">${escapeHtml(section.expectedOutcome)}</pre></div></div>`;
  }
  return `${html}</section>`;
}
