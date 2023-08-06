# winerp
An IPC based on Websockets. Fast, Stable, and easy-to-use, for inter-communication between your processes or discord.py bots.

> **BREAKING CHANGES (1.4.0):**  
The message source name is passed to all registered routes.
Instead of:
> ```py
> @ipc.route() # < v1.4.0
> async def route_name():
>     ...
> ```
> Use: 
> ```py
> @ipc.route() # >= v1.4.0
> async def route_name(source):
>     ...
> ```

### Key Features

 - **Fast** with minimum recorded response time being `< 2ms`
 - Lightweight, Stable and Easy to integrate.
 - No limitation on number of connected clients. 

## Installation
Stable:
```py
pip install -U winerp
```
Main branch (can be unstable/buggy):
```py
pip install git+https://www.github.com/BlackThunder01001/winerp
```

### Working:
This library uses a central server for communication between multiple clients. You can connect a large number of clients for sharing data, and data can be shared between any connected client.

1) Import the library:
```py
import winerp
```

2) Initialize winerp client:
```py
ipc_client = winerp.Client(local_name = "my-cool-app", port=8080)
```

3) Start the client:
```py
await ipc_client.start()
# or
asyncio.create_task(ipc_client.start())
```

- Registering routes:
```py
@ipc_client.route
async def route_name(source, user_name):
    return f"Hello {user_name}"
```

- Requesting data from another client:
```py
user_name = await ipc_client.request(route="fetch_user_name", source="another-cool-bot", user_id = 123)
```

- Sending *information* type data to other clients:
```py
data = [1, 2, 3, 4]
await ipc_client.inform(data, destinations=["another-cool-bot"])
```

## Example Usage:

Start the server on terminal using `$ winerp --port 8080`. You can also start the server using `winerp.Server`

### Client 1 (`some-random-bot`):
```py
import winerp
import discord
from discord.ext.commands import Bot
bot = Bot(command_prefix="!", intents=discord.Intents.all())

bot.ipc = winerp.Client(local_name = "some-random-bot", port=8080)

@bot.command()
async def request(ctx):
    # Fetching data from a client named "another-bot" using route "get_some_data"
    data = await bot.ipc.request("get_some_data", source = "another-bot")
    await ctx.send(data)


@bot.ipc.route()
async def get_formatted_data(source, user_id = None):
    return f"<@{user_id}>"


@bot.ipc.event
async def on_winerp_ready():
    print("Winerp Client is ready for connections")

bot.loop.create_task(bot.ipc.start())
bot.run("TOKEN")
```

### Client 2 (`another-bot`)
```py
import winerp
import discord
from discord.ext.commands import Bot
bot = Bot(command_prefix="?", intents=discord.Intents.all())

bot.ipc = winerp.Client(local_name = "another-bot", port=8080)

@bot.command()
async def format(ctx):
    # Fetching data from a client named "some-random-bot" using route "get_formatted_data"
    data = await bot.ipc.request("get_formatted_data", source = "some-random-bot", user_id = ctx.author.id)
    await ctx.send(data)


@bot.ipc.route()
async def get_some_data(source):
    return "You are very cool"


bot.loop.create_task(bot.ipc.start())
bot.run("TOKEN")
```

