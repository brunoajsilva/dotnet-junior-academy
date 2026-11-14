// Os módulos da academia, pela ordem do menu lateral e do cabeçalho.
//   dir    pasta em src/content/docs
//   label  nome completo (menu lateral e etiqueta por cima do título)
//   short  nome curto (cabeçalho)
//   start  primeira página do módulo (destino do cabeçalho)
// A cor de cada módulo está em src/styles/academy.css (--module-1 a --module-8).
export const modules = [
  { dir: "academia", label: "Introdução à Academia", short: "Academia", start: "academia/o-que-e/" },
  { dir: "csharp", label: "Introdução ao C#", short: "C#", start: "csharp/" },
  { dir: "dotnet", label: "Introdução ao .NET", short: ".NET", start: "dotnet/" },
  { dir: "auth", label: "Autenticação e Autorização", short: "Autenticação", start: "auth/" },
  { dir: "projeto", label: "Projeto final: BankingApp", short: "Projeto", start: "projeto/" },
] as const;
