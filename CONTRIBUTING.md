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
2. Em `site/src/modules.ts`, acrescenta uma linha à lista, na posição onde o módulo deve aparecer. A posição define o número e a cor do módulo (até 8).

```ts
{ dir: "logging", label: "Logging" },
```

## Avisos

Usa os blocos de Starlight: `:::note[Título]`, `:::tip[Título]`, `:::caution[Título]` e `:::danger[Título]`, fechados com `:::`. Dentro de um bloco «Saber mais», deixa uma linha em branco antes e depois de cada bloco.

O bloco «Saber mais» abre numa gaveta à direita (`site/src/components/Footer.astro`). Escreve-o sempre como `<details><summary>Saber mais</summary>`: o texto do `summary` tem de ser exatamente «Saber mais». Dentro cabe qualquer Markdown: texto, avisos, tabelas e código.

## Código no projeto final

Os exemplos do projeto final estão dentro das páginas `projeto/*`, em blocos de código com o caminho do ficheiro no título:

````md
```csharp title="BankingApp.Domain/Customers/Customer.cs"
public class Customer { }
```
````

Esse código não é compilado pelo repositório. Se o alterares, compila-o à parte (numa solução tua) antes de o publicar, e diz no pull request que o fizeste.

## Pedidos HTTP

Os exemplos usam o Bruno. A coleção usada no projeto final está na página «Autenticação JWT».

## Árvore de ficheiros

Nas páginas do projeto final, a estrutura escreve-se com o componente `FileTree` do Starlight, numa lista Markdown. O site transforma-a numa árvore clicável: ao escolher um item, o painel da direita mostra a descrição e o caminho (`site/src/scripts/project-tree.ts`).

```md
<FileTree>

- BankingApp/ Descrição da pasta.
  - **Account.cs** (novo) Descrição do ficheiro.
  - **Customer.cs** (alterado) Descrição do ficheiro.
  - **(apagar)** (a apagar) Ficheiros que se apagam, separados por vírgulas.

</FileTree>
```

As etiquetas reconhecidas, logo a seguir ao nome, são `(novo)`, `(alterado)` e `(a apagar)`.

## Antes de entregar

Segue o checklist de [docs/style-guide.md](docs/style-guide.md).
