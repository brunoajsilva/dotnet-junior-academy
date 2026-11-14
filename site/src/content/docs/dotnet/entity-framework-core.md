---
title: "Entity Framework Core"
description: "Ligar a API a uma base de dados com classes C#, migrations e consultas LINQ."
sidebar:
  order: 4
---

Ligar a API a uma base de dados com classes C#, migrations e consultas LINQ.

## O que é o Entity Framework Core

1. **Classes C#** Account, Customer
2. **EF Core** traduz e acompanha as alterações
3. **Base de dados** tabelas e linhas SQL

:::note[Nota]
DbContext: a sessão com a base de dados.

DbSet\<T\>: uma tabela, vista como coleção.

Provider: o pacote que fala com cada base de dados (por exemplo, SQL Server).

Migrations: o histórico versionado do esquema da base de dados.
:::

## Code-first: o modelo manda

1. **Classes C#** entidades e DbContext
2. **Migration** ficheiro C# gerado a partir do modelo
3. **Base de dados** esquema criado e atualizado

:::note[Nota]
Code-first: escreves as classes e o EF gera o esquema da base de dados.

Migrations: cada alteração ao modelo fica num ficheiro versionado com o código.

Database-first: parte de uma base existente e gera as classes (dotnet ef dbcontext scaffold).

Neste módulo: code-first. O código é a fonte de verdade do esquema.
:::

## Entidades

```csharp
public class Customer
{
    public int Id { get; set; }
    public string Name { get; set; } = "";
    public List<Account> Accounts { get; } = new();
}

public class Account
{
    public int Id { get; set; }
    public string Number { get; set; } = "";
    public decimal Balance { get; set; }
    public int CustomerId { get; set; }
    public Customer Customer { get; set; } = null!;
}
```

- Cada classe é uma tabela; cada propriedade, uma coluna.
- Id é a chave primária, por convenção.
- CustomerId é a chave estrangeira.
- Customer e Accounts são propriedades de navegação.

<details>
<summary>Saber mais</summary>

As entidades são classes simples. Por convenção, uma propriedade chamada Id (ou ClassNameId) é a chave primária. CustomerId é a chave estrangeira para Customer, e as propriedades de navegação (Customer, Accounts) permitem percorrer a relação em C# sem escrever JOINs.

</details>

## Configurar o EF Core: pacotes e ligação

```csharp
// packages (Api project)
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Design

// CLI tool (once per machine)
dotnet tool install --global dotnet-ef

// appsettings.json
"ConnectionStrings": {
  "BankingApp": "Server=...;Database=BankingApp"
}
```

- SqlServer é o provider: traduz o C# para SQL Server.
- Design dá ao dotnet ef o que precisa para gerar migrations.
- dotnet-ef é a ferramenta de linha de comandos.
- A connection string vive na configuração, nunca no código.

<details>
<summary>Saber mais</summary>

São precisos três elementos: o pacote do provider (Microsoft.EntityFrameworkCore.SqlServer), o pacote Design (para gerar migrations) e a ferramenta global dotnet-ef. A connection string fica no appsettings, e não no código.

:::caution[Armadilha]
Instalar o pacote Design só no projeto errado. Os comandos dotnet ef precisam de o encontrar no projeto de arranque.
:::

</details>

## DbContext e ligação

```csharp
public class BankingAppContext : DbContext
{
    public BankingAppContext(
        DbContextOptions<BankingAppContext> options)
        : base(options) { }

    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Account> Accounts => Set<Account>();
}

// Program.cs
builder.Services.AddDbContext<BankingAppContext>(o =>
    o.UseSqlServer(cs));
```

- O DbContext agrupa as tabelas disponíveis.
- É registado no container, com tempo de vida Scoped.
- UseSqlServer escolhe o provider.
- A connection string vem da configuração.

<details>
<summary>Saber mais</summary>

O DbContext representa uma sessão com a base de dados. Cada DbSet\<T\> é uma tabela. É registado no container com AddDbContext, que o torna Scoped, e recebe as opções (provider e connection string) no construtor.

</details>

## Configurar o modelo

```csharp
protected override void OnModelCreating(ModelBuilder mb)
{
    mb.Entity<Account>(e =>
    {
        e.Property(a => a.Number).HasMaxLength(20);
        e.HasIndex(a => a.Number).IsUnique();
        e.Property(a => a.Balance).HasPrecision(18, 2);
        e.HasOne(a => a.Customer)
            .WithMany(c => c.Accounts)
            .HasForeignKey(a => a.CustomerId);
    });
}
```

- As convenções resolvem o simples; a Fluent API resolve o resto.
- Tamanhos, índices e precisão decimal.
- A relação entre entidades.
- Fica no DbContext, fora das entidades.

<details>
<summary>Saber mais</summary>

As convenções cobrem o caso simples. Para o resto usa a Fluent API no OnModelCreating: tamanhos máximos, índices únicos (por exemplo, no número da conta), precisão de decimais e relações. Fica no DbContext, e as entidades continuam livres de detalhes de base de dados.

:::caution[Armadilha]
Esquecer a precisão do decimal. O EF avisa, e o valor pode ser truncado na base de dados.
:::

</details>

## Migrations: criar a primeira

```csharp
dotnet ef migrations add Initial

Migrations/
  20261022101500_Initial.cs
  BankingAppContextModelSnapshot.cs

// 20261022101500_Initial.cs (generated)
protected override void Up(MigrationBuilder mb)
{
    mb.CreateTable(
        name: "Accounts",
        columns: table => new { ... });
}

protected override void Down(MigrationBuilder mb)
    => mb.DropTable(name: "Accounts");
```

- migrations add compara o modelo com o snapshot e gera o código.
- Up aplica a alteração; Down desfaz.
- O snapshot guarda o último estado do modelo.
- Rever o ficheiro gerado antes de o aplicar.

<details>
<summary>Saber mais</summary>

dotnet ef migrations add compara o modelo atual com o snapshot da última migration e gera um ficheiro C# com os métodos Up (aplicar) e Down (desfazer). Lê sempre o ficheiro gerado antes de o aplicar: é aí que vês, por exemplo, uma coluna que ia ser apagada.

</details>

## Migrations: atualizar a base de dados

```csharp
dotnet ef database update
// applies the pending migrations

// the model changes: Customer gets TaxId
dotnet ef migrations add AddTaxId
dotnet ef database update

// go back to a previous migration
dotnet ef database update Initial

// drop the last migration (not applied)
dotnet ef migrations remove

// SQL script for production
dotnet ef migrations script --idempotent
```

- database update cria a base de dados, se faltar, e aplica o que está pendente.
- A tabela \_\_EFMigrationsHistory regista o que já foi aplicado.
- Cada alteração ao modelo gera uma nova migration.
- Em produção usa-se um script SQL revisto.

<details>
<summary>Saber mais</summary>

dotnet ef database update cria a base de dados, se não existir, e aplica as migrations pendentes. A tabela \_\_EFMigrationsHistory regista o que já foi aplicado, por isso podes correr o comando várias vezes. Em produção não se aplica diretamente: gera-se um script SQL, revê-se e executa-se com o processo normal de Release.

:::tip[Experimenta]
Acrescenta uma propriedade a Account, cria uma nova migration e abre o ficheiro gerado.
:::

</details>

## Consultar dados

```csharp
var highBalance = await _ctx.Accounts
    .Where(a => a.Balance > 300m)
    .OrderBy(a => a.Number)
    .ToListAsync();

var account = await _ctx.Accounts
    .Include(a => a.Customer)
    .FirstOrDefaultAsync(a => a.Number == number);

var total = await _ctx.Accounts
    .Where(a => a.CustomerId == id)
    .SumAsync(a => a.Balance);
```

- É o LINQ e o IQueryable que já conheces.
- Include carrega a relação na mesma consulta.
- Os métodos Async libertam a thread.
- AsNoTracking acelera as consultas só de leitura.

<details>
<summary>Saber mais</summary>

Consultar com o EF é usar o LINQ que já conheces sobre um DbSet. Include carrega a relação na mesma consulta (um JOIN). Os métodos Async (ToListAsync, FirstOrDefaultAsync) libertam a thread. AsNoTracking diz ao EF que não vais alterar os resultados, o que torna a consulta mais leve.

</details>

## Gravar alterações

```csharp
var c = new Customer { Name = "Ana" };
_ctx.Customers.Add(c);           // new
await _ctx.SaveChangesAsync();  // INSERT

c.Name = "Ana Pereira";         // changed
await _ctx.SaveChangesAsync();  // UPDATE

_ctx.Customers.Remove(c);        // removed
await _ctx.SaveChangesAsync();  // DELETE
```

- O EF acompanha as entidades que carrega.
- Nada vai para a base de dados até SaveChangesAsync.
- Todas as alterações de um SaveChanges correm numa transação.
- Alterar a propriedade basta: não há «update» explícito.

<details>
<summary>Saber mais</summary>

O EF acompanha as entidades que carrega (change tracking). Alteras uma propriedade, chamas SaveChangesAsync, e o EF gera o UPDATE só dos campos alterados, tudo numa transação. Para inserir, Add + SaveChangesAsync.

:::caution[Armadilha]
Esquecer o SaveChangesAsync. Não há erro e nada fica gravado.
:::

</details>

## Armadilhas comuns

#### Consulta em ciclo (N+1)

Carregar a relação dentro de um ciclo faz uma consulta por linha. Usar Include.

#### ToList cedo demais

Chamar ToList antes do Where traz a tabela toda para memória.

#### Esquecer o SaveChanges

Sem SaveChangesAsync, nada é gravado e nenhum erro aparece.

#### DbContext e threads

O DbContext não é seguro entre threads: não o partilhar em tarefas paralelas.

<details>
<summary>Saber mais</summary>

O N+1 acontece quando carregas uma lista (1 consulta) e depois acedes a uma relação de cada item (N consultas). Include resolve com um JOIN. ToList antes do Where traz tudo para memória. Estes dois erros não dão exceção: só se notam na lentidão, por isso convém olhar para o SQL gerado (LogTo ou o log do EF).

</details>

## Persistir as contas

:::note[Exercício prático]
Resolve no teu IDE antes de abrires a solução ou o resultado esperado.
:::

1. **Modelo.** entidades Customer e Account e o BankingAppContext
2. **Configurar.** índice único em Number e precisão do Balance
3. **Migration.** criar a migration Initial e aplicá-la à base de dados
4. **Substituir.** a lista em memória pelo DbContext nos três endpoints
5. **Devolver.** o nome do cliente na resposta, com Include

<details>
<summary>Ver resultado esperado</summary>

```text
Accounts
Id Number  Balance CustomerId
 1 AC-001  320.00 1
 2 AC-002  150.00 1

Customers
Id Name
 1 Ana Pereira
```

</details>

:::note[Extra]
Criar uma consulta que devolve o total de saldos por cliente, calculado na base de dados.
:::

<details>
<summary>Saber mais</summary>

Só passas ao capítulo seguinte quando o resultado esperado aparecer no teu computador. Se algo falhar, lê a mensagem de erro de baixo para cima: a última linha costuma dizer o que correu mal.

:::tip[Experimenta]
Criar uma consulta que devolve o total de saldos por cliente, calculado na base de dados.
:::

</details>
