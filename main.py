import nextcord
from pdf2image import convert_from_path
import aiohttp
import os
import warnings
from PIL import Image
import random
from Private.config import TOKEN

warnings.simplefilter ('ignore', Image.DecompressionBombWarning)
dir = os.path.dirname(__file__)
client = nextcord.Client()
is_thread = False
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    channel = message.channel.name
    channel_type = message.channel

    if message.attachments:

        for attachment in message.attachments:

            attachment_file = os.path.join(dir, r'attachment_file{n}.pdf'.format(n = random.randint(1,100000)))
            converted_pdfs = os.path.join(dir, r'ConvertedPDFs{i}'.format(i = random.randint(1,100000)))
            os.mkdir(converted_pdfs)

            if 'pdf' in attachment.content_type:
                print(isinstance(channel_type, nextcord.threads.Thread))
                if not isinstance(channel_type, nextcord.threads.Thread):
                    THREAD = await message.create_thread(name = 'Feedback for {nameu}'.format (nameu = str(message.author).split('#')[0]))
                else:
                    THREAD = message.channel

                async with aiohttp.ClientSession() as session:
                    url = attachment.url
                    async with session.get(url) as resp:
                        if resp.status ==200:
                            with open(attachment_file, mode ='wb') as f:
                                f.write(await resp.read())
                            

                convert_from_path(attachment_file, dpi=500, output_folder=converted_pdfs, fmt ="jpeg", size =(1000,None), poppler_path=r"C:\Users\Sahir\Downloads\Release-21.11.0-0\poppler-21.11.0\Library\bin", paths_only= True)
                
                os.remove(attachment_file)

                for image_path in os.listdir(converted_pdfs):
                    full_path = os.path.join(converted_pdfs,image_path)
                   
                    await THREAD.send(file=nextcord.File(full_path))
                    
                    os.remove(full_path)
                
                os.rmdir(converted_pdfs)

                return

client.run(TOKEN)  