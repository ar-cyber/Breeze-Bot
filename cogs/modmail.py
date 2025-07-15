import discord
from discord.ext import commands
from discord.ext.commands import Cog

from utils.config import config
import json
import random
class ticket(Cog):
    def __init__(self, bot):
        self.client = bot



    @discord.slash_command(name = "ping", description="Pong! Check the latency of the bot.")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f'PONG!\nLatency: {round(self.client.latency * 1000)}ms', ephemeral=True)
    
    
    @discord.slash_command(name = "claim", description = "Claim this ticket message")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def _reply(self, ctx: discord.ApplicationContext):
        data = json.load(open('cogs/modmemory.json', 'r'))
        for item in data['sessions']:
            if ctx.channel.name == item['text_channel']:
                if item['claimedby'] == ctx.user.id:
                    return await ctx.respond("You've already claimed this ticket!", ephemeral=True)
                if item['claimedby'] != "":
                    return await ctx.respond("Someone's already claimed this ticket!", ephemeral=True)
                user = await self.client.fetch_user(item['user'])
                await user.send(f"# **{str(ctx.user)} | {str(ctx.user.id)}** has claimed this ticket")
                await ctx.channel.send(f"# **{str(ctx.user)} | {str(ctx.user.id)}** has claimed this ticket")
                data['sessions'][data['sessions'].index(item)]['claimedby'] = ctx.user.id
                with open('cogs/modmemory.json', 'w') as fp:
                    json.dump(data, fp)
                return await ctx.respond("Sucessfully claimed the ticket!", ephemeral=True)
            else:
                pass
        await ctx.respond("You're not in a ticket channel!", ephemeral=True)

    @discord.slash_command(name = "close", description="Close this ticket.")
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def _close(self, ctx: discord.ApplicationContext):
        data = json.load(open('cogs/modmemory.json', 'r'))
        for item in data['sessions']:
            if ctx.channel.name == item['text_channel']:

                user = await self.client.fetch_user(item['user'])
                await user.send(f"# **{str(ctx.user)} | {str(ctx.user.id)}** has closed this ticket.")
                await ctx.channel.send(f"# **{str(ctx.user)} | {str(ctx.user.id)}** has closed this ticket.")
                print(data['sessions'].index(item))
                data['sessions'].remove(item)
                with open('cogs/modmemory.json', 'w') as fp:
                    json.dump(data, fp)
                return await ctx.respond("Sucessfully closed the ticket!", ephemeral=True)
            else:
                pass
        await ctx.respond("You're not in a ticket channel!", ephemeral=True)
    @discord.slash_command(name = "delete", description = "Delete a ticket. IRREVESIBLE!")
    @commands.has_permissions(moderate_members = True)
    @commands.guild_only()
    # @app_commands.describe(sure = "Write `I'm sure` if you really want to.")
    async def _del(self, ctx: discord.ApplicationContext, sure: str):
        if sure != "I'm sure":
            return await ctx.respond("`I'm sure` was not written in the sure argument.")
        data = json.load(open('cogs/modmemory.json', 'r'))
        for item in data['sessions']:
            if ctx.channel.name == item['text_channel']:
                return await ctx.respond("This ticket hasn't been closed (hint run `/close` before this)!", ephemeral=True)
            else:
                pass
        if "mod-" in ctx.channel.name:
            await ctx.channel.delete()
            return await ctx.respond("Success!", ephemeral=True)
        else:
            return await ctx.respond("You're not in a ticket channel!", ephemeral=True)
    class AssistView(discord.ui.View):
        def __init__(self, user: discord.User | discord.Member, client: commands.Bot):
            super().__init__(timeout = None)
            self.user = user
            self.client = client
        @discord.ui.button(label="Open a ticket!", style=discord.ButtonStyle.primary, custom_id="persistent_button")
        async def persistent_button(self, button: discord.ui.Button, interaction: discord.Interaction,):
            data = json.load(open('cogs/modmemory.json', 'r'))
            print(type(button))
            guild: discord.Guild = self.client.get_guild(int(config['setup']['guild']))
            print(guild.roles)
            print(interaction.user)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True),
            }

            for ROLE_ID in config['ticket']['allowed_roles'].split(':'):
                overwrites[guild.get_role(int(ROLE_ID))] = discord.PermissionOverwrite(view_channel=True)

            # print(overwrites)

            id = random.randint(0, 10000)
            modmail_channel = await guild.create_text_channel(f"ticket-{interaction.user.id}-{id}", overwrites=overwrites)
            await modmail_channel.send(f"@here\n {interaction.user} needs assistance. Please respond to them.")

            jsondata = {
                "user": interaction.user.id,
                "text_channel": f"ticket-{interaction.user.id}-{id}",
                "claimedby": ""
            }

            data['sessions'].append(jsondata)
            with open('cogs/modmemory.json', 'w') as fp:
                print(data)
                json.dump(data, fp)

            await interaction.response.send_message("Successfully created the ticket!", ephemeral=True)
    @commands.command(name = "assistance_message")
    async def _assist(self, ctx: discord.ApplicationContext):
        await ctx.send("Please press this button to contact our support team", view=self.AssistView(client=self.client, user=ctx.author))    
def setup(bot: commands.Bot):
    bot.add_view(ticket(bot).AssistView(bot.get_user(0), bot))
    bot.add_cog(ticket(bot))
