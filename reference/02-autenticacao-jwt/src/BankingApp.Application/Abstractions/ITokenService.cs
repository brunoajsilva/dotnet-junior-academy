using BankingApp.Domain.Customers;

namespace BankingApp.Application.Abstractions;

public interface ITokenService
{
    TokenResult Create(Customer customer);
}
