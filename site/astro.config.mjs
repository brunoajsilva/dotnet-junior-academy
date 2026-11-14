// Configuração do site. A ordem dos módulos no menu é a ordem da lista `sidebar`.
// Dentro de cada módulo, as páginas ordenam-se pelo campo `sidebar.order` no topo de cada ficheiro.
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// Onde o site é publicado. Definidos no pipeline; por omissão serve na raiz do servidor.
const site = process.env.SITE || undefined;
const base = process.env.BASE || "/";

export default defineConfig({
  site,
  base,
  integrations: [
    starlight({
      title: ".NET Backend Academy",
      description: "Academia de .NET para programadores de backend: C#, .NET, autenticação e um projeto final com Clean Architecture.",
      logo: { src: "./src/assets/logo.svg", replacesTitle: false },
      favicon: "/favicon.svg",
      defaultLocale: "root",
      locales: { root: { label: "Português", lang: "pt-PT" } },
      customCss: ["./src/styles/academy.css"],
      lastUpdated: true,
      sidebar: [
        { label: "Introdução à Academia", items: [{ autogenerate: { directory: "academia" } }] },
        { label: "Introdução ao C#", items: [{ autogenerate: { directory: "csharp" } }] },
        { label: "Introdução ao .NET", items: [{ autogenerate: { directory: "dotnet" } }] },
        { label: "Autenticação e Autorização", items: [{ autogenerate: { directory: "auth" } }] },
        { label: "Projeto final: BankingApp", items: [{ autogenerate: { directory: "projeto" } }] },
      ],
    }),
  ],
  // A página «Entrega final» importa o prompt de ../resources.
  vite: { server: { fs: { allow: [".."] } } },
});
