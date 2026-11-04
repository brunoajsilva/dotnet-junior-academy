# .NET Backend Academy: guia para agentes de IA

Este ficheiro é o ponto de entrada para qualquer IA (ou pessoa) que vá evoluir a academia.
Se leres só uma coisa, lê este ficheiro: tem o suficiente para acrescentar ou corrigir conteúdo sem conhecer a aplicação.

## O que é

Um site de ensino de .NET para programadores de backend de uma consultora de software para a banca.
É um site **Astro** gerado em build e publicado no GitHub Pages. O conteúdo vive em `content/` (YAML e ficheiros de código) e é validado por schemas (Zod) no build.
Idioma: **PT-PT**. Termos técnicos mantêm-se em inglês (Dependency Injection, middleware, controller, claim...).
Código e comentários de código: **inglês**. Domínio dos exemplos: um banco (clientes, contas, saldos, NIF).

## Como acrescentar uma lição ou um módulo (resumo)

1. Lê `docs/AUTHORING.md` (o passo a passo) e `docs/STYLE-GUIDE.md` (tom e regras de escrita).
2. Lição nova: `npm run new:lesson -- <módulo> <capítulo> <id> "Título" [code|cards|table|exercise]` e substitui o texto de exemplo.
   Módulo novo: `npm run new:module -- <id> "Título" "Nome curto"` cria `content/_drafts/<id>/`. Completa-o seguindo `docs/CONTENT-SCHEMA.md`, move-o para `content/modules/<id>/` e acrescenta `modules/<id>/module.yaml` ao `content/manifest.yaml`, antes do projeto final.
3. Valida: `npm run check` (diz exatamente o ficheiro e o campo com problema).
4. Testa: `npm test` (precisa de `npm install` e `npx playwright install chromium` uma vez).
5. Quando as lições estiverem publicadas: `npm run check -- --update-ids` regista os ids em `content/ids.lock`.
6. Resume ao utilizador o que criaste (capítulos, lições, perguntas) e o que não conseguiste verificar.

Há um prompt pronto a usar em `prompts/novo-modulo.md`.

## O que podes e não podes fazer

| Podes | Não podes (sem o utilizador pedir) |
|---|---|
| Criar e editar ficheiros em `content/` | Alterar `src/`, `tools/`, `astro.config.mjs` ou os workflows |
| Corrigir texto e código de módulos existentes | Mudar ids de lições já publicadas (o `ids.lock` falha o check) |
| Acrescentar lições, perguntas e links | Criar CSS, HTML ou cores novas para conteúdo |
| Propor um novo tipo de lição (descreve-o, não o implementes) | Mexer no módulo "Projeto final" fora do que foi pedido |

Se o pedido for de **código da aplicação** (`src/`), lê `docs/ARCHITECTURE.md` e `docs/DESIGN-RULES.md`, e corre `npm test` no fim.

## Regras inegociáveis

- Texto simples: sem Markdown, sem HTML, sem emojis. Parágrafos separam-se com uma linha em branco; em YAML usa um bloco `|-`.
- Código de exemplo em ficheiros próprios (`code/`), referenciados com `codeFile`. Nunca em strings YAML.
- Nunca copiar credenciais, chaves ou dados reais de clientes. Exemplos usam dados inventados (ana@example.com).
- Sem logótipos, nomes de empresas ou marcas como identidade. Pedidos HTTP: usa o **Bruno**, nunca o Postman.
- Dinheiro é `decimal`, nunca `double`. Datas em UTC.
- Não inventes APIs: se não tens a certeza de que um método existe na versão alvo (.NET 10, C# 14), escolhe outro exemplo ou assinala a dúvida no resumo final.
- Uma lição ensina **uma** ideia. Exemplos de código com no máximo 24 linhas.
- Cada capítulo termina com um quiz de 3 a 6 perguntas, com explicação do porquê.
- Os exemplos C# das lições são excertos e **não são compilados** no build. Diz sempre ao utilizador se o código não foi compilado.

## Mapa do repositório

```
content/              manifest.yaml, ids.lock e modules/<id>/ (YAML e ficheiros de código)
src/                  pages/ (rotas), layouts/, lib/ (renderização), client/ (progresso e interação), styles/
tools/                check, new, smoke (Node)
docs/                 ARCHITECTURE, DEVELOPMENT, AUTHORING, CONTENT-SCHEMA, STYLE-GUIDE, DESIGN-RULES
prompts/              prompts prontos a copiar
design/               fundações de design (tokens W3C e CSS)
```

## Se algo falhar

- `npm run check` dá a lista de erros, com o módulo, o capítulo e a lição. Corrige e volta a correr.
- `npm run build` falha com `does not match collection schema` quando um campo está em falta ou fora dos limites: a mensagem indica o caminho (por exemplo `chapters.0.lessons.2.points`).
- Se o `smoke` indicar `expected one h1`, `did not hydrate` ou `horizontal overflow`, o conteúdo tem um problema de estrutura ou uma linha sem quebras
  (por exemplo, uma URL ou um comando muito longo fora de um bloco de código). Parte-o ou move-o para um ficheiro `code/`.
