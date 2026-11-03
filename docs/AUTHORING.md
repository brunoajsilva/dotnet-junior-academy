# Do tema ao módulo

Receita para transformar "quero um módulo sobre X" num módulo publicado. Segue por ordem.

## 1. Perceber o pedido

Antes de escrever, fixa por escrito (no resumo final, não no ficheiro):

- **Tema** e **ideia central**: o que o aluno consegue fazer no fim que não fazia antes.
- **Público**: programador júnior a médio, já fez os módulos C# e .NET da academia. Não repitas o que lá está.
- **Versões**: .NET 10 e C# 14, salvo indicação contrária.
- **Âmbito**: um módulo = 2 a 5 capítulos. Cada capítulo = 3 a 14 lições. Se o tema é maior, propõe dividir em dois módulos.

Se faltar informação que muda o conteúdo (versão, biblioteca, nível), faz **uma** pergunta curta. Senão, assume e regista a assunção.

## 2. Verificar os factos

Para qualquer afirmação técnica que não sabes de cor, confirma na documentação oficial (learn.microsoft.com) antes de a escreveres.
Nunca inventes nomes de métodos, pacotes ou comandos. Cada módulo termina com links oficiais (`outro.docs`).

## 3. Esboçar o módulo

Antes do JSON, escreve o esboço como tabela:

| Capítulo | Lição | Tipo | Ideia única |
|---|---|---|---|
| 1. Registar com ILogger | ILogger e mensagens estruturadas | code | marcadores nomeados |
| | Níveis de log | table | quando usar cada nível |
| | Registar uma operação | exercise | aplicar no handler |

Regras de composição:
- Abre cada capítulo com uma lição `code` ou `cards` (o conceito), sem exercício logo à cabeça.
- Alterna explicação e prática: no máximo 4 lições seguidas sem `exercise`.
- Fecha o capítulo com um `exercise` que junta o que foi visto, e depois o quiz.
- O último capítulo pode ter um `exercise` com enunciado completo (a "mini-aplicação").

## 4. Escrever o JSON

Cria `content/modules/<id>.json`. O `id` é curto, em minúsculas, sem espaços (`efcore`, `logging`, `docker`).
Parte do exemplo `content/modules/_exemplo-logging.json` e segue `docs/CONTENT-SCHEMA.md`.

Ids obrigatórios e únicos:
- capítulos: `<id>-1`, `<id>-2`...
- lições: `<id>-1-1`, `<id>-1-2`, `<id>-2-1`...

Ficheiros que começam por `_` são ignorados pelo build (servem de exemplo).

## 5. Validar, gerar, testar

```bash
python3 src/validate.py content/modules/<id>.json
python3 src/build.py --out index.html
node src/tests/smoke.js index.html
```

O módulo aparece sozinho no menu do topo, antes do "Projeto final", com cor atribuída automaticamente.
Os módulos são renumerados: o "Projeto final" passa a ser o último.

## 6. Rever antes de entregar

Passa pela lista em `docs/STYLE-GUIDE.md` (secção "Checklist de qualidade").
No resumo ao utilizador diz: capítulos e lições criados, quantas perguntas, links usados, **o que não verificaste** (por exemplo, código não compilado).

## 7. Publicar

O utilizador faz `git add`, commit e `git push`. O GitHub Pages publica o `index.html`.

## Corrigir ou estender um módulo existente

- Módulos novos (JSON): edita o JSON, valida e gera.
- Módulos da base (Academia, C#, .NET, Autenticação): estão em `src/` (`m1.json`, `m2.json`, `mods.py`, `mod_auth.py`). Altera só o que foi pedido e volta a gerar.
- O "Projeto final" é gerado a partir de `src/m4_head.py`, `src/m4_tail.py` e `src/m4_stories.py` com `python3 src/asm.py`. Só mexas aí se o pedido for sobre o projeto.
