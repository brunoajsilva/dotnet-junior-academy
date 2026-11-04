# Prompt: criar um módulo novo

Copia o bloco abaixo, preenche os campos entre `[ ]` e cola-o numa sessão de IA com acesso a este repositório.

```
Lê o ficheiro AGENTS.md e os ficheiros referidos nele (docs/AUTHORING.md,
docs/CONTENT-SCHEMA.md, docs/STYLE-GUIDE.md).

Quero um módulo novo para a .NET Backend Academy.

Tema: [ex.: Entity Framework Core: migrations e consultas]
Para quem: [ex.: quem já fez C# e .NET e vai trabalhar com bases de dados]
Resultado esperado: [ex.: no fim, o aluno cria entidades, gera migrations e escreve consultas com LINQ]
Âmbito: [ex.: 3 capítulos, cerca de 8 lições cada]
Versões: .NET 10, C# 14 [alterar se for diferente]
Fontes a usar: [ex.: documentação oficial da Microsoft; links que colo abaixo]
Notas minhas: [ex.: insistir em AsNoTracking e em migrations com valor por omissão]

Faz, por esta ordem:
1. Mostra-me primeiro o esboço (tabela capítulo, lição, tipo, ideia única) e espera pela minha aprovação.
2. Depois de aprovado, cria o módulo com `npm run new:module` e completa-o (module.yaml, um chapter.yaml por capítulo, uma lição
   por ficheiro e os ficheiros de código em code/); depois move-o para content/modules/<id>/ e acrescenta-o
   ao content/manifest.yaml, antes do projeto.
3. Corre npm run check e npm test e corrige o que falhar.
4. No fim, resume: capítulos, lições, perguntas, links usados e o que NÃO conseguiste verificar.

Não alteres src/, tools/ nem os workflows. Não inventes APIs: confirma na documentação oficial.
```

## Variantes

**Só estender um módulo existente**
```
Lê AGENTS.md. No módulo content/modules/<id>/ acrescenta um capítulo sobre [tema], com 6 lições e um quiz.
Mantém o estilo do módulo e não alteres ids existentes. Valida e testa.
```

**Rever um módulo**
```
Lê AGENTS.md e docs/STYLE-GUIDE.md. Revê content/modules/<id>/ contra a checklist de qualidade.
Lista os problemas por gravidade e corrige os que forem de estilo. Não mudes o sentido técnico sem me perguntar.
```

**Gerar só o quiz de um capítulo**
```
Lê docs/CONTENT-SCHEMA.md (secção Quiz). Escreve 5 perguntas para o capítulo <id>-<n>, com distratores plausíveis
e explicação do porquê. Distribui a resposta certa por posições diferentes.
```
