// Os módulos da academia, pela ordem do menu lateral.
// `dir` é a pasta em src/content/docs. A cor de cada módulo está em src/styles/academy.css (--module-1 a --module-5).
export const modules = [
  { dir: "academia", label: "Introdução à Academia" },
  { dir: "csharp", label: "Introdução ao C#" },
  { dir: "dotnet", label: "Introdução ao .NET" },
  { dir: "auth", label: "Autenticação e Autorização" },
  { dir: "projeto", label: "Projeto final: BankingApp" },
] as const;
