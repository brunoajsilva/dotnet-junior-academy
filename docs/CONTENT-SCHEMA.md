# Esquema de conteúdo

Todo o conteúdo está em `content/`. Há dois tipos de ficheiro: YAML (estrutura e texto) e ficheiros de código (`.cs`, `.sh`, `.json`...). Os schemas (Zod) estão em `src/content.config.ts` e são verificados em cada build; `npm run check` aplica ainda as regras de escrita e os limites abaixo. O texto é **texto simples**: o site faz o escape de HTML, por isso Markdown e HTML aparecem tal e qual. Parágrafos longos escrevem-se em YAML com um bloco `|-` e uma linha em branco entre parágrafos.

## Referências entre ficheiros

Os caminhos são sempre relativos ao ficheiro onde aparecem.

```yaml
chapters:
  - $ref: chapters/logging-1/chapter.yaml
```
Um objeto com só `$ref` é substituído pelo conteúdo desse ficheiro YAML. A ordem da lista é a ordem no site.

```yaml
type: code
lang: cs
codeFile: code/logging-1-1.cs
```
`codeFile` aponta para um ficheiro de texto; o build lê-o e usa-o como `code`. O ficheiro tem o código tal e qual, sem escapes. A extensão acompanha `lang`.

## `manifest.yaml`

```yaml
title: .NET Backend Academy
modules:
  - modules/academia/module.yaml
  - modules/csharp/module.yaml
  - modules/projeto/module.yaml
```
A ordem da lista é a ordem dos módulos no site (o número é calculado). O `projeto` fica sempre em último.

## `ids.lock`

Lista dos ids que já guardam progresso de alunos (capítulos, lições, `sec:` e `ph:`). Escreve-se com `npm run check -- --update-ids`. Se um id da lista desaparecer, o `check` falha.

## Módulo de curso (`kind: "course"`)

`modules/<id>/module.yaml`:

| Campo | Obrigatório | Regras |
|---|---|---|
| `id` | sim | kebab-case, único; não pode ser `academia`, `csharp`, `dotnet`, `auth`, `projeto` |
| `kind` | sim | `"course"` |
| `title` | sim | título completo, mostrado no cabeçalho |
| `shortTitle` | sim | até 28 caracteres, usado nos menus |
| `tagline` | sim | 1 a 2 frases, até 220 caracteres |
| `chapters` | sim | 1 a 8 referências `$ref` a `chapters/<cap>/chapter.yaml` |
| `wrapUp` | sim | fecho do módulo (ver abaixo) |

### Capítulo (`chapter.yaml`)

| Campo | Regras |
|---|---|
| `id` | `<módulo>-<n>`, por exemplo `logging-1` (igual ao nome da pasta) |
| `title` | título curto |
| `intro` | 1 a 2 frases: o que o aluno vai aprender |
| `lessons` | 3 a 14 lições, cada uma num ficheiro `<id-da-lição>.yaml` ao lado do `chapter.yaml` (lista de `$ref`) |
| `quiz` | 3 a 6 perguntas |

### Lição

Campos comuns: `id` (começa por `<módulo>-`, único), `title`, `type`, e opcionalmente `learnMore`.

**`learnMore`** (o botão "Saber mais") abre uma gaveta lateral com explicação mais longa:

```yaml
learnMore:
  explanation: |-
    Explicação em 2 a 4 parágrafos.

    Segundo parágrafo.
  pitfall: Erro frequente a evitar (1 frase).
  tryIt: Algo para experimentar (1 a 2 frases).
```
`explanation` é obrigatório dentro do objeto; `pitfall` e `tryIt` são opcionais. Não uses outros campos.

**`type: "code"`**: ideia + exemplo

```yaml
id: logging-1-1
title: ILogger e mensagens estruturadas
type: code
language: cs
codeFile: code/logging-1-1.cs
keyPoints:
  - Frase curta 1.
  - Frase curta 2.
```
- `language`: `cs`, `sh`, `json`, `xml`, `http`, `bru` ou `txt` (os dois últimos sem realce).
- O ficheiro de código tem até 24 linhas. Código e comentários em inglês.
- `keyPoints`: 2 a 4 frases curtas, em PT-PT.

**`type: "cards"`**: conceitos lado a lado

```yaml
id: m-1-2
title: Os três tipos
type: cards
cards:
  - title: Singleton
    lines: [Uma instância para toda a aplicação.]
  - title: Scoped
    lines: [Uma instância por pedido.]
    codeFile: code/m-1-2-scoped.cs
```
2 a 8 cartões. `lines` é sempre uma lista de frases. `codeFile` (opcional) mostra um pequeno bloco no cartão.

**`type: "table"`**: comparações e referências

```yaml
id: m-1-3
title: Níveis de log
type: table
rows:
  - [Nível, Quando usar]
  - [Information, Um facto normal.]
  - [Error, Uma operação falhou.]
```
A primeira linha é o cabeçalho. Todas as linhas têm o mesmo número de colunas. Opcional: `"note"` (frase por baixo).

**`type: "exercise"`**: prática

```yaml
id: m-1-4
title: Registar uma operação
type: exercise
steps:
  - keyword: Injetar
    text: Injeta ILogger<T> no handler.
  - keyword: Sucesso
    text: Regista um Information com a conta e o valor.
expectedOutput: null
hint: Começa pelo caso de sucesso.
```
- `steps`: 2 a 8 passos. `keyword` é a palavra-chave a negrito (pode ser `""`), `text` a instrução.
- `expectedOutput`: `null`, ou a saída esperada em texto. Fica escondida atrás do botão "Ver resultado esperado".
- `hint` e `challenge` são opcionais (`challenge`: desafio adicional).

### Quiz

```yaml
- question: Pergunta?
  options: [Opção A, Opção B, Opção C, Opção D]
  correctIndex: 1
  explanation: Porque é que B está certa.
```
- `options`: 3 a 5 opções, sem repetições. `correctIndex`: índice da correta, a contar de 0.
- Distribui a resposta certa por posições diferentes ao longo do quiz.
- `explanation`: explicação mostrada depois de responder. Explica o raciocínio, não repitas a resposta.

### `wrapUp` (fim do módulo)

```yaml
wrapUp:
  learned:
    - O que o aluno já sabe fazer (3 a 5 itens)
  practiceIdeas:
    - Ideias para praticar (2 a 6 itens)
  docs:
    - title: Nome do artigo
      url: https://learn.microsoft.com/...
```
`docs`: só links `https://` para documentação oficial.

## Introdução (`kind: "intro"`)

`modules/academia/module.yaml` lista `sections`, cada uma em `sections/<id>.yaml` com `id`, `title` e `blocks` (parágrafos, listas, tabelas, passos). É um módulo da base: a estrutura dos blocos (`paragraph`, `cards`, `steps`, `outcomes`, `plan`, `schedule`, `software`) está em `src/content/schema.ts` e é desenhada por `src/lib/render/pages/intro.ts`.

O bloco `schedule` (página Cronograma) lista semanas, e cada semana os dias úteis com os módulos dados nesse dia:

```yaml
- type: schedule
  weeks:
    - title: Semana 1
      days:
        - day: 1
          items:
            - moduleId: csharp
              title: Fundamentos da linguagem
              detail: Tipos, operadores e métodos.
              routeId: csharp-1   # opcional: o título passa a ligação
```

## Projeto final (`kind: "project"`)

`modules/projeto/module.yaml` junta: `brief`, `days`, `layers`, `flow`, `finalDelivery`, `endpoints`, `acceptanceCriteria` e `extras` (um YAML cada) e `phases` (uma pasta por fase). Cada fase (`phases/<fase>/phase.yaml`) tem `day`, `kind`, `title`, `goal`, `uses` (ids de lições recomendadas), `trees` (árvores de ficheiros), `sections` (passos guiados com `files`) e, na fase do enunciado, `features` (grupos de user stories, com `id` `F1`...) e `userStories` (um ficheiro `user-stories/US*.yaml` por user story, com o campo `feature` a apontar para o grupo e a história formal para o Azure DevOps em `details`). As dependências (`dependsOn`) usam os ids das user stories, por exemplo `US4, US5`.

O código do BankingApp está em `phases/<fase>/code/`, com a estrutura de pastas real do projeto (`BankingApp.Application/Handlers/...`). Cada entrada de `files` referencia o seu ficheiro com `codeFile`. Estas estruturas são específicas do projeto: edita os campos que já existem em vez de inventar novos.

## Tipos de lição que existem mas não deves usar

`domain`, `pyramid` e `layers` existem nos módulos da base e têm desenhos próprios. Em módulos novos, usa `cards` com ordem explícita e diz ao utilizador que um novo tipo de lição seria útil.

## Limites que o site impõe

- Sem imagens, vídeos ou HTML. Só texto, código, tabelas e cartões.
- Não há campo para "pré-requisitos" nem para tempo estimado: descreve-os em `tagline` ou `intro`.
- O progresso do aluno é guardado no browser, por id de lição. **Nunca mudes o `id` de uma lição publicada**: o aluno perderia o progresso.
- Todos os ficheiros referenciados têm de existir e estar ligados a um módulo do manifesto (o `check` avisa de ficheiros órfãos). Pastas que começam por `_` são ignoradas.
