import discord
import random
from functools import reduce
import requests
import asyncio

from .lists import emojis, emojis_ru, emojis_thumbnail
from .config import url_one_in_50_last_games_info_hero, quiz_channel_id

last_msg_quiz_id = ''
reactions_for_quiz = []

def get_last_msg_quiz_id():
    global last_msg_quiz_id
    return last_msg_quiz_id

async def run_quiz(ctx):
    while True:
        # await asyncio.sleep(3)
        payload = {}
        headers = {}

        response = requests.request("GET", url_one_in_50_last_games_info_hero, headers=headers, data=payload)

        responseSerializeData = response.json()
        short_hero_info = responseSerializeData.get('DATA')
        _id = short_hero_info['_id']
        
        message = await ctx.send(embed=first_quiz_post(short_hero_info))

        global last_msg_quiz_id
        last_msg_quiz_id = message.id

        global reactions_for_quiz
        reactions_for_quiz = getQuizReactionList(short_hero_info, emojis)

        for random_reaction in range(len(reactions_for_quiz)):
            await message.add_reaction(str(reactions_for_quiz[random_reaction]))

        await asyncio.sleep(15)

        quiz_reactions.clear()
        
        message_info = await ctx.channel.fetch_message(id=last_msg_quiz_id)

        new_embed=discord.Embed(title="Результаты", description = get_all_lines_config(short_hero_info, message_info, reactions_for_quiz))
        new_embed.set_author(name = "Ссылка на игру", url = f'http://46.101.232.123/game/{_id}', icon_url = "https://cdn.discordapp.com/attachments/946766827562864671/946902974079303700/ASHA-icon.png")
        new_embed.set_thumbnail(url = get_pic_thumbnail(short_hero_info['race']) )
        await ctx.send(embed = new_embed)
        await asyncio.sleep(5)


section = {
  'first': {
    'green': '<:lbr:945195531838300171>',
    'yellow': '<:lb:945614573694775296>',
  },
  'central': {
    'green': '<:cbr:945193692677963847>',
    'yellow': '<:cb:945614298699407400>',
  },
  'end': {
    'green': '<:rbr:945195476658028544>',
    'yellow': '<:rb:945614314969116682>',
  }
}


def get_colored_bar(count, all_reactions_count, row_is_answer):

    empty_field = '<:0b:945193719093678081>'

    bar_list_empty = [empty_field] * 10
    print(bar_list_empty)

    if all_reactions_count <= 0:
        return reduce(lambda x, y: x + y, bar_list_empty)

    percent_fully_bar = count / all_reactions_count * 100

    if row_is_answer == False:
        firstbar = section['first']['yellow']
        centerbar=section['central']['yellow']
        endbar = section['end']['yellow']
    else:
        firstbar = section['first']['green']
        centerbar = section['central']['green']
        endbar = section['end']['green']

    for item in range(len(bar_list_empty)):
        if percent_fully_bar < 10:
            continue
        if item == 0:
            bar_list_empty[item] = firstbar
        elif item == 9:
            bar_list_empty[item] = endbar
        else:
            bar_list_empty[item] = centerbar
        percent_fully_bar -= 10
        
    return reduce(lambda x, y: x + y, bar_list_empty) 


# динамический список, хранит список отображаемых реакций

quiz_reactions = [] 


def first_quiz_post(short_hero_info):

    embed=discord.Embed(title='Угадайте фракцию героя?')
    embed.add_field(name='Атака', value=short_hero_info['attack'], inline=False)
    embed.add_field(name='Защита', value=short_hero_info['defence'], inline=False)
    embed.add_field(name='Колдовство', value=short_hero_info['spell_power'], inline=False)
    embed.add_field(name='Знание', value=short_hero_info['knowledge'], inline=False)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/946766827562864671/948063753373642792/ce56e0c8ae99e697.png')
    return embed

# получение списка из 1 правильной реакции и 3 случайных для отображения 

def getQuizReactionList(short_hero_info, list_reaction):
    emoji_4_list_for_reacions = []
    main_emoji = list_reaction[short_hero_info['race']]

    emoji_4_list_for_reacions.append(main_emoji)
    other_emojis = []
    
    for emoji in list_reaction:
        if list_reaction[emoji] != main_emoji:
            other_emojis.append(list_reaction[emoji])
            
    random_three_emojis = random.sample(other_emojis, 3)
    emoji_4_list_for_reacions = [*random_three_emojis, *emoji_4_list_for_reacions]

    return random.sample(emoji_4_list_for_reacions, 4)

# считаем все реакции на сообщении

def all_reactions_count_on_message(_reactions_for_quiz_info, _reactions_for_quiz):
    all_values = -len(_reactions_for_quiz)
    for reaction in _reactions_for_quiz_info.reactions:
        if str(reaction) in _reactions_for_quiz:
            all_values += (reaction.count)
    return all_values


def get_is_anwer_reaction(_reaction, main_emoji_race):
    main_emoji = emojis[main_emoji_race]
    if str(_reaction) == str(main_emoji):
        reaction_is_answer = True
        
    else:
        reaction_is_answer = False
    return reaction_is_answer 


def get_lines_config(short_hero_info, message_reactions, _reactions_for_quiz, _all_reactions_count):
    lines_config = []
    for reaction in message_reactions:
        if str(reaction) in _reactions_for_quiz:
            reaction_count_without_bot = reaction.count - 1
            reaction_is_answer = get_is_anwer_reaction(reaction, short_hero_info['race'])
            lines_config.append({
                'count_reaction': str(reaction_count_without_bot),
                'reaction': str(reaction),
                'race_ru': emojis_ru[str(reaction)],
                'bar': get_colored_bar(reaction_count_without_bot, _all_reactions_count, reaction_is_answer),
            }) 
    return lines_config

def get_pic_thumbnail(answer_race):
    return emojis_thumbnail[emojis[answer_race]]


def get_all_lines_config(short_hero_info, message_info, reactions_for_quiz):

    all_reactions_count = all_reactions_count_on_message(message_info, reactions_for_quiz)

    lines_config = get_lines_config(short_hero_info, message_info.reactions, reactions_for_quiz, all_reactions_count)

    list_lines_config = []
    

    for config in lines_config:
        list_lines_config.append(f"**{config['race_ru']}**\n`{config['count_reaction']}/{all_reactions_count}` {config['bar']} {config['reaction']}")

    return  '\n' + list_lines_config[0] + '\n' + list_lines_config[1] + '\n' +  list_lines_config[2] + '\n' + list_lines_config[3]

async def handle_click_reaction_on_quiz(channel,payload, bot, msg):
    if (channel.id) == quiz_channel_id:
        if payload.message_id == get_last_msg_quiz_id():
            if payload.member != bot.user:
                for item in quiz_reactions:
                    
                    if payload.member == item['user']:
                        reaction_quiz = item['reaction']
                        reaction_user = item['user']
                        await msg.remove_reaction(reaction_quiz, reaction_user)
                        if item in quiz_reactions:
                            quiz_reactions.remove(item)

                quiz_reactions.append({'user': payload.member,'reaction': payload.emoji})