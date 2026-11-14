// Os módulos da academia, pela ordem do menu lateral.
//   dir    pasta em src/content/docs
//   label  nome completo (menu lateral e etiqueta por cima do título)
// A cor de cada módulo está em src/styles/academy.css (--module-1 a --module-8).
export const modules = [
  { dir: "academia", label: "Introdução à Academia" },
  { dir: "csharp", label: "Introdução ao C#" },
  { dir: "dotnet", label: "Introdução ao .NET" },
  { dir: "auth", label: "Autenticação e Autorização" },
  { dir: "projeto", label: "Projeto Final" },
] as const;
