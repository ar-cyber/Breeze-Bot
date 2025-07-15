import discord
from discord.ext import commands
import os
import utils.config
from utils.checks import *
client = commands.Bot(command_prefix=utils.config.config['setup']['command_prefix'], intents=discord.Intents.all(), activity=discord.CustomActivity(name = "Voice your meeters | vb-audio.com", emoji="🎙"), status=discord.Status.dnd)



@client.event
async def on_ready():
    print("[INFO] Installing modules")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            cog_name = f'cogs.{filename[:-3]}'
            try:
                # print(type(cog_name))
                client.load_extension(cog_name)
                print(f'[SUCCESS] Loaded extension {cog_name}')
            except Exception as e:
                print(f'[ERROR] Failed to load {cog_name}: {e}')
    print(client.auto_sync_commands)
    if client.auto_sync_commands:
        print("[INFO] Syncing!")
        await client.sync_commands()
    print(f"[SUCCESS] Online as {client.user.name}")

@client.slash_command(name = "info", description = "View the info of the bot")
async def _info(ctx: discord.ApplicationContext):
    embed = discord.Embed(title = "VB-Audio Bot", description="This bot was custom-made for the VB-Audio Discord server")
    embed.set_thumbnail(url='https://i.imgur.com/GW0cFSw.png')
    embed.add_field(name = "Features", value = """- Working tag system
- Modmail
- Basic moderation commands
- Suggestion system
- Report system
- (Not in this build): GitHub integration
""")
    embed.set_footer(text=f"Created with ♥ by `robin_the_andrew`")
    await ctx.respond(embed=embed)


run_pb_check()

client.run(utils.config.config['setup']['token'])
