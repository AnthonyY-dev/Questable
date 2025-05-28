import nextcord
from nextcord.ext.commands import Bot
import dotenv
import os
from cogs import appwriteHandler
from appwrite.client import Client
from appwrite.services.databases import Databases
os.system("clear")

dotenv.load_dotenv()

client = Bot(intents=nextcord.Intents.all(), command_prefix="!")

loaded_cogs = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and not filename in ["__init__.py", "PrebuiltEmbeds.py", 'config.py', 'appwriteHandler.py']:
        client.load_extension(f"cogs.{filename[:-3]}")
        loaded_cogs.append(f"{filename[:-3].capitalize()}")

devMode = os.getenv("devMode", "0")

appWriteClient = Client()
if devMode=="0":
    appWriteClient.set_endpoint('https://fra.cloud.appwrite.io/v1') # Re  place with your Appwrite endpoint
    appWriteClient.set_project('68353a7b0002defacf67') # Replace with your project ID
    appWriteClient.set_key(os.getenv("prodAppwriteKey")) # Replace with your secret API key
elif devMode=="1":
    appWriteClient.set_endpoint('https://fra.cloud.appwrite.io/v1') # Re  place with your Appwrite endpoint
    appWriteClient.set_project('68353af3001e33714650') # Replace with your project ID
    appWriteClient.set_key(os.getenv("devAppwriteKey")) # Replace with your secret API key
databases = Databases(appWriteClient)

appwriteHandler.init(appwriteHandler, databases)

@client.slash_command(name="cogs", description="Shows all loaded cogs.")
async def cogs(inter: nextcord.Interaction):
    cogStr = "\n".join(f"<:Check:1376772416499613756> {cog}" for cog in loaded_cogs)
    await inter.send(embed=nextcord.Embed(title="Loaded Cogs", description=cogStr, color=nextcord.Color.blue()), ephemeral=True)

@client.event
async def on_ready():
    print("\033[0;32mClient Ready!\x1b[0m")




if devMode == "0":
    client.run(os.getenv("prod"))   
elif devMode == "1":
    client.run(os.getenv("dev"))
else:
    print('\x1b[91mERROR! The \x1b[1m"testmode"\x1b[0m\x1b[91m .env setting is invalid.')
