import nextcord

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
