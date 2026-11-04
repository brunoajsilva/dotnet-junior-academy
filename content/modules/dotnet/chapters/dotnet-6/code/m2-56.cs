BankingApp.sln
├─ BankingApp.Domain          entities and rules
├─ BankingApp.Application     use cases
├─ BankingApp.Infrastructure  EF Core
├─ BankingApp.Api             controllers
└─ BankingApp.Tests           tests

Api            -> Application, Infrastructure
Infrastructure -> Application
Application    -> Domain
Domain         -> (nothing)
