
import nextcord
from nextcord.ext.commands import Cog
from nextcord.ext import application_checks


from .config import StaffRoleIdArray, QuestCreationPerms, Channels
from .PrebuiltEmbeds import InvalidQuestInfo, QuestEmbed
from .appwriteHandler import addQuest

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
        
        addQuest(quest_name, description, quest_difficulty, xp_awarded)
        
        await inter.guild.get_channel(Channels["Quests"]).send(embed=QuestEmbed(quest_name, description, quest_difficulty, xp_awarded))
        
def setup(client):
    client.add_cog(Quests(client))
    print("\033[0;32mQuest Cog Ready!\x1b[0m")

