import type { APIRoute } from "astro";
import { loadModules } from "../../lib/load-site";

export const GET: APIRoute = async () =>
  new Response(JSON.stringify(await loadModules()), {
    headers: { "Content-Type": "application/json" },
  });
