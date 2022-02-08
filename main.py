from sys import modules
import discord
from discord.ext import commands
import requests
import random
import re
import asyncio #asyncio-3.4.3
from modules.sendLadderPair import sendLadderPair
from modules.closeLadderGamesByDiscordTag import closeLadderGamesByDiscordTag
import modules.lists
import modules.config
import modules.storageForLinks

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

    if str(message.channel) == 'Основной':
         if message.author != bot.user:
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
    num = 0
    s = ''
    user = 0
    for user in rating_user_list:
        num += 1
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

    await ctx.send(embed=embed)


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
    embed1 = discord.Embed(title="Команды рейтинговой игры", description = modules.lists.info_message_1)
    embed2 = discord.Embed(title="Команды хранилища", description=modules.lists.info_message_2)
    embed3 = discord.Embed(title="Развлекательные команды", description=modules.lists.info_message_3)
    embeds = [embed1, embed2, embed3]
    for embed_page_number in range(len(embeds)):    
        embeds[embed_page_number].set_footer(text=f"Раздел: [{embed_page_number+1}/{len(embeds)}]")
    message = await ctx.send(embed=embed1)
    cur_page = 0
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
    
    while True:
        try:

            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "▶️" and cur_page+1 != len(embeds):
                cur_page += 1
                await message.edit(embed = embeds[cur_page])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 0:
                cur_page -= 1
                await message.edit(embed = embeds[cur_page])
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)

        except asyncio.TimeoutError:
            embeds[cur_page].set_footer(text=f"Раздел: [{cur_page+1}/{len(embeds)}] [Время вышло]")
            await message.edit(embed = embeds[cur_page])
            await message.clear_reactions()
            break


@bot.command(pass_context=False)
async def Gi(ctx):
    if str(ctx.author) == 'Persona#4190':
        await ctx.send(modules.lists.Giovanni_message)


@bot.command()
async def mem(ctx, *args):
    

    con = modules.storageForLinks.sql_connection()
    modules.storageForLinks.sql_table(con)
    names_list = modules.storageForLinks.read_sqlite_table(con)
    names_list_only_name = modules.storageForLinks.read_name_sqlite_table(con)
    
    if args[0] == 'add':
       for role in ctx.author.roles:
            if str(role.id) in modules.config.rolelist_moder:
                name_mem = ''
                for name in args[1:-1:]:
                    name_mem += name +' '
                entities = (name_mem.strip(), args[-1], str(ctx.author))
                await ctx.send(modules.storageForLinks.sql_insert(con, entities))
                return

    if args[0] == 'list':
        out = ''
        buf = 0
        numbers_on_list = 4
        meme_record_list = []

        for _ in range((len(names_list)//numbers_on_list+1)-1):
            for one_record in range(numbers_on_list):
                out += names_list[one_record+buf] + '\n'
            meme_record_list.append(out)
            out=''
            buf += numbers_on_list
        for one_record in range(len(names_list)%numbers_on_list):
            out += names_list[one_record+buf] + '\n'
        meme_record_list.append(out)

        embed_list = []
        current_page = 1
        cur_page = 0
        embeds = []

        for one_embed in range(len(meme_record_list)):
            embed_list.append(discord.Embed(title=f"Страница {current_page}", description = meme_record_list[one_embed], color=0xaeba12))
            embed_list[current_page-1].set_footer(text=f"Раздел: [{current_page}/{len(meme_record_list)}]")
            current_page += 1
            embeds.append(embed_list[one_embed])
        message = await ctx.send(embed=embed_list[0])
        
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

# paginator
        while True:
            try:
                
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
                if str(reaction.emoji) == "▶️" and cur_page+1 != len(meme_record_list):
                    cur_page += 1
                    await message.edit(embed = embeds[cur_page])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 0:
                    cur_page -= 1
                    await message.edit(embed = embeds[cur_page])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                embeds[cur_page].set_footer(text=f"Раздел: [{cur_page+1}/{len(meme_record_list)}] [Время вышло]")
                await message.edit(embed = embeds[cur_page])
                await message.clear_reactions()
                break


    if args[0] == 'del':
        for role in ctx.author.roles:
            if str(role.id) in modules.config.rolelist_moder:
                name_mem = ''
                for name in args[1:]:
                    name_mem += name +' '
                await ctx.send(modules.storageForLinks.delete_sqlite_record(name_mem.strip()))
                return

    if args[0] == 'play':
        num_mem = ''
        for number in args[1:]:
            num_mem += number +' '
        await ctx.send(modules.storageForLinks.read_single_row(names_list_only_name[int(num_mem)-1]))


bot.run(modules.config.token)