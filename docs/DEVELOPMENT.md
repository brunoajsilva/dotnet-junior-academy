# Desenvolvimento

## Requisitos

Node 20 ou superior. Uma vez: `npm install` e `npx playwright install chromium` (para o teste de fumo).

## Comandos

| Comando | O que faz |
|---|---|
| `npm run dev` | Servidor de desenvolvimento em `http://localhost:4321/dotnet-junior-academy/`, recarrega ao guardar |
| `npm run check` | Valida o conteúdo (`tools/check.ts`) e os tipos (`astro check`) |
| `npm run build` | Gera `dist/` e o índice de pesquisa (Pagefind) |
| `npm run preview` | Serve `dist/` como o GitHub Pages |
| `npm test` | `check`, `build` e `tools/smoke.ts` |
| `npm run new:lesson` / `new:module` | Esqueletos de conteúdo (ver `docs/AUTHORING.md`) |
| `npm run format` | Prettier em `src/`, `tools/` e no YAML do conteúdo |

## O que cada teste verifica

- **check** (`tools/check.ts`): ficheiros referenciados existem e não há ficheiros órfãos, ids únicos, estrutura de cada tipo de módulo, regras de escrita (sem nomes de empresas nem emojis), limites de `docs/CONTENT-SCHEMA.md` nos módulos novos e `content/ids.lock` (ids publicados que desapareceram).
- **astro check / build**: schemas Zod de `src/content.config.ts` e tipos.
- **smoke** (`tools/smoke.ts`): serve `dist/` como o GitHub Pages e abre todas as páginas a 1280 px e 400 px: sem erros de script, um `h1`, página hidratada, sem scroll horizontal e sem links `#`. Testa ainda marcar como visto, quiz, gaveta, progresso após recarregar, diagrama de arquitetura e a existência do índice de pesquisa.

## Ids publicados

O progresso do aluno é guardado no browser por id. Depois de publicar, `npm run check -- --update-ids` regista os ids em `content/ids.lock`; a partir daí, remover ou mudar um id falha o `check`.

## Publicar no GitHub Pages

1. Settings, Pages, Source: **GitHub Actions** (uma vez).
2. `git push` para `main`: `.github/workflows/deploy.yml` corre o check, o build e publica `dist/`.
3. Pull requests e outros ramos correm `.github/workflows/ci.yml` (check, tipos, build e smoke).

O endereço e o caminho base estão em `site.config.mjs`. O URL final é `https://<utilizador>.github.io/<repositório>/`.

## Notas

- Links antigos do tipo `.../#csharp-1` continuam a funcionar: a página inicial redireciona-os.
- A cache do browser pode mostrar conteúdo antigo depois de publicar: recarrega com Ctrl/Cmd+Shift+R.
- No `npm run dev` a pesquisa não existe (o índice só é criado no build).
