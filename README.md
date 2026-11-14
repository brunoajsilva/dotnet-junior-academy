# .NET Backend Academy

Academia de .NET para programadores de backend: C#, .NET, autenticação e um projeto final guiado (BankingApp, Clean Architecture). O conteúdo está em português de Portugal; os termos técnicos ficam em inglês.

O site é feito com [Starlight](https://starlight.astro.build) (Astro). Cada capítulo é uma página Markdown.

## Requisitos

- Node.js 22.23.4 ou superior (o ficheiro `.nvmrc` indica a versão recomendada: `nvm use`)
- .NET SDK 10, só para compilar as soluções de referência

## Correr o site

```bash
cd site
npm install
npm run dev        # http://localhost:4321, recarrega ao guardar
npm run build      # gera site/dist e o índice de pesquisa
npm run preview    # serve site/dist
```

A pesquisa só existe depois de `npm run build`.

## Compilar as soluções de referência

```bash
dotnet build reference/01-solucao-base
dotnet test reference/01-solucao-base
dotnet build reference/02-autenticacao-jwt
dotnet test reference/02-autenticacao-jwt
```

## Estrutura

```text
site/                     o site Starlight
  astro.config.mjs        título, menu lateral e ordem dos módulos
  src/content/docs/       as páginas: academia/, csharp/, dotnet/, auth/, projeto/
  src/styles/academy.css  a cor e os ajustes da academia
reference/                código do projeto final que compila
  01-solucao-base/        BankingApp depois de «Montar a solução»
  02-autenticacao-jwt/    BankingApp depois de «Autenticação JWT»
resources/                ficheiros para os formandos
docs/                     guia de estilo e decisões
```

As páginas do projeto final mostram o código importando-o de `reference/`. Corrigir o código nessa pasta corrige a página.

## Módulos

| Pasta | Módulo |
| --- | --- |
| `academia/` | Introdução à Academia (o que é, objetivos, plano, cronograma, software) |
| `csharp/` | Introdução ao C# |
| `dotnet/` | Introdução ao .NET |
| `auth/` | Autenticação e Autorização |
| `projeto/` | Projeto final: BankingApp |

## Contribuir

Corrigir uma lição, acrescentar uma página ou um módulo: ver [CONTRIBUTING.md](CONTRIBUTING.md). Regras de escrita: [docs/style-guide.md](docs/style-guide.md). Porque é que o site é assim: [docs/decisions/0001-starlight.md](docs/decisions/0001-starlight.md).

## Pipeline

Em cada push e pull request, `.github/workflows/ci.yml` compila o site e compila e testa as soluções de referência. A publicação do site no destino interno ainda não está configurada: depende de onde o site vai ficar.
