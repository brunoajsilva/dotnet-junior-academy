# Esquema de conteúdo (módulos em JSON)

Um módulo é um ficheiro JSON com um objeto. O validador (`src/validate.py`) aplica tudo o que está aqui.
Todo o texto é **texto simples**: o site faz o escape de HTML, por isso Markdown e HTML aparecem tal e qual.
Parágrafos longos separam-se com `\n\n`.

## Módulo

| Campo | Obrigatório | Regras |
|---|---|---|
| `id` | sim | kebab-case, único, não pode ser `academia`, `csharp`, `dotnet`, `auth`, `projeto` |
| `kind` | sim | sempre `"course"` |
| `title` | sim | título completo, mostrado no cabeçalho |
| `short` | sim | até 22 caracteres, usado nos menus |
| `tagline` | sim | 1 a 2 frases, até 220 caracteres |
| `chapters` | sim | 1 a 8 capítulos |
| `outro` | sim | fecho do módulo (ver abaixo) |

## Capítulo

| Campo | Regras |
|---|---|
| `id` | `<módulo>-<n>`, por exemplo `logging-1` |
| `t` | título curto |
| `intro` | 1 a 2 frases: o que o aluno vai aprender |
| `lessons` | 3 a 14 lições |
| `quiz` | 3 a 6 perguntas |

## Lição

Campos comuns: `id` (começa por `<módulo>-`, único), `t` (título), `type`, e opcionalmente `more`.

### `more` (o botão "Saber mais")

Abre uma gaveta lateral com explicação mais longa. Todos os campos são texto.

```json
"more": {
  "more": "Explicação em 2 a 4 parágrafos.\n\nSegundo parágrafo.",
  "pit": "Erro frequente a evitar (1 frase).",
  "tryit": "Algo para experimentar (1 a 2 frases)."
}
```
`more` é obrigatório dentro do objeto; `pit` e `tryit` são opcionais. Não uses outros campos.

### `type: "code"`: ideia + exemplo

```json
{ "id": "logging-1-1", "t": "ILogger e mensagens estruturadas", "type": "code", "lang": "cs",
  "code": "var total = balance * 1.04m; // inferred type: decimal",
  "points": ["Frase curta 1.", "Frase curta 2.", "Frase curta 3."] }
```
- `lang`: `cs`, `sh`, `json`, `xml`, `http` ou `txt` (sem realce).
- `code`: até 24 linhas. Código e comentários em inglês. `\n` para mudar de linha.
- `points`: 2 a 4 frases curtas, em PT-PT.

### `type: "cards"`: conceitos lado a lado

```json
{ "id": "m-1-2", "t": "Os três tipos", "type": "cards",
  "items": [ { "t": "Singleton", "d": ["Uma instância para toda a aplicação."] },
             { "t": "Scoped",    "d": ["Uma instância por pedido."], "code": "services.AddScoped<IFoo, Foo>();" } ] }
```
2 a 6 cartões. `d` é sempre uma lista de frases. `code` (opcional) mostra um pequeno bloco no cartão.

### `type: "table"`: comparações e referências

```json
{ "id": "m-1-3", "t": "Níveis de log", "type": "table",
  "rows": [ ["Nível", "Quando usar"], ["Information", "Um facto normal."], ["Error", "Uma operação falhou."] ] }
```
A primeira linha é o cabeçalho. Todas as linhas têm o mesmo número de colunas. Opcional: `"note"` (frase por baixo).

### `type: "exercise"`: prática

```json
{ "id": "m-1-4", "t": "Registar uma operação", "type": "exercise",
  "steps": [ { "lead": "Injetar", "text": "Injeta ILogger<T> no handler." },
             { "lead": "Sucesso", "text": "Regista um Information com a conta e o valor." } ],
  "expected": null, "hint": "Começa pelo caso de sucesso." }
```
- `steps`: 2 a 8 passos. `lead` é a palavra-chave a negrito (pode ser `""`), `text` a instrução.
- `expected`: `null`, ou a saída esperada em texto (várias linhas com `\n`). Fica escondida atrás do botão "Ver resultado esperado".
- `hint` e `extra` são opcionais (`extra`: desafio adicional).

## Quiz

```json
{ "q": "Pergunta?", "o": ["Opção A", "Opção B", "Opção C", "Opção D"], "a": 1, "w": "Porque é que B está certa." }
```
- `o`: 3 a 5 opções, sem repetições. `a`: índice da correta, a contar de 0.
- Distribui a resposta certa por posições diferentes ao longo do quiz.
- `w`: explicação mostrada depois de responder. Explica o raciocínio, não repitas a resposta.

## `outro` (fim do módulo)

```json
"outro": {
  "done": ["O que o aluno já sabe fazer (3 a 5 itens)"],
  "practice": ["Ideias para praticar (2 a 6 itens)"],
  "docs": [ { "t": "Nome do artigo", "u": "https://learn.microsoft.com/..." } ]
}
```
`docs`: só links `https://` para documentação oficial.

## Tipos de lição que existem mas não deves usar

`domain`, `pyramid` e `layers` existem nos módulos da base e têm desenhos próprios. O validador não os aceita em módulos novos.
Se um tema precisar de um diagrama, usa `cards` com ordem explícita e diz ao utilizador que um novo tipo de lição seria útil.

## Limites que o site impõe

- Sem imagens, vídeos ou HTML. Só texto, código, tabelas e cartões.
- Não há campo para "pré-requisitos" nem para tempo estimado: descreve-os em `tagline` ou `intro`.
- O progresso do aluno é guardado no browser, por id de lição. **Nunca mudes o `id` de uma lição publicada**: o aluno perderia o progresso.
