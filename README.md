# .NET Academy

Academia de .NET para programadores de backend: C#, .NET, autenticação e um projeto final guiado (BankingApp, Clean Architecture). O conteúdo está em português de Portugal; os termos técnicos ficam em inglês.

O site é feito com [Starlight](https://starlight.astro.build) (Astro). Cada capítulo é uma página Markdown.

## Requisitos

- Node.js 22.23.4 ou superior (o ficheiro `.nvmrc` indica a versão recomendada: `nvm use`)

## Correr o site

```bash
cd site
npm install
npm run dev        # http://localhost:4321, recarrega ao guardar
npm run build      # gera site/dist
npm run preview    # serve site/dist
```

## Estrutura

```text
site/                     o site Starlight
  astro.config.mjs        título e configuração do Starlight
  src/modules.ts          os módulos, pela ordem do menu lateral
  src/components/         título com a etiqueta do módulo, gaveta «Saber mais» e índice que encolhe
  src/content/docs/       as páginas: academia/, csharp/, dotnet/, auth/, projeto/
  src/styles/academy.css  a cor e os ajustes da academia
resources/                ficheiros para os formandos
docs/                     guia de estilo e decisões
```

Os exemplos de código estão dentro das páginas, em blocos de código. O código C# do projeto final não é compilado no repositório.

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

Em cada push e pull request, `.github/workflows/ci.yml` compila o site. A publicação do site no destino interno ainda não está configurada: depende de onde o site vai ficar.
