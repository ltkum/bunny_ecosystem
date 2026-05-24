"""_summary_
    Sup bitch
    step 1 : on donne un potit config

{
    "name":"open",
    "description":"Ben, c'est une open quoi",
    "discord_command":"/alttpr preset open",
    "rtgg_command": "!race open",
    "timestamp":"1780101540",
    "trackers_wanted":2,
    "comms_wanted": 2,
    "BO_channel_id": 222,
    "tracker_channel_id": 221,
    "weekly_annoucement_channel": 242
}

"""
import discord
from discord import app_commands


async def launch_next_weekly_process(interaction: discord.Interaction,
                                     json_config: discord.Attachment):

    async def create_next_weekly(interaction: discord.Interaction):
        pass

    async def ask_for_BO():
        pass

    async def ask_for_team():
        pass

    async def announce_next_weekly():
        pass

    async def show_race_room():
        pass

    async def cleanup():
        pass

    await create_next_weekly(interaction)
