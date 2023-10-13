import disnake
import os
from disnake.ext import commands

from dotenv import load_dotenv

load_dotenv()

intents=disnake.Intents.all()
intents.message_content = True 
                    
class BotNews(commands.Bot):

        async def on_ready(self) -> None:
                print(self.user)
    

        
token = os.getenv('TOKEN')
bot = BotNews(intents=intents, command_prefix='*')

# COGS

def load_extensions(d, p):
    for filename in os.listdir(d):
        if filename.endswith('.py'):
            file = filename[:-3]
            bot.load_extension(f'{p}.{file}')

# ARQUIVOS

load_extensions('./c', 'c')


bot.run(token)
