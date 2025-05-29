import nextcord
from .config import Emojis, Branding

MissingSubcommandEmbed = nextcord.Embed(title="Missing Subcommand!", description="Please specify a subcommand.", colour=nextcord.Colour.red())

def MissingRoleEmbed(role_ids, guild: nextcord.Guild):
    role_mentions = []
    for role_id in role_ids:
        role = guild.get_role(role_id)
        if role:
            role_mentions.append(role.mention)
        else:
            role_mentions.append(f"`{role_id}`")  # fallback if not found

    return nextcord.Embed(
        title="You do not have permission to run this command.",
        description=f"Required Role(s): {', '.join(role_mentions)}",
        colour=nextcord.Colour.red()
    )

"""
validitys = {
            'name': False,
            'description': False,
            'difficulty': False,
        }
"""
def InvalidQuestInfo(validities):
   return nextcord.Embed(title="Invalid Quest Info", description=f"""**Name**: {Emojis['Check'] if validities['name'] else Emojis['X']}
**Description**: {Emojis['Check'] if validities['description'] else Emojis['X']}
**Difficulty**: {Emojis['Check'] if validities['difficulty'] else Emojis['X']}""", colour=nextcord.Colour.red())



def QuestEmbed(quest_name, description, difficulty, xp_awarded,  questId: str,image: str | None = None, isThreadQuestAccepted: bool | None = None):
    line = Emojis["Line"]
    
    color=nextcord.Colour.from_rgb(56, 182, 255)
    if isThreadQuestAccepted == True:
        color=nextcord.Colour.green()
    elif isThreadQuestAccepted == False:
        color=nextcord.Colour.red()
    
    qEmbed = nextcord.Embed(title=quest_name, description=f"""{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}

{description}

{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}

**XP Awarded:** {xp_awarded} {Emojis["XP"]}
**Difficulty:** `{str(difficulty)}/5` {Emojis["Difficulty"][difficulty]}

{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}{line}""", colour=color)

    qEmbed.set_author(name="Questable", url=Branding['QuestableLogoURL'])
    qEmbed.set_footer(text="ID: "+questId+" - Submit via /submit "+questId)

    return qEmbed



QuestNotFoundEmbed = nextcord.Embed(title="Error finding quest",description="The requested quest could not be found.", colour=nextcord.Colour.red())