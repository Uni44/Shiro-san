import discord
import random

async def ex(nombre, channelname, ctx, bot):
        channel = bot.get_channel(int(channelname))

        if nombre == "niveles":
          embed = discord.Embed(
          title = 'Información importante sobre los niveles de \"o\"',
          description = "Los niveles que se encuentran en el servidor actualmente son: <@&808128189972348939> , <@&808129006847000577> , <@&808129111607476246> , <@&808129227533975612> y <@&808129331632406528>.\n\nLa XP se gana hablando en los canales de discusión/texto.\n\nNo se entrega XP por hablar en los canales de <#746465958541000755>, <#742124678331760770>,  <#734873482290003978>, <#744453464943231048> y <#807128786234507304>.\n\nPuedes revisar la información de tu nivel con el comando a!level\n\n¿Para que sirven los niveles? Para desbloquear diferentes permisos y generar confianza en las autoridades del servidor.",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          #await channel.send(embed=embed)

        if nombre == "roles":
          embed = discord.Embed(
          title = 'Información de roles',
          description = "**- Roles del servidor:**\n\n<@&807129160102445087> : Rol inicial del servidor, se obtiene al unirse al servidor.\n\n<@&732105606848315463> : Rol otorgado a los streamers afiliados o socios en Twitch elegidos por <@269549755850293249>.\n\n<@&721622529109655582> : Rol otorgado por <@269549755850293249> a usuarios especiales.\n\n<@&733840082129387560> : Rol otorgado a los vips del canal de Uni44x en Twitch y también a algunos usarios del servidor que sean muy activos y ayuden a la comunidad.\n\n<@&751310822743212072>: Rol otorgado automáticamente los suscriptores de Twitch de Uni44x.\n\n<@&808160589406011425>: Rol otorgado a los booster del servidor.\n\n**- Autoridades del servidor:**\n\n<@&733771792665149490>: Rol de moderación del servidor.\n\n<@&721622486445326376>: Rol de los administradores del servidor. Este rol solo lo puede otorgar <@269549755850293249>.",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/735764283908030466/807345753033932800/Sin-titulo.gif')
          #await channel.send(embed=embed)

        if nombre == "reglas":
          embed = discord.Embed(
          title = 'Reglas del servidor:',
          description = "**- En los canales de texto está prohibido:**\n1.- Mandar contenido inapropiado como contenido de desnudez, pornografía, otro contenido sexual, gore, violencia, suicidio, autolesion, crueldad animal, screamers sera baneado permanentemente.\n\n2.- Mandar contenido inapropiado que perjudique el stream de los streamers sera baneado permanentemente.\n \n3.- Mandar información privada sera baneado permanentemente.\n \n4.- Pasar invitaciones a otros servidores sera advertido.\n \n5.- Tener una actitud tóxica dentro del servidor sera advertido hasta 3 veces y si el comportamiento del usuario no mejora sera baneado permanentemente.\n \n6.- Hacer mal uso de los canales temáticos sera advertido.\n\n7.- Enviar spoilers excesivamente sera advertido.\n \n8.- Hacer un excesivo spam o flood en los canales sera advertido.\n \n9.- Abusar de las menciones sin justificación alguna sera advertido.\n \n**- En canales de voz está prohibido:**\n1.- Transmitir contenido NSFW sera baneado permanentemente.\n \n2.- Mantener una actitud tóxica dentro del canal de voz sera advertido hasta 3 veces y si el comportamiento del usuario no mejora sera baneado permanentemente.\n \n3.- Alterar el ambiente de la llamada sera muteado y advertido.\n \n4.- Saturar el audio sera muteado y advertido.\n \n**- Extra:**\nSe sancionará con un permaban la violación de las Guidelines y ToS de Discord https://discord.com/guidelines - https://discord.com/terms\n\nSe te recomienda que leas las Directrices de la Comunidad de Twitch para no tener inconvenientes con la regla 2 de canales de texto. https://www.twitch.tv/p/es-es/legal/community-guidelines/\n\nIngresar multicuentas al servidor se traduce en un baneo permanentemente.\n\nAl recibir advertencias el sistema automáticamente sancionara al usuario dependiendo la cantidad que se acumulen del mismo.",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/735764283908030466/807345753033932800/Sin-titulo.gif')
          #await channel.send(embed=embed)

        if nombre == "invitacion":
          embed = discord.Embed(
          title = '**Invitación del servidor:**',
          description = "¿Quieres invitar nuevas personas al servidor?\n\nAquí tienes una invite para poder hacerlo: https://discord.gg/tXrJ2FZ",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          #await channel.send(embed=embed)

        if nombre == "verificar":
          embed = discord.Embed(
          title = '**Verificación:**',
          description = "Bienvenido a la **OTAKU ARMY**\n\nReacciona con el emoji para verificarte :white_check_mark:",
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/735764283908030466/807345753033932800/Sin-titulo.gif')
          #await channel.send(embed=embed)

        if nombre == "help1":
            embed = discord.Embed(
            title = 'Lista de comandos',
            colour = discord.Colour.from_rgb(219, 0, 255)
            )
            #commandos
            embed.add_field(name="🕹 Iniciar actividad \n(<:dev:853161030053527564> BETA)", value="sh!actividad")
            embed.add_field(name="📊 Muestra tu nivel y experiencia", value="sh!level")
            embed.add_field(name="📏 Me mide", value="sh!memide")
            embed.add_field(name="🎰 Generar codigo nuclear", value="sh!codigo")
            embed.add_field(name="💬 Te diré algo interesante...", value="sh!dime")
            embed.add_field(name="❓ Preguntame algo (Pregunta)", value="sh!pregunta")
            embed.add_field(name="💀 Te diré el año de tu muerte", value="sh!muerte")
            embed.add_field(name="🎲 Tirare los dados", value="sh!dados")
            embed.add_field(name="📷 Avatar (Miembro)", value="sh!avatar")
            embed.add_field(name="📷 Icono del server", value="sh!servericon")
            #embed.add_field(name="🍌 Meme alazar", value="sh!meme")
            embed.add_field(name="🔒 Comandos de privadas", value="sh!voice-help")
            embed.add_field(name="💻 Lista de comandos", value="sh!help")
            embed.add_field(name="💻 Lista de comandos de administración y moderación <:modtag:860610530578399293>", 
            value="sh!help2")
            embed.add_field(name="💌 Votame", value="sh!vote")
            embed.add_field(name="📩 Invitar a Shiro-san", value="sh!invite")
            #extra
            embed.set_thumbnail(url=bot.user.avatar_url)
            #await channel.send(embed=embed)
            
        if nombre == "help2":
          embed = discord.Embed(
          title = 'Lista de comandos',
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          #commandos
          embed.add_field(name="General", value="<:admtag:860610530489663518> `sh!say` (Texto) \n <:admtag:860610530489663518> `sh!sayto` (Canal, Texto) \n <:admtag:860610530489663518> `sh!join` \n <:admtag:860610530489663518> `oa!lock` \n <:admtag:860610530489663518> `oa!unlock` \n <:admtag:860610530489663518> `oa!hide` \n <:admtag:860610530489663518> `oa!unhide`")

          embed.add_field(name="Roles", value="<:admtag:860610530489663518> `sh!reactrole` (Emoji, Rol, Texto) \n <:admtag:860610530489663518> `sh!joinrole` (Rol) \n <:admtag:860610530489663518> `sh!joinrole-clear`")

          embed.add_field(name="Respuestas", value="<:admtag:860610530489663518> `sh!response-add` (Intentos, Palabra clave, Respuesta) \n <:admtag:860610530489663518> `sh!response-delete` (ID) \n <:admtag:860610530489663518> `sh!response-list`")

          embed.add_field(name="Moderación", value="<:modtag:860610530578399293> `sh!kick` (Miembro) \n <:modtag:860610530578399293> `sh!ban` (Miembro) \n <:modtag:860610530578399293> `sh!unban` (Miembro) \n <:modtag:860610530578399293> `sh!banlist` \n <:admtag:860610530489663518> `sh!setmuterol` (Rol) \n <:modtag:860610530578399293> `sh!tempmute` (Miembro, Tiempo [1m/h/d]) \n <:modtag:860610530578399293> `sh!mute` (Miembro) \n <:modtag:860610530578399293> `sh!unmute` (Miembro) \n <:modtag:860610530578399293> `sh!user-info` (Miembro) \n <:modtag:860610530578399293> `sh!clear` (Cantidad) \n <:modtag:860610530578399293> `sh!server-info` \n <:modtag:860610530578399293> `sh!warn` (Miembro, Razon) \n <:modtag:860610530578399293> `sh!infractions` (Miembro) \n <:admtag:860610530489663518> `sh!clear-infraction` (Miembro, ID) \n <:admtag:860610530489663518> `sh!clear-all-infractions` (Miembro)")

          embed.add_field(name="Niveles", value="<:admtag:860610530489663518> `sh!level-enable` \n <:admtag:860610530489663518> `sh!level-disable` \n <:admtag:860610530489663518> `sh!level-role-add` (Nivel, Rol) \n <:admtag:860610530489663518> `sh!level-role-remove` (Rol) \n <:admtag:860610530489663518> `sh!level-role-list` \n <:admtag:860610530489663518> `sh!level-channel-add` (Canal) \n <:admtag:860610530489663518> `sh!level-channel-remove` (Canal) \n <:admtag:860610530489663518> `sh!level-channel-list` \n ")

          embed.add_field(name="Bienvenidas", value="<:admtag:860610530489663518> `sh!welcome-set` (Canal) \n <:admtag:860610530489663518> `sh!welcome-clear`")

          embed.add_field(name="Log", value="<:admtag:860610530489663518> `sh!log-channel-set` (Canal) \n <:admtag:860610530489663518> `sh!log-channel-clear` \n <:admtag:860610530489663518> `sh!log-message-set` (Canal) \n <:admtag:860610530489663518> `sh!log-message-clear`")

          embed.add_field(name="Voice privado", value="<:admtag:860610530489663518> `sh!voice-create-hub`")

          embed.add_field(name="Anti invitaciones", value="<:admtag:860610530489663518> `sh!anti-invite-enable` \n <:admtag:860610530489663518> `sh!anti-invite-disable` \n <:admtag:860610530489663518> `sh!anti-invite-ignore-channel-add` \n <:admtag:860610530489663518> `sh!anti-invite-ignore-channel-remove` \n <:admtag:860610530489663518> `sh!anti-invite-ignore-channel-list`")

          embed.add_field(name="Chat IA (<:dev:853161030053527564> BETA)", value="<:admtag:860610530489663518> `sh!chat-ia-enable` \n <:admtag:860610530489663518> `sh!chat-ia-disable`")

          embed.add_field(name=":warning: OTA Ban global", value="<:admtag:860610530489663518> `sh!ota-global-ban` \n <:modtag:860610530578399293> `sh!ota-global-ban-info` (Usuario) \n <:modtag:860610530578399293> `sh!ota-global-ban-report` (Usuario, Información)")

          embed.add_field(name="Otro", value="`sh!invite` \n `sh!vote` \n `sh!report`")
          #extra
          embed.set_thumbnail(url=bot.user.avatar_url)
          #await channel.send(embed=embed)

        if nombre == "voice help":
          embed = discord.Embed(
          title = 'Lista de comandos de los canales privado',
          colour = discord.Colour.from_rgb(219, 0, 255)
          )
          #commandos
          embed.add_field(name="Banear miembro (Miembro)", value="sh!voice-ban")
          embed.add_field(name="Desbanear miembro (Miembro)", value="sh!voice-unban")
          embed.add_field(name="Renombrar canal (Nombre)", value="sh!voice-rename")
          embed.add_field(name="Ocultar canal", value="sh!voice-hide")
          embed.add_field(name="Revelar canal", value="sh!voice-unhide")
          embed.add_field(name="Cambiar limite (Limite)", value="sh!voice-limit")
          embed.add_field(name="Bloquear canal", value="sh!voice-lock")
          embed.add_field(name="Desbloquear canal", value="sh!voice-unlock")

          #extra
          embed.set_thumbnail(url=bot.user.avatar_url)

        if channel != None:
          await channel.send(embed=embed)
        else:
          return embed
