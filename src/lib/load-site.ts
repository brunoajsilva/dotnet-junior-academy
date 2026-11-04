/** Build-time access to the content collection, shared by every Astro page. */
import { getCollection } from "astro:content";
import type { AcademyModule } from "../content/schema";
import { buildSite, type Site } from "./site";

let cachedModules: AcademyModule[] | null = null;

export async function loadModules(): Promise<AcademyModule[]> {
  if (!cachedModules) {
    const entries = await getCollection("modules");
    // structuredClone: the collection hands out frozen objects and the renderers must not depend on that
    cachedModules = structuredClone(entries.map((entry) => entry.data as AcademyModule)).sort(
      (first, second) => first.number - second.number,
    );
  }
  return cachedModules;
}

export async function loadSite(): Promise<Site> {
  return buildSite(await loadModules());
}
