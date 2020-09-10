# A2B Dispatch v1
# Made by Jan Imhof

import json
import discord
import geopy.distance
import requests
import math
import xml.etree.ElementTree as ET

from discord.ext import commands

# Opening the config.json file that stores the Discord Token, AVWX auth header and FSEconomy Datafeed
with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['token']  # Psst keep secret
client = commands.Bot(command_prefix='!')  # Meaning that all commands must start with a ! so for instance !quote
client.remove_command('help')  # removes the custom help command


def get_station(loc):
    """
    Function that returns json data from a certain station (Airport) using AVWX
    :param loc: a four letter ICAO code e.g. KJFK
    :return: json data received from AVWX
    """
    url = 'https://avwx.rest/api/station/' + loc + '?format=json'
    headers = {'Authorization': config['authHeader']}
    r = requests.request("GET", url, headers=headers)
    data = r.json()
    return data


def get_distance(loc1, loc2):
    """
    Function that returns json data from a certain station (Airport) using AVWX
    :param loc1: a four letter ICAO code e.g. KJFK
    :param loc2: a four letter ICAO code e.g. KJFK
    :return: distance (float) between loc1 and loc2 in nautical miles
    """
    station1 = get_station(loc1)
    station2 = get_station(loc2)
    coords_1 = (station1['latitude'], station1['longitude'])
    coords_2 = (station2['latitude'], station2['longitude'])
    return round(geopy.distance.geodesic(coords_1, coords_2).nm)


def get_number_of_stops(type, distance):
    url = "https://server.fseconomy.net/data?userkey=" + config[
        'datafeed'] + "&format=xml&query=aircraft&search=configs"
    response = requests.request("GET", url)
    root = ET.fromstring(response.content)
    for plane in root:
        for entry in plane:
            if type == entry.text:
                cruise_speed = float(plane[3].text)
                gph = float(plane[4].text)
                fuel_capacity = float(plane[9].text) + float(plane[10].text) + float(plane[11].text) + float(
                    plane[12].text) + float(plane[13].text) + float(plane[14].text) + float(plane[15].text) + float(
                    plane[16].text) + float(plane[17].text) + float(plane[18].text) + float(plane[19].text)
                max_flight_time = fuel_capacity / gph  # Maximum flight time the plane can achieve according to it's
                # maximum fuel capacity
                max_range = cruise_speed * max_flight_time
                if max_range > distance:
                    return "(direct)"
                if distance / max_range < 2:
                    return "(1 stop)"
                return "(" + str(math.ceil(distance / max_range)) + " stops)"


def get_plane_info(registration):
    url = 'https://server.fseconomy.net/data?userkey=' + config[
        'datafeed'] + '&format=xml&query=aircraft&search=registration&aircraftreg=' + registration
    response = requests.request("GET", url)
    root = ET.fromstring(response.content)
    return [root[0][1].text, root[0][4].text, root[0][9].text]


@client.command()
async def help(ctx):
    help_embed = discord.Embed(
        title="A2B Bot",
        description='See the commands list below',
        color=discord.Colour.red()
    )
    # Setting all the Values
    help_embed.add_field(name='Request a quote using: \n!quote registration origin destination ',
                         value='!estimate N828SY KJFK KBOS', inline=False)
    await ctx.send(embed=help_embed)


@client.command()
async def estimate(ctx, registration, destination):
    user = ctx.author
    plane = get_plane_info(registration)
    type = plane[0]
    origin = plane[1]
    equipment = plane[2]
    distance = get_distance(origin, destination)
    number_of_stops = get_number_of_stops(type, distance)
    price = distance * 10
    if equipment == 'VFR':
        price += distance * 2
    if distance < 1000:
        days = 3
    else:
        days = 7
    quote_embed = discord.Embed(
        title="A2B Bot",
        description='See your estimate below',
        color=discord.Colour.red()
    )
    quote_embed.add_field(name="Customer:", value=user.mention, inline=False)
    quote_embed.add_field(name="Distance:", value=str(distance) + "nm " + str(number_of_stops), inline=False)
    quote_embed.add_field(name="Cost:", value="v$" + str(price) + " + expenses", inline=False)
    quote_embed.add_field(name="Delivery within:", value=str(days) + " days", inline=False)
    quote_embed.add_field(name="Next steps:", value="If you want to get a mo"
                                                    " tool using straight line distance. If you wish to accept"
                                                    " the quote please reply with your acceptance.", inline=False)
    await ctx.send(embed=quote_embed)


client.run(TOKEN)
