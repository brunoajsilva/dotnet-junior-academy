var repo = Substitute.For<IAccountRepository>();
repo.GetAsync("AC-001")
    .Returns(new Account("AC-001", ana, 200m));

var service = new AccountService(
    repo, new PromoInterest(0.02m));

var interest = await service.CalculateAsync("AC-001");

Assert.Equal(4m, interest);
await repo.Received(1).GetAsync("AC-001");
