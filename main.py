import discord
from discord import message
from discord.colour import Color
from discord.ext import commands
from discord.ext.commands.core import Command, has_permissions
from discord.flags import Intents
from discord.ext.commands import clean_content
import time, traceback, random, subprocess
import asyncio
import datetime
import youtube_dl
import string


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=("!"), intents=intents)


@client.event
async def on_ready():
    print("Bots online")
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"at darksnake's cock."))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Wrong syntax.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have requirements for it.")

# 8ball
@client.command()
async def question(ctx):
    reply = ["Yes",
             "No",
             "It's certain",
             "Without a doubt",
             ":doubt:",
             "Most likely yeah",
             "Most likely no",
             "Absolutely no",
             "Dobtful"
             ]

    await ctx.send(f'{random.choice(reply)}')

# ban/ kick

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, reason=None):
    if member == None or member == ctx.message.author:
        await ctx.send(f"{member.mention} you can't ban yourself idiot.", delete_after=4)
        return
    if reason == None:
        reason = 'Nothing.'
    await member.ban(reason=reason)
    embed2 = discord.Embed(title="User banned:",
                           description=f"{ctx.message.author} banned {member} from the server. Reason: {reason}",
                           color=0x6109af)
    await ctx.send(embed=embed2)
    await member.send(f"You have been banned from **{member.guild.name}**")
    guild = client.get_guild(“your server id”)
    await member.send(f"You got banned on {member.guild.name}")


@client.command()
@has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f"{user} unbanned")


@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, reason=None):
    if member == None or member == ctx.message.author:
        await ctx.send(f"{member.mention} you can't kick urself monkey.", delete_after=4)
        return
    if reason == None:
        reason = 'Nothing.'
    await member.kick(reason=reason)
    embed2 = discord.Embed(title="User Kicked:",
                           description=f"{member} **kicked**. **Reason**: {reason}",
                           color=0x6109af)
    await ctx.send(embed=embed2)
    guild = client.get_guild(“your server id”)
    await member.send(f"You got kicked on {member.guild.name}")


# welcome/leave


@client.event
async def on_member_join(member: discord.Member):
    guild = client.get_guild(“your server id”)
    channel = client.get_channel(“channel id”) #where you want the bot to send msg
    embed = discord.Embed(title=f"{member}", description=f"joined in {member.guild.name}!", color=0x6109af)
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)

   

@client.event
async def on_member_remove(member:discord.Member):
    guild = client.get_guild(“server id”)
    channel = client.get_channel(“your channel id”)
    embed = discord.Embed(title=f"{member}", description=f"left **{member.guild.name}**!", color=0x6109af)
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)

#funcommands
@client.command()
async def gay(ctx, *, user:discord.Member = None):
    member = user or ctx.message.author
    rnd = random.randint(1, 100)
    embed = discord.Embed(title="How gay are you?", color=0x6109af)
    embed.add_field(name=f"Gay test:", value=f"{member.mention} is **{rnd}%** gay")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/856275426934390784/884791063573856298/Gay_Pride_Flag.svg.png")
    await ctx.send(embed=embed)
    guild = client.get_guild()
    
#userinfocommand (for admins)
@client.command()
@commands.has_guild_permissions(administrator=True)
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(title="User Info", color=0x6109af)

    embed.add_field(name='Name: ', value=f'{member.name}#{member.discriminator}', inline=True)
    embed.add_field(name='Nickname:', value=f'{(member.nick if member.nick else "Not setted.")}', inline=True)
    embed.add_field(name="Created at: ", value=f'{member.created_at}', inline=True)
    embed.add_field(name='Roles: ', value=f'{len(member.roles)}', inline=True)
    embed.add_field(name='Booster', value=f'{("Yes." if member.premium_since else "No.")}', inline=True)
    embed.set_thumbnail(url=f'{member.avatar_url}')
    await ctx.send(embed=embed)

#clear command
@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=0):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title="Cleared", description=f"**{amount} messages**", color=0x6109af)
    await ctx.send(embed=embed, delete_after=4)
  
#dicksizecommand
@client.command()
async def size(ctx, *, user:discord.Member = None):
    rnd = random.randint(1, 25)
    member = user or ctx.message.author
    embed1 = discord.Embed(title="What's your dick size?", color=0x6109af)
    embed1.add_field(name=f"Dick Size:",value=f"{member.mention} has got **{rnd} cm**")
    embed1.set_thumbnail(url="https://cdn.discordapp.com/emojis/386910268220768276.png?v=1")
    await ctx.send(embed=embed1)

#bot reply to a message

@client.listen("on_message")
async def stuff(message):
    content = message.content.lower()
    if "" in content:
       await message.channel.send("")
    elif "" in content:
      await message.channel.send("")
    elif "" in content:
        await message.channel.send("")

#giverole/removerole
@client.command()
@has_permissions(manage_roles=True)
async def giverole(ctx, member: discord.Member, role: discord.Role):
 if ctx.author.top_role > member.top_role or ctx.author == ctx.guild.owner:
    await member.add_roles(role)
    embed = discord.Embed(title="Role added", description=f"**Gave {member.mention} ** **{role}**", color=0x6109af)
    await ctx.send(embed=embed)


@client.command()
@has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.top_role > member.top_role or ctx.author == ctx.guild.owner:
        await member.remove_roles(role)
        embed = discord.Embed(title="Role removed", description=f"**Removed {member.mention}** **{role}**", color=0x6109af)
        await ctx.send(embed=embed)


#funcommand (u have to type 2 names with “”) ex: !ship “you” “him”
@client.command()
async def ship(ctx, name1: clean_content, name2: clean_content):
    rnd = random.randint(0, 100)
    if 0 <= rnd <= 10:
        status = "Very low".format(random.choice([
                                                             "Friendzone",
                                                             'Just friends',
                                                             'Friends',
                                                            ]))
    elif 10 <= rnd <= 20:
        status = "Low af :(".format(random.choice([
            "Still in the friendzone",
            "There's not a lot of love there",
            'Friends',
        ]))
    elif 20 <= rnd <= 30:
        status = "Pretty low :/".format(random.choice([    "There's a small sense of romance from one person",
                                                           "There's a small bit of love somewhere",
                                                           "But someone has a bit of love for someone"]))
    elif 30 <= rnd <= 40:
        status = "Fair".format(random.choice([
                                                      "There's a bit of love there!",
                                                      "There is a bit of love there...",
                                                      ]))
    elif 40 <= rnd <= 50:
        status = "Moderate".format(random.choice([
                                                          "it's very one-sided OwO",
                                                          "There's some potential",
                                                          "The love is getting there..."]))
    elif 60 < rnd <= 70:
            status = "Good".format(random.choice([
                                                      "I feel the romance progressing!",
                                                      "There's some love in the air!",
                                                      "I'm starting to feel some love!"]))
    elif 70 < rnd <= 80:
            status = "Great!".format(random.choice(["There is definitely love somewhere!",
                                                       "I can see the love is there! Somewhere...",
                                                       "I definitely can see that love is in the air"]))
    elif 80 < rnd <= 90:
            status = "Over average!".format(random.choice([
                                                              "Definitely it feels the love",
                                                              "It feels the love! There's a sign of a match",
                                                              "It senses a match!",
                                                              ]))
    elif 90 < rnd <= 100:
            status = "True love!".format(random.choice(["It's a match",
                                                          "It's definitely a match",
                                                          "Love is most definitely in the air"]))




    embed = discord.Embed(title="Love test for:",description=f"**{name1}** and **{name2}** :heart_decoration:", color=0x6109af)

    embed.add_field(name="Results:", value=f"**{rnd}%**", inline=True)
    embed.add_field(name="Status:", value=f"**{status}**", inline=True)
    await ctx.send(embed=embed)


#checks user profilepic
@client.command()
async def pfp(ctx, *, user:discord.Member = None):
  member = user or ctx.author
  embed = discord.Embed(title=f"Profile pic of {member}", color=0x6109af)
  embed.set_image(url=member.avatar_url).set_image(url=member.avatar_url)
  await ctx.send(embed=embed)


@client.command()
async def simp(ctx, *, user:discord.Member = None):
    member = user or ctx.author
    rnd = random.randint(0, 100)
    embed = discord.Embed(title="Simp Meter", color=0x6109af)
    embed.add_field(name="Simp level:", value=f"{member.mention} is **{rnd}%** simp")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/882242404185428048/886194884506189854/wa70zfigrsl41.png")
    await ctx.send(embed=embed)


#dead by daylight setup randomizer (not updated)
@client.command(aliases=["perks"])
async def perkroulette(ctx):
    survivor_perks = ('Repressed Alliance', 'Blood Pact', 'Soul Guard', 'Dark Sense', 'Deja Vu', 'Hope', 'Lightweight',
                      'No One Left Behind', "Plunderer's Instinct", 'Premonition', 'Resilience', 'Slippery Meat',
                      'Small Game', 'Spine Chill', 'This is Not Happening', "We'll Make It", 'Open-Handed',
                      'Up the Ante', 'Ace in the Hole', 'Deliverance', 'Autodidact', 'Diversion', 'Flip-Flop',
                      'Buckle Up', 'Mettle of Man', 'Self Care', 'Empathy', 'Botany Knowledge', 'Leader', 'Bond',
                      'Prove Thyself', 'Dead Hard', 'No Mither', "We're Gonna Live Forever", 'Stake Out', 'Tenacity',
                      "Detective's Hunch", 'Technician', 'Lithe', 'Alert', 'Calm Spirit', 'Iron Will', 'Saboteur',
                      'Head On', 'Poised', 'Solidarity', 'Aftercare', 'Breakdown', 'Distortion',
                      'Windows Of Opportunity', 'Boil Over', 'Dance With Me', 'Decisive Strike', 'Sole Survivor',
                      'Object of Obsession', 'Adrenaline', 'Sprint Burst', 'Quick and Quiet', 'Better Together',
                      'Fixated', 'Inner Strength', 'Balanced Landing', 'Urban Evasion', 'Streetwise', 'Pharmacy',
                      'Wake Up!', 'Vigil', 'Lucky Break', 'Any Means Necessary', 'Breakout', 'Babysitter',
                      'Camaraderie', 'Second Wind', 'Borrowed Time', 'Left Behind', 'Unbreakable')
    killerPerks = (
        'Save the Best for Last', 'Dying Light', 'Play With your Food', 'Beast of Prey', 'Hex: Huntress Lullaby',
        'Territorial Imperative', 'Remember Me', 'Blood Warden', 'Fire Up', 'Knock Out', 'Barbecue & Chilli',
        "Franklin's Demise", 'Make Your Choice', "Hangman's Trick", 'Surveillance', 'Bamboozle', 'Coulrophobia',
        'Pop Goes The Weasel', 'Monitor & Abuse', 'Overcharge', 'Overwhelming Presence', 'Shadowborn', 'Bloodhound',
        'Predator', 'Enduring', 'Lightborn'  'Tinkerer', 'Agitation', 'Unnerving Presence', 'Brutal Strength',
        "Nurse's Calling", 'Stridor', 'Thanatophobia', 'Hex: Devour Hope', 'Hex: Ruin', 'Hex: The Third Seal',
        'Spirit Fury', 'Hex: Haunted Ground', 'Rancor', 'Discordance', 'Iron Maiden', 'Mad Grit',
        'Corrupt Intervention',
        'Dark Devotion', 'Infectious Fright', 'Furtive Chase', "I'm All Ears", 'Thrilling Tremors', 'Cruel Limits',
        'Mindbreaker', 'Surge', 'Blood Echo', 'Nemesis', 'Zanshin Tactics', 'Gear Head', "Dead Man's Switch",
        'Hex: Retribution', 'Bitter Murmur', 'Deerstalker', 'Distressing', 'Insidious', 'Iron Grasp',
        'Monstrous Shrine',
        'No One Escapes Death', 'Sloppy Butcher', 'Spies From The Shadows', 'Thrill of the Hunt', 'Unrelenting',
        'Whispers',
        'Forced Penance', 'Trail of Torment', 'Deathbound')

    items = ('Flashlight', 'Sport Flashlight', 'Utility Flashlight', 'Broken Key', 'Dull Key', 'Skeleton Key', 'Map',
             'Rainbow Map', 'Camping Aid Kit', 'First Aid Kit', 'Emergency Med-Kit', 'Ranger Med-Kit', 'Worn-Out Tools',
             'Toolbox', 'Mechanic\'s Toolbox', 'Commodious Toolbox', 'Engineer\'s Toolbox', 'Alex\'s Toolbox')

    killersName = (
    "https://cdn.discordapp.com/attachments/886220095477661696/886220262775873586/K22_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220277409779754/CA_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220295256555530/K23_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220537930612756/MK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220309387165747/SH_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220328391561216/HA_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220353242800168/DO_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220369680277534/BE_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220386218418217/K24_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220402936909834/SD_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220421161156658/FK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220494909624370/KK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220436692680714/K25_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220456057794640/GK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220471002103828/HK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220582356668416/OK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220604989112330/QK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220620906504252/SK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220636538695690/UK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220669170384896/K20_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220681946230824/K21_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220703056142386/HB_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220706826821662/NR_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220737495588925/WR_charSelect_portrait.png"
    )

    survivor_links = (
    "https://cdn.discordapp.com/attachments/886220095477661696/886220211852816494/MS2_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220260292821043/S24_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220292375076894/S25_charSelect_portrait.png, https://cdn.discordapp.com/attachments/886220095477661696/886220314235793438/LS_charSelect_portrait.png, https://cdn.discordapp.com/attachments/886220095477661696/886220328831954944/AV_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220350206144522/FM_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220366484238406/DK_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220384171614238/S27_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220387413811200/S26_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220403477983292/QS_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220419101769738/FS_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220454438776892/GS_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220474097475644/AF_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220491084431420/KS_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220520020914196/BO_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220535388864553/MS_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220600249569300/QM_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220603420471356/QF_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220620910694420/SS_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220635381047326/US_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220651776598026/S22_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220680260104212/S23_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220698383708190/CM_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220699180630036/DF_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220703681114162/JP_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220704847134730/MT_charSelect_portrait.png",
    "https://cdn.discordapp.com/attachments/886220095477661696/886220706466107392/NK_charSelect_portrait.png")

    survsrnd = random.choice(survivor_links)

    Perk1 = random.choice(killerPerks)
    Perk2 = random.choice(killerPerks)
    Perk3 = random.choice(killerPerks)
    Perk4 = random.choice(killerPerks)

    sPerk1 = random.choice(survivor_perks)
    sPerk2 = random.choice(survivor_perks)
    sPerk3 = random.choice(survivor_perks)
    sPerk4 = random.choice(survivor_perks)

    itemrnd = random.choice(items)
    killers = random.choice(killersName)

    embedsurvperks = discord.Embed(title=" Survivors Perks Randomizer", color=0x6109af)
    embedsurvperks.add_field(name="Perk 1:", value=sPerk1)
    embedsurvperks.add_field(name="Perk 2: ", value=sPerk2)
    embedsurvperks.add_field(name="Perk 3:", value=sPerk3)
    embedsurvperks.add_field(name="Perk 4:", value=sPerk4)
    embedsurvperks.add_field(name="Item:", value=itemrnd)
    embedsurvperks.set_thumbnail(url=survsrnd)

    killerembed = discord.Embed(title="Killer Perks Randomizer", color=0x6109af)
    killerembed.add_field(name="Perk 1:", value=Perk1)
    killerembed.add_field(name="Perk 2: ", value=Perk2)
    killerembed.add_field(name="Perk 3:", value=Perk3)
    killerembed.add_field(name="Perk 4:", value=Perk4)
    killerembed.add_field(name="Killer", value="=")
    killerembed.set_thumbnail(url=killers)

    await ctx.send(embed=embedsurvperks)
    await ctx.send(embed=killerembed)

#music command (not working anymore)

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not ctx.message.author:
        await ctx.send("You are not in a vc.")
    else:
        await channel.connect()


@client.command()
async def leave(ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_connected():
        await vc.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@client.command()
async def play(ctx, *, url):
    FFMPEG_OPTIONS = {"before_options": '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 ', 'options': "-vn"}
    ydl_options = {"format":"bestaudio"}
    voicechat = ctx.voice_client

    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url, **ydl_options)
        voicechat.play(source)

@client.command()
async def pause(ctx):
    ctx.voice_client.pause()
    await ctx.send("Paused!")

@client.command()
async def resume(ctx):
    ctx.voice_client.resume()
    await ctx.send("Resumed!")

#antiscam nitro gift
@client.listen("on_message")
async def scam(message):
    content = message.content.lower()
    nitro = "nitro"
    if "http" in content or "steam" in content:
        if nitro in content:
           await message.delete()
           await message.channel.send(f"Stop sending scam links retard. {message.author.mention}", delete_after=4)
           channel = client.get_channel()
           embed = discord.Embed(name="Nitro Scam Link:", description=f"{message.author} sent scam link in {message.channel.mention}\n Message Content: `{message.content}`", color=0x6109af)
           await channel.send(embed=embed)

#a password generator
@client.command()
async def passgen(ctx, length = 10):
    numbers = "1234567890"
    everything = string.ascii_uppercase + string.ascii_lowercase + string.punctuation + numbers
    psw = (random.choice(everything) for i in range(length))
    author = ctx.message.author.name
    await ctx.send("```I sent you a random password in your private messages```")
    await ctx.author.send(f"".join(psw))


@client.command()
async def move(ctx, member: discord.Member, chan):
    member_id = member.id
    channel = discord.utils.get(ctx.guild.channels, name=chan)
    await member.edit(voice_channel=channel)

client.run("your token")
