// Configuração do site. A ordem dos módulos no menu é a de src/modules.ts.
// Dentro de cada módulo, as páginas ordenam-se pelo campo `sidebar.order` no topo de cada ficheiro.
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { modules } from "./src/modules.ts";

// Onde o site é publicado. Definidos no pipeline; por omissão serve na raiz do servidor.
const site = process.env.SITE || undefined;
const base = process.env.BASE || "/";

export default defineConfig({
  site,
  base,
  integrations: [
    starlight({
      title: ".NET Academy",
      description: "Academia de .NET para programadores de backend: C#, .NET, autenticação e um projeto final com Clean Architecture.",
      logo: { src: "./src/assets/logo.svg", replacesTitle: false },
      favicon: "/favicon.svg",
      defaultLocale: "root",
      locales: { root: { label: "Português", lang: "pt-PT" } },
      // Sem pesquisa e só com tema claro.
      pagefind: false,
      components: {
        Footer: "./src/components/Footer.astro",
        PageTitle: "./src/components/PageTitle.astro",
        ThemeProvider: "./src/components/ThemeProvider.astro",
        ThemeSelect: "./src/components/Empty.astro",
      },
      expressiveCode: {
        themes: ["dark-plus"],
        useStarlightUiThemeColors: false,
        styleOverrides: {
          borderRadius: "12px",
          borderColor: "#333337",
          codeBackground: "#1e1e1e",
          codeFontFamily: '"IBM Plex Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace',
          codeFontSize: "0.92rem",
          codeLineHeight: "1.7",
          codePaddingBlock: "1.1rem",
          codePaddingInline: "1.4rem",
          uiFontFamily: '"IBM Plex Sans", system-ui, sans-serif',
          frames: {
            frameBoxShadowCssValue: "0 1px 2px rgb(14 26 53 / 0.12), 0 14px 28px -16px rgb(14 26 53 / 0.45)",
            editorTabBarBackground: "#252526",
            editorActiveTabBackground: "#1e1e1e",
            editorActiveTabForeground: "#cccccc",
            editorActiveTabBorderColor: "#333337",
            editorTabBarBorderBottomColor: "#333337",
            terminalTitlebarBackground: "#252526",
            terminalTitlebarForeground: "#cccccc",
            terminalTitlebarBorderBottomColor: "#333337",
            terminalBackground: "#1e1e1e",
            inlineButtonForeground: "#cccccc",
          },
        },
      },
      customCss: [
        "@fontsource/ibm-plex-sans/400.css",
        "@fontsource/ibm-plex-sans/500.css",
        "@fontsource/ibm-plex-sans/600.css",
        "@fontsource/ibm-plex-sans/700.css",
        "@fontsource/ibm-plex-mono/400.css",
        "@fontsource/ibm-plex-mono/500.css",
        "./src/styles/academy.css",
      ],
      lastUpdated: true,
      sidebar: modules.map((module) => ({ label: module.label, collapsed: true, items: [{ autogenerate: { directory: module.dir } }] })),
    }),
  ],
  // A página «Entrega final» importa o prompt de ../resources.
  vite: { server: { fs: { allow: [".."] } } },
});
