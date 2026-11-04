import { defineCollection } from "astro:content";
import { fileURLToPath } from "node:url";
import { moduleSchema } from "./content/schema";
import { loadContent } from "./lib/content-loader";

const modules = defineCollection({
  loader: {
    name: "academy-modules",
    load: async ({ store, parseData, generateDigest }) => {
      const contentDirectory = fileURLToPath(new URL("../content", import.meta.url));
      const { modules } = await loadContent(contentDirectory);
      store.clear();
      for (const academyModule of modules) {
        const data = await parseData({ id: String(academyModule.id), data: academyModule });
        store.set({ id: String(academyModule.id), data, digest: generateDigest(JSON.stringify(academyModule)) });
      }
    },
  },
  schema: moduleSchema,
});

export const collections = { modules };
