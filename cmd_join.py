import discord

async def ex(args, message, client, invoke):
  voiceChannel = discord.utils.get(message.guild.voice_channels, name='General')
  await voiceChannel.connect()