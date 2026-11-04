# Arquitetura

Site gerado com Astro (HTML estático) e publicado no GitHub Pages. O conteúdo (YAML e código) é lido no build, validado por schemas e convertido em páginas. No browser corre um único script que repõe o progresso do aluno e trata das interações.

## Fluxo

1. **Build.** `src/content.config.ts` define a collection `modules`: um loader lê `content/manifest.yaml`, segue as referências `$ref` e `codeFile` (`src/lib/content-loader.ts`) e valida cada módulo com Zod. Um erro de conteúdo falha o build com o caminho do campo.
2. **Páginas.** `src/pages/index.astro` e `src/pages/[route].astro` geram uma página por rota (início, módulo, capítulo, secção, fase do projeto). `src/lib/render/page.ts` devolve o HTML da coluna principal; `src/layouts/Base.astro` junta o menu, a barra e a gaveta. `src/pages/pesquisa.astro` usa o Pagefind.
3. **Dados para o browser.** `src/pages/data/modules.json.ts` publica todos os módulos (com o código) num JSON. O browser lê-o uma vez e fica em cache.
4. **Cliente.** `src/client/app.ts` carrega esse JSON, redesenha a página com o progresso do `localStorage` (chave `academia-dotnet-v1`, por id de lição e de quiz) e liga os eventos (`events.ts`). A página já chega completa, por isso lê-se mesmo sem JavaScript.
5. **Pesquisa.** `npm run build` corre o Pagefind sobre `dist/`. Só existe no site gerado, não em `npm run dev`.

## Código (`src/`)

| Ficheiro | Responsabilidade |
|---|---|
| `content/schema.ts` | Schemas Zod de todo o conteúdo e os tipos TypeScript que daí saem (`CourseModule`, `Lesson`, `Phase`...) |
| `content.config.ts` | Collection `modules` (loader + schema) |
| `lib/content-loader.ts` | Ler YAML, `$ref` e `codeFile` (usado também por `tools/check.ts` e `tools/new.ts`) |
| `lib/load-site.ts` | Ler a collection uma vez por build |
| `lib/site.ts` | Tabela de rotas (`Site`, `Route`) e cores dos módulos novos |
| `lib/progress.ts` | Progresso do aluno (`LearnerProgress`), `localStorage` e cálculo de percentagens |
| `lib/html.ts` | Escape de HTML, ícones, `rewriteHashLinks()` (ver abaixo) |
| `lib/render/context.ts` | `RenderContext`: tudo o que um renderizador precisa (site, progresso, rota atual, gaveta) |
| `lib/render/page.ts` | Rota para HTML da coluna principal e título da página |
| `lib/render/navigation.ts` | Menu lateral, comutador de módulos, indicador de progresso |
| `lib/render/blocks.ts`, `code.ts`, `shared.ts` | Lições, cartões, tabelas, passos, realce de código, barras e paginação |
| `lib/render/pages/` | Início, introdução, módulo e capítulo (com quiz) |
| `lib/render/project/` | Projeto final: arquitetura, ficheiros, plano, user stories e o detalhe de cada uma |
| `client/app.ts` | Arranque no browser |
| `client/events.ts` | Cliques: um `data-action="..."` por botão e um handler por ação |
| `client/render.ts`, `drawer.ts`, `clipboard.ts`, `dom.ts` | Redesenhar com progresso, gaveta "Saber mais", copiar, helpers de DOM |
| `layouts/Base.astro` | Casca da página |
| `styles/` | CSS (tokens, base, layout, components/, pages/) importado por `styles/index.css` |

Regras do código:
- Os renderizadores devolvem **strings HTML** e todo o texto passa por `escapeHtml()`. Correm no build (Node) e no browser, por isso **não podem tocar em `document` ou `window`**.
- Não há estado global: cada renderizador recebe um `RenderContext`. O build usa progresso vazio; só o cliente carrega o do `localStorage`.
- As páginas escrevem links internos como `href="#id-da-rota"`; `rewriteHashLinks()` converte-os em URLs reais (com o `base` do site) e o clique em `#...` navega para a página certa.
- Os botões interativos usam `data-action` (e `data-key`, `data-chapter`...); os nomes das ações estão em `client/events.ts`.
- Cada página tem de ter um `h1` (o teste de fumo verifica).

## CSS

Ordem de importação em `src/styles/index.css` (a cascata depende dela): `tokens`, `base`, `layout`, `components/*`, `pages/*`, `accessibility` (sempre por último). Nenhum valor de cor ou tipografia fora de `tokens.css`.

## Conteúdo (`content/`)

```
manifest.yaml                              lista e ordem dos módulos
ids.lock                                   ids publicados (nunca podem desaparecer)
modules/<id>/module.yaml                   metadados do módulo e referências
modules/<id>/chapters/<cap>/chapter.yaml   capítulo: lista de lições e quiz
modules/<id>/chapters/<cap>/<lição>.yaml   uma lição por ficheiro
modules/<id>/chapters/<cap>/code/          um ficheiro por exemplo de código
modules/academia/sections/<id>.yaml        secções da introdução
modules/projeto/                           brief, layers, flow, endpoints...
modules/projeto/phases/<fase>/phase.yaml   fase: árvores, secções, features e user stories
modules/projeto/phases/<fase>/code/        código do BankingApp, com a estrutura de pastas real
_examples/, _drafts/                       exemplos e rascunhos (pastas com _ são ignoradas)
```

Detalhe dos campos em `docs/CONTENT-SCHEMA.md`.

## Onde mexer

| Quero... | Edito... |
|---|---|
| Corrigir um texto ou um exemplo de código | o ficheiro da lição ou o ficheiro em `code/` |
| Acrescentar uma lição | `npm run new:lesson` |
| Acrescentar um módulo | `npm run new:module`, depois `manifest.yaml` |
| Mudar a ordem dos módulos | a ordem em `manifest.yaml` |
| Mudar a aparência de um componente | `src/styles/components/<componente>.css` |
| Mudar uma cor ou fonte | `src/styles/tokens.css` |
| Novo tipo de lição | `src/content/schema.ts` + `src/lib/render/blocks.ts` + `src/styles/components/` + `docs/CONTENT-SCHEMA.md` + `tools/check.ts` |

## Decisões e limites conhecidos

- A interatividade é JavaScript simples (sem Preact): os renderizadores devolvem strings HTML que servem o build e o browser. Migrar para componentes Astro/Preact é possível lição a lição, sem mexer no conteúdo.
- As lições são YAML estruturado (pontos, cartões, tabelas, passos), não Markdown livre; o Markdown só faria sentido para texto corrido longo.
- Os exemplos C# das lições são excertos e não são compilados. O código do projeto final (`phases/*/code`) também não tem `.csproj`, por isso o CI não corre `dotnet build`.
