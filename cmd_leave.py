import discord

async def ex(args, message, client, invoke):
  voiceChannel = discord.utils.get(client.voice_clients, guild=message.guild)
  await voiceChannel.disconnect()