import discord
from discord import Member
from server import server

"""
    This file contains helper functions, used in several command definitions for Discord.
"""

# Dictionary containing all command info, processed through kwargs.
commands = {
    # Player cog commands
    'player': {
        'whoareyou': {
            'brief': 'Who am I?',
            'help': 'USAGE: !whoareyou',
        },

        'newb': {
            'brief': 'Send a message in /newb.',
            'help': 'USAGE: !newb [message]',
            'pass_context': True
        }
    },

    # Admin cog commands
    'admin': {
        'a': {
            'brief': 'Send a message in /a.',
            'help': 'USAGE: !a [message]',
            'pass_context': True
        },

        'admins': {
            'brief': 'List all online administrators.',
            'help': 'USAGE: !admins',
            'pass_context': True
        },

        'prison': {
            'brief': 'Prison a player.',
            'help': 'USAGE: !prison [id/name] [time(minutes)] [reason]',
            'pass_context': True
        },

        'getlogs': {
            'brief': 'Gather server logs of a specific phrase.',
            'help': 'USAGE: !getlogs [phrase]',
            'descrption': 'Surround in "" if there are spaces in the phrase',
            'aliases': ['gl'],
            'pass_context': True
        },

        'kick': {
            'brief': 'Kick a player.',
            'help': 'USAGE: !kick [id/name] [reason]',
            'pass_context': True
        },

        'w': {
            'brief': 'Whisper a player.',
            'help': 'USAGE: !w [id/name] [message]',
            'pass_context': True
        }
    },

    # Developer cog commands
    'developer': {
        'dt': {
            'brief': 'Send a message in /dt.',
            'help': 'USAGE: !dt [message]',
            'pass_context': True
        }
    }
}


class Role:
    # Admin roles have rank, id and level keys
    EXECUTIVE = {'rank': 'Executive', 'id': 465896094333927424, 'level': 99999}
    HEAD = {'rank': 'Head', 'id': 465894668094144512, 'level': 1337}
    SENIOR = {'rank': 'Senior', 'id': 465896014130184192, 'level': 4}
    GENERAL = {'rank': 'General', 'id': 465887716354031624, 'level': 3}
    JUNIOR = {'rank': 'Junior', 'id': 465896256972128266, 'level': 2}
    PROBIE = {'rank': 'Probie', 'id': 475211931905556490, 'level': 1}
    ADMINISTRATOR = {'rank': 'Administrator', 'id': 465874213324980244, 'level': 0}
    ADMIN_ROLES = [EXECUTIVE, HEAD, SENIOR, GENERAL, JUNIOR, PROBIE, ADMINISTRATOR]

    HELPER = '465874370904981514'
    DEVELOPER = '465874671733309440'
    TESTER = '465874643337740290'


class Channel:
    # IDs for every channel in the server

    # HELP/GENERAL
    GENERAL = 465873343518736397

    # ADMINISTRATORS
    DISCUSSION_ADMIN = 466404751857287178
    CHAT = 465873855672745985
    COMMANDS = 465875438321795074

    # HELPERS
    DISCUSSION_HELPER = 466420981813215232
    NEWBIE = 465874164960460800

    # PUBLIC SERVICES
    GOVERNMENT = 466434019278585869
    NEWS_AGENCY = 466434102661349380

    # DEVELOPMENT
    TESTERS = 465874413267582986
    CONFIRMED_BUGS = 471553508118626315
    BUGS = 465879591656095754
    BOT_TODO = 466949031898382356


class Section:
    # Lists of channel IDs for each section
    HELP_GENERAL: list[int] = [Channel.GENERAL]
    ADMINISTRATORS: list[int] = [Channel.DISCUSSION_ADMIN, Channel.CHAT, Channel.COMMANDS]
    HELPERS: list[int] = [Channel.DISCUSSION_HELPER, Channel.NEWBIE]
    PUBLIC_SERVICES: list[int] = [Channel.GOVERNMENT, Channel.NEWS_AGENCY]
    DEVELOPMENT: list[int] = [Channel.TESTERS, Channel.CONFIRMED_BUGS, Channel.BUGS, Channel.BOT_TODO]


def get_admin_level(author: Member) -> int:
    """
    Returns the admin level of a Discord member or None if they are not an admin
    """
    level = -1  # level 0 is taken by the base role
    for role in author.roles:
        for admin_role in Role.ADMIN_ROLES:
            if role.id == admin_role['id']:
                if admin_role['level'] > level:
                    level = admin_role['level']
    if level < 0:  # If not an admin
        level = None
    return level


def get_admin_rank(author: Member) -> str:
    """
    Returns the rank name of a Discord member or None if they are not an admin
    """
    rank = None
    level = 0
    for role in author.roles:
        for admin_role in Role.ADMIN_ROLES:
            if role.id == admin_role['id']:
                if admin_role['level'] > level:
                    rank = admin_role['rank']
                    level = admin_role['level']
    return rank


def has_role(author: Member, role_id_list: list) -> bool:
    """
    Verifies a Discord member has any number of roles
    """
    for role_id in role_id_list:
        has_current_role = False
        for role in author.roles:
            if role.id == role_id:
                has_current_role = True
        if not has_current_role:
            return False
    return True


def in_section(channel_id: str, section_list: list) -> bool:
    """
    Verifies a Discord message waas posted in the correct channel by taking in a Section class, a list of channels
    in the Discord server
    """
    for section_channel_id in section_list:
        if channel_id == section_channel_id:
            return True
    return False


# Checks if the message was sent and adds feedback for the user
async def send_check(bot, message: discord.Message, data: str):
    sent = await server.get_server().write(data)
    if sent:
        await bot.add_reaction(message, '✅')
    else:
        await bot.add_reaction(message, '❌')
