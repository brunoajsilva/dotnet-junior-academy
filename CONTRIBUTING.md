# Contribuir

Tudo o que se escreve está em `site/src/content/docs/`. Cada ficheiro é uma página. Não há schemas nem passos de geração: edita o ficheiro, vê no browser, faz commit.

## Ver o resultado

```bash
cd site
npm install      # uma vez
npm run dev
```

Antes de abrir um pull request, corre `npm run build` em `site/`. Tem de terminar com `Complete!`.

## Corrigir uma lição

Abre a página do capítulo (por exemplo `site/src/content/docs/csharp/fundamentos-da-linguagem.md`), procura o título da lição (`## Título`) e edita o texto. Não precisas de mais nada.

## Estrutura de uma página de capítulo

````md
---
title: "Fundamentos da linguagem"
description: "Uma frase que resume o capítulo."
sidebar:
  order: 1
---

Introdução curta.

## Título da lição

```csharp
decimal balance = 320.50m;
```

- Ponto-chave
- Outro ponto-chave

<details>
<summary>Saber mais</summary>

Explicação mais profunda.

:::caution[Armadilha]
O erro que um júnior realmente comete.
:::

:::tip[Experimenta]
Algo que se faz em menos de 2 minutos.
:::

</details>

## Quiz

### Pergunta 1

Texto da pergunta.

- **A.** Opção
- **B.** Opção

<details>
<summary>Ver resposta</summary>

**B. Opção**

Porquê.

</details>
````

## Acrescentar uma lição

Acrescenta uma secção `## Título da lição` na página do capítulo, no sítio onde ela deve aparecer, com a estrutura acima: um exemplo de código, 2 a 4 pontos-chave e, se houver profundidade, um bloco «Saber mais».

## Acrescentar uma página

1. Cria o ficheiro `.md` na pasta do módulo (por exemplo `site/src/content/docs/dotnet/logging.md`).
2. Põe o cabeçalho com `title`, `description` e `sidebar.order`.
3. O menu lateral atualiza-se sozinho.

## Mudar a ordem das páginas

Dentro de um módulo, a ordem é o número `sidebar.order` no cabeçalho de cada página (a página `index.md` usa `0`). Troca os números. Para mudar o texto que aparece no menu sem mudar o título, usa `sidebar.label`.

## Acrescentar um módulo

1. Cria a pasta `site/src/content/docs/<módulo>/` com um `index.md` (`sidebar.order: 0`, `sidebar.label: "Visão geral"`) e as páginas.
2. Em `site/astro.config.mjs`, acrescenta uma entrada à lista `sidebar`, na posição onde o módulo deve aparecer:

```js
{ label: "Logging", items: [{ autogenerate: { directory: "logging" } }] },
```

## Avisos

Usa os blocos de Starlight: `:::note[Título]`, `:::tip[Título]`, `:::caution[Título]` e `:::danger[Título]`, fechados com `:::`. Dentro de um bloco «Saber mais», deixa uma linha em branco antes e depois de cada bloco.

## Código no projeto final

O código do projeto final vive em `reference/` e compila. As páginas `projeto/*.mdx` importam-no:

```mdx
import { Code } from "@astrojs/starlight/components";
import customer from "../../../../../reference/01-solucao-base/src/BankingApp.Domain/Customers/Customer.cs?raw";

<Code code={customer} lang="csharp" title="BankingApp.Domain/Customers/Customer.cs" />
```

Para mudar o código, edita o ficheiro em `reference/` e corre `dotnet build` e `dotnet test` nessa solução.

## Pedidos HTTP

Os exemplos usam o Bruno. A coleção está em `reference/02-autenticacao-jwt/docs/bruno/`.

## Antes de entregar

Segue o checklist de [docs/style-guide.md](docs/style-guide.md).
