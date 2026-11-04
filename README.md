# .NET Backend Academy

Site de ensino de .NET para programadores de backend, com módulos, lições, quizzes, progresso guardado no browser, pesquisa e um projeto final guiado (BankingApp, Clean Architecture).

Feito com [Astro](https://astro.build) e TypeScript. As páginas são geradas em build (HTML estático, publicado no GitHub Pages). O conteúdo vive em ficheiros YAML e de código dentro de `content/`, validado por schemas Zod.

## Módulos

| # | Módulo | Tipo |
|---|---|---|
| 1 | Academia (introdução, software, plano) | `intro` |
| 2 | C# | `course` |
| 3 | .NET | `course` |
| 4 | Autenticação e Autorização | `course` |
| 5 | Projeto final: BankingApp | `project` |

A ordem é a de `content/manifest.yaml`.

## Requisitos

- Node.js 20 ou superior (o CI usa 22)

## Correr localmente

```bash
npm install
npm run dev        # http://localhost:4321/dotnet-junior-academy/  (recarrega ao guardar)
npm run build      # gera dist/ e o índice de pesquisa (Pagefind)
npm run preview    # serve dist/ tal como o GitHub Pages
npm run check      # valida o conteúdo e os tipos (rápido)
npm test           # check + build + teste de todas as páginas (precisa de: npx playwright install chromium)
```

A pesquisa só existe depois de `npm run build`; em `npm run dev` a página de pesquisa avisa disso.

## Estrutura

```
content/    tudo o que se escreve: manifest.yaml, modules/<id>/ (YAML por módulo, capítulo e lição; código ao lado)
src/
  content/  schemas Zod e tipos do conteúdo (schema.ts)
  lib/      carregar conteúdo, rotas, progresso e renderizadores (lib/render/)
  client/   código do browser: progresso, quiz, gaveta "Saber mais", copiar
  pages/    páginas Astro (início, [route], pesquisa, modules.json)
  layouts/  casca da página
  styles/   CSS (tokens, base, layout, components, pages)
tools/      check.ts (validação), new.ts (esqueletos), smoke.ts (teste de todas as páginas)
docs/       arquitetura, desenvolvimento, esquema do conteúdo, estilo, design
prompts/    prompts prontos para evoluir o conteúdo com IA
design/     fundações de design (tokens W3C e CSS)
.github/    CI (check, build, smoke) e deploy para o GitHub Pages
```

Como tudo se liga está em `docs/ARCHITECTURE.md`.

## Trabalhar no conteúdo

- Corrigir uma lição: edita o ficheiro dela, `content/modules/<módulo>/chapters/<capítulo>/<id-da-lição>.yaml`, ou o código ao lado em `code/`.
- Nova lição: `npm run new:lesson -- csharp csharp-1 m1-20 "Título" code` (tipos: `code`, `cards`, `table`, `exercise`).
- Novo módulo: `npm run new:module -- logging "Logging" "Logging"`, depois segue `docs/AUTHORING.md` (ou o prompt em `prompts/novo-modulo.md`).
- Antes de cada commit: `npm run check`. Antes de mexer em `src/`: `npm test`.

Os campos têm nomes por extenso (`title`, `keyPoints`, `learnMore`, `question`, `correctIndex`, `wrapUp`...). Um nome desconhecido ou mal escrito falha o build com o caminho do problema.

**Nunca mudes o `id` de uma lição, capítulo, secção ou fase já publicados**: o progresso dos alunos é guardado por id. Depois de publicar, corre `npm run check -- --update-ids` para os registar em `content/ids.lock`; o `check` falha se algum desaparecer.

## Publicar

O workflow `.github/workflows/deploy.yml` publica em cada push para `main`. Configuração única: Settings, Pages, Source: **GitHub Actions**. O endereço e o caminho base estão em `site.config.mjs` (se o repositório mudar de nome, altera aí ou define `SITE` e `BASE`). Pull requests correm `.github/workflows/ci.yml`.

## Limitações conhecidas

- O código C# das lições e do projeto final não é compilado (não há `.csproj`), por isso o CI não corre `dotnet build`.
- Os renderizadores devolvem strings HTML, partilhadas entre o build e o browser, em vez de componentes Astro.

## Documentação

| Ficheiro | Para quê |
|---|---|
| `docs/ARCHITECTURE.md` | Como a aplicação funciona e onde mexer em cada coisa |
| `docs/DEVELOPMENT.md` | Comandos, testes, formatação, publicação |
| `docs/AUTHORING.md` | Do tema ao módulo, passo a passo |
| `docs/CONTENT-SCHEMA.md` | Ficheiros e campos do conteúdo |
| `docs/STYLE-GUIDE.md` | Tom, língua e regras de escrita |
| `docs/DESIGN-RULES.md` | CSS, tokens e regras de design |
| `AGENTS.md` | Guia para agentes de IA |
