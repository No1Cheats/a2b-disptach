# A2B Dispatch v1
# Made by Jan Imhof

import json
import discord
import geopy.distance
import requests
from discord.ext import commands
import xml.etree.ElementTree as ET

# Opening the config.json file that stores the Discord Token and avwx Auth code
with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['token']  # Psst keep secret
client = commands.Bot(command_prefix='!')  # Meaning that all commands must start with a ! so for instance !quote
client.remove_command('help')  # removes the custom help command


def get_station(loc):
    url = 'https://avwx.rest/api/station/' + loc + '?format=json'
    headers = {'Authorization': config['authHeader']}
    r = requests.request("GET", url, headers=headers)
    data = r.json()
    return data


def get_distance(loc1, loc2):
    station1 = get_station(loc1)
    station2 = get_station(loc2)
    coords_1 = (station1['latitude'], station1['longitude'])
    coords_2 = (station2['latitude'], station2['longitude'])
    return round(geopy.distance.geodesic(coords_1, coords_2).nm)


def get_plane_info(registration):
    url = 'https://server.fseconomy.net/data?userkey=' + config[
        'datafeed'] + '&format=xml&query=aircraft&search=registration&aircraftreg=' + registration
    response = requests.request("GET", url)
    root = ET.fromstring(response.content)
    return [root[0][4].text, root[0][9].text]


@client.command()
async def help(ctx):
    help_embed = discord.Embed(
        title="A2B Bot",
        description='See the commands list below',
        color=discord.Colour.red()
    )
    # Setting all the Values
    help_embed.add_field(name='Request a quote using: \n!quote registration origin destination ',
                         value='!quote N828SY KJFK KBOS', inline=False)
    await ctx.send(embed=help_embed)


@client.command()
async def quote(ctx, registration, destination):
    plane = get_plane_info(registration)
    origin = plane[0]
    equipment = plane[1]
    distance = get_distance(origin, destination)
    price = distance * 10
    if equipment == 'VFR':
        price += distance*2
    quote_embed = discord.Embed(
        title="A2B Bot",
        description='See your quote below',
        color=discord.Colour.red()
    )
    quote_embed.add_field(name="Customer:", value=" customerName", inline=False)
    quote_embed.add_field(name="Distance:", value= str(distance) + "nm", inline=False)
    quote_embed.add_field(name="Cost:", value="v$" + str(price) + " + expenses", inline=False)
    quote_embed.add_field(name="Delivery within:", value="x days", inline=False)
    quote_embed.add_field(name="If you are interested in accepting this quote please reply back with your acceptance. ", value="\u200b", inline=False)
    await ctx.send(embed=quote_embed)


client.run(TOKEN)
