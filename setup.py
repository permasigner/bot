import asyncio
import os

import mongoengine
from dotenv import find_dotenv, load_dotenv

from data.model.guild import Guild

load_dotenv(find_dotenv())

async def setup():
    print("STARTING SETUP...")
    guild = Guild()

    # you should have this setup in the .env file beforehand
    guild._id          = int(os.environ.get("MAIN_GUILD_ID"))

    # If you're re-running this script to update a value, set case_id
    # to the last unused case ID or else it will start over from 1!
    guild.case_id      = 1

    # required for permissions framework!
    guild.role_administrator = 1001908113517072424  # put in the role IDs for your server here
    guild.role_moderator     = 1001910120164380742  # put in the role IDs for your server here
    guild.role_birthday      = 1001912852191383644  # put in the role IDs for your server here
    guild.role_memberone     = 1001913027840458894  # put in the role IDs for your server here
    guild.role_memberedition = 1001913007447752764  # put in the role IDs for your server here
    guild.role_memberpro     = 1001912992704778250  # put in the role IDs for your server here
    guild.role_memberplus    = 1001912973499043901  # put in the role IDs for your server here

    guild.channel_reports        = 1001913478774259742  # put in the channel IDs for your server here
    # channel where reactions will be logged
    guild.channel_emoji_log      = 1001913499850637414  # put in the channel IDs for your server here
    # channel for private mod logs
    guild.channel_private        = 1001907318448984125  # put in the channel IDs for your server here
    # channel where self-assignable roles will be posted
    guild.channel_reaction_roles = 1001906581539143690  # put in the channel IDs for your server here
    # rules-and-info channel
    guild.channel_rules          = 1001906343583694980  # put in the channel IDs for your server here
    # channel for public mod logs
    guild.channel_public         = 1001906642901807144 # put in the channel IDs for your server here
    # optional, required for /issue command
    guild.channel_common_issues  = 1001906642901807144  # put in the channel IDs for your server here
    # #general, required for permissions
    guild.channel_general        = 1001905995334811671 # put in the channel IDs for your server here
    # required for filter
    guild.channel_development    = 1001907852547457025  # put in the channel IDs for your server here
    # required, #bot-commands channel
    guild.channel_botspam        = 1001913223219523694  # put in the channel IDs for your server here
    # optional, needed for booster #emote-suggestions channel
    guild.channel_booster_emoji  = 123  # put in the channel IDs for your server here
    
    guild.channel_reaction_colors = 1001906608193945680
    guild.channel_suggestions     = 1001914233501520023

    # you can fill these in if you want with IDs, or you ca use commands later
    guild.logging_excluded_channels = []  # put in a channel if you want (ignored in logging)
    guild.filter_excluded_channels  = []  # put in a channel if you want (ignored in filter)
    guild.filter_excluded_guilds    = []  # put guild ID to whitelist in invite filter if you want

    guild.nsa_guild_id = 1001911837962534972 # you can leave this as is if you don't want Blootooth (message mirroring system)

    guild.save()
    print("DONE")

if __name__ == "__main__":
    if os.environ.get("DB_CONNECTION_STRING") is None:
        mongoengine.register_connection(
            host=os.environ.get("DB_HOST"), port=int(os.environ.get("DB_PORT")), alias="default", name="botty")
    else:
        mongoengine.register_connection(
            host=os.environ.get("DB_CONNECTION_STRING"), alias="default", name="botty")
    res = asyncio.get_event_loop().run_until_complete( setup() )
