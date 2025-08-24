import discord #TODO: import the discord module DONE///
from discord.ext import commands
import os
from dotenv import load_dotenv
from messages_template import announcement, permission_granted, permission_denied #TODO: import the variables defined from messages.py DONE///

# This is to load .env file
#load_dotenv("discord.env")

#The file can't be read on my computer even if its in the same directory, so I just put the actual directory as the argument.   
load_dotenv(r'C:\School Files\UP CAPES\SKILLS TEST\pinoy-big-sister-bot\discord_template.env') 
TOKEN = os.getenv("DISCORD_TOKEN")
GENERAL_CHAT_ID = int(os.getenv("GENERAL_CHAT_ID"))
ANNOUCEMENTS_ID = int(os.getenv("ANNOUNCEMENTS_ID"))

#print(TOKEN, CHANNEL_ID)

#For setting up bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# This is executed when you run the program
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        synced = await bot.tree.sync() 
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    
    await show_embed() #TODO: call the show_embed() function DONE///

async def show_embed():
    print("The bot is now ready for use!")
    print("-----------------------------")
    channel_id = GENERAL_CHAT_ID #TODO: place here your channel ID in variable
    channel = bot.get_channel(channel_id)

    if channel:
        embed = discord.Embed(
            title="Bot ni Pinoy Big Sister",
            description=(
                "Welcome sa **Pinoy Big Sister**, mga online housemates! \n" \
                "Sa mga sumusunod na edisyon sa **Pinoy Big Sister**, ito ang gagamiting channel ni Big Sister para sa mga:\n" \
                "(1) **anunsiyo** (/announcements)\n" \
                "(2) **nominsayon** (/nominate)\n" \
                "(3) paghingi ng **permission** (/permission)" # TODO:fill in the description here
            ),
            color=0x5e17eb
        )
        await channel.send(embed=embed)
    else:
        print(f"Channel with ID {channel_id} not found.")


#This is for creating slash commands
@bot.tree.command(name="announcements", description="Tingnan ang anunsiyo ni Big Sister")
async def announcements_quote(interaction: discord.Interaction):
    await interaction.response.send_message(announcement)
    
#TODO: make the commands for /permission and /nominate DONE////
@bot.tree.command(name="permission", description="Humingi ng permiso kay Big Sister")
async def permission_quote(interaction: discord.Interaction, channel: discord.VoiceChannel):
    if len(channel.members) > 0:
        await interaction.response.send_message(permission_denied)
    else:
        await interaction.response.send_message(permission_granted)

#TEST COMMAND
@bot.tree.command(name="list_members", description="TEST")
async def permission_quote(interaction: discord.Interaction, channel: discord.VoiceChannel):
    for name in channel.members:
        await interaction.response.send_message(name)
        

#/nominate is restricted to members of the server
@bot.tree.command(name="nominate", description="Magnominate ng housemate hanggang 3 points")
async def nominate(interaction: discord.Interaction, points: int, nominee: discord.Member):
    if points > 3 or points < 0:
        await interaction.response.send_message(f'Invalid nomination')
    else:
        await interaction.response.send_message(f'Binibigyan mo ng {points} point/s si {nominee.display_name}.')


#TODO: run the token by calling the TOKEN variable DONE///
bot.run(TOKEN)
