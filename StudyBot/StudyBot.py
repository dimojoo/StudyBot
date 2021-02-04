# Some of the starter code was taken from https://realpython.com/how-to-make-a-discord-bot-python/
import time
from selenium import webdriver
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands


#Web Driver Set Up
driver = webdriver.Firefox() #sets the webdriver to use Firefox, can be swapped with other options (Chrome)



load_dotenv() #loads .env file that holds the bot token
TOKEN = os.getenv('DISCORD_TOKEN')  # These 2 functions search the .env file for the bot token and the name of the guild
GUILD = os.getenv('DISCORD_GUILD')

prefix = '!'
bot = commands.Bot(command_prefix=prefix, case_insensitive=True) #sets the default bot command prefix to !


@bot.event
async def on_ready():
    print(f'{bot.user} is connected to discord!') #Puts message in console confirming if bot is successfully online
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n' #says what server the bot joined
        f'{guild.name}(id: {guild.id})')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send( #sends each new member joining the server a message informing them of the commands
        f'{member.name}, Hey you can use !CGG "insert url here" to get a screenshot of that site!')


@bot.command(name='CGG', help='Takes your Site links and returns you a screenshot of the page you want to visit')
async def on_message(ctx, URL=None):
    if ('https://www.google.com/' or 'http://www.google.com/') in URL: #makes sure that the URL is valid and that it only leads to the site you want it to go to
            await ctx.channel.send('Getting the screenshot of  ' + URL + ', please wait a second.')
            driver.get(URL) #enter site
            time.sleep(5) #delay by 5 seconds to give server time to load web page

            # originally had a different way of doing this, but due to it not screenshotting the entire page, beyond the viewable boundaries
            # I found a better solution online that allows the entire page to be captured. Credit: https://stackoverflow.com/a/47785912

            element = driver.find_element_by_tag_name('body')
            element_png = element.screenshot_as_png
            with open("screenshot.png", "wb") as file:
                file.write(element_png)
            await ctx.channel.send('Here you go, EZPZ')
            await ctx.send(file=discord.File('screenshot.png')) #sends the file in the channel
            os.remove('screenshot.png')
    else:
        await ctx.channel.send('That link does not lead to the correct site or was copied incorrectly, please make sure to copy '
                               'paste the link exactly as it is in your searchbar')


bot.run(TOKEN)


test