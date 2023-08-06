# Slitherway

[![PyPi version](https://badgen.net/pypi/v/slitherway/)](https://pypi.org/project/slitherway/)

Slitherway is a lightweight python wrapper around the [Flyway](https://flywaydb.org/) CLI.  
It allows you to run migrations directly from your python applications and tests

In order to use, you must have the Flyway CLI installed on your machine!

## Example

Using slitherway is simple

```py
from slitherway.commands import migrate
from slitherway.models import FlywayCommandArgs

args = FlywayCommandArgs(
    user=pg.POSTGRES_USER,
    password=pg.POSTGRES_PASSWORD,
    locations=["migrations"],
    url=f"jdbc:postgresql://localhost:{pg.get_exposed_port(5432)}/{pg.POSTGRES_DB}",
)

migrate(args)
```
