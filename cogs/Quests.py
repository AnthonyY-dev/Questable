
import nextcord
from nextcord.ext.commands import Cog
from nextcord.ext import application_checks

import nextcord.ext
import nextcord.ext.commands


from .config import StaffRoleIdArray, QuestCreationPerms, Channels, Emojis, QuestAcceptDenyPerms
from .PrebuiltEmbeds import InvalidQuestInfo, QuestEmbed, QuestNotFoundEmbed, MissingRoleEmbed, questCompletedEmbed, questPendingEmbed, ProfileEmbed
from .appwriteHandler import addQuest, getQuestById, markQuestAccepted, checkIfQuestPendingOrCompleted, denyQuest, pendQuest, getUserInfo


class Quests(Cog):

    def __init__(self, client: nextcord.ext.commands.Bot):
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
        
        # Is a real quest, now check if its already pending or completed
        pendingOrCompleted = checkIfQuestPendingOrCompleted(inter.user.id, quest_id)
        
        if not pendingOrCompleted == 'ready':
            if pendingOrCompleted == 'pending':
                await inter.send(embed=questPendingEmbed, ephemeral=True)
                return
            if pendingOrCompleted == 'completed':
                await inter.send(embed=questCompletedEmbed, ephemeral=True)
                return
            return
        
        
        
        
        submissionsChannel = inter.guild.get_channel(Channels["QuestSubmissions"])
        
        view = nextcord.ui.View(timeout=None)
        
        acceptBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label="Accept", emoji=Emojis["Check"])
        denyBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label="Deny", emoji=Emojis["X"])
        
        pendingTag = submissionsChannel.get_tag(1377494517531410463)
        acceptedTag = submissionsChannel.get_tag(1377494563446587422)
        deniedTag = submissionsChannel.get_tag(1377494594551414835)
        
        async def acceptCallback(btnInter: nextcord.Interaction):
            if not any(role.id in QuestAcceptDenyPerms for role in btnInter.user.roles):
                await btnInter.response.send_message(embed=MissingRoleEmbed(QuestAcceptDenyPerms, btnInter.guild), ephemeral=True)
                return
            
            markQuestAccepted(inter.user.id,quest_id)
            
            acceptedView = nextcord.ui.View(timeout=None)
            acceptBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label=f"Quest accepted by {btnInter.user.global_name}", emoji=Emojis["Check"], disabled=True)
            denyBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label=f"Deny", emoji=Emojis["X"], disabled=True)
            acceptedView.add_item(acceptBtn)
            acceptedView.add_item(denyBtn)
            await btnInter.channel.edit(applied_tags=[acceptedTag])
            
            await btnInter.message.edit(content=f"Quest accepted by {btnInter.user.mention}",embed=QuestEmbed(questDetails['name'], questDetails['description'], int(questDetails['difficulty']), int(questDetails['xp_awarded']), quest_id, isThreadQuestAccepted=True), view=acceptedView)
            
        
        async def denyCallback(btnInter: nextcord.Interaction):
            if not any(role.id in QuestAcceptDenyPerms for role in btnInter.user.roles):
                await btnInter.response.send_message(embed=MissingRoleEmbed(QuestAcceptDenyPerms, btnInter.guild), ephemeral=True)
                return
            
            deniedView = nextcord.ui.View(timeout=None)
            acceptBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label="Accept", emoji=Emojis["Check"], disabled=True)
            denyBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label=f"Quest Denied by {btnInter.user.global_name}", emoji=Emojis["X"], disabled=True)
            deniedView.add_item(acceptBtn)
            deniedView.add_item(denyBtn)
            
            denyQuest(inter.user.id, quest_id)
            await btnInter.channel.edit(applied_tags=[deniedTag])
            
            await btnInter.message.edit(content=f"Quest Denied by {btnInter.user.mention}",embed=QuestEmbed(questDetails['name'], questDetails['description'], int(questDetails['difficulty']), int(questDetails['xp_awarded']), quest_id, isThreadQuestAccepted=False), view=deniedView)
        
        acceptBtn.callback = acceptCallback
        denyBtn.callback = denyCallback
        
        view.add_item(acceptBtn)
        view.add_item(denyBtn)
        
        pendQuest(inter.user.id, quest_id)
        
        thread = await submissionsChannel.create_thread(name=f"{inter.user.global_name}'s Submission for \"{questDetails['name']}\"", applied_tags=[pendingTag], embed=QuestEmbed(questDetails['name'], questDetails['description'], int(questDetails['difficulty']), int(questDetails['xp_awarded']), quest_id),content=f"{inter.user.mention} Please post any relevant details / images / videos here!\n-# {quest_id}", view=view)
        
        await inter.send(f"Done! Your quest submission was created at {thread.mention}.", ephemeral=True)
        
    @nextcord.slash_command(name="staff_panel", description="Authorized Access Only - Opens a panel for quests, incase this one has expired.")
    @application_checks.has_any_role(*QuestAcceptDenyPerms)
    async def staff_panel(self, inter: nextcord.Interaction):
        thread = inter.channel
        msg = await thread.fetch_message(thread.id)
        
        if not msg:
            await inter.send("Error! This is not a quest submission, or the starting message was deleted, or this quest has already been accepted / denied.")
            return
        quest_id = ""
        try:
            quest_id = msg.content.split("\n")[1].removeprefix("-# ")
        except Exception:
            await inter.send("Error, could not parse the starting message of this thread, so I could not find the ID.", ephemeral=True)
            return
            
        questDetails = getQuestById(quest_id)
        if questDetails == 404:
            await inter.send(embed=QuestNotFoundEmbed, ephemeral=True)
            return
        
        
        submissionsChannel = inter.guild.get_channel(Channels["QuestSubmissions"])
        
        view = nextcord.ui.View(timeout=None)
        
        acceptBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label="Accept", emoji=Emojis["Check"])
        denyBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label="Deny", emoji=Emojis["X"])
        
        pendingTag = submissionsChannel.get_tag(1377494517531410463)
        acceptedTag = submissionsChannel.get_tag(1377494563446587422)
        deniedTag = submissionsChannel.get_tag(1377494594551414835)
        
        async def acceptCallback(btnInter: nextcord.Interaction):
            if not any(role.id in QuestAcceptDenyPerms for role in btnInter.user.roles):
                await btnInter.response.send_message(embed=MissingRoleEmbed(QuestAcceptDenyPerms, btnInter.guild), ephemeral=True)
                return
            
            markQuestAccepted(inter.user.id,quest_id)
            
            acceptedView = nextcord.ui.View(timeout=None)
            acceptBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.green, label=f"Quest accepted by {btnInter.user.global_name}", emoji=Emojis["Check"], disabled=True)
            denyBtn = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label=f"Deny", emoji=Emojis["X"], disabled=True)
            acceptedView.add_item(acceptBtn)
            acceptedView.add_item(denyBtn)
            await btnInter.channel.edit(applied_tags=[acceptedTag])
            
            await msg.edit(content=f"Quest accepted by {btnInter.user.mention}",embed=QuestEmbed(questDetails['name'], questDetails['description'], int(questDetails['difficulty']), int(questDetails['xp_awarded']), quest_id, isThreadQuestAccepted=True), view=None)
            await btnInter.response.edit_message(content="Done! Quest accepted.", view=None)
        
        async def denyCallback(btnInter: nextcord.Interaction):
            if not any(role.id in QuestAcceptDenyPerms for role in btnInter.user.roles):
                await btnInter.response.send_message(embed=MissingRoleEmbed(QuestAcceptDenyPerms, btnInter.guild), ephemeral=True)
                return
            
            denyQuest(inter.user.id, quest_id)
            await btnInter.channel.edit(applied_tags=[deniedTag])
            
            await msg.edit(content=f"Quest Denied by {btnInter.user.mention}",embed=QuestEmbed(questDetails['name'], questDetails['description'], int(questDetails['difficulty']), int(questDetails['xp_awarded']), quest_id, isThreadQuestAccepted=False), view=None)
            await btnInter.response.edit_message(content="Done! Quest denied.", view=None)
        acceptBtn.callback = acceptCallback
        denyBtn.callback = denyCallback
        
        view.add_item(acceptBtn)
        view.add_item(denyBtn)
        
        await inter.send("Staff Panel", view=view, ephemeral=True)
        
    @nextcord.slash_command(name="profile", description="Views your current profile! Shows XP needed to progress to the next level, and other stats.")
    async def profile(self,inter: nextcord.Interaction):
        userInfo = getUserInfo(inter.user.id)
        
        await inter.send(embed=ProfileEmbed(inter.user, userInfo))
        
        
def setup(client: nextcord.ext.commands.Bot):
    client.add_cog(Quests(client))
    print("\033[0;32mQuest Cog Ready!\x1b[0m")

