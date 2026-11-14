# .NET Academy: guia para agentes de IA

Site de ensino de .NET para programadores de backend de uma consultora de software. Feito com Starlight: cada capítulo é uma página Markdown em `site/src/content/docs/`.

Como acrescentar ou corrigir conteúdo: [CONTRIBUTING.md](CONTRIBUTING.md). Regras de escrita completas: [docs/style-guide.md](docs/style-guide.md). Porque o site é assim: [docs/decisions/0001-starlight.md](docs/decisions/0001-starlight.md).

## Módulos

| Pasta em `site/src/content/docs/` | Módulo |
| --- | --- |
| `academia/` | Introdução à Academia (o que é, objetivos, plano, cronograma, software) |
| `csharp/` | Introdução ao C# |
| `dotnet/` | Introdução ao .NET |
| `auth/` | Autenticação e Autorização |
| `projeto/` | Projeto final: BankingApp |

O código do projeto final (BankingApp) está dentro das páginas de `projeto/`, em blocos de código com o caminho do ficheiro no título. Não há soluções .NET no repositório.

## Regras de escrita

- Idioma: PT-PT. Termos técnicos mantêm-se em inglês (Dependency Injection, middleware, controller, claim...).
- Código e comentários de código: inglês. Domínio dos exemplos: um banco (clientes, contas, saldos, NIF).
- Texto simples e direto, sem emojis. Evita travessões longos.
- Nunca copiar credenciais, chaves ou dados reais de clientes. Exemplos usam dados inventados (ana@example.com).
- Sem logótipos, nomes de empresas ou marcas como identidade. Pedidos HTTP: usa o **Bruno**, nunca o Postman.
- Dinheiro é `decimal`, nunca `double`. Datas em UTC.
- Não inventes APIs: se não tens a certeza de que um método existe na versão alvo (.NET 10, C# 14), escolhe outro exemplo ou assinala a dúvida.
- Uma lição ensina uma ideia. Exemplos de código curtos (cabem num ecrã).

## Onde está cada coisa

```text
site/src/content/docs/   as páginas (editar aqui)
site/src/modules.ts      os módulos, pela ordem do menu lateral (a posição define número e cor)
site/astro.config.mjs    configuração do Starlight (sem pesquisa e só com tema claro)
site/src/styles/         o estilo da academia (academy.css) e as cores dos módulos
site/src/components/     título da página com a etiqueta do módulo
resources/               ficheiros para os formandos (prompt do front-end)
docs/                    guia de estilo e decisões
.github/workflows/       CI: compila o site em cada push e pull request
```

## Correr o site

Requer Node.js 22.23.4 ou superior (`.nvmrc` indica a versão recomendada).

```bash
cd site
npm install
npm run dev      # http://localhost:4321
npm run build    # gera site/dist e o índice de pesquisa
```

## Limites

- Edita as páginas à vontade. Só mexes em `site/astro.config.mjs`, `site/package.json` ou no CI se o utilizador pedir.
- Não atualizes as versões do Astro e do Starlight sem pedido: estão fixas de propósito.
- Não acrescentes componentes, CSS ou cores novas para o conteúdo. O site é só claro e não tem pesquisa, de propósito.

## Antes de entregar

- `cd site && npm run build` termina com `Complete!`.
- O código C# das páginas não é compilado pelo repositório. Diz sempre o que não conseguiste verificar (por exemplo, código C# que não compilaste).
