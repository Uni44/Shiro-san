import discord
import os

from async_repair import *

import cmd_embed
import cmd_say
import cmd_sayto

import perms

import random

from keep_alive import keep_alive

from discord.ext import commands

from discord_components import DiscordComponents, Button, ButtonStyle

intents=intents=discord.Intents.all()
intents.presences = True
intents.members = True

# Read the Data files and store them in a variable
#TokenFile = open("./data/Token.txt", "r") # Make sure to paste the token in the txt file
TOKEN = os.environ['TOKEN']#TokenFile.read()
#TokenFile.close()

OWNERID = 269549755850293249

# Define "bot"
bot = commands.Bot(command_prefix = "sh!", case_insensitive=False, intents=intents)
DiscordComponents(bot)

bot.remove_command("help")

# Let us Know when the bot is ready and has started
@bot.event
async def on_ready():
    await sql_create_db()
    print("Bot is ready")
    await minutework()

import asyncio
async def minutework():
  while True:
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching,name=" anime | sh!"))
    await asyncio.sleep(20)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching,name=" anime | OTAKU ARMY"))
    await asyncio.sleep(20)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching,name=" anime | sh!invite"))
    await asyncio.sleep(20)
    #inicio
    #temp mute
    #c.execute ("SELECT * FROM mute_temps")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM mute_temps")

    if len(items) > 0:
      for item in items:
        if datetime.datetime.now() >= datetime.datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S.%f'):
          #c.execute ("SELECT * FROM muterole WHERE guild_id = '" + item[0] + "'")
          #items22 = c.fetchall()
          items22 = await QueryGET("SELECT * FROM muterole WHERE guild_id = '" + item[0] + "'")
          
          if len(items22) > 0:
            guild = bot.get_guild(int(item[0]))
            role = get(guild.roles, id=int(items22[0][1]))
            miembro = guild.get_member(int(item[1]))

            if miembro:
              await miembro.remove_roles(role)
          
          #c.execute("DELETE FROM mute_temps WHERE guild_id = '" + item[0] + "' AND user_id = '" + item[1] + "'")
          await QueryEX("DELETE FROM mute_temps WHERE guild_id = '" + item[0] + "' AND user_id = '" + item[1] + "'")
          #conn.commit()
    #fin

import sqlite3

#async def QueryEX(query):
#  try:
#    conn2 = sqlite3.connect('database.db')
#    cursor = conn2.cursor()
#    cursor.execute(query)
#
#    conn2.commit()
#  finally:
#    conn2.close()

rutina_sql = False

rutina_sql_cola = []

async def QueryEX(query):
  global rutina_sql_cola

  rutina_sql_cola.append(query)
  await QueryEX_Rutina()

async def QueryGET(query):
  obteniendo = True
  while obteniendo:
    if conn == None:
      await dbConnect()
      cursor.execute(query)
      items = cursor.fetchall()
      await dbDisconnect()
      obteniendo = False
      return items

#conn2 = sqlite3.connect('database.db')
#cursor = conn2.cursor()

#conn = sqlite3.connect('database.db')
#c = conn.cursor()
#cursor = conn.cursor()

conn = None
#c = None
cursor = None

async def dbConnect():
  global conn
  #global c
  global cursor
  conn = sqlite3.connect('database_dc_bot.db')
  #c = None
  cursor = conn.cursor()

async def dbDisconnect():
  global conn
  #global c
  global cursor
  conn.close()
  conn = None
  #c = None
  cursor = None

async def QueryEX_Rutina():
  global rutina_sql
  global rutina_sql_cola

  if rutina_sql == False:
    rutina_sql = True
    while rutina_sql:
      if conn == None:
        await dbConnect()

      #try:
        #conn2 = sqlite3.connect('database.db')
        #cursor = conn2.cursor()
    
        for k in sorted(rutina_sql_cola):
          cursor.execute(k)
          conn.commit()
          rutina_sql_cola.remove(k)

      #finally:
        #conn2.close()
      
        if len(rutina_sql_cola) <= 0:
          await dbDisconnect()
          rutina_sql = False

# A simple and small ERROR handler
@bot.event
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
      embed.add_field(name=f':x: Error', value=f'Ese comando no existe.')
      await ctx.send(embed=embed)
    else:
      if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f':x: Error', value=f'No tengo los permisos necesarios.')
        await ctx.send(embed=embed)
      else:
        if isinstance(error, commands.MemberNotFound):
          embed.add_field(name=f':x: Error', value=f'El miembro no fue encontrado.')
          await ctx.send(embed=embed)
        else:
          embed.add_field(name = f':x: Error', value = f"```{error}```")
          if permisosCheck(ctx.author, 2):
            await ctx.send(embed = embed)
          channel = bot.get_channel(848814902478897203)
          await channel.send("<@" + str(ctx.author.id) + "> " + "<#" + str(ctx.channel.id) + ">", embed = embed)
          raise error

# Load command to manage our "Cogs" or extensions
@bot.command()
async def load(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Enabled the Cog!")

# Unload command to manage our "Cogs" or extensions
@bot.command()
async def unload(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Disabled the Cog!")

# Reload command to manage our "Cogs" or extensions
@bot.command(name = "reload")
async def reload_(ctx, extension):
    # Check if the user running the command is actually the owner of the bot 
    if ctx.author.id == OWNERID:
        bot.reload_extension(f'Cogs.{extension}')
        await ctx.send(f"Reloaded the Cog!") 

# Automatically load all the .py files in the Cogs folder
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'Cogs.{filename[:-3]}')
        except Exception:
            raise Exception
            

#CUSTOM COMANDOS

#@bot.command(name = "embed")
#async def embed_(ctx, nombre: str, channelname: str):
#  if permisosCheck(ctx.author, 4):
#    await cmd_embed.ex(nombre, channelname, ctx, bot)

@bot.command(name = "say")
async def say_(ctx, *texto:str):
  if permisosCheck(ctx.author, 2):
    await ctx.message.delete()
    if not texto:
      await ctx.send("Por favor ingrese un texto.")
      return
    texto = ' '.join(texto)
    await cmd_say.ex(texto, ctx)

@bot.command(name = "sayto")
async def sayto_(ctx, channel: discord.TextChannel, texto: str):
  if permisosCheck(ctx.author, 2):
    await cmd_sayto.ex(channel, texto, ctx, bot)

@bot.command(name = "memide")
async def memide_(ctx):
  await ctx.send("A <@" + str(ctx.author.id) + "> le mide " + str(random.randint(0, 50)) + " cm")

@bot.command(name = "codigo")
async def codigo_(ctx):
  if random.randint(0, 1) == 0: #codigo de 5
    await ctx.send("<@" + str(ctx.author.id) + "> su codigo nuclear esta listo: " + str(random.randint(1, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)))
  else: #codigo de 6
    await ctx.send("<@" + str(ctx.author.id) + "> su codigo nuclear esta listo: " + str(random.randint(1, 3)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)))

from discord.utils import get
#@bot.command(name = "giveroleall")
#async def giveroleall_(ctx, rol: discord.Role):
#  if permisosCheck(ctx.author, 3):
#    role = rol
#    for member in ctx.guild.members:
#      if member.bot == False:
#        await member.add_roles(role)
#
#    await ctx.send("Listo.")

#@bot.command(name = "removeroleall")
#async def removeroleall_(ctx, rol: discord.Role):
#  if permisosCheck(ctx.author, 3):
#    role = rol
#    for member in ctx.guild.members:
#      if member.bot == False:
#        await member.remove_roles(role)
#
#    await ctx.send("Listo.")

#@bot.command(name = "verificar")
#async def verificar_(ctx, estado: str):
#  if permisosCheck(ctx.author, 3):
#    if estado == "no":
#      VERIFICARFile = open("./data/Verificar.txt", "w")
#      VERIFICARFile.write(estado)
#      VERIFICARFile.close()
#      
#      await ctx.send("Listo. Estado de la verificación cambiado a: " + estado)
#    else:
#      if estado == "si":
#        VERIFICARFile = open("./data/Verificar.txt", "w")
#        VERIFICARFile.write(estado)
#        VERIFICARFile.close()
#
#        await ctx.send("Listo. Estado de la verificación cambiado a: " + estado)
#      else:
#        await ctx.send("Estados disponibles si y no.")

@bot.command(name = "reactrole")
async def reactrole(ctx, emoji, role: discord.Role, *, message):
  if permisosCheck(ctx.author, 2):
    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id,
        'remove_role_id': "null"}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

#@bot.command(name = "msg")
#async def msg (ctx, user: discord.User, texto: str):
#  if permisosCheck(ctx.author, 3):
#    await user.send(texto)
#    channel = bot.get_channel(846517618973212673)
#    await channel.send(" <@" + str(bot.user.id) + "> <@" + str(user.id) + ">: " + texto)

###EXTRA

import requests
import shutil
from PIL import Image, ImageDraw, ImageFont
@bot.command(name = "weltest")
async def weltest_(ctx):
  if ctx.author.id == OWNERID:
    await create_member_welcome(ctx.author, ctx, "Hola <@" + str(ctx.author.id) + ">, ¡Bienvenido a **" + ctx.guild.name + "**!")

#@bot.command(name = "secreto89")
#async def secreto89 (ctx):
#  await ctx.message.delete()
#  await ctx.author.send("Esto es un secreto... pero busca al bot de OTAKU CRAFT y dile lo siguiente: 89 es, estamos esperando la temp 2.")

@bot.command(name = "help")
async def help(ctx):
  await cmd_embed.ex("help1", ctx.channel.id, ctx, bot)

@bot.command(name = "ayuda")
async def ayuda(ctx):
  await cmd_embed.ex("help1", ctx.channel.id, ctx, bot)

@bot.command(name = "help2")
async def help2(ctx):
  if permisosCheck(ctx.author, 1):
    await cmd_embed.ex("help2", ctx.channel.id, ctx, bot)

@bot.command(name = "leave_guild")
async def leave_guild(ctx):
  if ctx.author.id == OWNERID:
    await ctx.message.delete()
    await ctx.guild.leave()

@bot.command(name = "list_guild")
async def list_guild(ctx):
  if ctx.author.id == OWNERID:
    texto = "> **Lista de todos los servers:**"
    for guild in bot.guilds:
     texto = texto + "\nNombre: " + guild.name + "\nID: " + str(guild.id)
    await ctx.send(texto)

###SHIRO-SAN NEW COMANDOS

@bot.command(name = "joinrole")
async def joinrole(ctx, role: discord.Role):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM joinrole WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM joinrole WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      #c.execute("INSERT INTO joinrole VALUES ('" + str(ctx.guild.id) + "', '" + str(role.id) + "')")
      await QueryEX("INSERT INTO joinrole VALUES ('" + str(ctx.guild.id) + "', '" + str(role.id) + "')")
      await ctx.send("Listo. Rol auto asignado guardado, para eliminar el rol utiliza `joinrole-clear`.")
    else:
      await ctx.send("Ya hay un rol auto asignado. Utiliza `joinrole-clear` para eliminar el rol.")
    #conn.commit()

@bot.command(name = "joinrole-clear")
async def joinrole_clear(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM joinrole WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM joinrole WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("No hay un rol auto asignado. Utiliza `joinrole` para añadir un rol.")
    else:
      #c.execute ("DELETE FROM joinrole WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("DELETE FROM joinrole WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. Rol auto asignado eliminado.")
    #conn.commit()

@bot.command(name = "legacy-response-list")
async def response_list(ctx):
  if permisosCheck(ctx.author, 2):
    count = 0
    texto = ""
    with open('responses.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['guild_id'] == ctx.author.guild.id and x['active'] == "True":
                  count = count + 1
                  texto = texto + "> ID: " + x['id'] + "\n > Veces para activar: " + str(x['veces']) + "\n" + "> Palabra para activar: " + x['key'] + "\n" + "> Respuesta: " + x['response'] + "\n\n"
            await ctx.send(texto)
    if count <= 0:
      await ctx.send("No tienes respuestas automaticas. Utiliza `response-add` para añadir una.")

@bot.command(name = "legacy-response-add")
async def response_add(ctx, veces_para_activar: int, palabra_clave: str, respuesta: str):
  if permisosCheck(ctx.author, 2):
    passe = False

    count = 0
    last_id = 0

    with open('responses.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['guild_id'] == ctx.author.guild.id and x['active'] == "True":
                  count = count + 1
                  last_id = int(x['id'])

    if count >= 12:
      passe = True
      await ctx.send("Ya has llegado al limite de respuestas automaticas, utiliza `response_list` para ver la lista completa y `response_delete` para eliminar algunas.")

    if passe == False:
      with open('responses.json') as json_file:
          data = json.load(json_file)

          new_react_role = {'id': str(last_id + 1),
          'guild_id': ctx.author.guild.id,
          'veces': veces_para_activar,
          'key': palabra_clave,
          'response': respuesta,
          'active': "True",
          'try': 0}

          data.append(new_react_role)

      with open('responses.json', 'w') as f:
          json.dump(data, f, indent=4)
      await ctx.send("Listo.")
    
@bot.command(name = "legacy-response-delete")
async def response_delete(ctx, id: int):
  if permisosCheck(ctx.author, 2):
    with open('responses.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['guild_id'] == ctx.author.guild.id and x['id'] == str(id) and x['active'] == "True":
                  x['active'] = "False"
    with open('responses.json', 'w') as f:
        json.dump(data, f, indent=4)
    await ctx.send("Listo.")

@bot.command(name = "response-list")
async def response_list(ctx):
  if permisosCheck(ctx.author, 2):
    texto = ""

    #c.execute ("SELECT * FROM responses_messages WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM responses_messages WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      for item in items:
        texto = texto + "> ID: " + item[5] + "\n > Veces para activar: " + item[3] + "\n" + "> Palabra para activar: " + item[1] + "\n" + "> Respuesta: " + item[2] + "\n\n"
      await ctx.send(texto)
    else:
      await ctx.send("No tienes respuestas automaticas. Utiliza `response-add` para añadir una.")

@bot.command(name = "response-add")
async def response_add(ctx, veces_para_activar: int, palabra_clave: str, respuesta: str):
  if permisosCheck(ctx.author, 2):
    passe = False

    count = 0
    last_id = 0
    
    #c.execute ("SELECT * FROM responses_messages WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM responses_messages WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      last_id = items[len(items) - 1][5]

    if len(items) >= 10:
      passe = True
      await ctx.send("Ya has llegado al limite de respuestas automaticas, utiliza `response_list` para ver la lista completa y `response_delete` para eliminar algunas.")

    if passe == False:
      #c.execute("INSERT INTO responses_messages VALUES ('" + str(ctx.guild.id) + "', '" + palabra_clave.lower() + "', '" + respuesta + "', '" + str(veces_para_activar) + "', '0" + "', '" + str(int(last_id) + 1) + "')")
      await QueryEX("INSERT INTO responses_messages VALUES ('" + str(ctx.guild.id) + "', '" + palabra_clave.lower() + "', '" + respuesta + "', '" + str(veces_para_activar) + "', '0" + "', '" + str(int(last_id) + 1) + "')")
      #conn.commit()
      await ctx.send("Listo. Ahora cada " + str(veces_para_activar) + " vez/veces que alguien ponga `" + palabra_clave.lower() + "` respondere con `" + respuesta + "`.")
    
@bot.command(name = "response-delete")
async def response_delete(ctx, id: int):
  if permisosCheck(ctx.author, 2):
    #c.execute("DELETE FROM responses_messages WHERE guild_id = '" + str(ctx.guild.id) + "' AND id = '" + str(id) + "'")
    await QueryEX("DELETE FROM responses_messages WHERE guild_id = '" + str(ctx.guild.id) + "' AND id = '" + str(id) + "'")
    ##conn.commit()
    await ctx.send("Listo.")

@bot.command(name = "add-response-admin")
async def response_add(ctx, guild_id: int, veces_para_activar: int, palabra_clave: str, respuesta: str):
  if ctx.author.id == OWNERID:
    passe = False

    count = 0
    last_id = 0
    
    #c.execute ("SELECT * FROM responses_messages WHERE guild_id = '" + str(guild_id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM responses_messages WHERE guild_id = '" + str(guild_id) + "'")

    if len(items) > 0:
      last_id = items[len(items) - 1][5]

    if len(items) >= 12:
      passe = True
      await ctx.send("Ya has llegado al limite de respuestas automaticas, utiliza `response_list` para ver la lista completa y `response_delete` para eliminar algunas.")

    if passe == False:
      #c.execute("INSERT INTO responses_messages VALUES ('" + str(guild_id) + "', '" + palabra_clave.lower() + "', '" + respuesta + "', '" + str(veces_para_activar) + "', '0" + "', '" + str(int(last_id) + 1) + "')")
      await QueryEX("INSERT INTO responses_messages VALUES ('" + str(guild_id) + "', '" + palabra_clave.lower() + "', '" + respuesta + "', '" + str(veces_para_activar) + "', '0" + "', '" + str(int(last_id) + 1) + "')")
      #conn.commit()
      await ctx.send("Listo. Ahora cada " + str(veces_para_activar) + " vez/veces que alguien ponga `" + palabra_clave.lower() + "` respondere con `" + respuesta + "`.")

@bot.command(name = "ban")
async def ban(ctx, miembro: discord.Member):
  if permisosCheck(ctx.author, 1):
    await miembro.ban(reason = "Shiro-san Ban by " + ctx.author.name)
    await ctx.send("Listo. El Miembro <@" + str(miembro.id) + "> fue baneado con exito.")

    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      channel = bot.get_channel(int(items[0][1]))
      embed = discord.Embed(
      title = '**BAN**',
      description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
      colour = discord.Colour.from_rgb(219, 0, 255)
      )
      embed.set_thumbnail(url=miembro.avatar_url)
      await channel.send(embed=embed)

@bot.command(name = "kick")
async def kick(ctx, miembro: discord.Member):
  if permisosCheck(ctx.author, 1):
    await miembro.kick(reason = "Shiro-san Kick by " + ctx.author.name)
    await ctx.send("Listo. El Miembro <@" + str(miembro.id) + "> fue expulsado con exito.")

    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      channel = bot.get_channel(int(items[0][1]))
      embed = discord.Embed(
      title = '**KICK**',
      description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
      colour = discord.Colour.from_rgb(219, 0, 255)
      )
      embed.set_thumbnail(url=miembro.avatar_url)
      await channel.send(embed=embed)

@bot.command(name = "userinfo")
async def user_info(ctx, miembro: discord.Member):
  if permisosCheck(ctx.author, 1):

    rol = ""
    if permisosCheck(miembro, 3):
      rol = rol +"Dueño del server, "
    if permisosCheck(miembro, 2):
      rol = rol + "Administrador, "
    if permisosCheck(miembro, 1):
      rol = rol + "Moderador, "
    rol = rol + "Miembro"

    if miembro.bot:
      embed = discord.Embed(
      title = 'Información de ' + miembro.name + " (" + miembro.display_name + ") <:bottag:860610530447589376>",
      description = "**Estado del usuario:** " + rol + ".",
      colour = discord.Colour.from_rgb(219, 0, 255)
      )
    else:
      embed = discord.Embed(
      title = 'Información de ' + miembro.name + " (" + miembro.display_name + ")",
      description = "**Estado del usuario:** " + rol + ".",
      colour = discord.Colour.from_rgb(219, 0, 255)
      )
    
    embed.add_field(name="Entró al Servidor el", value=miembro.joined_at.strftime("%b %d, %Y %H:%M:%S"))
    embed.add_field(name="Entró a Discord el", value=miembro.created_at.strftime("%b %d, %Y %H:%M:%S"))
    if miembro.premium_since == None:
      embed.add_field(name="Mejorando desde", value="No")
    else:
      embed.add_field(name="Mejorando desde", value=miembro.premium_since.strftime("%b %d, %Y %H:%M:%S"))
    embed.add_field(name="Discriminador", value=miembro.discriminator)
    embed.add_field(name="ID", value=str(miembro.id))
    embed.set_thumbnail(url=miembro.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name = "serverinfo")
async def server_info(ctx):
  if permisosCheck(ctx.author, 1):
    embed = discord.Embed(
    title = 'Información de ' + ctx.author.guild.name,
    description = "**Dueño:** " + str(ctx.author.guild.owner),
    colour = discord.Colour.from_rgb(255, 229, 247)
    )
    embed.add_field(name="Servidor Creado", value= ctx.author.guild.created_at.strftime("%b %d, %Y %H:%M:%S"))
    embed.add_field(name="Roles totales", value=len(ctx.author.guild.roles))
    embed.add_field(name="Miembros", value=len(ctx.guild.members))
    embed.add_field(name="Categorias", value=len(ctx.guild.categories))
    embed.add_field(name="Canales de texto", value=len(ctx.guild.text_channels))
    embed.add_field(name="Canales de voz", value=len(ctx.guild.voice_channels))
    embed.add_field(name="ID", value=str(ctx.guild.id))
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command(name = "clear")
async def clear(ctx, cantidad: int):
  if permisosCheck(ctx.author, 1):
    if cantidad > 50:
      await ctx.send("Solo puedes eliminar 50 mensajes.")
    else:
      await ctx.message.delete()
      passed = 0
      failed = 0
      async for msg in ctx.message.channel.history(limit=cantidad):
            try:
              await msg.delete()
              passed += 1
            except:
              failed += 1
      #await ctx.send(f"Listo. Eliminados {passed} mensajes. {failed} Fallos")
      #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

      if len(items) > 0:
        channel = bot.get_channel(int(items[0][1]))
        embed = discord.Embed(
        title = '**CLEAR**',
        description = "Canal: <#" + str(ctx.channel.id) + ">\n Mensajes: " + str(cantidad) + " \n Por: <@" + str(ctx.author.id) + ">",
        colour = discord.Colour.from_rgb(219, 0, 255)
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await channel.send(embed=embed)

@bot.command(name = "welcome-set")
async def welcome_set(ctx, channel: discord.TextChannel):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM welcomes WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM welcomes WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      #c.execute("INSERT INTO welcomes VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await QueryEX("INSERT INTO welcomes VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await ctx.send("Listo. Canal de bienvenidas asignado, para eliminarlo utiliza `sh!welcome-clear`.")
    else:
      await ctx.send("Error. Ya tienes un canal de bienvenidas asignado, para eliminarlo utiliza `sh!welcome-clear`.")
    #conn.commit()

@bot.command(name = "welcome-clear")
async def welcome_clear(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM welcomes WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM welcomes WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("No hay un canal de bienvenidas asignado. Utiliza `sh!welcome-set` para añadir uno.")
    else:
      #c.execute ("DELETE FROM joinrole WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("DELETE FROM welcomes WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. Canal de bienvenidas eliminado.")
    #conn.commit()

@bot.command(name = "vote")
async def vote(ctx):
  await ctx.message.delete()
  embed = discord.Embed(
  title = 'Me ayudarias un montón si votas por mí <:sataok:848337914765115412>.',
  colour = discord.Colour.from_rgb(219, 0, 255)
  )
  embed.description = "[Top.gg](https://top.gg/bot/848797506694414346/vote)\n[Aura Bot List](https://auralist.ml/bots/848797506694414346/vote)\n[Astrabots](https://astrabots.xyz/bot/848797506694414346/vote)\n[Bladebotlist](https://bladebotlist.xyz/bot/848797506694414346/vote)\n[DisBotlist](https://disbotlist.xyz/bot/848797506694414346/vote)\n[Upcord List](https://list.upcord.tk/bot/848797506694414346/vote)"
  embed.set_thumbnail(url=bot.user.avatar_url)
  await ctx.author.send(embed=embed)

@bot.command(name = "invite")
async def invite(ctx):
  await ctx.message.delete()
  await ctx.author.send("Gracias por invitar a Shiro-san <:sataok:848337914765115412>. https://discord.com/api/oauth2/authorize?client_id=848797506694414346&permissions=8&scope=bot")

@bot.command(name = "report")
async def report(ctx):
  await ctx.message.delete()
  await ctx.author.send("Para reportar un error podes hablar con el bot oficial de la **OTAKU ARMY** (OTAKU ARMY#4656) o con Uni44#4720 Gracias por reportar los errores, el bot aun sigue en desarrollo. <:sataok:848337914765115412> Servidor de Discord de la **OTAKU ARMY**: https://discord.gg/tXrJ2FZ")

@bot.command(name = "bot-info-servers")
async def bot_info_servers(ctx):
  if ctx.author.id == OWNERID:
    await ctx.send("Total de servers: " + str(len(bot.guilds)))

@bot.command(name = "pregunta")
async def pregunta(ctx, texto: str = "", texto2: str = ""):
  passs = False

  censurado = True

  if censurado == True:
    texto = texto.replace("@everyone", "everyone")
    texto = texto.replace("@here", "here")

  if len(texto) + len(texto2) <= 3:
    passs = True

  if passs == False:
    with open('pregunta_responses.json') as file:
            data = json.load(file)
            ina = random.randint(0, len(data) - 1)
            await ctx.send("<@" + str(ctx.author.id) + "> " + data[ina]['respuesta'])
  else:
    with open('pregunta_responses_other.json') as file:
            data = json.load(file)
            ina = random.randint(0, len(data) - 1)

            if data[ina]['respuesta'] == "func:repeat_text":
              if len(texto) > 0:
                await ctx.send("<@" + str(ctx.author.id) + "> " + texto)
            else:
              await ctx.send("<@" + str(ctx.author.id) + "> " + data[ina]['respuesta'])

@bot.command(name = "dados")
async def dados(ctx):
  ina = random.randint(0, 3)
  ina2 = random.randint(0, 6)
  if ina == 0:
    await ctx.send("<@" + str(ctx.author.id) + "> Tiro los dados y sale... ||" + str(ina2) + "||, ¡increíble!")
  if ina == 1:
    await ctx.send("<@" + str(ctx.author.id) + "> Tiro los dados y sale... ||" + str(ina2) + "||, Jaja, que suerte.")
  if ina == 2:
    await ctx.send("<@" + str(ctx.author.id) + "> Tiro los dados y sale... ||" + str(ina2) + "||, ¡Wow no me lo creo!")
  if ina == 3:
    await ctx.send("<@" + str(ctx.author.id) + "> Tiro los dados y sale... ||" + str(ina2) + "||, ¡Jaja!")

@bot.command(name = "avatar")
async def avatar(ctx, miembro: discord.Member = None):

  if miembro == None:
    miembro = ctx.author
  await ctx.send(str(miembro.avatar_url))

@bot.command(name = "servericon")
async def servericon(ctx):
  if str(ctx.author.guild.icon_url) == "":
    await ctx.send("Este servidor no tiene icono.")
  else:
    await ctx.send(str(ctx.author.guild.icon_url))

@bot.command(name = "dime")
async def dime(ctx):
  with open('dime_responses.json') as file:
            data = json.load(file)
            ina = random.randint(0, len(data) - 1)
            await ctx.send("<@" + str(ctx.author.id) + "> " + data[ina]['respuesta'])

import datetime
@bot.command(name = "muerte")
async def muerte(ctx):
  with open('dead_saves.json') as file:
    ano_actual = 2021 #año actual

    data = json.load(file)
    for x in data:
        if x['user_id'] == ctx.author.id and x['active'] == "True":
          with open('dead_responses_other.json') as file2:
            data2 = json.load(file2)
            ina33 = random.randint(0, len(data2) - 1)
            await ctx.send("<@" + str(ctx.author.id) + "> " + data2[ina33]['respuesta'] + " " + str(x['age']))

          if x['permanent'] == "False":
            if datetime.datetime.strptime(x['date'], '%Y-%m-%d') < datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d'):
              with open('dead_responses_other2.json') as file3:
                data33 = json.load(file3)
                ina333 = random.randint(0, len(data33) - 1)
                await ctx.send("<@" + str(ctx.author.id) + "> " + data33[ina333]['respuesta'])

              x['active'] = "False"
              with open('dead_saves.json', 'w') as f:
                json.dump(data, f, indent=4)

          return

    ina = ano_actual + random.randint(0, 110)
    ina_per = random.randint(0, 1)
          
    #responses whit json
    with open('dead_responses.json') as file44:
      data44 = json.load(file44)
      ina33 = random.randint(0, len(data44) - 1)
      await ctx.send("<@" + str(ctx.author.id) + "> " + data44[ina33]['respuesta'] + " " + str(ina))
          
    permanente = "False"
    if ina_per == 0:
      permanente = "True"

  with open('dead_saves.json') as json_file:
    new_react_role = {'user_id': ctx.author.id,
          'age': ina,
          'permanent': permanente,
          'date': str(datetime.date.today()),
          'active': "True"}

    data.append(new_react_role)

  with open('dead_saves.json', 'w') as f:
    json.dump(data, f, indent=4)

@bot.command(name = "actividad")
async def actividad(ctx, tipo="a"):
  if tipo == "a":
    embed = discord.Embed(
              title = ':information_source: Información',
              description = 'Lista de actividades.',
              colour = discord.Colour.from_rgb(219, 0, 255)
              )
    embed.add_field(name="<:a:912487539384942604> YouTube Together", value="youtube | yt")
    embed.add_field(name="<:a:912486525642612766> Poker Night", value="poker | pn")
    embed.add_field(name="<:a:853161030062702592> Betrayal", value="betrayal | be")
    embed.add_field(name="<:a:853161030062702592> Fishington", value="fishington | fi")
    embed.add_field(name="<:a:912486814634360872> Chess in the Park", value="chess | ch")
    embed.add_field(name="<:a:912487014924943422> Doodle Crew", value="doodle | dc")
    embed.add_field(name="<:a:912487204297797702> Letter Tile", value="letter | lt")
    embed.add_field(name="<:a:912487372766195752> SpellCast", value="spell | sp")
    embed.add_field(name="<:a:912487972769783820> Checkers In The Park", value="checkers | cp")
    embed.add_field(name="<:a:912487972102869003> Word Snacks", value="snacks | ws")

    embed.add_field(name=":information_source: Ayuda", value="Prueba poniendo `oa!actividad yt`")
    embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)
    await ctx.send(embed=embed)
    return

  try:
    channel = ctx.author.voice.channel

    if tipo.lower() == "yt" or tipo.lower()  == "youtube":
      res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                          "max_age": 86400,
                          "max_uses": 0,
                          "target_application_id": "755600276941176913",
                          "target_type": 2,
                          "temporary": "false",
                      },
                      headers={
                          "Authorization": 'Bot ' + str(TOKEN),
                          "Content-Type": "application/json"
                      })

      response = json.loads(res.text)

      embed = discord.Embed(
              title = '¡Actividad añadida!',
              description = 'Añadido <:a:912487539384942604> **YouTube Together** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
              colour = discord.Colour.from_rgb(219, 0, 255)
              )
      embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

      await ctx.send(embed=embed)
    else:
      if tipo.lower() == "poker" or tipo.lower()  == "pn":
        res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                            "max_age": 86400,
                            "max_uses": 0,
                            "target_application_id": "755827207812677713",
                            "target_type": 2,
                            "temporary": "false",
                        },
                        headers={
                            "Authorization": 'Bot ' + str(TOKEN),
                            "Content-Type": "application/json"
                        })

        response = json.loads(res.text)

        embed = discord.Embed(
                title = '¡Actividad añadida!',
                description = 'Añadido <:a:912486525642612766> **Poker Night** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                colour = discord.Colour.from_rgb(219, 0, 255)
                )
        embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

        await ctx.send(embed=embed)
      else:
        if tipo.lower() == "betrayal" or tipo.lower()  == "be":
          res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                              "max_age": 86400,
                              "max_uses": 0,
                              "target_application_id": "773336526917861400",
                              "target_type": 2,
                              "temporary": "false",
                          },
                          headers={
                              "Authorization": 'Bot ' + str(TOKEN),
                              "Content-Type": "application/json"
                          })

          response = json.loads(res.text)

          embed = discord.Embed(
                  title = '¡Actividad añadida!',
                  description = 'Añadido <:a:853161030062702592> **Betrayal.io** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                  colour = discord.Colour.from_rgb(219, 0, 255)
                  )
          embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

          await ctx.send(embed=embed)
        else:
          if tipo.lower() == "fishington" or tipo.lower()  == "fi":
            res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                                "max_age": 86400,
                                "max_uses": 0,
                                "target_application_id": "814288819477020702",
                                "target_type": 2,
                                "temporary": "false",
                            },
                            headers={
                                "Authorization": 'Bot ' + str(TOKEN),
                                "Content-Type": "application/json"
                            })

            response = json.loads(res.text)

            embed = discord.Embed(
                    title = '¡Actividad añadida!',
                    description = 'Añadido <:a:853161030062702592> **Fishington.io** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                    colour = discord.Colour.from_rgb(219, 0, 255)
                    )
            embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

            await ctx.send(embed=embed)
          else:
            if tipo.lower() == "chess" or tipo.lower()  == "ch":
              res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                                "max_age": 86400,
                                "max_uses": 0,
                                "target_application_id": "832012774040141894",
                                "target_type": 2,
                                "temporary": "false",
                            },
                            headers={
                                "Authorization": 'Bot ' + str(TOKEN),
                                "Content-Type": "application/json"
                            })

              response = json.loads(res.text)

              embed = discord.Embed(
                      title = '¡Actividad añadida!',
                      description = 'Añadido <:a:912486814634360872> **Chess in the Park** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                      colour = discord.Colour.from_rgb(219, 0, 255)
                      )
              embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

              await ctx.send(embed=embed)
            else:
              if tipo.lower() == "doodle" or tipo.lower()  == "dc":
                res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                                  "max_age": 86400,
                                  "max_uses": 0,
                                  "target_application_id": "878067389634314250",
                                  "target_type": 2,
                                  "temporary": "false",
                              },
                              headers={
                                  "Authorization": 'Bot ' + str(TOKEN),
                                  "Content-Type": "application/json"
                              })

                response = json.loads(res.text)

                embed = discord.Embed(
                        title = '¡Actividad añadida!',
                        description = 'Añadido <:a:912487014924943422> **Doodle Crew** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                        colour = discord.Colour.from_rgb(219, 0, 255)
                        )
                embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

                await ctx.send(embed=embed)
              else:
                if tipo.lower() == "letter" or tipo.lower()  == "lt":
                  res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                                    "max_age": 86400,
                                    "max_uses": 0,
                                    "target_application_id": "879863686565621790",
                                    "target_type": 2,
                                    "temporary": "false",
                                },
                                headers={
                                    "Authorization": 'Bot ' + str(TOKEN),
                                    "Content-Type": "application/json"
                                })

                  response = json.loads(res.text)

                  embed = discord.Embed(
                          title = '¡Actividad añadida!',
                          description = 'Añadido <:a:912487204297797702> **Letter Tile** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                          colour = discord.Colour.from_rgb(219, 0, 255)
                          )
                  embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

                  await ctx.send(embed=embed)
                else:
                  if tipo.lower() == "spell" or tipo.lower()  == "sp":
                    res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                                      "max_age": 86400,
                                      "max_uses": 0,
                                      "target_application_id": "852509694341283871",
                                      "target_type": 2,
                                      "temporary": "false",
                                  },
                                  headers={
                                      "Authorization": 'Bot ' + str(TOKEN),
                                      "Content-Type": "application/json"
                                  })

                    response = json.loads(res.text)

                    embed = discord.Embed(
                            title = '¡Actividad añadida!',
                            description = 'Añadido <:a:912487372766195752> **SpellCast** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                            colour = discord.Colour.from_rgb(219, 0, 255)
                            )
                    embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

                    await ctx.send(embed=embed)
                  else:
                    if tipo.lower() == "checkers" or tipo.lower()  == "cp":
                      res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                                        "max_age": 86400,
                                        "max_uses": 0,
                                        "target_application_id": "832013003968348200",
                                        "target_type": 2,
                                        "temporary": "false",
                                    },
                                    headers={
                                        "Authorization": 'Bot ' + str(TOKEN),
                                        "Content-Type": "application/json"
                                    })

                      response = json.loads(res.text)

                      embed = discord.Embed(
                              title = '¡Actividad añadida!',
                              description = 'Añadido <:a:912487972769783820> **Checkers In The Park** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                              colour = discord.Colour.from_rgb(219, 0, 255)
                              )
                      embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

                      await ctx.send(embed=embed)
                    else:
                      if tipo.lower() == "snacks" or tipo.lower()  == "ws":
                        res = requests.post('https://discord.com/api/v8/channels/' + str(channel.id) + '/invites', json={
                                          "max_age": 86400,
                                          "max_uses": 0,
                                          "target_application_id": "879863976006127627",
                                          "target_type": 2,
                                          "temporary": "false",
                                      },
                                      headers={
                                          "Authorization": 'Bot ' + str(TOKEN),
                                          "Content-Type": "application/json"
                                      })

                        response = json.loads(res.text)

                        embed = discord.Embed(
                                title = '¡Actividad añadida!',
                                description = 'Añadido <:a:912487972102869003> **Word Snacks** a [' + channel.name + '](https://discord.gg/' + response['code'] + ')\n> Haga clic en el link para unirse.',
                                colour = discord.Colour.from_rgb(219, 0, 255)
                                )
                        embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

                        await ctx.send(embed=embed)

                #FIN
                      else:
                        embed = discord.Embed(
                              title = ':x: Error',
                              description = 'La actividad solicitada no fue encontrada.',
                              colour = discord.Colour.from_rgb(219, 0, 255)
                              )
                        embed.add_field(name="<:a:912487539384942604> YouTube Together", value="youtube | yt")
                        embed.add_field(name="<:a:912486525642612766> Poker Night", value="poker | pn")
                        embed.add_field(name="<:a:853161030062702592> Betrayal", value="betrayal | be")
                        embed.add_field(name="<:a:853161030062702592> Fishington", value="fishington | fi")
                        embed.add_field(name="<:a:912486814634360872> Chess in the Park", value="chess | ch")
                        embed.add_field(name="<:a:912487014924943422> Doodle Crew", value="doodle | dc")
                        embed.add_field(name="<:a:912487204297797702> Letter Tile", value="letter | lt")
                        embed.add_field(name="<:a:912487372766195752> SpellCast", value="spell | sp")
                        embed.add_field(name="<:a:912487972769783820> Checkers In The Park", value="checkers | cp")
                        embed.add_field(name="<:a:912487972102869003> Word Snacks", value="snacks | ws")

                        embed.add_field(name=":information_source: Ayuda", value="Prueba poniendo `oa!actividad yt`")
                        embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

                        await ctx.send(embed=embed)
  except AttributeError:
    await ctx.send('No estas en un chat de voz.')

@bot.command(name = "banlist")
async def banlist(ctx):
  if permisosCheck(ctx.author, 1):
    ban_list = await ctx.guild.bans()
    if not ban_list:
      await ctx.send("No hay baneos en este servidor.")
    else:
      userid = [user.user.id for user in ban_list]
      name = [user.user.name for user in ban_list]
      discriminator = [user.user.discriminator for user in ban_list]
      bot = [user.user.bot for user in ban_list]
      idd = [user.user.id for user in ban_list]
      razon = [user.reason for user in ban_list]

      newlist = []
      for item in bot:
        if item:
          item = "<:bottag:860610530447589376>"
        else:
          item = ""
        newlist.append(item)
        bot = newlist
        total = list((zip(userid, name, discriminator, bot, idd, razon)))
        pretty_list = set()
        for details in total:
          data = "> •<@{}>{} ({}#{}) ID: {}\n Razon: {}\n".format(details[0], details[3], details[1], details[2], details[4], details[5])
          pretty_list.add(data)

      await ctx.channel.trigger_typing()

      await asyncio.sleep(2)

      if len("**Ban list:** \n{}".format("\n".join(pretty_list))) < 3900:
        await ctx.send("**Ban list:** \n{}".format("\n".join(pretty_list)))
      else:
        await ctx.send("La lista de baneos de tu servidor es muy extensa, por favor utiliza la lista de Discord.")

@bot.command(name = "unban")
async def unban(ctx, id: int):
  if permisosCheck(ctx.author, 1):
    ban_list = await ctx.guild.bans()
    for user in ban_list:
      if user.user.id == id:
        await ctx.guild.unban(user.user, reason = "Shiro-san Unban By: " + ctx.author.name)
        await ctx.send("Listo. El Miembro <@" + str(user.user.id) + "> fue desbaneado con exito.")

        #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
        #items = c.fetchall()
        items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

        if len(items) > 0:
          channel = bot.get_channel(int(items[0][1]))
          embed = discord.Embed(
          title = '**UNBAN**',
          description = "Miembro: <@" + str(user.user.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          embed.set_thumbnail(url=user.user.avatar_url)
          await channel.send(embed=embed)

        break

@bot.command(name = "setmuterol")
async def setmuterol(ctx, role: discord.Role):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")
    
    if len(items) == 0:
      #c.execute("INSERT INTO muterole VALUES ('" + str(ctx.guild.id) + "', '" + str(role.id) + "')")
      await QueryEX("INSERT INTO muterole VALUES ('" + str(ctx.guild.id) + "', '" + str(role.id) + "')")
      await ctx.send("Listo. Rol de Muteado añadido.")
    else:
      #c.execute("UPDATE muterole SET role_id = '" + str(role.id) + "' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE muterole SET role_id = '" + str(role.id) + "' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. Rol de Muteado actualizado.")
    #conn.commit()

@bot.command(name = "mute")
async def mute(ctx, miembro: discord.Member):
  if permisosCheck(ctx.author, 1):
    if miembro == ctx.author:
      await ctx.send("Te vas a automutear?")
      return
    
    #c.execute ("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("Error. No posees un rol de Muteado asignado, para asignar uno el administrador debe utiliza el comando `setmuterol`.")
    else:
      role = get(miembro.guild.roles, id=int(items[0][1]))
      await miembro.add_roles(role)
      await ctx.send("Listo. El Miembro <@" + str(miembro.id) + "> fue Muteado con exito.")

      #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

      if len(items) > 0:
        channel = bot.get_channel(int(items[0][1]))
        embed = discord.Embed(
        title = '**MUTE**',
        description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
        colour = discord.Colour.from_rgb(219, 0, 255)
        )
        embed.set_thumbnail(url=miembro.avatar_url)
        await channel.send(embed=embed)

@bot.command(name = "unmute")
async def unmute(ctx, miembro: discord.Member):
  if permisosCheck(ctx.author, 1):
    #c.execute ("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")
    
    if len(items) == 0:
      await ctx.send("Error. No posees un rol de Muteado asignado, para asignar uno el administrador debe utiliza el comando `setmuterol`.")
    else:
      role = get(miembro.guild.roles, id=int(items[0][1]))
      await miembro.remove_roles(role)
      await ctx.send("Listo. El Miembro <@" + str(miembro.id) + "> fue Desmuteado con exito.")

      #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

      if len(items) > 0:
        channel = bot.get_channel(int(items[0][1]))
        embed = discord.Embed(
        title = '**UNMUTE**',
        description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
        colour = discord.Colour.from_rgb(219, 0, 255)
        )
        embed.set_thumbnail(url=miembro.avatar_url)
        await channel.send(embed=embed)

@bot.command(name = "tempmute")
async def tempmute(ctx, miembro: discord.Member, tiempo):
  await func_tempmute(ctx, miembro, tiempo, True)

async def func_tempmute(ctx, miembro: discord.Member, tiempo, manual: bool = True):
  if not manual or permisosCheck(ctx.author, 3):
    if manual:
      if miembro == ctx.author:
        await ctx.send("Te vas a automutear?")
        return
    
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    
    new_tiempo = 0

    try:
        new_tiempo = int(tiempo[:-1]) * time_convert[tiempo[-1]]
    except:
        new_tiempo = tiempo

    if new_tiempo < 60 and manual:
      await ctx.send("Error. El mínimo tiempo para mutear temporalmente a alguien es de 1 minuto. Utilize `1m`.")
      return

    fechadeunban = datetime.datetime.now() + datetime.timedelta(seconds=new_tiempo)

    #c.execute ("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      if manual:
        await ctx.send("Error. No posees un rol de Muteado asignado, para asignar uno el administrador debe utiliza el comando `setmuterol`.")
    else:
      role = get(miembro.guild.roles, id=int(items[0][1]))
      await miembro.add_roles(role)

      #c.execute("INSERT INTO mute_temps VALUES ('" + str(ctx.guild.id) + "', '" + str(miembro.id) + "', '" + str(fechadeunban) + "')")
      await QueryEX("INSERT INTO mute_temps VALUES ('" + str(ctx.guild.id) + "', '" + str(miembro.id) + "', '" + str(fechadeunban) + "')")
      #conn.commit()

      if manual:
        await ctx.send("Listo. El Miembro <@" + str(miembro.id) + "> fue Muteado temporalmente.")

      #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

      if len(items) > 0:
        if manual:
          channel = bot.get_channel(int(items[0][1]))
          embed = discord.Embed(
          title = '**Mute Temporal**',
          description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">\nFecha de finalización: " + str(fechadeunban),
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          embed.set_thumbnail(url=miembro.avatar_url)
          await channel.send(embed=embed)
        else:
          channel = bot.get_channel(int(items[0][1]))
          embed = discord.Embed(
          title = '**Mute Temporal**',
          description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(bot.user.id) + ">\nFecha de finalización: " + str(fechadeunban),
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          embed.set_thumbnail(url=miembro.avatar_url)
          await channel.send(embed=embed)


#conn = sqlite3.connect('database.db')

#c = conn.cursor()

@bot.command(name = "test1")
async def test1(ctx, str1, str2):
  if permisosCheck(ctx.author, 4):
    #c.execute("INSERT INTO test VALUES ('" + str1 + "', '" + str2 + "')")
    await QueryEX("INSERT INTO test VALUES ('" + str1 + "', '" + str2 + "')")
    ##conn.commit()

@bot.command(name = "test2")
async def test2(ctx, str1):
  if permisosCheck(ctx.author, 4):
    #c.execute ("SELECT * FROM test WHERE test_name = '" + str1 + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM test WHERE test_name = '" + str1 + "'")

    if len(items) == 0:
      await ctx.send("No hay nada")
    else:
      await ctx.send("1: " + items[0][0] + " 2: " + items[0][1])

@bot.command(name = "sql_create_db")
async def sql_create_db_cm(ctx):
  if ctx.author.id == OWNERID:
    await sql_create_db()

async def sql_create_db():
  await dbConnect()
  c = cursor

  c.execute("""CREATE TABLE IF NOT EXISTS test (test_name TEXT, test_str TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS muterole (guild_id TEXT, role_id TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS joinrole (guild_id TEXT, role_id TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS levels_ops (guild_id TEXT, option TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS levels (guild_id TEXT, user_id TEXT, points TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS levels_ops_roles (guild_id TEXT, role_id TEXT, level TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS levels_ops_channel (guild_id TEXT, channel_id TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS channel_log (guild_id TEXT, channel_id TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS warns (guild_id TEXT, user_id TEXT, razon TEXT, fecha TEXT, by TEXT, id TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS channel_message_log (guild_id TEXT, channel_id TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS privadas_guild_creadores (guild_id TEXT, channel_id TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS privadas_guild_creadas (guild_id TEXT, channel_id TEXT, creator_id TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS mute_temps (guild_id TEXT, user_id TEXT, fecha_unmute TEXT)""")

  c.execute("""CREATE TABLE IF NOT EXISTS anti_invite_ops (guild_id TEXT, option TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS anti_invite_ops_channel (guild_id TEXT, channel_id TEXT)""")
    
  c.execute("""CREATE TABLE IF NOT EXISTS global_ban_ops (guild_id TEXT, option TEXT)""")
  c.execute("""CREATE TABLE IF NOT EXISTS responses_messages (guild_id TEXT, key TEXT, respuesta TEXT, veces TEXT, try TEXT, id TEXT)""")

  c.execute("""CREATE TABLE IF NOT EXISTS chat_ia_ops (guild_id TEXT, option TEXT)""")

  conn.commit()

  await dbDisconnect()
  c = None

@bot.command(name = "sql_create_db_dm")
async def sql_create_db_dm(ctx):
  if ctx.author.id == OWNERID:
    await dbConnect()
    c = cursor

    c.execute("""CREATE TABLE IF NOT EXISTS dm_channels (user_name TEXT, user_discriminator TEXT, channel_id TEXT, user_id TEXT)""")

    conn.commit()

    await dbDisconnect()
    c = None

@bot.command(name = "sql_command")
async def sql_command(ctx, passw, comando):
  if ctx.author.id == OWNERID:
    if passw == "2b2tzk":
      #c.execute("" + comando + "")
      await QueryEX("" + comando + "")

    ##conn.commit()

@bot.command(name = "sql_create_db_gbban")
async def sql_create_db_gbban(ctx):
  if ctx.author.id == OWNERID:
    await dbConnect()
    c = cursor

    c.execute("""CREATE TABLE IF NOT EXISTS global_bans (user_id TEXT, user_name TEXT, user_discriminator TEXT, banned_server_name TEXT, banned_by TEXT, authorized_by TEXT, fecha TEXT, bot TEXT, user_image TEXT, user_image_censored TEXT, nivel_peligro TEXT, razon TEXT, id TEXT)""")

    conn.commit()

    await dbDisconnect()
    c = None

@bot.command(name = "level-enable")
async def level(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM levels_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    points = 0

    if len(items) == 0:
      #c.execute("INSERT INTO levels_ops VALUES ('" + str(ctx.guild.id) + "', 'enable')")
      await QueryEX("INSERT INTO levels_ops VALUES ('" + str(ctx.guild.id) + "', 'enable')")
      await ctx.send("Listo. Los niveles fueron activados.")
    else:
      #c.execute("UPDATE levels_ops SET option = 'enable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE levels_ops SET option = 'enable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. Los niveles fueron activados.")
    #conn.commit()

@bot.command(name = "level-disable")
async def level(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM levels_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    points = 0

    if len(items) == 0:
      #c.execute("INSERT INTO levels_ops VALUES ('" + str(ctx.guild.id) + "', 'disable')")
      await QueryEX("INSERT INTO levels_ops VALUES ('" + str(ctx.guild.id) + "', 'disable')")
      await ctx.send("Listo. Los niveles fueron desactivados.")
    else:
      #c.execute("UPDATE levels_ops SET option = 'disable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE levels_ops SET option = 'disable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. Los niveles fueron desactivados.")
    #conn.commit()

@bot.command(name = "level")
async def level(ctx, miembro: discord.Member = None):
  miembrose = ctx.author

  if miembro != None:
    miembrose = miembro

  #c.execute ("SELECT * FROM levels WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembrose.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM levels WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembrose.id) + "'")

  points = 0

  if len(items) == 0:
    pass
  else:
    points = int(items[0][2])

  level = int(points / 30)

  embed = discord.Embed(
  title = '**' + miembrose.name + '**',
  description = "Nivel: **" + str(level) + "**\n XP: " + str(points) + "/" + str(int((level + 1) * 30)),
  colour = discord.Colour.from_rgb(219, 0, 255)
  )
  embed.set_thumbnail(url=miembrose.avatar_url)
  await ctx.send(embed=embed)

async def add_points(user: discord.User, guild: discord.Guild, points: int):
  #c.execute ("SELECT * FROM levels WHERE guild_id = '" + str(guild.id) + "' AND user_id = '" + str(user.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM levels WHERE guild_id = '" + str(guild.id) + "' AND user_id = '" + str(user.id) + "'")

  points2 = 0 + points

  if len(items) == 0:
    #c.execute("INSERT INTO levels VALUES ('" + str(guild.id) + "', '" + str(user.id) + "', '" + str(points2) + "')")
    await QueryEX("INSERT INTO levels VALUES ('" + str(guild.id) + "', '" + str(user.id) + "', '" + str(points2) + "')")
  else:
    points2 = points2 + int(items[0][2])
    #c.execute("UPDATE levels SET points = '" + str(points2) + "' WHERE guild_id = '" + str(guild.id) + "' AND user_id = '" + str(user.id) + "'")
    await QueryEX("UPDATE levels SET points = '" + str(points2) + "' WHERE guild_id = '" + str(guild.id) + "' AND user_id = '" + str(user.id) + "'")
  #conn.commit()

  ##levels
  level = int(points2 / 30)
  #c.execute ("SELECT * FROM levels_ops_roles WHERE guild_id = '" + str(guild.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM levels_ops_roles WHERE guild_id = '" + str(guild.id) + "'")

  for item in items:
    if level >= int(item[2]):
      passe = False

      for rol in user.roles:
        if rol.id == int(item[1]):
          passe = True
          break

      if passe == False:
        role = get(user.guild.roles, id=int(item[1]))
        await user.add_roles(role)

@bot.command(name = "level-role-add")
async def level_role_add(ctx, nivel: int, rol: discord.Role):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM levels_ops_roles WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops_roles WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) >= 20:
      await ctx.send("Error: Ya tienes 20 roles asignados a los niveles, para agregar mas elimina uno.")
    else:
      #c.execute("INSERT INTO levels_ops_roles VALUES ('" + str(ctx.guild.id) + "', '" + str(rol.id) + "', '" + str(nivel) + "')")
      await QueryEX("INSERT INTO levels_ops_roles VALUES ('" + str(ctx.guild.id) + "', '" + str(rol.id) + "', '" + str(nivel) + "')")
      await ctx.send("Listo. El rol se asignara con el nivel especificado. Recuerda que el rol a asignar tiene que estar por debajo del rol de bot.")
    #conn.commit()

@bot.command(name = "level-role-remove")
async def level_role_remove(ctx, nivel: int):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM levels_ops_roles WHERE guild_id = '" + str(ctx.guild.id) + "' AND level = '" + str(nivel) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops_roles WHERE guild_id = '" + str(ctx.guild.id) + "' AND level = '" + str(nivel) + "'")

    if len(items) == 0:
      await ctx.send("Error: Rol por nivel no encontrado.")
    else:
      #c.execute("DELETE FROM levels_ops_roles WHERE guild_id = '" + str(ctx.guild.id) + "' AND level = '" + str(nivel) + "'")
      await QueryEX("DELETE FROM levels_ops_roles WHERE guild_id = '" + str(ctx.guild.id) + "' AND level = '" + str(nivel) + "'")
      await ctx.send("Listo. El rol de nivel se elimino.")
    #conn.commit()

@bot.command(name = "level-role-list")
async def level_role_list(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM levels_ops_roles WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops_roles WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("No tienes roles asignados a niveles.")
    else:
      texto = "> **Roles por nivel**:\n"
      for item in items:
        texto = texto + "\n> Nivel: **" + item[2] + "**\n> Rol: <@&" + item[1] + ">\n"
      await ctx.send(texto)
    #conn.commit()

@bot.command(name = "level-channel-add")
async def level_channel_add(ctx, channel: discord.TextChannel):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM levels_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) >= 20:
      await ctx.send("Error: Ya tienes 20 canales ignorados, para agregar mas elimina uno.")
    else:
      #c.execute("INSERT INTO levels_ops_channel VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await QueryEX("INSERT INTO levels_ops_channel VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await ctx.send("Listo. El canal especificado no dará experiencia para los niveles.")
    #conn.commit()

@bot.command(name = "level-channel-remove")
async def level_role_remove(ctx, channel: discord.TextChannel):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM levels_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

    if len(items) == 0:
      await ctx.send("Error: Canal no encontrado o no ignorado.")
    else:
      #c.execute("DELETE FROM levels_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
      await QueryEX("DELETE FROM levels_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
      await ctx.send("Listo. El canal se dejo de ignorar.")
    #conn.commit()

@bot.command(name = "level-channel-list")
async def level_channel_list(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM levels_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("No tienes canales ignorados.")
    else:
      texto = "> **Canales ignorados**:\n"
      for item in items:
        texto = texto + "\n> Canal: <#" + item[1] + ">\n"
      await ctx.send(texto)
    #conn.commit()

@bot.command(name = "level-admin-setxp")
async def level_admin_setxp(ctx, miembro: discord.Member, xp: int):
  if ctx.author.id == OWNERID:
    #c.execute ("SELECT * FROM levels WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")

    if len(items) == 0:
      #c.execute("INSERT INTO levels VALUES ('" + str(ctx.guild.id) + "', '" + str(miembro.id) + "', '" + str(xp) + "')")
      await QueryEX("INSERT INTO levels VALUES ('" + str(ctx.guild.id) + "', '" + str(miembro.id) + "', '" + str(xp) + "')")
      await ctx.send("Listo.")
    else:
      #c.execute("UPDATE levels SET points = '" + str(xp) + "' WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")
      await QueryEX("UPDATE levels SET points = '" + str(xp) + "' WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")
      await ctx.send("Listo.")
    #conn.commit()

@bot.command(name = "log-channel-set")
async def log_channel_set(ctx, channel: discord.TextChannel):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      #c.execute("INSERT INTO channel_log VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await QueryEX("INSERT INTO channel_log VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await ctx.send("Listo. El canal especificado se mostraran los cambios echos por el bot.")
    else:
      #c.execute("UPDATE channel_log SET channel_id = '" + str(channel.id) + "' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE channel_log SET channel_id = '" + str(channel.id) + "' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. El canal especificado se mostraran los cambios echos por el bot.")
    #conn.commit()

@bot.command(name = "log-channel-clear")
async def log_channel_clear(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("Error: No tienes un canal asignado.")
    else:
      #c.execute("DELETE FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("DELETE FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo.")
    #conn.commit()

@bot.command(name = "warn")
async def warn(ctx, miembro: discord.Member, *razon:str):
  if not razon:
    await ctx.send("Por favor ingrese una razón.")
    return
  razon = ' '.join(razon)
  await func_warn(ctx, miembro, razon, True)

async def func_warn(ctx, miembro: discord.Member, razon: str = "Sin razón", manual: bool = True):
  if manual and permisosCheck(ctx.author, 1):
    if miembro == ctx.author:
      await ctx.send("Te vas a autowarnear?")
      return
    
    #c.execute ("SELECT * FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")

    #c.execute("INSERT INTO warns VALUES ('" + str(ctx.guild.id) + "', '" + str(miembro.id) + "', '" + razon + "', '" + str(datetime.datetime.today()) + "', '" + str(ctx.author.id) + "', '" + str(len(items) + 1) + "')")
    await QueryEX("INSERT INTO warns VALUES ('" + str(ctx.guild.id) + "', '" + str(miembro.id) + "', '" + razon + "', '" + str(datetime.datetime.today()) + "', '" + str(ctx.author.id) + "', '" + str(len(items) + 1) + "')")
    #conn.commit()

    embed = discord.Embed(
          title = '**Advertencia**',
          description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">\n Razon: " + razon,
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
    embed.set_thumbnail(url=miembro.avatar_url)
    
    await ctx.send(embed=embed)

    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      channel = bot.get_channel(int(items[0][1]))
      await channel.send(embed=embed)
  else:
    if not manual:
      #c.execute ("SELECT * FROM warns WHERE guild_id = '" + str(miembro.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM warns WHERE guild_id = '" + str(miembro.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")

      #c.execute("INSERT INTO warns VALUES ('" + str(ctx.guild.id) + "', '" + str(miembro.id) + "', '" + razon + "', '" + str(datetime.datetime.today()) + "', '" + str(ctx.author.id) + "', '" + str(len(items) + 1) + "')")
      await QueryEX("INSERT INTO warns VALUES ('" + str(miembro.guild.id) + "', '" + str(miembro.id) + "', '" + razon + "', '" + str(datetime.datetime.today()) + "', '" + str(bot.user.id) + "', '" + str(len(items) + 1) + "')")
      #conn.commit()

      embed = discord.Embed(
          title = '**Advertencia**',
          description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(bot.user.id) + ">\n Razon: " + razon,
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
      embed.set_thumbnail(url=miembro.avatar_url)

      #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(miembro.guild.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(miembro.guild.id) + "'")

      if len(items) > 0:
        channel = bot.get_channel(int(items[0][1]))
        await channel.send(embed=embed)

@bot.command(name = "infractions")
async def infractions(ctx, miembro: discord.Member):
  if permisosCheck(ctx.author, 1):
    #c.execute ("SELECT * FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")

    if len(items) == 0:
      await ctx.send("El miembro no tiene advertencias.")
    else:
      embed = discord.Embed(
          title = '**Advertencia**',
          description = "Miembro: <@" + str(miembro.id) + ">",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
      embed.set_thumbnail(url=miembro.avatar_url)

      for item in items:
        embed.add_field(name="Advertencia n° " + item[5], value= "Por: <@" + item[4] + "> \n Razon: " + item[2] + "\n Fecha: " + item[3])
      await ctx.send(embed=embed)

@bot.command(name = "clear-infraction")
async def clear_infraction(ctx, miembro: discord.Member, id: int):
  if permisosCheck(ctx.author, 2):
    #c.execute("DELETE FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "' AND id ='" + str(id) + "'")
    await QueryEX("DELETE FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "' AND id ='" + str(id) + "'")
    ##conn.commit()
    await ctx.send("Listo. Advertencia n° " + str(id) + ". Eliminada.")

    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      channel = bot.get_channel(int(items[0][1]))
      embed = discord.Embed(
          title = '**Eliminar una advertencia**',
          description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
      embed.set_thumbnail(url=miembro.avatar_url)
      await channel.send(embed=embed)


@bot.command(name = "clear-all-infractions")
async def clear_all_infractions(ctx, miembro: discord.Member):
  if permisosCheck(ctx.author, 2):
    #c.execute("DELETE FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")
    await QueryEX("DELETE FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(miembro.id) + "'")
    ##conn.commit()
    await ctx.send("Listo. Todas las advertencias del miembro fueron eliminadas.")
    
    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      channel = bot.get_channel(int(items[0][1]))
      embed = discord.Embed(
          title = '**Eliminar todas las dvertencias**',
          description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
      embed.set_thumbnail(url=miembro.avatar_url)
      await channel.send(embed=embed)

@bot.command(name = "ota-global-ban")
async def ota_global_ban(ctx):
  
  embed = discord.Embed(
  title = ':warning: **OTA BAN GLOBAL**',
  description = "El sistema de ban global de la **OTAKU ARMY** se encarga de asegurar y banear a todos los usuarios y bots de Discord que puedan suponer un peligro para los servidores. El sistema esta controlado por el Staff de la **OTAKU ARMY** y nos comprometemos a tener completa seriedad con este sistema que es opcional en este bot. Al activar nos autorizas a banear a usuarios y bots que supongan un peligro para Discord o que hayan incumplido las **Directivas de la comunidad de Discord** o las **Condiciones del servicio de Discord**. Puedes desactivarlo en cualquier momento. Se recomienda tener los logs del bot activado para recibir los avisos de baneos globales y su información.",
  colour = discord.Colour.from_rgb(255, 0, 0)
  )
  embed.add_field(name=":white_check_mark: **ACTIVAR**", value="<:admtag:860610530489663518> `sh!ota-global-ban-enable`")
  embed.add_field(name="<:x_:853161029864128512> **DESACTIVAR**", value="<:admtag:860610530489663518> `sh!ota-global-ban-disable`")
  embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
  await ctx.send(embed=embed)

@bot.command(name = "ota-global-ban-enable")
async def ota_global_ban_enable(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    points = 0

    if len(items) == 0:
      #c.execute("INSERT INTO global_ban_ops VALUES ('" + str(ctx.guild.id) + "', 'enable')")
      await QueryEX("INSERT INTO global_ban_ops VALUES ('" + str(ctx.guild.id) + "', 'enable')")
    else:
      #c.execute("UPDATE global_ban_ops SET option = 'enable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE global_ban_ops SET option = 'enable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #conn.commit()

    embed = discord.Embed(
    title = ':warning: **OTA BAN GLOBAL**',
    description = ":white_check_mark: El sistema de baneos globales de la **OTAKU ARMY** fue activado.",
    colour = discord.Colour.from_rgb(255, 0, 0)
    )
    embed.add_field(name="<:x_:853161029864128512> **DESACTIVAR**", value="<:admtag:860610530489663518> `sh!ota-global-ban-disable`")
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
    await ctx.send(embed=embed)

@bot.command(name = "ota-global-ban-disable")
async def ota_global_ban_disable(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    points = 0

    if len(items) > 0:
      #c.execute("DELETE FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("DELETE FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #conn.commit()

    embed = discord.Embed(
    title = ':warning: **OTA BAN GLOBAL**',
    description = "<:x_:853161029864128512> El sistema de baneos globales de la **OTAKU ARMY** fue desactivado.",
    colour = discord.Colour.from_rgb(255, 0, 0)
    )
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
    await ctx.send(embed=embed)

@bot.command(name = "log-message-set")
async def log_channel_set(ctx, channel: discord.TextChannel):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM channel_message_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_message_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      #c.execute("INSERT INTO channel_message_log VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await QueryEX("INSERT INTO channel_message_log VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await ctx.send("Listo. El canal especificado se mostraran los logs de mensajes.")
    else:
      #c.execute("UPDATE channel_message_log SET channel_id = '" + str(channel.id) + "' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE channel_message_log SET channel_id = '" + str(channel.id) + "' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. El canal especificado se mostraran los logs de mensajes.")
    #conn.commit()

@bot.command(name = "log-message-clear")
async def log_channel_clear(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM channel_message_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_message_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("Error: No tienes un canal asignado.")
    else:
      #c.execute("DELETE FROM channel_message_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("DELETE FROM channel_message_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo.")
    #conn.commit()

@bot.command(name = "lock")
async def lock(ctx, channel : discord.TextChannel=None):
  if permisosCheck(ctx.author, 2):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("Listo. Canal bloqueado.")

    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      channel = bot.get_channel(int(items[0][1]))
      embed = discord.Embed(
          title = '**Bloquear canal**',
          description = "Canal: <#" + str(ctx.channel.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
      embed.set_thumbnail(url=ctx.author.avatar_url)
      await channel.send(embed=embed)

@bot.command(name = "unlock")
async def unlock(ctx, channel : discord.TextChannel=None):
  if permisosCheck(ctx.author, 2):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("Listo. Canal desbloqueado.")

@bot.command(name = "hide")
async def hide(ctx, channel : discord.TextChannel=None):
  if permisosCheck(ctx.author, 2):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.view_channel = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("Listo. Canal ocultado.")

    #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      channel = bot.get_channel(int(items[0][1]))
      embed = discord.Embed(
          title = '**Ocultar canal**',
          description = "Canal: <#" + str(ctx.channel.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
      embed.set_thumbnail(url=ctx.author.avatar_url)
      await channel.send(embed=embed)

@bot.command(name = "unhide")
async def unhide(ctx, channel : discord.TextChannel=None):
  if permisosCheck(ctx.author, 2):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.view_channel = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("Listo. Canal revelado.")

@bot.command(name = "voice-help")
async def voice_help(ctx):
  await cmd_embed.ex("voice help", ctx.channel.id, ctx, bot)

@bot.command(name = "voice-create-hub")
async def voice_create_hub(ctx):
  if permisosCheck(ctx.author, 2):
    guild = ctx.guild
    overwrites = {
      guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    channel = await guild.create_voice_channel("Entra para crear privado", overwrites=overwrites)

    #c.execute ("SELECT * FROM privadas_guild_creadores WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM privadas_guild_creadores WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      #c.execute("INSERT INTO privadas_guild_creadores VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await QueryEX("INSERT INTO privadas_guild_creadores VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await ctx.send("Listo. Se creo el canal de voz para crear privadas.")
    else:
      #c.execute("UPDATE privadas_guild_creadores SET channel_id = '" + str(channel.id) + "' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE privadas_guild_creadores SET channel_id = '" + str(channel.id) + "' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. Se creo el canal de voz para crear privadas.")
    #conn.commit()

@bot.command(name = "voice-ban")
async def voice_ban(ctx, miembro: discord.Member):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return
    
  channel = ctx.author.voice.channel

  if channel == None:
    return

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(miembro.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(miembro.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      overwrite = channel.overwrites_for(miembro)
      overwrite.connect = False
      await channel.set_permissions(miembro, overwrite=overwrite)

      await ctx.send("Listo miembro baneado del canal privado.")

      if miembro.voice.channel == channel:
        await miembro.move_to(None)
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "voice-unban")
async def voice_unban(ctx, miembro: discord.Member):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return

  channel = ctx.author.voice.channel

  if channel == None:
    return

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(miembro.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(miembro.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      overwrite = channel.overwrites_for(miembro)
      overwrite.connect = True
      await channel.set_permissions(miembro, overwrite=overwrite)

      await ctx.send("Listo miembro desbaneado del canal privado.")
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "voice-kick")
async def voice_kick(ctx, miembro: discord.Member):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return

  channel = ctx.author.voice.channel
  
  if channel == None:
    return

  if miembro.voice.channel != channel:
    return

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(miembro.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(miembro.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      await miembro.move_to(None)
      await ctx.send("Listo miembro desconectado del canal privado.")
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "voice-rename")
async def voice_rename(ctx, nombre: str = "Privado"):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return

  contenidonew = (nombre[:20]) if len(nombre) > 20 else nombre

  channel = ctx.author.voice.channel
  
  if channel == None:
    return

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      await channel.edit(name="🔒 " + contenidonew)
      await ctx.send("Listo. Canal renombrado.")
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "voice-hide")
async def voice_hide(ctx):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return

  channel = ctx.author.voice.channel

  if channel == None:
    return

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.view_channel = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

      await ctx.send("Listo. canal escondido.")
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "voice-unhide")
async def voice_unhide(ctx):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return

  channel = ctx.author.voice.channel

  if channel == None:
    return

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.view_channel = True
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

      await ctx.send("Listo. canal revelado.")
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "voice-limit")
async def voice_limit(ctx, limite: int = 6):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return

  channel = ctx.author.voice.channel

  if channel == None:
    return

  if limite < 0:
    limite = 0

  if limite > 99:
    limite = 99

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      await channel.edit(user_limit=limite)

      await ctx.send("Listo. Limite editado.")
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "voice-lock")
async def voice_lock(ctx):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return

  channel = ctx.author.voice.channel

  if channel == None:
    return

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.connect = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

      await ctx.send("Listo. canal bloqueado.")
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "voice-unlock")
async def voice_unlock(ctx):
  if not ctx.author.voice:
    await ctx.send("No estas en un chat de voz.")
    return

  channel = ctx.author.voice.channel

  if channel == None:
    return

  #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

  if len(items) > 0:
    if items[0][2] == str(ctx.author.id):
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.connect = True
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

      await ctx.send("Listo. canal desbloqueado.")
    else:
      await ctx.send("No eres el creador del canal privado.")

@bot.command(name = "ota-global-ban-info")
async def ota_global_ban_info(ctx, user: discord.User):
  if True:
    #c.execute ("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      #c.execute ("SELECT * FROM global_bans WHERE user_id = '" + str(user.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM global_bans WHERE user_id = '" + str(user.id) + "'")

      if len(items) > 0:
        await ctx.channel.trigger_typing()
        await asyncio.sleep(1)
        msg = await ctx.send("Buscando información...")
        await ctx.channel.trigger_typing()
        items[0][0]

        bannerds = bot.get_user(int(items[0][4]))

        await asyncio.sleep(4)

        embed = discord.Embed(
        title = '**BANEO GLOBAL**',
        description = "**Usuario:** " + items[0][1] + "#" + items[0][2] + "\n**ID:** " + items[0][0] + "\n**Censurado:** " + items[0][9] + "\n**Servidor de origen:** " + items[0][3] + "\n**Nivel:** **" + items[0][10] + "**\n**Razon:** " + items[0][11] + "\n**Fecha:** " + items[0][6] + "\n**Bot:** " + items[0][7] + "\n**Autor del baneo global:** <@" + items[0][4] + ">\n**Autorizado por:** <@" + items[0][5] + ">\n **GB ID:** " + items[0][12],
        colour = discord.Colour.from_rgb(255, 0, 0)
        )
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
        embed.set_author(name=bannerds.name + "#" + str(bannerds.discriminator) + " ID: " + str(bannerds.id), icon_url=bannerds.avatar_url)

        if items[0][9] == "si":
          embed.set_image(url="https://www.yoinfluyo.com/images/stories/hoy/ago18/150818/censura_nationalgeo.png")
        else:
          embed.set_image(url=items[0][8])

        await msg.delete()
        await ctx.send(embed=embed)
      else:
        await ctx.send("No hay información sobre este usuario y no es afectado por el sistema.")
    else:
      await ctx.send("El sistema de ban global de la **OTAKU ARMY** no se encuentra activo en este servidor, para acceder a esta información primero actívalo.")

@bot.command(name = "ota-global-ban-report")
async def ota_global_ban_report(ctx, user: discord.User, informacion: str = "n/a"):
  if permisosCheck(ctx.author, 1):
    #c.execute ("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      await ctx.channel.trigger_typing()
      await asyncio.sleep(1)
      embed = discord.Embed(
      title = '**REPORTE DE USUARIO**',
      description = "**Usuario:** " + user.name + "#" + str(user.discriminator) + "\n**ID:** " + str(user.id) + "\n**Servidor de origen:** " + ctx.guild.name + "\n**Información:** " + informacion,
      colour = discord.Colour.from_rgb(255, 0, 0)
      )
      embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
      embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator) + " ID: " + str(ctx.author.id), icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      await ctx.channel.trigger_typing()
      channel_report = bot.get_channel(866456211980288002)
      await channel_report.send(embed=embed)
      await asyncio.sleep(4)
      await ctx.send("Gracias por enviar un informe. Mientras lo revisamos, el usuario seguirán estando. Si al revisarlo descubrimos que este usuario ha infringido las Directivas de la comunidad de Discord, las Condiciones del servicio de Discord o suponga un peligro para Discord, adoptaremos las medidas necesarias.")
    else:
      await ctx.send("El sistema de ban global de la **OTAKU ARMY** no se encuentra activo en este servidor, para acceder a esta función primero actívalo.")

@bot.command(name = "anti-invite-enable")
async def anti_invite_enable(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM anti_invite_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM anti_invite_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      #c.execute("INSERT INTO anti_invite_ops VALUES ('" + str(ctx.guild.id) + "', 'enable')")
      await QueryEX("INSERT INTO anti_invite_ops VALUES ('" + str(ctx.guild.id) + "', 'enable')")
      await ctx.send("Listo. El sistema anti invitaciones fue activado.")
    else:
      #c.execute("UPDATE anti_invite_ops SET option = 'enable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE anti_invite_ops SET option = 'enable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. El sistema anti invitaciones fue activado.")
    #conn.commit()

@bot.command(name = "anti-invite-disable")
async def anti_invite_disable(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM anti_invite_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM anti_invite_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      #c.execute("INSERT INTO anti_invite_ops VALUES ('" + str(ctx.guild.id) + "', 'disable')")
      await QueryEX("INSERT INTO anti_invite_ops VALUES ('" + str(ctx.guild.id) + "', 'disable')")
      await ctx.send("Listo. El sistema anti invitaciones fue desactivado.")
    else:
      #c.execute("UPDATE anti_invite_ops SET option = 'disable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await QueryEX("UPDATE anti_invite_ops SET option = 'disable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. El sistema anti invitaciones fue desactivado.")
    #conn.commit()

@bot.command(name = "anti-invite-ignore-channel-add")
async def level_channel_add(ctx, channel: discord.TextChannel):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM anti_invite_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM anti_invite_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) >= 20:
      await ctx.send("Error: Ya tienes 20 canales ignorados, para agregar mas elimina uno.")
    else:
      #c.execute("INSERT INTO anti_invite_ops_channel VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await QueryEX("INSERT INTO anti_invite_ops_channel VALUES ('" + str(ctx.guild.id) + "', '" + str(channel.id) + "')")
      await ctx.send("Listo. El canal especificado sera ignorado.")
    #conn.commit()

@bot.command(name = "anti-invite-ignore-channel-remove")
async def level_channel_remove(ctx, channel: discord.TextChannel):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM anti_invite_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM anti_invite_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")

    if len(items) == 0:
      await ctx.send("Error: Canal no encontrado o no ignorado.")
    else:
      #c.execute("DELETE FROM anti_invite_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
      await QueryEX("DELETE FROM anti_invite_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "' AND channel_id = '" + str(channel.id) + "'")
      await ctx.send("Listo. El canal se dejo de ignorar.")
    #conn.commit()

@bot.command(name = "anti-invite-ignore-channel-list")
async def level_channel_list(ctx):
  if permisosCheck(ctx.author, 2):
    #c.execute ("SELECT * FROM anti_invite_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM anti_invite_ops_channel WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("No tienes canales ignorados.")
    else:
      texto = "> **Canales ignorados**:\n"
      for item in items:
        texto = texto + "\n> Canal: <#" + item[1] + ">\n"
      await ctx.send(texto)
    #conn.commit()

@bot.command(name = "chat-ia-enable")
async def chat_ia_enable(ctx):
  if permisosCheck(ctx.author, 2):
    items = await QueryGET("SELECT * FROM chat_ia_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await QueryEX("INSERT INTO chat_ia_ops VALUES ('" + str(ctx.guild.id) + "', 'enable')")
      await ctx.send("Listo. Las respuestas con IA fueron activadas.")
    else:
      await QueryEX("UPDATE chat_ia_ops SET option = 'enable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. Las respuestas con IA fueron activadas.")

@bot.command(name = "chat-ia-disable")
async def chat_ia_disable(ctx):
  if permisosCheck(ctx.author, 2):
    items = await QueryGET("SELECT * FROM chat_ia_ops WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await QueryEX("INSERT INTO chat_ia_ops VALUES ('" + str(ctx.guild.id) + "', 'disable')")
      await ctx.send("Listo. Las respuestas con IA fueron desactivadas.")
    else:
      await QueryEX("UPDATE chat_ia_ops SET option = 'disable' WHERE guild_id = '" + str(ctx.guild.id) + "'")
      await ctx.send("Listo. Las respuestas con IA fueron desactivadas.")

@bot.command(name = "banner")
async def banner(ctx, miembro:discord.Member = None):
  user = miembro
  if user == None:
      user = ctx.author
  req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
  banner_id = req["banner"]
  # If statement because the user may not have a banner
  if banner_id:
    banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
    await ctx.send(f"{banner_url}")
  else:
    await ctx.send("El miembro no tiene banner")

## MODERATION OTA

@bot.command(name = "mod")
async def boton(ctx, miembro:discord.Member):
  user = miembro

  if permisosCheck(ctx.author, 1):
    #if ctx.guild.id != 848833707426578472: #Cambiar ID de Servidor
      #return

    if not user or user == None:
      await ctx.send("Error, por favor ingrese un miembro.")
      return

    if user.id == bot.user.id:
      await ctx.send("Error, por favor ingrese un miembro.")
      return

    await ctx.message.delete()

    embed = discord.Embed(
            title = '**VERIFICAR USUARIO**',
            description = "El usuario fue encontrado como: <@" + str(user.id) + "> (" + user.name + "#" + str(user.discriminator) + ") \nID: " + str(user.id) + "\n\n\n **Verifica que el usuario sea el correcto.**",
            colour = discord.Colour.from_rgb(255, 0, 255)
            )
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
    embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator) + " ID: " + str(ctx.author.id), icon_url=ctx.author.avatar_url)
    embed.set_image(url=user.avatar_url)
    embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)
    mensaje = await ctx.send(embed=embed,
          components = [
              [Button(style=ButtonStyle.green, label = "Confirmar", custom_id="button1"),
              Button(style=ButtonStyle.red, label = "Cancelar", custom_id="button2")],
          ],
      )
    
    if True:
    #while True:
      interaction = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)

      if interaction.custom_id == "button1":
        if permisosCheck(ctx.author, 1):
          await interaction.respond(content="Confirmado con éxito, por favor seleccione la regla que incumplió el miembro.")

          embed2 = discord.Embed(
                  title = '**INFORMACIÓN DEL USUARIO**',
                  description = "Infracciones de <@" + str(user.id) + "> (" + user.name + "#" + str(user.discriminator) + ") \nID: " + str(user.id) + ":",
                  colour = discord.Colour.from_rgb(255, 0, 255)
                  )
          embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
          embed2.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator) + " ID: " + str(ctx.author.id), icon_url=ctx.author.avatar_url)
          embed2.set_image(url=user.avatar_url)
          embed2.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)

          items = await QueryGET("SELECT * FROM warns WHERE guild_id = '" + str(ctx.guild.id) + "' AND user_id = '" + str(user.id) + "'")

          rol = ""
          if permisosCheck(miembro, 3):
            rol = rol +"Dueño del server, "
          if permisosCheck(miembro, 2):
            rol = rol + "Administrador, "
          if permisosCheck(miembro, 1):
            rol = rol + "Moderador, "
          rol = rol + "Miembro"

          embed2.add_field(name=":information_source: Información del miembro", value="Toda la información resumida del miembro.", inline=False)
          embed2.add_field(name="Entró al Servidor el", value=miembro.joined_at.strftime("%b %d, %Y %H:%M:%S"))
          embed2.add_field(name="Entró a Discord el", value=miembro.created_at.strftime("%b %d, %Y %H:%M:%S"))
          if miembro.premium_since == None:
            embed2.add_field(name="Mejorando desde", value="No")
          else:
            embed2.add_field(name="Mejorando desde", value=miembro.premium_since.strftime("%b %d, %Y %H:%M:%S"))
          embed2.add_field(name="Discriminador", value=miembro.discriminator)
          embed2.add_field(name="ID", value=str(miembro.id))

          if len(items) == 0:
            embed2.add_field(name="<:a:853161030052741151> Todo en orden", value="El miembro no tiene advertencias.", inline=False)
          else:
            for item in items:
              embed2.add_field(name="Advertencia n° " + item[5], value= "Por: <@" + item[4] + "> \n Razon: " + item[2] + "\n Fecha: " + item[3], inline=False)

          await mensaje.edit(embed=embed2, components = [
          [Button(style=ButtonStyle.red, label = "🚨 Punir", custom_id="Punir"),
          Button(style=ButtonStyle.grey, label = "❌ Terminar", custom_id="Cancelar")],
          ])
          
          if True:
          #while True:
            interaction = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)

            if interaction.custom_id == "Punir":
              if permisosCheck(ctx.author, 1):
                await interaction.respond(content="Entrando al menú de punición.")
                await mod_menu_reglas(ctx, user, mensaje, embed, embed2, 1)

            if interaction.custom_id == "Cancelar":
              if permisosCheck(interaction.user, 1):
                embed = discord.Embed(
                        title = '**VERIFICAR USUARIO**',
                        description = "Miembro: <@" + str(user.id) + "> (" + user.name + "#" + str(user.discriminator) + ") \nID: " + str(user.id) + "\n\n\n **Todo correcto.**",
                        colour = discord.Colour.from_rgb(255, 0, 255)
                        )
                embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
                embed.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator) + " ID: " + str(ctx.author.id), icon_url=ctx.author.avatar_url)
                embed.set_image(url=user.avatar_url)
                embed.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)
                await interaction.respond(content="Terminado con éxito.")
                await mensaje.edit("<:a:853161030052741151> **Terminado**", embed=embed, components=[])

      if interaction.custom_id == "button2":
        if permisosCheck(interaction.user, 1):
          await interaction.respond(content="Cancelado con éxito.")
          await mensaje.edit("<:a:853161029864128512> **Cancelado**", embed=embed, components=[])

async def mod_menu_reglas(ctx, miembro, mensaje, embed, embed2, pagina):
  if pagina == 1:
    await mensaje.edit(embed=embed2, components = [
      Button(style=ButtonStyle.grey, label = "Mandar contenido inapropiado.", custom_id="R1"),
      Button(style=ButtonStyle.grey, label = "Mandar contenido inapropiado que perjudique a los streamers.", custom_id="R2"),
      Button(style=ButtonStyle.grey, label = "Mandar información privada.", custom_id="R3"),
      Button(style=ButtonStyle.grey, label = "Pasar invitaciones a otros servidores.", custom_id="R4"),
      Button(style=ButtonStyle.blue, label = "Siguiente ➡", custom_id="Siguiente1"),
      #Button(style=ButtonStyle.grey, label = "Tener una actitud tóxica.", custom_id="R5"),
      #Button(style=ButtonStyle.grey, label = "Hacer mal uso de los canales temáticos.", custom_id="R6"),
      #Button(style=ButtonStyle.grey, label = "Hacer un excesivo spam o flood en los canales.", custom_id="R7"),
      #Button(style=ButtonStyle.grey, label = "Abusar de las menciones sin justificación alguna.", custom_id="R8"),
      #Button(style=ButtonStyle.grey, label = "Transmitir contenido NSFW.", custom_id="R9"),
      #Button(style=ButtonStyle.grey, label = "Transmitir contenido NSFW.", custom_id="R10"),
      #Button(style=ButtonStyle.grey, label = "Mantener una actitud tóxica.", custom_id="R11"),
      #Button(style=ButtonStyle.grey, label = "Alterar el ambiente de la llamada.", custom_id="R12"),
      #Button(style=ButtonStyle.grey, label = "Saturar el audio.", custom_id="R13"),
      #Button(style=ButtonStyle.grey, label = "Violación de Guidelines y ToS de Discord.", custom_id="R14"),
      #Button(style=ButtonStyle.grey, label = "Ingresar multicuentas al servidor.", custom_id="R15"),
      #Button(style=ButtonStyle.grey, label = "Preparar o realizar raideos a servidores.", custom_id="R16"),
      #Button(style=ButtonStyle.grey, label = "❌ Cancelar", custom_id="Cancelar"),
      ])

  if pagina == 2:
    await mensaje.edit(embed=embed2, components = [
      Button(style=ButtonStyle.grey, label = "Tener una actitud tóxica.", custom_id="R5"),
      Button(style=ButtonStyle.grey, label = "Hacer mal uso de los canales temáticos.", custom_id="R6"),
      Button(style=ButtonStyle.grey, label = "Hacer un excesivo spam o flood en los canales.", custom_id="R7"),
      Button(style=ButtonStyle.grey, label = "Abusar de las menciones sin justificación alguna.", custom_id="R8"),
      Button(style=ButtonStyle.blue, label = "Siguiente ➡", custom_id="Siguiente2"),
      ])

  if pagina == 3:
    await mensaje.edit(embed=embed2, components = [
      Button(style=ButtonStyle.grey, label = "Transmitir contenido NSFW.", custom_id="R9"),
      Button(style=ButtonStyle.grey, label = "Mantener una actitud tóxica.", custom_id="R10"),
      Button(style=ButtonStyle.grey, label = "Alterar el ambiente de la llamada.", custom_id="R11"),
      Button(style=ButtonStyle.grey, label = "Saturar el audio.", custom_id="R12"),
      Button(style=ButtonStyle.blue, label = "Siguiente ➡", custom_id="Siguiente3"),
      ])

  if pagina == 4:
    await mensaje.edit(embed=embed2, components = [
      Button(style=ButtonStyle.grey, label = "Violación de Guidelines y ToS de Discord.", custom_id="R13"),
      Button(style=ButtonStyle.grey, label = "Ingresar multicuentas al servidor.", custom_id="R14"),
      Button(style=ButtonStyle.grey, label = "Preparar o realizar raideos a servidores.", custom_id="R15"),
      Button(style=ButtonStyle.grey, label = "❌ Cancelar", custom_id="Cancelar"),
      Button(style=ButtonStyle.blue, label = "Siguiente ➡", custom_id="Siguiente5"),
      ])

  if pagina == 5:
    await mensaje.edit(embed=embed2, components = [
      Button(style=ButtonStyle.grey, label = "❌ Cancelar", custom_id="Cancelar"),
      Button(style=ButtonStyle.blue, label = "Siguiente ➡", custom_id="Siguiente5"),
      ])

  if True:
  #while True:
    interaction = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
    if permisosCheck(ctx.author, 1):
      reglaID = interaction.custom_id
      reglaLabel = interaction.component.label

      if interaction.custom_id == "Siguiente1":
        if permisosCheck(ctx.author, 1):
          await interaction.respond(content="Siguiente pagina.")
          await mod_menu_reglas(ctx, miembro, mensaje, embed, embed2, 2)
          return

      if interaction.custom_id == "Siguiente2":
        if permisosCheck(ctx.author, 1):
          await interaction.respond(content="Siguiente pagina.")
          await mod_menu_reglas(ctx, miembro, mensaje, embed, embed2, 3)
          return

      if interaction.custom_id == "Siguiente3":
        if permisosCheck(ctx.author, 1):
          await interaction.respond(content="Siguiente pagina.")
          await mod_menu_reglas(ctx, miembro, mensaje, embed, embed2, 4)
          return

      if interaction.custom_id == "Siguiente4":
        if permisosCheck(ctx.author, 1):
          await interaction.respond(content="Siguiente pagina.")
          await mod_menu_reglas(ctx, miembro, mensaje, embed, embed2, 5)
          return

      if interaction.custom_id == "Siguiente5":
        if permisosCheck(ctx.author, 1):
          await interaction.respond(content="Siguiente pagina.")
          await mod_menu_reglas(ctx, miembro, mensaje, embed, embed2, 1)
          return

      if interaction.custom_id == "Cancelar":
        if permisosCheck(ctx.author, 1):
          await interaction.respond(content="Cancelado con éxito.")
          await mensaje.edit("<:a:853161029864128512> **Cancelado**", embed=embed, components=[])
          return

      await interaction.respond(content="Continuado con éxito, por favor ahora seleccione una medida a tomar.")
      await mod_menu_medidas(ctx, miembro, mensaje, embed, embed2, reglaID, reglaLabel, 1)

async def mod_menu_medidas(ctx, miembro, mensaje, embed, embed2, reglaID, reglaLabel, pagina):
  user = miembro

  if pagina == 1:
    await mensaje.edit(embed=embed2, components=[
    Button(style=ButtonStyle.red, label = "Advertencia.", custom_id="M1"),
    Button(style=ButtonStyle.red, label = "Advertencia, Muteo temporal por 2 horas.", custom_id="M2"),
    Button(style=ButtonStyle.red, label = "Advertencia, Muteo temporal por 7 días.", custom_id="M3"),
    Button(style=ButtonStyle.red, label = "Advertencia, Muteo temporal por 30 días.", custom_id="M4"),
    Button(style=ButtonStyle.blue, label = "Siguiente ➡", custom_id="Siguiente1"),
    #Button(style=ButtonStyle.red, label = "Advertencia, Muteo permanente", custom_id="M5"),
    #Button(style=ButtonStyle.red, label = "Advertencia, Baneo permanente.", custom_id="M6"),
    #Button(style=ButtonStyle.green, label = "❌ Cancelar", custom_id="Cancelar"),
    #Button(style=ButtonStyle.blue, label = "Siguiente ➡", custom_id="Siguiente2"),
    ])

  if pagina == 2:
    await mensaje.edit(embed=embed2, components=[
    Button(style=ButtonStyle.red, label = "Advertencia, Muteo permanente", custom_id="M5"),
    Button(style=ButtonStyle.red, label = "Advertencia, Baneo permanente.", custom_id="M6"),
    Button(style=ButtonStyle.green, label = "❌ Cancelar", custom_id="Cancelar"),
    Button(style=ButtonStyle.blue, label = "Siguiente ➡", custom_id="Siguiente2"),
    ])

  if True:
  #while True:
    interaction = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
    if permisosCheck(ctx.author, 1):
      medidaID = interaction.custom_id
      medidaLabel = interaction.component.label

      if interaction.custom_id == "Siguiente1":
          if permisosCheck(ctx.author, 1):
            await interaction.respond(content="Siguiente pagina.")
            await mod_menu_medidas(ctx, miembro, mensaje, embed, embed2, reglaID, reglaLabel, 2)
            return

      if interaction.custom_id == "Siguiente2":
          if permisosCheck(ctx.author, 1):
            await interaction.respond(content="Siguiente pagina.")
            await mod_menu_medidas(ctx, miembro, mensaje, embed, embed2, reglaID, reglaLabel, 1)
            return

      if interaction.custom_id == "Cancelar":
          if permisosCheck(ctx.author, 1):
            await interaction.respond(content="Cancelado con éxito.")
            await mensaje.edit("<:a:853161029864128512> **Cancelado**", embed=embed, components=[])
            return

      embed3 = discord.Embed(
        title = '**MEDIDAS TOMADAS**',
        description = "Contra el usuario: <@" + str(user.id) + "> (" + user.name + "#" + str(user.discriminator) + ") \nID: " + str(user.id) + "\n **Razon:** " + reglaLabel +" \n **Medidas:** " + medidaLabel,
        colour = discord.Colour.from_rgb(255, 0, 0)
        )
      embed3.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
      embed3.set_author(name=ctx.author.name + "#" + str(ctx.author.discriminator) + " ID: " + str(ctx.author.id), icon_url=ctx.author.avatar_url)
      embed3.set_image(url=user.avatar_url)
      embed3.set_footer(text = 'Solicitado por ' + ctx.author.name + "#" + ctx.author.discriminator)
      await interaction.respond(content="Listo todo correcto, tomando medidas.")
      await mensaje.edit("<:a:853161030052741151> **Medidas tomadas con exito**", embed=embed3, components=[])

      await mod_medidas(ctx, miembro, mensaje, reglaID, reglaLabel, medidaID, medidaLabel)

async def mod_medidas(ctx, miembro, mensaje, reglaID, reglaLabel, medidaID, medidaLabel):
  if medidaID == "M1":
    await func_warn(ctx.channel, miembro, reglaLabel, False)
    await miembro.send("Hola, has recibido una advertencia por `" + reglaLabel + "` dentro del servidor de **" + ctx.guild.name + "**. Te recomendamos leer las reglas del servidor y las Directivas de la comunidad de Discord https://discord.com/guidelines para no tener mas inconvenientes.")
    return
  if medidaID == "M2":
    await func_tempmute(ctx.channel, miembro, "2h", False)
    await func_warn(ctx.channel, miembro, reglaLabel, False)
    await miembro.send("Hola, has recibido una advertencia y has sido silenciado por 2 horas por `" + reglaLabel + "` dentro del servidor de **" + ctx.guild.name + "**. Te recomendamos leer las reglas del servidor y las Directivas de la comunidad de Discord https://discord.com/guidelines para no tener mas inconvenientes.")
    return
  if medidaID == "M3":
    await func_tempmute(ctx.channel, miembro, "7d", False)
    await func_warn(ctx.channel, miembro, reglaLabel, False)
    await miembro.send("Hola, has recibido una advertencia y has sido silenciado por 7 días por `" + reglaLabel + "` dentro del servidor de **" + ctx.guild.name + "**. Te recomendamos leer las reglas del servidor y las Directivas de la comunidad de Discord https://discord.com/guidelines para no tener mas inconvenientes.")
    return
  if medidaID == "M4":
    await func_tempmute(ctx.channel, miembro, "30d", False)
    await func_warn(ctx.channel, miembro, reglaLabel, False)
    await miembro.send("Hola, has recibido una advertencia y has sido silenciado por 30 días por `" + reglaLabel + "` dentro del servidor de **" + ctx.guild.name + "**. Te recomendamos leer las reglas del servidor y las Directivas de la comunidad de Discord https://discord.com/guidelines para no tener mas inconvenientes.")
    return
  if medidaID == "M5":
    items = await QueryGET("SELECT * FROM muterole WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) == 0:
      await ctx.send("Error. No posees un rol de Muteado asignado, para asignar uno el administrador debe utiliza el comando `setmuterol`.")
    else:
      role = get(miembro.guild.roles, id=int(items[0][1]))
      await miembro.add_roles(role)

      #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

      if len(items) > 0:
        channel = bot.get_channel(int(items[0][1]))
        embed = discord.Embed(
        title = '**MUTE**',
        description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
        colour = discord.Colour.from_rgb(219, 0, 255)
        )
        embed.set_thumbnail(url=miembro.avatar_url)
        await channel.send(embed=embed)
    
    await func_warn(ctx.channel, miembro, reglaLabel, False)
    await miembro.send("Hola, has recibido una advertencia y has sido silenciado permanentemente por `" + reglaLabel + "` dentro del servidor de **" + ctx.guild.name + "**. Te recomendamos leer las reglas del servidor y las Directivas de la comunidad de Discord https://discord.com/guidelines para no tener mas inconvenientes.")
    return
  if medidaID == "M6":
    await func_warn(ctx.channel, miembro, reglaLabel, False)
    await miembro.send("Hola, has recibido una advertencia y has sido baneado permanentemente por `" + reglaLabel + "` dentro del servidor de **" + ctx.guild.name + "**. Te recomendamos leer las reglas del servidor y las Directivas de la comunidad de Discord https://discord.com/guidelines para no tener mas inconvenientes.")
    await miembro.ban(reason = "Shiro-san Ban by " + ctx.author.name)

    #LOG
    items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(ctx.guild.id) + "'")

    if len(items) > 0:
      channel = bot.get_channel(int(items[0][1]))
      embed = discord.Embed(
      title = '**BAN**',
      description = "Miembro: <@" + str(miembro.id) + ">\n Por: <@" + str(ctx.author.id) + ">",
      colour = discord.Colour.from_rgb(219, 0, 255)
      )
      embed.set_thumbnail(url=miembro.avatar_url)
      await channel.send(embed=embed)
    return

###################################### UTILERIA ######################################

@bot.event
async def on_voice_state_update(member, before, after):
  if after.channel != None:
    #c.execute ("SELECT * FROM privadas_guild_creadores WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(after.channel.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM privadas_guild_creadores WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(after.channel.id) + "'")

    if len(items) > 0:
      if before.channel != None:
        #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
        #items = c.fetchall()
        items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")

        if len(items) > 0:
          if len(before.channel.members) <= 0:
            await before.channel.delete()
            #c.execute("DELETE FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
            await QueryEX("DELETE FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
            #conn.commit()
            
      guild = member.guild
      category = after.channel.category
      overwrites = {
        guild.me: discord.PermissionOverwrite(view_channel=True, connect=True),
        member: discord.PermissionOverwrite(view_channel=True, connect=True)
      }
      channel = await guild.create_voice_channel("🔒 Canal de " + member.name, overwrites=overwrites,category=category)

      #c.execute("INSERT INTO privadas_guild_creadas VALUES ('" + str(member.guild.id) + "', '" + str(channel.id) + "', '" + str(member.id) + "')")
      await QueryEX("INSERT INTO privadas_guild_creadas VALUES ('" + str(member.guild.id) + "', '" + str(channel.id) + "', '" + str(member.id) + "')")
      #conn.commit()

      await channel.edit(user_limit=6)
      await member.move_to(channel)
    else:
      if before.channel != None:
        #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
        #items = c.fetchall()
        items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")

        if len(items) > 0:
          if len(before.channel.members) <= 0:
            await before.channel.delete()
            #c.execute("DELETE FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
            await QueryEX("DELETE FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
            #conn.commit()
  else:
    #c.execute ("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")

    if len(items) > 0:
      if len(before.channel.members) <= 0:
        await before.channel.delete()
        #c.execute("DELETE FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
        await QueryEX("DELETE FROM privadas_guild_creadas WHERE guild_id = '" + str(member.guild.id) + "' AND channel_id = '" + str(before.channel.id) + "'")
        #conn.commit()

@bot.event
async def on_message_delete(message):
  if message.author.bot:
    return
    
  if not message.guild:
    return

  #c.execute ("SELECT * FROM channel_message_log WHERE guild_id = '" + str(message.guild.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM channel_message_log WHERE guild_id = '" + str(message.guild.id) + "'")

  if len(items) > 0:
    contenidonew = (message.content[:500] + '...') if len(message.content) > 500 else message.content
    
    embed1 = discord.Embed(title="Mensaje eliminado en " +  message.channel.name)
    embed1.add_field(name=f"**Mensaje eliminado**", value=f"Mensaje:\n" + contenidonew + "", inline=True)
    embed1.add_field(name=f"**Author del mensaje**", value=f"Author:\n<@" + str(message.author.id) + ">", inline=True)
    if message.attachments:
      for x in message.attachments:
        embed1.add_field(name=f"**Archivo adjunto**", value=f"Link:\n" + x.url, inline=True)
    dele = bot.get_channel(int(items[0][1]))
    await dele.send(embed=embed1)

@bot.event
async def on_message_edit(before, after):
  if before.author.bot:
    return

  if before.content == after.content:
    return
  
  #c.execute ("SELECT * FROM channel_message_log WHERE guild_id = '" + str(before.guild.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM channel_message_log WHERE guild_id = '" + str(before.guild.id) + "'")

  if len(items) > 0:
    contenidoold = (before.content[:500] + '...') if len(before.content) > 500 else before.content
    contenidonew = (after.content[:500] + '...') if len(after.content) > 500 else after.content

    embed1 = discord.Embed(title="Mensaje editado en " +  before.channel.name)
    embed1.add_field(name=f"**Mensaje original**", value=f"Mensaje:\n" + contenidoold + "", inline=True)
    embed1.add_field(name=f"**Mensaje editado**", value=f"Mensaje:\n" + contenidonew + "", inline=True)
    embed1.add_field(name=f"**Author del mensaje**", value=f"Author:\n<@" + str(before.author.id) + ">", inline=True)
    dele = bot.get_channel(int(items[0][1]))
    await dele.send(embed=embed1)

async def create_member_welcome(member, channel, msg):

  base = Image.open("base.png").convert("RGBA")
  txt = Image.new("RGBA", base.size, (255,255,255,0))
  fnt = ImageFont.truetype("impact.ttf", 52)
  d = ImageDraw.Draw(txt)
  
  x=516
  y=460
  font=fnt
  draw=d
  text=member.name
  shadowcolor = "black"
  draw.text((x-2, y), text, font=font, fill=shadowcolor, aling="center", anchor="mb")
  draw.text((x+2, y), text, font=font, fill=shadowcolor, aling="center", anchor="mb")
  draw.text((x, y-2), text, font=font, fill=shadowcolor, aling="center", anchor="mb")
  draw.text((x, y+2), text, font=font, fill=shadowcolor, aling="center", anchor="mb")
  draw.text((x-2, y-2), text, font=font, fill=shadowcolor, aling="center", anchor="mb")
  draw.text((x+2, y-2), text, font=font, fill=shadowcolor, aling="center", anchor="mb")
  draw.text((x-2, y+2), text, font=font, fill=shadowcolor, aling="center", anchor="mb")
  draw.text((x+2, y+2), text, font=font, fill=shadowcolor, aling="center", anchor="mb")

  d.text((516,460), member.name, font=fnt, fill=(255,255,255,255), aling="center", anchor="mb")

  out = Image.alpha_composite(base, txt)

  r = requests.get(member.avatar_url, stream = True)
  if r.status_code == 200:
    r.raw.decode_content = True
    with open("avatar.png",'wb') as f:
        shutil.copyfileobj(r.raw, f)

  icon = Image.open("avatar.png").convert("RGBA")
  icon = icon.resize((260, 260))
  #mask_im = Image.new("L", icon.size, 0)
  #draw = ImageDraw.Draw(mask_im)
  #draw.ellipse((140, 120, 380, 380), fill=255)
  #mask_im.save('mask_circle.jpg', quality=95)

  back_im = out.copy()
  back_im.paste(icon, (386, 40))

  back_im.save("welcome.png", quality=95)

  await channel.send(msg, file=discord.File('welcome.png'))

@bot.event
async def on_member_join(member):
  #c.execute ("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(member.guild.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(member.guild.id) + "'")

  if len(items) > 0:
    #c.execute ("SELECT * FROM global_bans WHERE user_id = '" + str(member.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM global_bans WHERE user_id = '" + str(member.id) + "'")

    if len(items) > 0:
      bannerds = bot.get_user(int(items[0][4]))

      await asyncio.sleep(4)

      embed = discord.Embed(
      title = '**BANEO GLOBAL**',
      description = "**Usuario:** " + items[0][1] + "#" + items[0][2] + "\n**ID:** " + items[0][0] + "\n**Censurado:** " + items[0][9] + "\n**Servidor de origen:** " + items[0][3] + "\n**Nivel:** **" + items[0][10] + "**\n**Razon:** " + items[0][11] + "\n**Fecha:** " + items[0][6] + "\n**Bot:** " + items[0][7] + "\n**Autor del baneo global:** <@" + items[0][4] + ">\n**Autorizado por:** <@" + items[0][5] + ">\n **GB ID:** " + items[0][12],
      colour = discord.Colour.from_rgb(255, 0, 0)
      )
      embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
      embed.set_author(name=bannerds.name + "#" + str(bannerds.discriminator) + " ID: " + str(bannerds.id), icon_url=bannerds.avatar_url)

      if items[0][9] == "si":
        embed.set_image(url="https://www.yoinfluyo.com/images/stories/hoy/ago18/150818/censura_nationalgeo.png")
      else:
        embed.set_image(url=items[0][8])

      if items[0][7] == "si":
        await member.guild.owner.send(":warning: Alerta de seguridad en tu servidor de " + member.guild.name + ". Alguien intento añadir un bot peligroso al mismo, pero fue baneado de inmediato por el sistema de ban global de la **OTAKU ARMY**. <@" + items[0][0] + "> puede que los datos no coincidan con los  que están registrados ya que los usuarios o bots pueden cambiar de nombre y/o avatar, te recomendamos guiarte con la id.", embed=embed)
      else:
        await member.guild.owner.send(":warning: Alerta de seguridad en tu servidor de " + member.guild.name + ". Un usuario peligroso se unió al mismo, pero fue baneado de inmediato por el sistema de ban global de la **OTAKU ARMY**. <@" + items[0][0] + "> puede que los datos no coincidan con los  que están registrados ya que los usuarios o bots pueden cambiar de nombre y/o avatar, te recomendamos guiarte con la id.", embed=embed)

      await member.ban(reason = "OTAKU ARMY BAN GLOBAL")
      return
  else:
    #c.execute ("SELECT * FROM global_bans WHERE user_id = '" + str(member.id) + "'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM global_bans WHERE user_id = '" + str(member.id) + "'")

    if len(items) > 0:
      bannerds = bot.get_user(int(items[0][4]))

      await asyncio.sleep(4)

      embed = discord.Embed(
      title = '**BANEO GLOBAL**',
      description = "**Usuario:** " + items[0][1] + "#" + items[0][2] + "\n**ID:** " + items[0][0] + "\n**Censurado:** " + items[0][9] + "\n**Servidor de origen:** " + items[0][3] + "\n**Nivel:** **" + items[0][10] + "**\n**Razon:** " + items[0][11] + "\n**Fecha:** " + items[0][6] + "\n**Bot:** " + items[0][7] + "\n**Autor del baneo global:** <@" + items[0][4] + ">\n**Autorizado por:** <@" + items[0][5] + ">\n **GB ID:** " + items[0][12],
      colour = discord.Colour.from_rgb(255, 0, 0)
      )
      embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
      embed.set_author(name=bannerds.name + "#" + str(bannerds.discriminator) + " ID: " + str(bannerds.id), icon_url=bannerds.avatar_url)

      if items[0][9] == "si":
        embed.set_image(url="https://www.yoinfluyo.com/images/stories/hoy/ago18/150818/censura_nationalgeo.png")
      else:
        embed.set_image(url=items[0][8])

      if items[0][7] == "si":
        await member.guild.owner.send(":warning: Alerta de seguridad en tu servidor de " + member.guild.name + ". Alguien logro añadir un bot peligroso al mismo, no se llevaron acabo acciones por que el sistema de ban global de la **OTAKU ARMY** esta desactivado. <@" + items[0][0] + "> puede que los datos no coincidan con los  que están registrados ya que los usuarios o bots pueden cambiar de nombre y/o avatar, te recomendamos guiarte con la id.", embed=embed)
      else:
        await member.guild.owner.send(":warning: Alerta de seguridad en tu servidor de " + member.guild.name + ". Un usuario peligroso se unió al mismo, no se llevaron acabo acciones por que el sistema de ban global de la **OTAKU ARMY** esta desactivado. <@" + items[0][0] + "> puede que los datos no coincidan con los  que están registrados ya que los usuarios o bots pueden cambiar de nombre y/o avatar, te recomendamos guiarte con la id.", embed=embed)


  if member.bot:
      pass
  else:
      #c.execute ("SELECT * FROM joinrole WHERE guild_id = '" + str(member.guild.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM joinrole WHERE guild_id = '" + str(member.guild.id) + "'")

      if len(items) == 0:
        pass
      else:
        role = get(member.guild.roles, id=int(items[0][1]))
        await member.add_roles(role)

  #if member.guild.id == 714556967347159101: #cambiar
    #VERIFICARFile = open("./data/Verificar.txt", "r")
    #VERIFICAR = VERIFICARFile.read()
    #VERIFICARFile.close()

    #if str(VERIFICAR) == "no":
    #  role = get(member.guild.roles, id=807129160102445087) #cambiar
    #  await member.add_roles(role)
    #else:
    #  role = get(member.guild.roles, id=834597550015250443) #cambiar
    #  await member.add_roles(role)

  #c.execute ("SELECT * FROM welcomes WHERE guild_id = '" + str(member.guild.id) + "'")
  #items = c.fetchall()
  items = await QueryGET("SELECT * FROM welcomes WHERE guild_id = '" + str(member.guild.id) + "'")

  if len(items) == 0:
    pass
  else:
    channel = bot.get_channel(int(items[0][1]))
    await create_member_welcome(member, channel, "Hola <@" + str(member.id) + ">, ¡Bienvenido a **" + member.guild.name + "**!")

import json
@bot.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and int(x['message_id']) == payload.message_id:
                    role = discord.utils.get(bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)
                    if x['remove_role_id'] != "null":
                      role2 = discord.utils.get(bot.get_guild(
                        payload.guild_id).roles, id=x['remove_role_id'])
                      await payload.member.remove_roles(role2)

    if payload.channel_id == 915726741237026816:
      channel = bot.get_channel(915726741237026816)
      msg = await channel.fetch_message(payload.message_id)

      if "IA:ATCH!" not in msg.content:
        return

      if "IA:RES!" not in msg.content:
        remover2 = msg.content.find("IA:ATCH!")
        attach = msg.content[remover2 + 9 : len(msg.content) : ]

        remover3 = msg.content.find("IA:RES!")
        res = msg.content[0 : remover2 - 1 : ]

        nuevo = [
          res,
          attach,
        ]
        chatbot.train(nuevo)
      else:
        remover2 = msg.content.find("IA:ATCH!")
        attach = msg.content[remover2 + 9 : len(msg.content) : ]

        remover3 = msg.content.find("IA:RES!")
        res = msg.content[remover3 + 8 : remover2 - 1 : ]

        nuevo = [
          res,
          attach,
          ]
        chatbot.train(nuevo)
      
      await msg.reply("Listo. nuevo mensaje aprendido.")

@bot.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name and int(x['message_id']) == payload.message_id:
                role = discord.utils.get(bot.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

###ON MENSAJE

@bot.event
async def on_message(message):
  bypass = False
  closed = False
  
  #gb
  if message.channel.id == 861014419365953588:
    if message.author.bot == True:
      if message.author.id == 831402870229958676:
        comunication_channel = message.channel

        if message.content == "gb_comprobe;220911":
          await comunication_channel.send("gb_comprobe;441822")
        else:
          separador = ";"
          codigos = message.content.split(separador)
          
          if codigos[0] == "gb_send":
            #c.execute("INSERT INTO global_bans VALUES ('" + codigos[1] + "', '" + codigos[2] + "', '" + codigos[3] + "', '" + codigos[4] + "', '" + codigos[5] + "', '" + codigos[6] + "', '" +  codigos[7] + "', '" + codigos[8] + "', '" + codigos[9] + "', '" + codigos[10] + "', '" + codigos[11] + "', '" + codigos[12] + "', '" + codigos[13] + "')")
            await QueryEX("INSERT INTO global_bans VALUES ('" + codigos[1] + "', '" + codigos[2] + "', '" + codigos[3] + "', '" + codigos[4] + "', '" + codigos[5] + "', '" + codigos[6] + "', '" +  codigos[7] + "', '" + codigos[8] + "', '" + codigos[9] + "', '" + codigos[10] + "', '" + codigos[11] + "', '" + codigos[12] + "', '" + codigos[13] + "')")
            ##conn.commit()
            
            bannerds = bot.get_user(int(codigos[5]))
            
            for guild in bot.guilds:
              #c.execute ("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(guild.id) + "'")
              #items = c.fetchall()
              items = await QueryGET("SELECT * FROM global_ban_ops WHERE guild_id = '" + str(guild.id) + "'")

              logear_ban = False

              if len(items) > 0 and logear_ban:
                #c.execute ("SELECT * FROM channel_log WHERE guild_id = '" + str(guild.id) + "'")
                #items = c.fetchall()
                items = await QueryGET("SELECT * FROM channel_log WHERE guild_id = '" + str(guild.id) + "'")

                if len(items) > 0:
                  channel_id = int(items[0][1])
                  channel = bot.get_channel(channel_id)

                  embed = discord.Embed(
                  title = '**BANEO GLOBAL**',
                  description = "**Usuario:** " + codigos[2] + "#" + codigos[3] + "\n**ID:** " + codigos[1] + "\n**Censurado:** " + codigos[10] + "\n**Servidor de origen:** " + codigos[4] + "\n**Nivel:** **" + codigos[11] + "**\n**Razon:** " + codigos[12] + "\n**Fecha:** " + codigos[7] + "\n**Bot:** " + codigos[8] + "\n**Autor del baneo global:** <@" + codigos[5] + ">\n**Autorizado por:** <@" + codigos[6] + ">\n **GB ID:** " + codigos[13],
                  colour = discord.Colour.from_rgb(255, 0, 0)
                  )
                  embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6453-ban-hammer.png")
                  embed.set_author(name=bannerds.name + "#" + str(bannerds.discriminator) + " ID: " + str(bannerds.id), icon_url=bannerds.avatar_url)

                  if codigos[10] == "si":
                    embed.set_image(url="https://www.yoinfluyo.com/images/stories/hoy/ago18/150818/censura_nationalgeo.png")
                  else:
                    embed.set_image(url=codigos[9])
                  await channel.send(embed=embed)
              
              user_banned = None
              user_banned = guild.get_member(int(codigos[1]))

              if user_banned != None:
                user_banned.ban("OTAKU ARMY GLOBAL BAN")

              await asyncio.sleep(20)
              #logear a todos los logs que tengan global ban activado

  if isinstance(message.author, discord.User):
    bypass = True
    closed = True

#  if isinstance(message.author, discord.User):
#      if message.author.bot == False:
#        channel = bot.get_channel(846517618973212673)
#        await channel.send(" <@" + str(message.author.id) + "> <" + str(message.author.id)# + ">: " + message.content + " ")
#        for x in message.attachments:
#          await channel.send(" <@" + str(message.author.id) + "> <" + str(message.author.id) + ">: " + x.url)
#        bypass = True
#        closed = True

  if message.author == bot.user:
      bypass = True
      closed = True

  if message.author.bot:
      bypass = True
      closed = True

  if closed == False:
    #anti invite
    if "discord.gg/" in message.content.lower():
      if not permisosCheck(message.author, 1) or True:
        invitaciones = await message.guild.invites()
        code = message.content.split("discord.gg/")[1]
        pasoInvite = False

        for invite in invitaciones:
          if invite.code == code:
            pasoInvite = True

        #c.execute ("SELECT * FROM anti_invite_ops WHERE guild_id = '" + str(message.guild.id) + "' AND option = 'enable'")
        #items = c.fetchall()
        items = await QueryGET("SELECT * FROM anti_invite_ops WHERE guild_id = '" + str(message.guild.id) + "' AND option = 'enable'")

        if len(items) > 0 and not pasoInvite:
          #c.execute ("SELECT * FROM anti_invite_ops_channel WHERE guild_id = '" + str(message.guild.id) + "' AND channel_id = '" + str(message.channel.id) + "'")
          #items = c.fetchall()
          items = await QueryGET("SELECT * FROM anti_invite_ops_channel WHERE guild_id = '" + str(message.guild.id) + "' AND channel_id = '" + str(message.channel.id) + "'")

          if len(items) == 0:
            await message.delete()
            await func_tempmute(message.channel, message.author, "2h", False)
            await func_warn(message.channel, message.author, "Pasar invitaciones a otros servidores", False)
            await message.author.send("Hola, has recibido una advertencia y has sido silenciado por 2 horas por `Pasar invitaciones a otros servidores` dentro del servidor de **" + message.guild.name + "**. Te recomendamos leer las reglas del servidor y las Directivas de la comunidad de Discord https://discord.com/guidelines para no tener mas inconvenientes.")

    #responses
    try:
      #c.execute ("SELECT * FROM responses_messages WHERE guild_id = '" + str(message.author.guild.id) + "' AND key = '" + message.content.lower() + "'")
      #items = c.fetchall()

      if message.content.lower() != "" and message.content.lower() != " " and not "'" in message.content.lower() and not '"' in message.content.lower():
        items = await QueryGET("SELECT * FROM responses_messages WHERE guild_id = '" + str(message.author.guild.id) + "' AND key = '" + message.content.lower() + "'")

        if len(items) > 0:
          for item in items:
            if int(item[3]) >= int(item[4]):
              #c.execute("UPDATE responses_messages SET try = '0' WHERE guild_id = '" + str(message.author.guild.id) + "' AND id = '" + item[5] + "'")
              await QueryEX("UPDATE responses_messages SET try = '0' WHERE guild_id = '" + str(message.author.guild.id) + "' AND id = '" + item[5] + "'")
              #conn.commit()
              await message.channel.send(item[2])
            else:
              #c.execute("UPDATE responses_messages SET try = '" + int(item[4] + 1) + "' WHERE guild_id = '" + str(message.author.guild.id) + "' AND id = '" + item[5] + "'")
              await QueryEX("UPDATE responses_messages SET try = '" + int(item[4] + 1) + "' WHERE guild_id = '" + str(message.author.guild.id) + "' AND id = '" + item[5] + "'")
              #conn.commit()
    except Exception:
      raise Exception
          

    #legacy responses
    #with open('responses.json') as react_file:
    #        data = json.load(react_file)
    #        for x in data:
    #            if x['guild_id'] == message.author.guild.id and x['active'] == "True" and message.content.lower() == x['key']:
    #
    #              x['try'] = x['try'] + 1
    #
    #              if x['try'] >= x['veces']:
    #                x['try'] = 0
    #                await message.channel.send(x["response"])
    #              with open('responses.json', 'w') as f:
    #                json.dump(data, f, indent=4)

    ##level
    #c.execute ("SELECT * FROM levels_ops WHERE guild_id = '" + str(message.guild.id) + "' AND option = 'enable'")
    #items = c.fetchall()
    items = await QueryGET("SELECT * FROM levels_ops WHERE guild_id = '" + str(message.guild.id) + "' AND option = 'enable'")

    if len(items) > 0:
      #c.execute ("SELECT * FROM levels_ops_channel WHERE guild_id = '" + str(message.guild.id) + "' AND channel_id = '" + str(message.channel.id) + "'")
      #items = c.fetchall()
      items = await QueryGET("SELECT * FROM levels_ops_channel WHERE guild_id = '" + str(message.guild.id) + "' AND channel_id = '" + str(message.channel.id) + "'")

      if len(items) == 0:
        await add_points(message.author, message.guild, 1)

#    if message.author.guild.id != 714556967347159101:
#        bypass = True

    if message.content.lower().find('<:') >= 0:
      bypass = True

    if message.content.lower().find('https://') >= 0:
      bypass = True

    if bypass == False:
      if not bot.user.mentioned_in(message):
        if message.content != "":
          if message.reference:
            if message.reference.cached_message:
              if message.reference.cached_message.content != "" and not message.reference.cached_message.author.bot:
                ina = random.randint(0, 1)

                if ina == 0:
                  texto1 = await limpiarTextoDiscord(message.reference.cached_message.content)
                  texto2 = await limpiarTextoDiscord(message.content)

                  if len(message.attachments) > 0:
                    await IASendVerification(texto2, message)

                  if texto1 != "" or texto1 !=  " ":
                    if texto2 != "" or texto2 !=  " ":
                      nuevo = [
                        texto1,
                        texto2,
                        ]
                      chatbot.train(nuevo)
        else:
          if message.reference:
            if len(message.attachments) > 0 and message.reference.cached_message:
              ina = random.randint(0, 1)

              if ina == 0:
                await IASendVerification("IA:RES! " + message.reference.cached_message.content, message)

      else:
        if not "@everyone" in message.content and not "@here" in message.content:
          #modulo chattbot
          await message.channel.trigger_typing()
        
          continuar_mencion_normal = True

          mensaje_puro = await limpiarTextoDiscord(message.content)

          if len(mensaje_puro) > 0:
            items = await QueryGET("SELECT * FROM chat_ia_ops WHERE guild_id = '" + str(message.guild.id) + "' AND option = 'disable'")

            if len(items) == 0:
              if len(message.attachments) > 0:
                await IASendVerification(mensaje_puro, message)

              await IAGetResponse(mensaje_puro, message)
              continuar_mencion_normal = False
          else:
            if message.reference:
              if len(message.attachments) > 0 and message.reference.cached_message:
                await IASendVerification("IA:RES! " + message.reference.cached_message.content, message)

                await IAGetResponse("meme", message)
                continuar_mencion_normal = False

          #mencion normal

          if continuar_mencion_normal:
            ina = random.randint(0, 5)

            if ina == 0:
              await message.channel.send("<@" + str(message.author.id) + "> Hola! Puedes usar `sh!help` para la lista de comandos.")
            if ina == 1:
              await message.channel.send("<@" + str(message.author.id) + "> Puedes usar `sh!help` para la lista de comandos.")
            if ina == 2:
              await message.channel.send("<@" + str(message.author.id) + "> Hola :D para la lista de comandos usa `sh!help`")
            if ina == 3:
              await message.channel.send("<@" + str(message.author.id) + "> Mi prefijo es `sh!`")
            if ina == 4:
              await message.channel.send("<@" + str(message.author.id) + "> Buenas, Mi prefijo es `sh!`")
            if ina == 5:
              await message.channel.send("<@" + str(message.author.id) + "> Hola! Puedes usar `sh!help` para la lista de comandos.")

#      if message.content.lower() == ('otaku army'):
#        if AntiSpam("otaku_army", 3):
#          await message.channel.send('https://cdn.discordapp.com/attachments/735764283908030466/807345753033932800/Sin-titulo.gif')
#      else:
#        if message.content.lower().find('otaku') >= 0:
#          if AntiSpam("otaku", 3):
#            await message.channel.send('https://tenor.com/view/gabriel-dropout-gabriel-temna-gabriel-white-gabriel-gabriel-dropout-gabriel-white-temna-gif-14546428')

#      if message.content.lower().find('otaku craft') >= 0:
#        if AntiSpam("otaku", 4):
#          await message.channel.send('https://media.discordapp.net/attachments/714556968198733908/814976439794532392/logoanim.gif')

#      if message.content.lower().find('kanna') >= 0:
#        if AntiSpam("kanna", 3):
#          await message.channel.send('https://tenor.com/view/anime-kanna-cute-kawaii-happy-gif-8087657')

#      if message.content.lower().find('tohru') >= 0:
#        if AntiSpam("tohru", 3):
#          await message.channel.send('https://tenor.com/view/tohru-kobayashisan-chi-no-maid-dragon-dragon-maid-thumbs-up-gif-12390446')

#      if message.content.lower().find('senko') >= 0:
#        if AntiSpam("senko", 3):
#          await message.channel.send('https://tenor.com/view/senko-cute-talking-gif-14951601')

#      if message.content.lower().find('jahy sama') >= 0:
#        if AntiSpam("jahy", 3):
#          await message.channel.send('https://tenor.com/view/jahy-sama-anime-edit-cute-gif-18959171')

#      if message.content.lower().find('ruka') >= 0:
#        if AntiSpam("ruka", 3):
#          await message.channel.send('https://tenor.com/view/ruka-sarashina-bleh-gif-18269812')

#      if message.content.lower().find('xd') >= 0:
#        if AntiSpam("xd", 4):
#          await message.channel.send('xD')

#      if message.content.lower().find('sagiri') >= 0:
#        if AntiSpam("sagiri", 3):
#          await message.channel.send('https://tenor.com/view/anime-izumi-sagiri-ero-manga-sensei-sad-cute-gif-14549557')

#      if message.content.lower().find('toga himiko') >= 0:
#        if AntiSpam("toga", 4):
#          await message.channel.send('https://tenor.com/view/himiko-toga-gif-12978767')

#      if message.content.lower().find('gabriel') >= 0:
#        if AntiSpam("gabriel", 3):
#          await message.channel.send('https://tenor.com/view/gabriel-dropout-gabriel-temna-gabriel-white-gabriel-gabriel-dropout-gabriel-white-temna-gif-14546428')
    
#anti bug

#      if message.content.lower().find('https://gfycat.com/idioticbabyishilladopsis') >= 0:
#          await message.delete()
      
#      if message.content.lower().find('https://gfycat.com/idioticbabyishilladopsis.mp4') >= 0:
#          await message.delete()

  if isinstance(message.author, discord.Member):
    if message.author.guild.id == 714556967347159101:
      if message.content.lower().find('sh!invite') >= 0:
          if permisosCheck(message.author, 3):
            pass
          else:
            if message.author.bot:
              pass
            else:
              await message.delete()
              await message.author.send("Gracias por invitar a Shiro-san <:sataok:848337914765115412>. https://discord.com/api/oauth2/authorize?client_id=848797506694414346&permissions=8&scope=bot")
    else:
      await bot.process_commands(message)

from pathlib import Path
def AntiSpam(name, max):
  my_file = Path("./data/spam_" + name + ".txt")

  if my_file.is_file() == False:
    f = open("./data/spam_" + name + ".txt", "x")
    f.close()

  spam_xd_File = open("./data/spam_" + name + ".txt", "r")
  spam_xd = spam_xd_File.read()
  spam_xd_File.close()

  if (spam_xd == ""):
    spam_xd = 0

  spam_xd = int(spam_xd) + 1

  passa = False

  if spam_xd >= max:
    spam_xd = 0
    passa = True

  spam_xd_File = open("./data/spam_" + name + ".txt", "w")
  spam_xd_File.write(str(spam_xd))
  spam_xd_File.close()

  return passa

def permisosCheck(author, perm):
  try:
    if not perms.check(author, perm):
        return False
    return True
  except:
        return True
        pass

keep_alive()

## CHATBOT

from chatterbot import ChatBot
from chatterbot import filters
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("Kanna",
  storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
  database="chatterbot-database-2v",
  trainer='chatterbot.trainers.ListTrainer',
  #Un Logic_adapter es una clase que devuelve una respuesta ante una pregunta dada. 
    #Se pueden usar tantos logic_adapters como se quiera
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    logic_adapters=[ 
        #'chatterbot.logic.MathematicalEvaluation', #Este es un logic_adapter que responde preguntas sobre matemáticas en inglés
        #'chatterbot.logic.TimeLogicAdapter', #Este es un logic_adapter que responde preguntas sobre la hora actual en inglés
        
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.3,
            'default_response': 'Disculpa, no te he entendido bien. ¿Puedes ser más específico?.'
        }
        #{
        #    'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        #    'input_text': 'Eso es todo',
        #    'output_text': 'Perfecto. Hasta la próxima'
        #}
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    database_uri= os.environ['ia_database_uri']
)

nombre = [
    "Como te llamas?",
    "Me llamo Shiro",
]

creador = [
    "Quien te creo?",
    "Me creo Uni44",
]

genero = [
    "Sos chica?",
    "Si soy chica",
]

if False: #pre entrenar para algunos datos
  chatbot.set_trainer(ListTrainer)
  #chatbot.train(nombre)
  chatbot.train(creador)
  chatbot.train(genero)

chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("chatterbot.corpus.spanish")
chatbot.set_trainer(ListTrainer)

async def limpiarTextoDiscord(texto: str):
  mensaje_puro = texto
  mensaje_puro = mensaje_puro.replace("<@!" + str(bot.user.id) + "> ", "")
  mensaje_puro = mensaje_puro.replace("<@" + str(bot.user.id) + "> ", "") 
  mensaje_puro = mensaje_puro.replace("@everyone", "")
  mensaje_puro = mensaje_puro.replace("@here", "")

  remover = mensaje_puro.find("<@")

  while remover != -1:
    remover2 = mensaje_puro.find(">")

    if remover2 == -1:
      remover = -1
    else:
      if len(mensaje_puro) > remover:
        mensaje_puro = mensaje_puro[0 : remover : ] + mensaje_puro[remover2 + 1 : :]

    remover = mensaje_puro.find("<@")

  remover = mensaje_puro.find("<:")

  while remover != -1:
    remover2 = mensaje_puro.find(">")

    if remover2 == -1:
      remover = -1
    else:
      if len(mensaje_puro) > remover:
        mensaje_puro = mensaje_puro[0 : remover : ] + mensaje_puro[remover2 + 1 : :]

    remover = mensaje_puro.find("<:")

  while remover != -1:
    remover2 = mensaje_puro.find(">")

    if remover2 == -1:
      remover = -1
    else:
      if len(mensaje_puro) > remover:
        mensaje_puro = mensaje_puro[0 : remover : ] + mensaje_puro[remover2 + 1 : :]

    remover = mensaje_puro.find("<#")
  
  return mensaje_puro

async def IAGetResponse(texto: str, message):
  items = await QueryGET("SELECT * FROM chat_ia_ops WHERE guild_id = '" + str(message.guild.id) + "' AND option = 'disable'")

  if len(items) == 0:
    respuesta = "**BOT INTERNAL** N/A"

  @force_async
  def res():
    respuesta = chatbot.get_response(texto)
    return respuesta

  futures = list(map(lambda x: res(), range(1)))
  restaa = await asyncio.gather(*futures)
  restaa = str(restaa)[17 : len(restaa) -3 : ]
  respuesta = restaa

  if respuesta == "**BOT INTERNAL** N/A":
    respuesta = "auch encontre un bug en mi, ayuda"

  #respuesta = chatbot.get_response(mensaje_puro)

  #await message.channel.send("<@" + str(message.author.id) + "> " + str(respuesta))
  await message.reply(str(respuesta))

async def IASendVerification(texto: str, message):
  channel = bot.get_channel(915726741237026816)
  await channel.send(texto + " IA:ATCH! " + message.attachments[0].url)

# Run our bot
bot.run(str(TOKEN)) # Make sure you paste the CORRECT token in the "./data/Token.txt" file