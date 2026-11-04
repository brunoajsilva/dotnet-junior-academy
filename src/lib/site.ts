/**
 * The loaded modules plus the table of pages (routes) they produce.
 */
import type {
  AcademyModule,
  CourseModule,
  IntroModule,
  IntroSection,
  ProjectModule,
} from "../content/schema";

export type RouteTarget =
  | { kind: "moduleOverview"; module: CourseModule | ProjectModule }
  | { kind: "chapter"; module: CourseModule; chapterIndex: number }
  | { kind: "section"; module: IntroModule; section: IntroSection }
  | { kind: "phase"; module: ProjectModule; phaseIndex: number }
  | { kind: "finalDelivery"; module: ProjectModule };

export interface Route {
  /** Used in the URL: "csharp", "csharp-1", "academia-what", "projeto-p1"... */
  id: string;
  moduleId: string;
  title: string;
  target: RouteTarget;
}

export interface Site {
  modules: AcademyModule[];
  /** Every page except the home page, in reading order. */
  routes: Route[];
  routeById(id: string): Route | undefined;
  moduleById(id: string): AcademyModule | undefined;
  /** The page a module's menu entry opens. */
  firstRouteId(module: AcademyModule): string;
  /** Routes listed under a module in the side menu. */
  menuRoutes(module: AcademyModule): Route[];
  projectModule(): ProjectModule | undefined;
}

export function phaseRouteId(module: ProjectModule, phaseId: string): string {
  return `${module.id}-${phaseId}`;
}

/** The id stays "projeto-check" so existing links and bookmarks keep working. */
export function finalDeliveryRouteId(module: ProjectModule): string {
  return `${module.id}-check`;
}

export function sectionRouteId(module: IntroModule, sectionId: string): string {
  return `${module.id}-${sectionId}`;
}

function routesOfModule(module: AcademyModule): Route[] {
  const route = (id: string, title: string, target: RouteTarget): Route => ({
    id,
    moduleId: module.id,
    title,
    target,
  });

  switch (module.kind) {
    case "intro":
      return module.sections.map((section) =>
        route(sectionRouteId(module, section.id), section.title, { kind: "section", module, section }),
      );
    case "course":
      return [
        route(module.id, `${module.title}: visão geral`, { kind: "moduleOverview", module }),
        ...module.chapters.map((chapter, chapterIndex) =>
          route(chapter.id, chapter.title, { kind: "chapter", module, chapterIndex }),
        ),
      ];
    case "project":
      return [
        route(module.id, "Visão geral e arquitetura", { kind: "moduleOverview", module }),
        ...module.phases.map((phase, phaseIndex) =>
          route(
            phaseRouteId(module, phase.id),
            phase.day ? `${phase.day} · ${phase.title}` : phase.title,
            { kind: "phase", module, phaseIndex },
          ),
        ),
        route(finalDeliveryRouteId(module), "Dia 6 · Entrega final", { kind: "finalDelivery", module }),
      ];
  }
}

export function buildSite(modules: AcademyModule[]): Site {
  const routes = modules.flatMap(routesOfModule);
  const routesById = new Map(routes.map((route) => [route.id, route]));
  const modulesById = new Map(modules.map((module) => [module.id, module]));

  return {
    modules,
    routes,
    routeById: (id) => routesById.get(id),
    moduleById: (id) => modulesById.get(id),
    firstRouteId: (module) =>
      module.kind === "intro" ? sectionRouteId(module, module.sections[0].id) : module.id,
    menuRoutes: (module) =>
      routes.filter(
        (route) => route.moduleId === module.id && (module.kind === "intro" || route.id !== module.id),
      ),
    projectModule: () => modules.find((module): module is ProjectModule => module.kind === "project"),
  };
}

/** Modules that have a hand-picked colour in tokens.css; the others cycle through --c-x0..x5. */
const MODULES_WITH_FIXED_COLOUR = ["academia", "csharp", "dotnet", "auth", "projeto"];

/** CSS custom properties for the modules that do not have a fixed colour. */
export function extraModuleColours(modules: AcademyModule[]): Record<string, string> {
  const colours: Record<string, string> = {};
  let nextIndex = 0;
  for (const module of modules) {
    if (MODULES_WITH_FIXED_COLOUR.includes(module.id)) continue;
    colours[`--c-${module.id}`] = `var(--c-x${nextIndex % 6})`;
    nextIndex++;
  }
  return colours;
}
