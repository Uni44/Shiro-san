async def ex(channel, texto, ctx, bot):
  censurado = True
  if censurado == True:
    texto = texto.replace("@everyone", "everyone")
    texto = texto.replace("@here", "here")
  await channel.send(texto)