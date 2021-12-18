from urllib.parse import unquote

import requests
import discord
from discord.ext import commands

import regexparser
import secret

PREFIX = "]"
ITEMS = {k.upper(): unquote(v) for k, v in regexparser.dict_items().items()}
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")


def to_upper(string: str) -> str:
    """ Wrapper for str.upper()"""
    return string.upper()


def get_request(item_name: str) -> requests.Response:
    """ Sends a GET request to TBOIR wiki and returns the response"""
    return requests.get(
        "https://bindingofisaacrebirth.fandom.com/api.php?",
        params=
        {
            "action": "query",
            "format": "json",
            "maxlag": "",
            "prop": "extracts",
            "titles": ITEMS[item_name],
            "redirects": 1,
            "formatversion": "2",
            "exsentences": "10",
            "exlimit": "2",
            "explaintext": 1
        }
    )


def item_exists(item_name: str) -> bool:
    """ Checks if str is an item in TBOIR by searching the item list. """
    return item_name in ITEMS.keys()


def create_message_string(response: requests.Response) -> str:
    """ Creates a beautiful, ready to send string from the response from get_request(). """
    try:
        response = response.json()["query"]["pages"][0]
        title = response["title"]
        extract = response["extract"]
        return "**{}**\n```yaml\n{}\n```".format(title, extract)
    except ValueError:
        return "Something went wrong at the parsing stage."


@bot.command()
async def lookup(ctx, *args: to_upper) -> None:
    """
    Gets a list of arguments, turns them into a string that corresponds to a TBOIR item,
    calls item_exists() on it, then calls get_request(),
    calls create_message_string() and then sends the message.
    """
    if args:
        item_name = " ".join(args[:])
    else:
        e = discord.Embed(Title="Error", description="No item specified")
        await ctx.send(embed=e)
        return None
    if item_exists(item_name):
        await ctx.send(create_message_string(get_request(item_name)))
        return None
    else:
        e = discord.Embed(Title="Error", description="No such item")
        await ctx.send(embed=e)


@bot.command()
async def help(ctx):
    """ A Help command. """
    e = discord.Embed(
        Title="Help",
        description="Use `]lookup <item name>` to get info on an item."
                    "\n\nAll item information is taken from The Binding Of Isaac Rebirth wiki, "
                    "https://bindingofisaacrebirth.fandom.com"
    )
    await ctx.send(embed=e)


@bot.event
async def on_command_error(ctx, error):
    """ Error handling. """
    if isinstance(error, commands.CommandNotFound):
        e = discord.Embed(Title="Error", description="No command found, try `]help` for help")
        await ctx.send(embed=e)
    else:
        e = discord.Embed(Title="Error", description="Unknown error detected")
        await ctx.send(embed=e)


if __name__ == "__main__":
    bot.run(secret.token)

