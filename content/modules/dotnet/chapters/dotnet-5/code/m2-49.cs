Assert.Equal(180m, result);
Assert.True(account.IsActive);
Assert.False(list.Any());
Assert.Null(result);
Assert.Contains("AC-001", numbers);
Assert.Empty(list);

// exceptions
var ex = Assert.Throws<InvalidAccountException>(
    () => new Account("AC-001", ana, -5m));
Assert.Equal("AC-001", ex.Number);
