# .NET Backend Academy: guia para agentes de IA

Site de ensino de .NET para programadores de backend de uma consultora de software para a banca. Feito com Starlight: cada capítulo é uma página Markdown em `site/src/content/docs/`.

Como acrescentar ou corrigir conteúdo: [CONTRIBUTING.md](CONTRIBUTING.md). Regras de escrita completas: [docs/style-guide.md](docs/style-guide.md).

## Regras de escrita

- Idioma: PT-PT. Termos técnicos mantêm-se em inglês (Dependency Injection, middleware, controller, claim...).
- Código e comentários de código: inglês. Domínio dos exemplos: um banco (clientes, contas, saldos, NIF).
- Texto simples e direto, sem emojis. Evita travessões longos.
- Nunca copiar credenciais, chaves ou dados reais de clientes. Exemplos usam dados inventados (ana@example.com).
- Sem logótipos, nomes de empresas ou marcas como identidade. Pedidos HTTP: usa o **Bruno**, nunca o Postman.
- Dinheiro é `decimal`, nunca `double`. Datas em UTC.
- Não inventes APIs: se não tens a certeza de que um método existe na versão alvo (.NET 10, C# 14), escolhe outro exemplo ou assinala a dúvida.
- Uma lição ensina uma ideia. Exemplos de código curtos (cabem num ecrã).
- Cada capítulo termina com um quiz de 3 a 6 perguntas, com explicação do porquê.

## Onde está cada coisa

```text
site/src/content/docs/   as páginas (editar aqui)
site/astro.config.mjs    menu lateral e ordem dos módulos
reference/               código do projeto final que compila (as páginas importam-no)
resources/               ficheiros para os formandos
docs/                    guia de estilo e decisões
```

## Antes de entregar

- `cd site && npm run build` termina com `Complete!`.
- Se mexeste em `reference/`, `dotnet build` e `dotnet test` na solução alterada.
- Diz sempre o que não conseguiste verificar (por exemplo, código C# que não compilaste).
