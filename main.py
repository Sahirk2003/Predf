import nextcord
from pdf2image import convert_from_path
import aiohttp
import os
import warnings
from PIL import Image
import random
from Private.config import TOKEN

intents = nextcord.Intents.all()
warnings.simplefilter ('ignore', Image.DecompressionBombWarning)
dir = os.path.dirname(__file__)
client = nextcord.Client(intents = intents)
is_thread = False
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    channel = message.channel

    if message.attachments:

        for attachment in message.attachments:

            if 'pdf' in attachment.content_type:

                attachment_file = os.path.join(dir, r'attachment_file{n}.pdf'.format(n = random.randint(1,100000)))
                converted_pdfs = os.path.join(dir, r'ConvertedPDFs{i}'.format(i = random.randint(1,100000)))
                os.mkdir(converted_pdfs)

               
                if not isinstance(channel, nextcord.threads.Thread):
                    send_message = await channel.send(content = "Converting {}".format(attachment.filename))
                    THREAD = await send_message.create_thread(name = attachment.filename)
                else:
                    await channel.send(content = "Converting {}".format(attachment.filename))
                    THREAD = channel

                async with aiohttp.ClientSession() as session:
                    url = attachment.url
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            with open(attachment_file, mode ='wb') as f:
                                f.write(await resp.read())
                            

                image_paths_list = convert_from_path(attachment_file, dpi=500, output_folder=converted_pdfs, fmt ="jpeg", size =(1000,None), paths_only= True)
                
                os.remove(attachment_file)

                for image_path in image_paths_list:
                  
                    await THREAD.send(file=nextcord.File(image_path))
                    os.remove(image_path)

                os.rmdir(converted_pdfs)
            
            return

client.run(TOKEN)  