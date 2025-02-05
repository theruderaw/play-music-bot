import discord
from discord.ext import commands
import os
import requests
from random import randrange
import traceback
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Add this to your .env file

maps = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

def times(time):
     date,time = time.split(' ')
     dates = date.split('-')[::-1]
     res = [str(int(dates[0])),maps[int(dates[1])],dates[2]]

     return ' '.join(res)+' '+time

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.command()
async def w(ctx, *, city: str):
        # Get weather data
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        data = response.json()
        times(data['location']['localtime'])
        if response.status_code == 200:
            res = f'''{ctx.author.mention} Displaying weather for {data['location']['name']}, {data['location']['country']} at {times(data['location']['localtime'])}- Temperature = {data['current']['temp_c']}\u00B0C'''
            await ctx.send(res)

@bot.command()
async def random(ctx, *, params:str):
    if ' ' in params:
        min,max = map(int,params.split(' '))
    else:
        min = 1
        max = int(params)
    choice = randrange(min,max+1)
    res = f'''{ctx.author.mention} your choice between {min} and {max} is {choice}'''
    await ctx.send(res)

bot.run(DISCORD_TOKEN)