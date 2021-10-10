import discord
import asyncio
import os
import requests
import string
from colorama import Fore, Back, Style

token = 'YOUR TOKEN HERE'

prefix = '!'
intents = discord.Intents.default()
client = commands.Bot(
    description='Find Invite Links From Server',
    self_bot=True,
    intents=intents
)
totalvalid = 0
totalinvalid = 0


async def scrape():
    print(Fore.GREEN + 'Started Scraping...')
    global totalvalid
    global totalinvalid
    messages = []
    fmessages = []
    gmessages = []
    invites = []
    possible = []
    allowed = 'abcdefghijklmnopqrstuvwxyz1234567890:/'
    extra = '`~*'
    check = 'discord.gg/'
    try:
        channel_id = int(input('Channel ID: '))
        channel = client.get_channel(channel_id)
        if channel == None:
            print(Fore.RED + 'Error: Invalid Channel')
    except Exception as e:
        print(Fore.RED + 'Error' + e)
    async for message in channel.history(limit=5000):
        messages.append(message.content)
    for message in messages:
        fmessages.append(message.split())
    for item in fmessages:
        for content in item:
            gmessages.append(content.split('\n'))
    for message in fmessages:
        for amessage in message:
            if amessage.find('discord.gg/') != -1:
                for element in amessage:
                    if element.lower() not in allowed:
                        amessage.replace(element, '')
                index = amessage.find('discord.gg/')
                short = amessage[index:]
                if len(short) > 21 or len(short) < 18:
                    possible.append(short)
                else:
                    invites.append(amessage[index:])
    f = open('scraped.txt', 'w')
    for item in invites:
        f.write('https://' + item + '\n')
    f.close()
    l = open('failed.txt', 'w')
    for item in possible:
        l.write('https://' + item + '\n')
    print(Fore.GREEN + 'Finished Scraping')
    return True


async def check():
    print(Fore.GREEN + 'Started Checking...')
    global totalvalid
    global totalinvalid
    g = open('scraped.txt', 'r')
    h = open('valid.txt', 'w')
    i = open('invalid.txt', 'w')
    for line in g:
        invite = line.strip()
        r = requests.get(invite).text
        times = r.count('discord.com/invite/')
        if times == 2:
            h.write(invite + '\n')
            totalvalid += 1
        else:
            i.write(invite + '\n')
            totalinvalid += 1
    g.close()
    h.close()
    i.close()
    print(Fore.GREEN + 'Finished Checking')


@ client.event
async def on_ready():
    global totalvalid
    global totalinvalid
    os.system('cls')
    print(Fore.GREEN + 'Starting Program...')
    await scrape()
    await check()
    print(Fore.GREEN + f'Total Valid Invites: {totalvalid}')
    print(Fore.RED + f'Total Invalid Invites: {totalinvalid}')
    os._exit(1)

client.run(token, bot=False)
