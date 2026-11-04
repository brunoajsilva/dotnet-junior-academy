var c = new Customer { Name = "Ana" };
_ctx.Customers.Add(c);           // new
await _ctx.SaveChangesAsync();  // INSERT

c.Name = "Ana Pereira";         // changed
await _ctx.SaveChangesAsync();  // UPDATE

_ctx.Customers.Remove(c);        // removed
await _ctx.SaveChangesAsync();  // DELETE
