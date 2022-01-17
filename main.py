

import os
import warnings
from PIL import Image


warnings.simplefilter ('ignore', Image.DecompressionBombWarning)
print ('start')
TOKEN = 
dir = os.path.dirname(__file__)

attachment = os.path.join(dir, r'attachment_file.pdf')
converted_pdfs = os.path.join(dir, r'ConvertedPDFs')
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    channel = str(message.channel.name)
    
    if message.attachments:
        for attachment in message.attachments:
            if 'pdf' in attachment.content_type:
                #await message.channel.send(attachment.url)
                async with aiohttp.ClientSession() as session:
                    url = attachment.url
                    async with session.get(url) as resp:
                        if resp.status ==200:
                            f = await aiofiles.open(attachment, mode ='wb')
                            await f.write(await resp.read())
                            f.close

                convert_from_path(attachment, dpi=500, output_folder=converted_pdfs, fmt ="jpeg", size =(1000,None), poppler_path = r"C:\Users\Sahir\Downloads\Release-21.11.0-0\poppler-21.11.0\Library\bin", paths_only= True)
                for image_path in os.listdir(converted_pdfs):
                    full_path = os.path.join(converted_pdfs,image_path)
                    await message.channel.send(file=discord.File(full_path))
                    os.remove(full_path)
       
client.run(TOKEN)  