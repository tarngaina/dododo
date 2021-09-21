from discord import File, Forbidden
from json import loads, dump
from traceback import format_exc as exc

CHANNEL_ID = 889792058565488660
data_channel = None
data_message = None


async def data_prepare(channels):
  find_data_channel(channels)
  await find_data_message()


def find_data_channel(channels):
  global data_channel
  for channel in channels:
    if channel.id == CHANNEL_ID:
      data_channel = channel
      break

async def find_data_message():
  global data_message
  if not data_channel:
    return

  async for message in data_channel.history(limit = 4):
    if (message.content == 'read') and message.attachments:
      data_message = message
      break
      
  if not data_message:
    with open(f'data.json', 'w+', encoding = 'utf-8') as f:
      f.write('{}')
    data_message = await data_channel.send('read', file = File('data.json'))
        
      
async def load_pref():
  if not data_channel:
    return False, 'No data source found.'
  
  if not data_message:
    await find_data_message()

  try:
    files = await data_message.attachments[0].to_file()
    dic = loads(files.fp.read())
    return True, dic

  except Forbidden:
    await find_data_message()
    return False, 'Something is wrong right now, try again.'
  except Exception as e:
    print(exc())
    return False, str(e)

async def save_pref(dic):
  global data_message
  if not data_channel:
    return False, 'No data source found.'

  if not data_message:
    await find_data_message()

  try:
    with open(f'data.json', 'w+', encoding = 'utf-8') as f:
      dump(dic, f, ensure_ascii = False, indent = 2)
    await data_message.delete()
    data_message = await data_channel.send('read', file = File('data.json'))
    return True, ''

  except Forbidden:
    await find_data_message()
    return False, 'Something is wrong right now, try again.'
  except Exception as e:
    print(exc())
    return False, str(e)


