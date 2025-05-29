
import nextcord
from nextcord.ext.commands import Cog
from nextcord.ext import application_checks


from .config import StaffRoleIdArray, QuestCreationPerms, Channels, Emojis
from .PrebuiltEmbeds import InvalidQuestInfo, QuestEmbed, QuestNotFoundEmbed
from .appwriteHandler import addQuest, getQuestById

class Quests(Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="create_quest", description="Creates a quest.")
    @application_checks.has_any_role(*QuestCreationPerms)
    async def create_quest(self, inter: nextcord.Interaction, quest_name: str, description: str, quest_difficulty: int, xp_awarded: int):
        validitys = {
            'name': False,
            'description': False,
            'difficulty': False,
        }
        if len(quest_name) <= 256:
            validitys['name'] = True
        if len(description) <= 1024:
            validitys['description'] = True
        if quest_difficulty >= 1 and quest_difficulty <= 5 :
            validitys['difficulty'] = True
        isAllValid = False
        if validitys['name'] and validitys['description'] and validitys['difficulty']: isAllValid=True

        if not isAllValid:
            await inter.send(embed=InvalidQuestInfo(validitys), ephemeral=True)
            return
        
        questId = addQuest(quest_name, description, quest_difficulty, xp_awarded)
        
        await inter.guild.get_channel(Channels["Quests"]).send(embed=QuestEmbed(quest_name, description, quest_difficulty, xp_awarded, questId))
        await inter.send(embed=nextcord.Embed(title="Done! Your quest has been created.", colour=nextcord.Colour.green()), ephemeral=True)
        
    @nextcord.slash_command(name="submit", description="Submits a quest.")
    async def submit(self, inter: nextcord.Interaction, quest_id: str):
        questDetails = getQuestById(quest_id)
        if questDetails == 404:
            await inter.send(embed=QuestNotFoundEmbed, ephemeral=True)
            return
        
        # Is a real quest
        submissionsChannel = inter.guild.get_channel(Channels["QuestSubmissions"])
        
        view = nextcord.ui.View(timeout=None)
        
        acceptBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label="Accept", emoji=Emojis["Check"])
        denyBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label="Deny", emoji=Emojis["X"])
        
        async def acceptCallback(btnInter: nextcord.Interaction):
            pass
        
        async def denyCallback(btnInter: nextcord.Interaction):
            deniedView = nextcord.ui.View(timeout=None)
            acceptBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label="Accept", emoji=Emojis["Check"], disabled=True)
            denyBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label=f"Quest Denied by {btnInter.user.global_name}", emoji=Emojis["X"], disabled=True)
            deniedView.add_item(acceptBtn)
            deniedView.add_item(denyBtn)
            await btnInter.message.edit(content=f"Quest Denied by {btnInter.user.mention}",embed=QuestEmbed(questDetails['name'], questDetails['description'], int(questDetails['difficulty']), int(questDetails['xp_awarded']), quest_id, isThreadQuestAccepted=False), view=deniedView)
        
        acceptBtn.callback = acceptCallback
        denyBtn.callback = denyCallback
        
        view.add_item(acceptBtn)
        view.add_item(denyBtn)
        
        thread = await submissionsChannel.create_thread(name=f"{inter.user.global_name}'s Submission for \"{questDetails['name']}\"", applied_tags=[submissionsChannel.get_tag(1377494517531410463)], embed=QuestEmbed(questDetails['name'], questDetails['description'], int(questDetails['difficulty']), int(questDetails['xp_awarded']), quest_id),content=f"{inter.user.mention} Please post any relevant details / images / videos here!", view=view)
        
        await inter.send(f"Done! Your quest submission was created at {thread.mention}.", ephemeral=True)
        
        
        
        
        
        
def setup(client):
    client.add_cog(Quests(client))
    print("\033[0;32mQuest Cog Ready!\x1b[0m")

