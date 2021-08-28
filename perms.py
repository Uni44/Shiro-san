import json

with open("settings.json") as f:
  settings = json.load(f)

lvl1 = settings["perms"]["lvl1"]
lvl2 = settings["perms"]["lvl2"]
lvl3 = settings["perms"]["lvl3"]
lvl4 = settings["perms"]["lvl4"]

def get(memb):
  lvl = [0]
  for r in memb.roles:
    if r.name in lvl4:
      lvl.append(4)
    if r.name in lvl3:
      lvl.append(3)
    elif r.name in lvl2:
      lvl.append(2)
    elif r.name in lvl1:
      lvl.append(1)
  return max(lvl)

def get2(memb):
  lvl = [0]
  for r in memb.roles:
    if memb.guild.owner_id == memb.id:
      lvl.append(4)
    if memb.guild.owner_id == memb.id:
      lvl.append(3)
    elif memb.guild_permissions.administrator:
      lvl.append(2)
    elif memb.guild_permissions.ban_members:
      lvl.append(1)
  return max(lvl)
def check(memb, lvl):
  return get2(memb) >= lvl