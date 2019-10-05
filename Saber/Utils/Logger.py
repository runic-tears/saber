import discord
from Saber.SaberCore import SECONDARY_COLOR, WARNING_COLOR, ERROR_COLOR, DEFAULT_COLOR, SUCCESS_COLOR, MAIN_LOGS_CHANNEL
import datetime
import discord
from discord.ext import commands
import datetime as dt

MOD_ACTION_COLOR = ERROR_COLOR

BOT = None


def init(actual_bot):
    global BOT
    BOT = actual_bot


class OldLog:
    def __init__(self, log_type='info', log_data='Data was not specified'):
        self.type = log_type
        self.data = log_data

    async def send(self, client_object, send_to=MAIN_LOGS_CHANNEL):
        triggered_at = datetime.datetime.utcnow()

        log_embed = discord.Embed(
            description=self.data
        )

        log_embed.timestamp = triggered_at
        del triggered_at

        if self.type == 'info':
            log_embed.colour = SECONDARY_COLOR
        elif self.type == 'warning':
            log_embed.colour = WARNING_COLOR
        elif self.type == 'error':
            log_embed.colour = ERROR_COLOR
        elif self.type == 'success':
            log_embed.colour = SUCCESS_COLOR
        elif self.type == 'mod_action':
            log_embed.colour = MOD_ACTION_COLOR
        else:
            log_embed.colour = DEFAULT_COLOR

        channel = discord.Client.get_channel(client_object, send_to)
        return await channel.send(embed=log_embed)


class Log:
    def __init__(self, guild, embed=False) -> None:
        super().__init__()
        self.embed = embed
        self.guild = guild
        self.bot = BOT

    async def generate_log_data(self, _type='info', text=None):
        triggered_at = dt.datetime.utcnow().strftime('UTC: %H:%M:%S')

        emote = ""

        if _type == 'info':
            emote = "\N{INFORMATION SOURCE}"
        elif _type == 'warning':
            emote = "\N{WARNING SIGN}"
        elif _type == 'error':
            emote = "\N{CROSS MARK}"
        elif _type == 'success':
            emote = "\N{WHITE HEAVY CHECK MARK}"

        return f"[`{triggered_at}`] {emote} {text}"

    async def log_to(self, channel, text):
        log = discord.utils.get(BOT.get_guild(self.guild).text_channels, name=channel)

        if log is None:
            return print(
                f"[LOGGER: {self.guild.name}] Couldn't find a channel named as #{channel}, ignoring...")  # Отменяем процесс логирования, если канал не найден

        await log.send(text)