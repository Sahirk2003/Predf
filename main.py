import nextcord
from pdf2image import convert_from_path
import aiofiles
import aiohttp
import os
import warnings
from PIL import Image
from Private.config import TOKEN

warnings.simplefilter ('ignore', Image.DecompressionBombWarning)
print ('start')
dir = os.path.dirname(__file__)

attachment_file = os.path.join(dir, r'attachment_file.pdf')
print (attachment_file)
converted_pdfs = os.path.join(dir, r'ConvertedPDFs')
print(converted_pdfs)
client = nextcord.Client()

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
                            f = await aiofiles.open(attachment_file, mode ='wb')
                            await f.write(await resp.read())
                            f.close

                convert_from_path(attachment_file, dpi=500, output_folder=converted_pdfs, fmt ="jpeg", size =(1000,None), paths_only= True)
                os.remove(attachment_file)
                for image_path in os.listdir(converted_pdfs):
                    full_path = os.path.join(converted_pdfs,image_path)
                    await message.channel.send(file=nextcord.File(full_path))
                    os.remove(full_path)
                
       
client.run(TOKEN)  