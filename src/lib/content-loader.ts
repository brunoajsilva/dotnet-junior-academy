/**
 * Reads the content folder (YAML) into plain objects. Used by the Astro build, by tools/check.ts
 * and by tools/new.ts, so all of them see exactly the same thing.
 *
 *   - `{ $ref: "other.yaml" }` is replaced by the parsed content of that file.
 *   - `{ codeFile: "code/x.cs" }` gets a `code` property with the text of the file.
 *
 * Paths are always relative to the file that mentions them.
 */
import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import YAML from "yaml";

type Json = unknown;
type JsonObject = Record<string, Json>;

export interface LoadedModule {
  module: JsonObject;
  /** Absolute paths of every file that was read (YAML and code). */
  files: string[];
}

export interface LoadedContent {
  title: string;
  modules: JsonObject[];
  files: string[];
  root: string;
}

async function readYaml(path: string): Promise<Json> {
  const text = await readFile(path, "utf8");
  try {
    return YAML.parse(text);
  } catch (error) {
    const reason = error instanceof Error ? error.message.split("\n")[0] : String(error);
    throw new Error(`${path}: invalid YAML (${reason})`);
  }
}

function isReference(node: JsonObject): boolean {
  const keys = Object.keys(node);
  return keys.length === 1 && keys[0] === "$ref";
}

async function resolveNode(node: Json, file: string, files: string[]): Promise<Json> {
  if (Array.isArray(node)) return Promise.all(node.map((item) => resolveNode(item, file, files)));
  if (node === null || typeof node !== "object") return node;

  const object = node as JsonObject;
  if (isReference(object)) return loadFile(resolve(dirname(file), String(object.$ref)), files);

  const keys = Object.keys(object);
  const values = await Promise.all(keys.map((key) => resolveNode(object[key], file, files)));
  const resolved: JsonObject = {};
  keys.forEach((key, index) => (resolved[key] = values[index]));

  if (typeof resolved.codeFile === "string") {
    const codePath = resolve(dirname(file), resolved.codeFile);
    files.push(codePath);
    resolved.codeFile = codePath;
    resolved.code = (await readFile(codePath, "utf8")).replace(/\n$/, "");
  }
  return resolved;
}

async function loadFile(path: string, files: string[]): Promise<Json> {
  files.push(path);
  return resolveNode(await readYaml(path), path, files);
}

/** Load one module given the path of its module.yaml. */
export async function loadModule(modulePath: string): Promise<LoadedModule> {
  const files: string[] = [];
  const module = (await loadFile(resolve(modulePath), files)) as JsonObject;
  return { module, files };
}

/** Load the manifest and every module it lists, numbering the modules in manifest order. */
export async function loadContent(contentDirectory: string): Promise<LoadedContent> {
  const root = resolve(contentDirectory);
  const files: string[] = [];
  const manifestPath = join(root, "manifest.yaml");
  const manifest = (await readYaml(manifestPath)) as { title: string; modules: string[] };
  files.push(manifestPath);

  const modules = (await Promise.all(
    manifest.modules.map((modulePath) => loadFile(join(root, modulePath), files)),
  )) as JsonObject[];
  modules.forEach((module, index) => (module.number = index + 1));
  return { title: manifest.title, modules, files, root };
}
