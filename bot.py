import aiohttp
from googleapiclient.discovery import build
from discord.ext import commands
from googletrans import Translator
from youtube_api import YouTubeDataAPI

import requests
import random

import json

config = open('config.json')

config = json.load(config)

bot_name = config['bot_name']
google_api_key = config['google_api_key']
cse_id = config['cse_id']
token = config['discord_bot_token']

try:
    yt = YouTubeDataAPI(google_api_key)
except Exception as e:
    print('Improperly set google api key.')

client = commands.Bot(command_prefix='.', connector=aiohttp.TCPConnector(ssl=False))


# Tell admin when the bot is online
@client.event
async def on_ready():
    print(bot_name + ' online')


# Example of how the bot can reply, to test, type hello
@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.content.lower() == "hello":
        if message.author.name != bot_name:
            await message.channel.send("Hi" + message.author.name)


# Command to reference a youtube video. Example: .yt Charlie bit my finger
@client.command(aliases=['yt'])
async def youtube(ctx, *, search):
    try:
        youtube_search = yt.search(search)

        publish_date = youtube_search[0]['video_publish_date']

        vid = "https://www.youtube.com/watch?v=" + youtube_search[0]['video_id']
        await ctx.send("**Date Published:** " + str(publish_date) + "\n" + str(vid))

    except Exception as e:
        await ctx.send("Could not find a video of this search. Ensure you have set your google API key properly.")


# Command to post a recipe related to a food item. Example: .recipe apple
@client.command(aliases=['recipe'])
async def food(ctx, *, search):
    try:
        params = (
            ('q', search),
            ('p', '1'),
        )
        response = requests.get('http://www.recipepuppy.com/api/', params=params)

        recipe = response.json()
        response_length = len(recipe['results'])
        index = random.randint(0, response_length)
        recipe = recipe['results'][index]['href']
        await ctx.send(recipe)

    except Exception:
        await ctx.send("Could not find a recipe related to that.")


# Command to ask the bot a random question in the form of an 8ball. Example: .8ball will it rain today?
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        "It is decidedly so.",
        "My instincts say without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask me again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "I'm very doubtful."]
    await ctx.send(random.choice(responses))


# Command to post weather information. Example: .w Ottawa
@client.command(aliases=['w'])
async def weather(ctx, *, city):
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=3e6826fb716810018759216195531995&q='
    url = api_address + city
    try:
        json_data = requests.get(url).json()

        if json_data['cod'] == '404':
            await ctx.send(json_data['message'])
        else:
            city_name = json_data['name']
            country = json_data['sys']['country']
            longitude = json_data['coord']['lon']
            latitude = json_data['coord']['lat']
            weather = json_data['weather'][0]['description']
            temperature = round(float(json_data['main']['temp']) - 273.15)
            temperature = round(temperature, 2)
            feels_like = float(json_data['main']['feels_like']) - 273.15
            feels_like = round(feels_like, 2)
            humidity = json_data['main']['humidity']

            await ctx.send(
                'City: ' + str(city_name) + "\nCountry: " + str(country) + "\nCoordinates: " + str(
                    longitude) + ", " + str(latitude) +
                "\nWeather: " + str(weather) + "\n" + "Temperature: " + str(temperature) + "°C\nFeels like: " + str(
                    feels_like) + "°C\nHumidity: " + str(humidity) + "%")

    except Exception:
        await ctx.send("Could not find location or weather information.")


# Command to translate. Example: .tr en J'aime la pizza
@client.command(aliases=['tr'])
async def translate(ctx, *, text):
    try:
        query = text.split(" ")
        translator = Translator()
        if len(query) == 1:
            query = translator.translate(text)
            await ctx.send(query.text)
        else:
            language = query[0]
            query.pop(0)
            query = " ".join(query)
            query = translator.translate(query, dest=language)

            await ctx.send(query.text)

    except Exception:
        await ctx.send(
            "Ensure you have specified a proper language code and ran the command properly."
            "\nLanguage codes: https://cloud.google.com/translate/docs/languages"
            "\nExample: .tr en J'aime la pizza")


# Command to post a google search result. Example: .g What is the structure of water
@client.command(aliases=['g'])
async def google(ctx, *, text):
    try:
        def google_search(search_term, google_api_key, cse_id, **kwargs):
            service = build("customsearch", "v1", developerKey=google_api_key)
            res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
            return res['items']

        results = google_search(
            text, google_api_key, cse_id, num=10)
        link = results[0]["link"]
        await ctx.send(link)

    except Exception:
        await ctx.send('Search failed. Perhaps the api key was not set properly.')


# Command to post an image from google. Example: .image alligator
@client.command(aliases=['image'])
async def picture(ctx, *, text):
    try:
        url = 'https://www.googleapis.com/customsearch/v1?key={}&cx={}&searchType=image&q={}'
        result = requests.get(url.format(google_api_key, cse_id, text)).json()['items']
        link = result[0]['link']
        await ctx.send(link)
    except Exception:
        await ctx.send("Could not find image. Ensure you have properly set a google developer api key.")


# Start bot
client.run(token)
