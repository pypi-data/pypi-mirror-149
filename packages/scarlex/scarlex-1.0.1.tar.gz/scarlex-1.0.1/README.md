# Scarlex Asynchronous API Wrapper

- [Discord] : https://discord.gg/ZKzmmt4gvq
- [Site] : https://scarlex.org/api

# How To Use

- join our Discord for any support (link above).
- register your own profile on our website (link above).
- then login and you're ready to fetch endpoints and check your stats.

# Examples

```python
# import ApiClient from sharex package.
from scarlex import ApiClient
# import asyncio if you want to run clint Synchronously else the pacakage is in asynchronous format.
import asyncio

# create an instance of client with name and password
client = ApiClient(name="Vishal", password="A cool password")

data = asyncio.run(client.make_request("progressbar?max=100&value=69&size=100&style=3"))
# If using asynchronously [can be used only inside async functions]
# data = await client.make_request("progressbar?max=100&value=69&size=100&style=3")

print(data.json)
print(data.status)
print(data.message)
```
## Developers / Contributors
- **[Vishal#0001]( https://github.com/krvishalsh )**