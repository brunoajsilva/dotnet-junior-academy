using BankingApp.Application.Common;

namespace BankingApp.Tests.Application;

public class ResponseTests
{
    [Fact]
    public void Ok_HasDataAndNoErrors()
    {
        var response = Response<int>.Ok(42);

        Assert.True(response.Success);
        Assert.Equal(42, response.Data);
        Assert.Empty(response.Errors);
    }

    [Fact]
    public void Fail_IsNotSuccessAndKeepsAllErrors()
    {
        var response = Response<int>.Fail(Error.Validation("a"), Error.Conflict("b"));

        Assert.False(response.Success);
        Assert.Equal(2, response.Errors.Count);
    }

    [Fact]
    public void Map_OnFailure_KeepsTheErrors()
    {
        var response = Response<int>.Fail(Error.NotFound("x")).Map(n => n.ToString());

        Assert.False(response.Success);
        Assert.Equal("not_found", response.Errors[0].Code);
    }
}
