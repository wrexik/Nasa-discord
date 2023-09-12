from pyautogui import sleep
import os
import aiohttp
import requests
import configparser
import time
import json
import random

import asyncio
from gtts import gTTS

from datetime import datetime
import discord
from discord.ext.commands import CommandNotFound
from discord.ext.commands import Bot
from discord.ext import commands

from traitlets import default

#Made with Love - Wrexik
intents = discord.Intents.all()
client = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix="!",intents=intents)
config = configparser.ConfigParser()

bot.remove_command('help')

#checks if config file exists
if not os.path.exists("config.ini"):
    print("Creating config file...")

    config['Options'] = {'bot_name': 'Sitara',
                     'bot_pfp': 'https://i.postimg.cc/63vzgSPN/round-sitara.png',
                     'default_activity': 'Your Mother',
                     'twitch_username': 'notwrexik'}
    
    config['Setup'] = {'bot_secret': 'YOUR SECRET',
                       'bot_prefix':'!',
                       'nasa_api_key': 'YOUR NASA API KEY'}
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Done saved as {}".format("config.ini"))
    print("Customize the config to your options and restart the program")
    print("Get the NASA API key on: https://api.nasa.gov/")
    print("exiting in 5s")
    time.sleep(5)
    exit()

else: 
    config.read('config.ini')

    bot_name = config['Options']['bot_name']
    bot_pfp = config['Options']['bot_pfp']
    default_activity = config['Options']['default_activity']
    twitch_username = config['Options']['twitch_username']

    bot_secret = config['Setup']['bot_secret']
    bot_prefix = config["Setup"]['bot_prefix']
    nasakey = config['Setup']['nasa_api_key']

    twitch_link = "https://www.twitch.tv/" + twitch_username

apikey = "&api_key=" + nasakey

intents = discord.Intents.default()
client = commands.Bot(command_prefix=bot_prefix, intents=intents)

@bot.event
async def on_ready():
    #connect to dc
    print(f'{bot.user} je tady ❤️')
    await bot.change_presence(activity=discord.Streaming(name=default_activity, url= twitch_link))

@client.event
async def on_error():
    print(f'{bot.user} Had an error')

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, CommandNotFound):
    if str(error)[9:][:1] == bot_secret['bot_prefix']:
      pass
    else:
      return await ctx.send(str(error))

###
###end of setup
###

@bot.command()
async def cur(ctx, arg1, camera):
    async with aiohttp.ClientSession() as session:
        
        sol = "?sol=" + str(arg1)

        posiblecams = ["FHAZ", "fhaz", "RHAZ", "rhaz", "MAST", "mast", "CHEMCAM", "chemcam", "MAHLI", "mahli", "MARDI", "mardi", "NAVCAM", "navcam"]
        cam = None
        for name in posiblecams:     
            if name == str(camera):
                cam = "&camera="+ str(camera)
                break
        if cam is None:
            await ctx.send(f"{ctx.author.mention} Following camera is invalid ```{camera}``` Make you use one of following: ```FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM```")
            return
        
        url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos" +str(sol) +str(cam) +str(apikey)
        
        req = requests.get(url)
        data = json.loads(req.text)
        num_images = len(data["photos"])

        if num_images == 0:
            await ctx.send(f"{ctx.author.mention} Images found 📸: **{num_images}** Try different camera or SOL")
        
        else:
            await ctx.send(f"{ctx.author.mention} Select the number of image. Images found 📸: **{num_images}**")
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            response = await bot.wait_for("message", check=check)
            imgnum = int(response.content) - 1 #the -1 to not confuse users :D

            if imgnum > num_images:
                await ctx.send(f"{ctx.author.mention} Make sure you choose a right number 😊")
                await response.add_reaction('💀')
            else:
                await response.add_reaction('🔍')

                embed = discord.Embed(title="Boba Space™️", color=discord.Color.purple())
                img_src = data["photos"][imgnum]["img_src"]
                #print(img_src)
                img_id = data["photos"][imgnum]["id"]
                #print(img_id)
                img_date_photo = data["photos"][imgnum]
                if img_date_photo:
                    img_date = img_date_photo["earth_date"]
                    embed.set_footer(text=img_date)
                else:
                    print("no date :(")
                #print(img_date)

                print("getting image of id {}".format(img_id))

                embed.set_image(url=img_src)
                embed.set_author(name=  bot_name, icon_url= bot_pfp)
                await ctx.send(embed=embed)
        print(f'{ctx.author} Requested mars pics')

@bot.command()
async def cameras(ctx):
    await ctx.send("Possible cameras: ```FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM```")



@bot.command()
async def apod(ctx):
    async with aiohttp.ClientSession() as session:
        url = f"https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if 'copyright' in data:
                author = True
                copyright = data['copyright']
            else:
                author = False

            explanation = data['explanation']
            img_date = data['date']
            img_url = data['url']

            if author == True: 
                img_title = "APOD - " + str(copyright)
            else:
                img_title = "APOD "

            embed = discord.Embed(title=img_title, url="https://apod.nasa.gov/", color=discord.Color.purple()) # Create embed
            embed.set_image(url=img_url) # Set the embed image to the value of the 'link' key

            if len(explanation) > 1021:
                embed.add_field(name="", value=explanation[:1021] + "...")
            else:
                embed.add_field(name="", value=explanation)
            
            embed.set_footer(text=img_date)
            embed.set_author(name=  bot_name, icon_url= bot_pfp)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention} Failed to retrieve APOD data:", response.text)
            print("Failed to retrieve APOD data:", response.text)
    print(f'{ctx.author} APOD - requested')

@bot.command()
async def iss(ctx, command):
    print(f'{ctx.author} requested iss info')

    if command == "location":
        location = "https://api.wheretheiss.at/v1/satellites/25544"
        response = requests.get(location)
        if response != 200:
            data = response.json()

            lat = data['latitude']
            lon = data['longitude']
            velo = data['velocity']

            google = "https://api.wheretheiss.at/v1/coordinates/" + str(lat) + "," + str(lon)

            response = requests.get(google)
            data = response.json()

            mapurl = data['map_url']
            country = data['country_code']
            timezone = data['timezone_id']

            embed=discord.Embed(title="ISS location", url="https://wheretheiss.at/", color=discord.Color.purple())
            embed.set_thumbnail(url="https://media.tenor.com/UP2aPHHipTgAAAAC/astronaut-spinning.gif")
            embed.add_field(name= "latitude & longitude", value=f"{str(lat)}, {str(lon)}", inline=False)
            embed.add_field(name= "Velocity", value=f"{velo} km/h", inline=True)
            embed.add_field(name= "Timezone & Country code", value=f"{timezone} - {country}", inline=True)
            embed.add_field(name= "Google Maps", value=f"{mapurl}", inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send(f"{ctx.author.mention} Failed to retrieve ISS location")
            print("Failed to retrieve ISS location")

    elif command == "people":
        url = "http://api.open-notify.org/astros.json"
        response = requests.get(url)
        
        if response.status_code != 200:
            await ctx.send("Error: Failed to retrieve data from API.")
            return
        
        data = response.json()
        people = [person for person in data["people"] if person["craft"] == "ISS"]
        count = len(people)
        embed = discord.Embed(title="People currently on the ISS", color=discord.Color.purple())
        embed.add_field(name="Count", value=str(count), inline=False)
        
        for person in people:
            name = person.get("name")
            embed.add_field(name="Name", value=name, inline=True)
            
        await ctx.send(embed=embed)

@bot.command(aliases=['help', 'how'])
async def help_me(ctx):
    embed=discord.Embed(title="Help", description="All comands listed with description!", color=0xdd94ff)
    embed.add_field(name="APOD", value="Usage: !apod (shows astronomy picture of the day)", inline=False)
    embed.add_field(name="CUR", value="Usage: !cur [sol date number] [camera]. Use !cameras to show list of valid cameras or simply use the command to guide you! :)", inline=False)
    embed.add_field(name="ISS", value="""Usage: !iss ["location" or "people"]. One shows velocity and location of ISS on google maps and the other shows people that are currently on the ISS!""", inline=False)
    embed.add_field(name="FUN... yeah made sure to include that", value="Usage: use !fun to enable the features for one time only, for another usage you'll need to use !fun again. More info after triggering the command. :) ", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def fun(ctx):
    await ctx.message.add_reaction('🤝')

    await ctx.channel.send(f"Let's cause chaos {ctx.author}")

    embed=discord.Embed(title="OHH i see someone looking for some fun", description="You are in the right place! Here is a list of the options you have.", color=0xdf99ff)
    embed.add_field(name="MOTD", value="""Use: !motd - To change motd of the bot (Playing "with lego") for example""", inline=False)
    embed.add_field(name="SAY", value="Use: !say - To simply get the bot to say whatever you want, yeah whatever...", inline=False)
    embed.add_field(name="SENDMSG", value="Use: !sendmsg - To send messages to people from the server to their dm's. the command will guide you through.   ", inline=False)
    embed.add_field(name="DECIDE", value="Use: !decide - Type decide [option 1] [option 2], the bot will randomly decide for you.", inline=False)
    embed.add_field(name="TTS", value="Use: !tts - Yeah, this will literary say whatever you want to the channel you are currently connected to!", inline=False)
    embed.set_footer(text="#chaos")
    await ctx.send(embed=embed)


@bot.command()
async def motd(ctx, *args):
    print(f'{ctx.author} requested motd')

    message=""
    for arg in args:
        message = message + " " + arg

    await bot.change_presence(activity= discord.Streaming(name= message, url= twitch_link))
    await ctx.send(f'{ctx.author.mention}'" changed status of the bot to"f'**{message}**!')
        

@bot.command()
async def say(ctx, *args):
    try:
        await ctx.message.delete()
        response = ""
        
        for arg in args:
            response = response + " " + arg
        await ctx.channel.send(response)
    except discord.Forbidden:
        response = ""
        
        for arg in args:
            response = response + " " + arg
        await ctx.channel.send(response)

@bot.command()
async def sendmsg(ctx):
    # Prompt user for recipient and message
    await ctx.send(f"{ctx.author.mention} Enter user ID(s) separated by spaces:")
    recipients_msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    recipients = recipients_msg.content.split()

    await ctx.send(f"{ctx.author.mention} Enter your message 😂:")
    msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    await msg.add_reaction('💀')

    # Send message to each recipient
    for recipient_id in recipients:
        try:
            recipient = await bot.fetch_user(int(recipient_id))
            await recipient.send(msg.content)
            await ctx.send(f"Message sent to {recipient.name}.")
        except:
            await ctx.send(f"😭 Failed to send message to {recipient_id}.")

@bot.command()
async def deside(ctx, arg1, arg2):
    rolled = random.randint(0, 1)
    print(f'{ctx.author} requested deside')
    if rolled == 0:
        await ctx.send(f"Rolled: {arg1}")
    else:
        await ctx.send(f"Rolled: {arg2}")

@bot.command()
async def tts(ctx, *, message: str):
    voice_channel = ctx.author.voice.channel

    try:
        # Join the voice channel
        voice = await voice_channel.connect()

        # Convert the message to text-to-speech audio
        tts = gTTS(text=message, lang='en-gb')
        tts.save("tts.mp3")

        # Play the audio
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("tts.mp3"))
        voice.play(source)

        # Wait for the audio to finish playing
        while voice.is_playing():
            await asyncio.sleep(1)

        # Disconnect from the voice channel
        await voice.disconnect()

        # Remove the temporary audio file
        os.remove("tts.mp3")

    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")

@bot.command()
async def spider(ctx):
        try:
            await ctx.message.delete()
            await ctx.send("https://cdn.discordapp.com/attachments/524811430923599884/894764730797928478/temp.gif")
        except discord.Forbidden:
            await ctx.send("https://cdn.discordapp.com/attachments/524811430923599884/894764730797928478/temp.gif")

#errors 💀
@motd.error
async def mars_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} No motd set")

@cur.error
async def mars_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} make sure you write **!cur [sol date] [camera]**")

@iss.error
async def mars_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{ctx.author.mention} make sure you write **!iss location / people**")

bot.run(bot_secret)