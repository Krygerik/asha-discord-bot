import discord
from discord.ext import commands
import requests
import random
import re
from modules.sendLadderPair import sendLadderPair
from modules.closeLadderGamesByDiscordTag import closeLadderGamesByDiscordTag

url_top_10_users = "http://46.101.232.123:3002/api/auth/get-player-rating-list?limit=10"

url_1000_users = "http://46.101.232.123:3002/api/auth/get-player-rating-list?limit=1000"

# orig
token = 'ODA4NjE5MjczMjgyNzgxMjA0.YCJLYg.7Wys8ydGWXwvb_Eq5C8Icl1w1vQ'

# test
# token = 'ODgzOTg3MTUwMTIxNTk4OTg2.YTR7MA.Mg7iY1P6Ac_V-GJzFGJxC_Pilt0'

bot = commands.Bot(command_prefix='.', intents = discord.Intents.all())

headers = \
    {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'accept': '*/*'}

# global variables

role_game_search = '883320181588389948'
# orig

# role_game_search = '874979428038500432'
# test


rating_roles = [
    'Рекрут',
    'Воин',
    'Рыцарь',
    'Воевода',
    'Ветеран',
    'Герой',
    'Легенда',
    'Властелин',
    'Титан',
    'Дракон',
]


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('.info'))
    print(f'Bot is online')


@bot.command(pass_context=True)
async def astrology(ctx):
    astrology_list = [
        f"Сегодня у тебя будет {random.randint(0, 25)} атаки",
        "Сегодня можно и в раш сыграть",
        f"Сегодня у тебя будет {random.randint(12, 50)} колдовства",
        f"У тебя будет {random.randint(2, 50)} боевых статов",
        f"У тебя будет {random.randint(2, 50)} магических статов",
        "Сегодня стоит стать воином света и изгнать демонов со святой земли",
        "Сегодня, хотя бы на час, стоит изгнать из себя быдло и стать настоящим магом — повелителем всех стихий",
        "Маны много не бывает, бой будет затяжным",
        "Оппонент может выйти на кольце, будьте осторожны с боевыми машинами",
        "В тебе сегодня живёт маленький эксперементатор, можно выводить необычные билды",
        "Пруха и Мораль — наши лучшие друзья",
        "Удача и мораль не подвластны тебе сегодня",
        "Сегодня ничего значительного не произойдёт",
        "Чумовая катка будет сегодня!",
        "Ментор сегодня не друг вам",
        "Сегодня билд ляжет, как по маслу",
        "Сегодня много интересных камней на поле!",
        "Сегодня поляны чисты",
        "Вложиться в защиту — хорошая идея, тут и к гадалке не ходи",
        "Сегодня стоит защититься от магии",
        "Сильный оппонент может многому тебя научить",
        "Сегодня нужно врываться внутрь",
        "Используйте клич 'Вперёд мои войны', покрутитесь на стуле 3 раза, похлопайте в ладоши и найдите Меч Мощи под подушкой",
        "Используйте клич 'Вперёд мои войны' и врывайтесь внутрь, победа ждёт где-то между вторым и третьим АТБ",
        "Ставь лайк и получишь Сапоги магической защиты или Меч мощи под подушкой, предложение ограничено",
        "Не веришь? Проверено! Напиши в чат оппоненту 'Удачи и хорошей игры', выпей два глотка воды, хлопни 5 раз в ладоши, пикни эльфа - и в лавке тебя будет ждать 10 напа и 2 прухи",
        "Скупая всю лавку — помните, вы будете одеты, как чёрт",
        "Вы самый сильный, вы самый лучший — так вам сказала ваша мама, давайте не будем сегодня её расстраивать",
        "Пруха всегда уходит от Зуба, сегодня она уходит к вам",
        "Сегодня тачки эльфу упадут",
        "Сегодня можно поиграть против стримеров...только...это...стрим то закрой",
        "Парнишка, моральку качай :hohotun: и побежали",
        "Ууу, с такими билдами тебе в школу Зуба надо",
        "Ууу, с такими билдами тебе только Эксель Наргота поможет",
        "Ууу, с такми билдами тебе только на стрим к Ситису нужно, поучишься залетать внутрь",
        f"{random.randint(0, 6)} морали за АТБ. Ооо повезло, повезло)",
        f"Лавка на {random.randint(2, 12)} напа орку. Это всё мне? — Тебе, тебе. — А за что? — Так, просто так… просто так",
        "Перешли это сообщение 3 своим друзья и получишь 12 колдовства в лавке. Проигнорируешь — получишь техлуз на следующем турнире",
        "Томик Хаоса на Некре? Не дождёшься...Ну ладно, но только 1 раз!",
        "Дружище, дарю тебе эту замечательную книгу 'Томик Хаоса' в следующей игре на Орке, мне для тебя ничего не жалко!",
        "Глушка Призыва - Отличная школа, Васян — хороший герой, Подчин - не имба против Орка, а запускать стрим не синим - грех",
        f"{random.randint(0, 7)} удачи за АТБ. Ооо повезло, повезло)",
        "Сегодня по духам лучше не бить — они могут обидеться",
        "Вложиться в атаку — хорошая идея, тут и к гадалке не ходи",
        "Вложиться в знания — хорошая идея, тут и к гадалке не ходи",
        "Вложиться в защиту — хорошая идея, тут и к гадалке не ходи",
        "Вложиться в колдовство — хорошая идея, тут и к гадалке не ходи",
        "Я слышал, что синий имеет преимущество при черке",
        "Я слышал, что красный имеет преимущество при черке",
        "Самые красивые девочки только в РТА",
        "День курицы. Хороший день, если конечно ты не червячок",
        "Побудьте сегодня Тёмным Властелином, вам не будет равных",
        "Самое время поиграть зеркалку, покажите миру на что вы способны!",
        "Асха всех любит, но кто её установил — она любит сильнее",
        "Армагедон — имба",
        "Не имей 100 друзей, а имей сканер и 100 смурфов",
        "Оппонент скоро узнает, что у тебя 3 двухпроцентки",
        "Твой винрейт будет расти как на дрожжах, нужно всего лишь...",
        "Краг не имба? Время доказать обратное!",
        "Васян не имба? Время доказать обратное!",
        "Золтан не имба? Время доказать обратное!",
        "Дираэль не имба? Время доказать обратное!",
        "Зехир не имба? Время доказать обратное!",
        "Вульфстен не имба? Время доказать обратное!",
        "Орландо не имба? Время доказать обратное!",
        "Рутгер не имба? Время доказать обратное!",
        "Не бери Гнома, не понижай винрейт",
        "Не бери Некроманта, не понижай винрейт",
        "Не бери Демона, не понижай винрейт",
        "Не бери Хума, не понижай винрейт",
        "Не бери Эльфа, не понижай винрейт",
        "Не бери Орка, не понижай винрейт",
        "Не бери Лигу, не понижай винрейт",
        "Не бери Мага, не понижай винрейт",
        f"Твой хаос сегодня всего-лишь на {random.randint(0, 50)} сп",
        "Тебя ждёт ФАНТАСТИЧЕСКАЯ мораль",
        "Тебя ждёт ФАНТАСТИЧЕСКАЯ удача",
        "Служи Тьме и тебя ждёт награда",
        "Служи Хаосу и тебя ждёт награда",
        "Служи Призыву и тебя ждёт награда",
        "Служи Свету и тебя ждёт награда",
        "Вода камень точит",
        "По тебе школа кукловодства плачет",
        "Самое время повысить винрейт Гнома!",
        "Самое время повысить винрейт Демона!",
        "Самое время повысить винрейт Некроманта!",
        "Самое время повысить винрейт Хума!",
        "Самое время повысить винрейт Лиги!",
        "Самое время повысить винрейт Орка!",
        "Самое время повысить винрейт Мага!",
        "Самое время повысить винрейт Эльфа!",
        "Сегодня в Асхе раздают рейтинг",
    ]

    await ctx.send(f' {random.choice(astrology_list)}')
    # print (ctx.message.author)
    if str(ctx.message.author) == 'ArhyDevil#4612':
        random_5 = random.randint(0, 5)
        if random_5 == 0:
            await ctx.send(f' Ваня Платов, вам сегодня любой противник подвластен, удачи!')


@bot.command(pass_context=True)
async def speak(ctx):
    speak_list = [
        "Моя милая пустота",
        "Не понимаю вас...живых...",
        "От одного взгляда на тебя, мне дурно",
        "Поживешь подольше — увидишь побольше",
        "Вот скажи мне, игрок, в чём сила? Разве в золоте? Вот и сестра говорит, что в золоте. Вот много у сестры золота и чего? Я вот думаю, что сила в цвете флага, у кого синий, тот и сильнее.",
        "Почему мы сами не можем выбрать себе цвета для ников?",
        "Как ты относишься к такому заработку, как охота на героев?",
        "Твой статус убийцы героев пока находиться на любительском уровне. Мы говорим только потому, чтобы понять, хочешь ли ты перейти на профессиональный.",
        "Месть — это блюдо, которое лучше подавать холодным.",
        "Мне сложно поверить, что горожане это сервера выбрали тебя на какую-либо должность, кроме покойника.",
        "Если мои ответы пугают тебя, перестань говорить со мной.",
        "В данный момент я рассматриваю все возможные варианты стать живым...или хотя бы...не полностью мёртвым.",
        "Тебе тоже некуда бежать! Смерть всё равно быстрее!",
        "Я все люблю цветы. Но розы лучше, чем пионы, пионы лучше лютиков. Но ничего нет лучше хризантем. Лепестки мне напоминают рой клинков. А хризантема есть сущность самой войны.",
        "Я был серьёзен и на завтра строил планы. Но судьба имеет чувство юмора.",
        "Я былого не вспоминаю и будущего не жду. Раз тогда я там нес печаль, то и тут ещё поношу.",
        "Я ещё вернусь",
        # "Андрюха, у нас труп, возможно криминал, по коням!"
        # "Я никогда не поднимал руку на женщину, потому что я сильнее бью с ноги",
        "Ты уже играл на рейтинг?",
        "Хочешь со мной пообщаться? Я подумаю об этом завтра.",
        "Выбирай жизнь. Выбирай будущее. Выбирай семью. Я выбрал могилу.",
        "Ты меня заводишь, детка",
        "Я просто выгляжу как труп, а в душе я бабочка",
        "Спать в гробу — это небылицы. Я сплю в морозильнике. Кстати, пицца с чесноком — это вкусно, только иногда это портит свидание. Если брызнуть на меня святой водой, я промокну. Распятие?! Да, пожалуйста, если вас это заводит. Да, и я определенно не умею превращаться в летучую мышь. Хотя это, конечно, было бы круто.",
        "Совет от профессионала: если лезешь на вампира, которому хреналион лет, советую не драться перочинным ножичком.",
        "У меня очень давно не было смертных друзей. Проблема у них такая — любят умирать.",
        "Кровь — это деньги души, монеты жизни. Она — всего лишь способ продать жизнь. Пить чью-то кровь значит целиком забирать эту жизнь себе.",
        "Не понимаю я кое-что о зомби. Что с ними происходит, когда они не могут поживиться человечинкой? Умирают с голоду? Так они уже мертвые.",
        "Никогда не думали, как вампиры бреются, если они не отражаются в зеркале?",
        "Знаете, как называются вампиры, которые пьют кровь животных? Вегетарианцы.",
        "Я с детства был помешан на вампирской тематике. Мне нравились старые книги про вампиров, я зачитывал их до дыр.",
        "Как выяснилось в ходе эксперимента, деревянный кол в груди смертелен для человека не менее, чем для вампира.",
        "И треснул мир напополам, дымит разлом,\nИ льётся кровь, идёт война добра со злом.\nИ меркнет свет, в углах паук плетёт узор,\nПо тёмным улицам летит «Ночной Дозор»",
        "Мертвые не рассказывают сказки",
        "Не важно, кто прав, важно кто лев!",
        "То, что ты показываешь характер, вовсе не говорит о том, что этот характер у тебя есть.",
        "Чего такой серьезный?",
        "Вот смотрю на тебя и столько мыслей сразу, а слов не хватает…",
        "Вампир с плохим прикусом оставляет на шее след от брекетов.",
        "Не понимаю я этих демонов, навесят знак, потом бегают по полю, как угорелые."
        "Это твоя жизнь, и она становится короче каждую минуту.",
        "Ты хотел изменить свою жизнь, но не мог этого сделать сам. Я — то, кем ты хотел бы быть. Я выгляжу так, как ты мечтаешь выглядеть. Я умён, талантлив и, самое главное, свободен от всего, что сковывает тебя. Меня даже смертельный холод не берёт!",

    ]

    await ctx.send(f' {random.choice(speak_list)}')


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
        if role_game_search in message.content:
            await message.add_reaction('⚔️')
    if str(message.channel) == 'основной':
        if str(message.author) == 'zub#9433':
            if 'додик' in message.content.lower():
                random_5 = random.randint(0, 10)
                if random_5 == 0:
                    await message.channel.send('Додик? Молодежный сленг не всегда понятен мне.')
                if random_5 == 1:
                    await message.channel.send('Директор мира, ну прекратите, я вас совсем не узнаю!')
            if 'негодяй' in message.content.lower():
                random_5 = random.randint(0, 6)
            if random_5 == 0:
                await message.channel.send('Негодяи и подлецы, всё верно')
            if random_5 == 1:
                await message.channel.send('Плуты и проныры')
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
    if role_game_search in msg.content:
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


# CREATE_LADDER_RESPONSE_MESSAGES = {
# 	ERRORS: {
#         // Отсутствуют необходимые данные в запросе
#         NO_DATA: 'no_data',
#         // Недостаточно данных в запросе
#         NOT_ENOUGH_DATA: 'not_enough_data',
#         // Слишком много игроков с такими данными
#         TOO_MUCH_PLAYERS_WITH_SUCH_DATA: 'too_much_players_with_such_data',
#     },
#     SUCCESS: {
#         // Рейтинговая встреча успешно создана
#         LADDER_SUCCESSFULLY_CREATED: 'ladder_successfully_created',
#     }
# };

@bot.command(pass_context=False)
async def top10(ctx):
    payload = {}
    headers = {}
    response = requests.request("GET", url_top_10_users, headers=headers, data=payload)
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
    response = requests.request("GET", url_1000_users, headers=headers, data=payload)
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
    response = requests.request("GET", url_1000_users, headers=headers, data=payload)
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
    response = requests.request("GET", url_1000_users, headers=headers, data=payload)
    responseSerializeData = response.json()
    rating_user_list = responseSerializeData.get('DATA')

    print(rating_user_list)

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
    for role in rating_roles:
        # print(role)

        if role in user_roles:
            main_role = role
    embed = discord.Embed(title=main_role, description=f"Рейтинг: {main_rating} Место: {main_num}", color=0xaeba12)
    embed.set_author(name=main_user, icon_url=ctx.author.avatar_url)

    # https://www.youtube.com/watch?v=rUd2diUWDyI&ab_channel=%D0%98%D0%BB%D1%8C%D1%8F%D0%9C%D0%B8%D1%82%D1%8C%D0%BA%D0%BE
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
        if role_game_search in msg.content and author_command_stop == str(msg.author):
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

info_message = '''
Команды:
1)`@game-search` — испытать судьбу и сыграть на рейтинг, оппонент скоро найдётся, он скрестит мечи прямо под твоим запросом. 
Для подсчёта рейтинга АСХА должна быть включена. Можно играть несколько игр за раз!
2)`.stop` — Завершает текущую рейтинговую встречу. Если начать встречу с новым оппонентом, то предыдущая рейтинговая втреча будет автоматически завершена. 
3)`.top10` — Топ 10 игроков Асхи
4)`.bottom10` — Топ 10 игроков Асхи, только наоборот 
5)`.prof` — посмотреть свой профиль  
6)`.astrology` — воспользоваться услугами лучшего Астролога Асхана.
7)`.attack` — если хочешь измерить свой боевой потенциал.
8)`.speak` — поговорить с Джованни, сейчас он плохо себя чувствует, так как немного мёртв.) '''


@bot.command(pass_context=False)
async def info(ctx):
    await ctx.send(info_message)


Giovanni_message = '''
Высший вампир Джованни нуждается в тёмной энергии для воскрешения из мёртвых. Только Асха может помочь провести ритуал. Бросай вызов любому игроку в смертельной битве и сражайся за рейтинг и место в общем ладдере. 

Пиши @game-search в этом чате, твоему оппоненту нужно только скрестить мечи под этим сообщением и игра будет зарегистрирована.
Дальше — играй через гр или радмин (всё как обычно). 
.stop — завершает текущую рейтинговую встречу. Если начать встречу с новым оппонентом, то предыдущая рейтинговая втреча будет автоматически завершена. 
Для игры нужна включённая Асха. В Асхе должен быть указан ваш дискорд-тег. (Указывается при регистрации на сайте)

Отследить свой прогресс можно по ссылке:
http://46.101.232.123/rating
'''


@bot.command(pass_context=False)
async def Gi_adm(ctx):
    if str(ctx.author) == 'Persona#4190':
        await ctx.send(Giovanni_message)


bot.run(token)
