async def ex(mensaje, ctx):
  censurado = True
  if censurado == True:
    mensaje = mensaje.replace("@everyone", "everyone")
    mensaje = mensaje.replace("@here", "here")
  await ctx.channel.send(mensaje)