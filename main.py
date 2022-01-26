from sys import modules
import discord
from discord.ext import commands
import requests
import random
import re

from modules.sendLadderPair import sendLadderPair
from modules.closeLadderGamesByDiscordTag import closeLadderGamesByDiscordTag
import modules.lists
import modules.config
bot = commands.Bot(command_prefix='.', intents = discord.Intents.all())


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('.info'))
    print(f'Bot is online')


@bot.command(pass_context=True)
async def astrology(ctx):
    await ctx.send(f' {random.choice(modules.lists.astrology_list)}')


@bot.command(pass_context=True)
async def speak(ctx):
    await ctx.send(f' {random.choice(modules.lists.speak_list)}')


@bot.command(pass_context=True)
async def attack(ctx):
    author = ctx.message.author
    s = random.randint(0, 50)
    await ctx.send(f'{author.mention}, твоя атака - {s}')
    if s == 50:
        await ctx.send("У тебя самый большой меч на сервере, %s" % bot.get_emoji(609013410948186162))
    if s == 0:
        await ctx.send('🤏🏽 ')


@bot.event
async def on_message(message):
    if str(message.channel) == 'rating-game-search':
        if modules.config.role_game_search in message.content:
            await message.add_reaction('⚔️')

    if str(message.channel) == 'основной':
        
        # if str(message.author) == 'zub#9433':
        #     if 'додик' in message.content.lower():
        #         random_5 = random.randint(0, 10)
        #         if random_5 == 0:
        #             await message.channel.send('Додик? Молодежный сленг не всегда понятен мне.')
        #         if random_5 == 1:
        #             await message.channel.send('Директор мира, ну прекратите, я вас совсем не узнаю!')
        #     if 'негодяй' in message.content.lower():
        #         random_5 = random.randint(0, 10)
        #         if random_5 == 0:
        #             await message.channel.send('Негодяи и подлецы, всё верно')
        #         if random_5 == 1:
        #             await message.channel.send('Плуты и проныры')
        #     if 'пердеть' in message.content.lower():
        #         random_5 = random.randint(0, 10)
        #         if random_5 == 0:
        #             await message.channel.send('Вы у нас от рук отбились?')
        #         if random_5 == 1:
        #             await message.channel.send('Максимальное осуждение')
        #         if random_5 == 2:
        #             await message.channel.send('Пожилой член партии пердящих в лужу?')
        
        if 'балансер' in message.content.lower():
            random_5 = random.randint(0, 16)
            if random_5 == 0:
                await message.channel.send('Балансеp — это мужчина честной судьбы.')
            if random_5 == 1:
                await message.channel.send('Балансеp — это хорошо. ')
            if random_5 == 2:
                await message.channel.send(
                    'Балансеp — это человек, который всегда говорит то, что думает, и делает то, что говорит.')
            if random_5 == 3:
                await message.channel.send(
                    'Балансеp — это не только тот, кто сам ответственен, но и кто своей ответственностью спасает других, даже ценой собственной репутации.')
    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    channel = discord.utils.get(bot.get_all_channels(), id=payload.channel_id)
    msg = await channel.fetch_message(id=payload.message_id)
    if modules.config.role_game_search in msg.content:
        print(msg.reactions)
        for reaction in msg.reactions:
            if (reaction.emoji == '⚔️' and reaction.me == True and reaction.count > 1 and payload.member != msg.author):
                # if (reaction.emoji == '⚔️' and reaction.me == True and reaction.count > 1 ):
                # if (reaction.emoji == '⚔️' and reaction.me == True and reaction.count == 2):
                print(msg.author)
                print(payload.member)
                author_msg = msg.author
                author_react = payload.member
                message = sendLadderPair([str(author_msg), str(author_react)])
                if message == 'ladder_successfully_created':
                    await channel.send('Рейтинговая встреча успешно создана')
                if message == 'no_data':
                    await channel.send('Отсутствуют необходимые данные в запросе (проверьте свой дискорд-тег)')
                if message == 'not_enough_data':
                    await channel.send('Недостаточно данных в запросе')
                if message == 'too_much_players_with_such_data':
                    await channel.send(
                        'Слишком много игроков с такими данными (скорее-всего есть аккаунты с вашим дискорд-тегом)')
                s = "между {0} и {1}".format(author_msg.mention, author_react.mention)
                await channel.send(s)
                await msg.delete()


@bot.command(pass_context=False)
async def top10(ctx):
    payload = {}
    headers = {}
    response = requests.request("GET", modules.config.url_top_10_users, headers=headers, data=payload)
    responseSerializeData = response.json()
    rating_user_list = responseSerializeData.get('DATA')
    print(rating_user_list)
    num = 0
    s = ''
    user = 0
    for user in rating_user_list:
        num += 1
        s += '{0} {1} {2}\n'.format(num, user.get('nickname'), user.get('rating'))
    await ctx.send(s)


@bot.command(pass_context=False)
async def bottom10(ctx):
    payload = {}
    headers = {}
    response = requests.request("GET", modules.config.url_1000_users, headers=headers, data=payload)
    responseSerializeData = response.json()
    rating_user_list = responseSerializeData.get('DATA')
    # print(rating_user_list[::-1])
    num = 0
    s = ''
    user = 0
    for user in rating_user_list[:-11:-1]:
        num += 1
        s += '{0} {1} {2}\n'.format(num, user.get('nickname'), user.get('rating'))
    await ctx.send(s)


@bot.command(pass_context=False)
async def rank(ctx):
    payload = {}
    headers = {}
    response = requests.request("GET", modules.config.url_1000_users, headers=headers, data=payload)
    responseSerializeData = response.json()
    rating_user_list = responseSerializeData.get('DATA')
    num = 0
    s = ''
    user = 0
    for user in rating_user_list:
        num += 1
        if (str(ctx.message.author)).split('#')[0] == str(user.get('nickname')):
            s += 'nick: **{0}**\nrating: **{1}**\nrank: **{2}**\n'.format(user.get('nickname'), user.get('rating'), num)
    await ctx.send(s)


@bot.command(pass_context=False)
async def prof(ctx):
    payload = {}
    headers = {}
    response = requests.request("GET", modules.config.url_1000_users, headers=headers, data=payload)
    responseSerializeData = response.json()
    rating_user_list = responseSerializeData.get('DATA')
    # print(rating_user_list)
    num = 0
    s = ''
    user = 0
    # print(Roles.keys)
    for user in rating_user_list:
        num += 1
        # if ((str(ctx.message.author)).split('#')[0]).lower() == (str(user.get('nickname'))).lower():
        if (str(ctx.message.author)).lower() == (str(user.get('discord'))).lower():
            s += 'nick: **{0}**\nrating: **{1}**\nrank: **{2}**\n'.format(user.get('nickname'), user.get('rating'), num)
            main_user = user.get('nickname')
            main_rating = user.get('rating')
            main_num = num
    
    user_roles = re.findall(r"(?<=name=').*?(?=')", str(ctx.message.author.roles))
    for role in modules.lists.rating_roles:
        if role in user_roles:
            main_role = role
    embed = discord.Embed(title=main_role, description=f"Рейтинг: {main_rating} Место: {main_num}", color=0xaeba12)
    embed.set_author(name=main_user, icon_url=ctx.author.avatar_url)


    # embed.add_field(name="Достижения", value="Убийца драконов", inline=True)
    # embed.add_field(name="ᅠ", value="Король гномов", inline=True)
    # embed.add_field(name="ᅠ", value="Приятный", inline=True)
    # embed.add_field(name="Турниры", value="Рейтинговый 2020 (3 место) \n Рекрутский 2020 (2 место)", inline=False)
    # самая лучшая раса

    # embed.set_footer(text="text снизу")
    await ctx.send(embed=embed)


# embed.set_author(name = bot.user.name, icon_url = bot.user.avatar_url)
# # embed.set_footer(name = str(number) )
# # embed.set_image( icon_url = ctx.author.avatar_url )
# # embed.set_image( icon_url = ctx.author.avatar_url )

# @bot.command(pass_context = False)
# async def emoji(ctx):
# 	await ctx.send("Ку, %s" % bot.get_emoji(609013410948186162))
# 	# await ctx.send("Ку, %s" % bot.get_emoji(884696604056125470))


@bot.command(pass_context=True)
async def stop(ctx):
    messages = await ctx.channel.history(limit=200).flatten()
    author_command_stop = str(ctx.message.author)
    for msg in messages:
        # print(msg.author)
        # print(author_command_stop)
        if modules.config.role_game_search in msg.content and author_command_stop == str(msg.author):
            # print(1)
            # if author_command_stop == msg.author:
            # if str(msg.author) == author_command_stop:
            await msg.delete()

    message = closeLadderGamesByDiscordTag(str(ctx.author))

    if message == 'ladder_successfully_close':
        await ctx.send('Активная встреча успешно закрыта')
    if message == 'player_has_no_open_ladder':
        await ctx.send('У данного игрока отсутствуют открытые встречи')
    if message == 'player_not_found':
        await ctx.send('Игрок с таким тегом дискорда отсутствует')
    if message == 'no_data':
        await ctx.send(' Отсутствует информация об игроке')


@bot.command(pass_context=False)
async def info(ctx):
    await ctx.send(modules.lists.info_message)


@bot.command(pass_context=False)
async def Gi(ctx):
    if str(ctx.author) == 'Persona#4190':
        await ctx.send(modules.lists.Giovanni_message)


bot.run(modules.config.token)