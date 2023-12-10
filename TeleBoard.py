from pyperclip import copy,paste
from os.path import abspath
from telethon import TelegramClient
from os import getenv, remove
from sys import argv
from win32clipboard import CF_HDROP, IsClipboardFormatAvailable, OpenClipboard as opencb, GetClipboardData as getcb, CloseClipboard as closecb
from PIL import ImageGrab

api_id = getenv('tg_api_id')
api_hash = getenv('tg_api_hash')
tg_phone = getenv('tg_phone')
chat_id = int(getenv('tg_chat_id'))
dl_dir = 'TBDownloads'
temp = 'tbtemp.jpg'

client = TelegramClient(tg_phone, api_id, api_hash) 

filepaths = argv[1:]
async def send_files(filepaths):
    for f in filepaths:
        try:
            await client.send_file(chat_id, f)
        except Exception as e:
            print(e)

async def main():

    await client.connect()

    if not await client.is_user_authorized():        
        await client.send_code_request(tg_phone)
        code = input('Enter login code sent on telegram: ')
        await client.sign_in(tg_phone, code)
        
    if not filepaths:
        msg = (await client.get_messages(chat_id))[0]
        copy(abspath(await msg.download_media(dl_dir+'/')) if msg.file else msg.text)

    elif '-s' not in filepaths: 
        await send_files(filepaths)
    elif IsClipboardFormatAvailable(CF_HDROP):
        opencb()
        copiedfilepaths = getcb(CF_HDROP) 
        closecb()
        await send_files(copiedfilepaths)
    else:
        try: 
            ImageGrab.grabclipboard().convert('RGB').save(open(temp, 'w'), 'JPEG')
            await send_files([temp])
        except:
            await client.send_message(chat_id, paste())
    try:
        remove(temp)
    except:
        print('delete error')
client.loop.run_until_complete(main())