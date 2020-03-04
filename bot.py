import discord
import asyncio
from discord.ext import commands
import random
from random import randint
from discord.utils import get
import youtube_dl
import os

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

# Words
hello_words = ['hello', 'hi', 'привет', 'Привет', 'ку', 'Ку', 'Дарова', 'дарова']
answer_words = ['узнать информацию о сервере', 'какая информация', 'команды', 'команды сервера', 'что здесь делать?','что здесь делать']
goodbye_words = ['пока', 'бб', 'bb', 'bye', 'до встречи', 'пока всем', 'пока бот']
comm_words = ['как дела?', 'как дела', 'как ты?', 'как ты']

@client.event

async def on_ready():
	print('Бот подключен')

	await client.change_presence(status = discord.Status.online, activity = discord.Game('собирание гаек'))

@client.event

async def on_member_join( member ):
	channel = client.get_channel( 684850433809973250 )

	role = discord.utils.get( member.guild.roles, id = 684811591035781141 )

	await member.add_roles ( role )
	await channel.send( embed = discord.Embed(description = f'Пользователь ``{member.name}``, присоединился к нам!', color = discord.Color.blue()))

# Сказать от имени бота
@client.command()
@commands.has_permissions( administrator = True)
async def say(ctx, *, arg):

    await ctx.message.delete()
    await ctx.send(f'{arg}')

# Очистить
@client.command()
@commands.has_permissions( administrator = True)
async def clear(ctx,amount : int):
    
    channel_log = client.get_channel(684856831322882089) #Айди канала логов

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:white_check_mark: Удалено {amount} сообщений.**', color=0x0c0c0c))
    await channel_log.send(embed = discord.Embed(description = f'**:wastebasket:  Удалено {amount} сообщений.**', color=0x0c0c0c))

# Кик
@client.command()
@commands.has_permissions( administrator = True) 
async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = client.get_channel(684856831322882089) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c))
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0x0c0c0c)) 

# Бан    
@client.command()
@commands.has_permissions( administrator = True) 
async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = client.get_channel(684856831322882089) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0x0c0c0c))

# Разговоры
@client.event

async def on_message(message):
	await client.process_commands(message)

	msg = message.content.lower()

	if msg in hello_words:
		await message.channel.send('Привет дорогой друг!')

	if msg in answer_words:
		await message.channel.send('Пропишите в чат команду `!help`, и все узнаете.')

	if msg in goodbye_words:
		await message.channel.send('Пока, спасибо что общался с нами.')

	if msg in comm_words:
		await message.channel.send('У меня хорошо! Разработчик вкрутил мне новые батарейки, так что я чувствую себя вполне хорошо! А у тебя как?')


# Мут
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)

async def mute(ctx, user_id, userName: discord.User):
    if ctx.message.author.server_permissions.administrator:

        user = ctx.message.author
        role = discord.utils.get(user.server.roles, name ='muted')

        await client.add_roles(user, role)

# Репорт
@client.command()
async def report(ctx,member: discord.Member = None,*,arg = None):

    channel = client.get_channel(684861344612352030) #Айди канала жалоб

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif arg is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        await ctx.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}**', color=0x0c0c0c))
        await channel.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}\n:bust_in_silhouette: Автор жалобы: {ctx.author.mention}**', color=0x0c0c0c))

# Пинг
@client.command() 
async def ping(ctx):
    await ctx.send(embed = discord.Embed(description = f'**:gear: Ваш пинг:** { randint( 15, 100 ) }', color=0x0c0c0c))

# Калькулятор
@client.command()
async def math( ctx, a : int, arg, b : int ):

    try:

        if arg == '+':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a + b }', color=0x0c0c0c))  

        elif arg == '-':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a - b }', color=0x0c0c0c))  

        elif arg == '/':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a / b }', color=0x0c0c0c))

        elif arg == '*':
            await ctx.send(embed = discord.Embed(description = f'**:bookmark_tabs: Результат:** { a * b }', color=0x0c0c0c))      

    except:
        
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: Произошла ошибка.**', color=0x0c0c0c)) 

# Орел и Решка
@client.command()
async def coin( ctx ):
    coins = [ 'орел', 'решка' ]
    coins_r = random.choice( coins )
    coin_win = 'орел'

    if coins_r == coin_win:
        await ctx.send(embed = discord.Embed(description= f''':tada: { ctx.message.author.name }, выиграл! 
            Тебе повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

    if coins_r != coin_win:
        await ctx.send(embed = discord.Embed(description= f''':thumbsdown:  { ctx.message.author.name }, проиграл! 
            Тебе не повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c)) 

# Войти в канал
@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
# Выйти из канала
@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()

# Музыка
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')

    try:
        if song_there:
            os.remove('song.mp3')
            print('[log] Старый файл удален')
    except PermissionError:
        print('[log] Не удалось удалить файл')

    await ctx.send('Пожалуйста ожидайте')

    voice = get(client.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('[log] Загружаю музыку...')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'[log] Переименовываю файл: {file}')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after = lambda e: print(f'[log] {name}, музыка закончила свое проигрывание'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас проигрывается музыка: {song_name[0]}')

# Connect
token = open('token.txt', 'r').readline()

client.run(token)