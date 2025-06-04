
import nextcord
from nextcord.ext.commands import Cog
from nextcord.ext import commands
from nextcord.ext import application_checks

from .PrebuiltEmbeds import MissingRoleEmbed
from .config import StaffRoleIdArray

class Events(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        if isinstance(error, application_checks.errors.ApplicationMissingAnyRole):
            await interaction.send(embed=MissingRoleEmbed(error.missing_roles, interaction.guild), ephemeral=True)

        else:
            print(error)
    @Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        await member.add_roles(member.guild.get_role(1375341523163545685))
        
def setup(client):
    client.add_cog(Events(client))
