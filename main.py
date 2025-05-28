import nextcord
from nextcord.ext.commands import Bot
import dotenv
import os

dotenv.load_dotenv()

client = Bot(intents=nextcord.Intents.all(), command_prefix="!")

loaded_cogs = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename in ["__init__.py", "PrebuiltEmbeds.py", 'config.py', 'appwriteHandler.py']:
        client.load_extension(f"cogs.{filename[:-3]}")
        loaded_cogs.append(f"{filename[:-3].capitalize()}")

print(loaded_cogs)
@client.slash_command(name="cogs", description="Shows all loaded cogs.")
async def cogs(inter: nextcord.Interaction):
    cogStr = "\n".join(f"<:Check:1376772416499613756> {cog}" for cog in loaded_cogs)
    await inter.send(embed=nextcord.Embed(title="Loaded Cogs", description=cogStr, color=nextcord.Color.blue()), ephemeral=True)

devMode = os.getenv("devMode")

if devMode == "0":
    client.run(os.getenv("prod"))   
elif devMode == "1":
    client.run(os.getenv("dev"))
else:
    print('\x1b[91mERROR! The \x1b[1m"testmode"\x1b[0m\x1b[91m .env setting is invalid.')

