import disnake
import os
from disnake.ext import commands

from dotenv import load_dotenv

load_dotenv() ## INICIAR O DOTENV

## CONFIG NECESSÁRIAS PARA O PROJETO

intents=disnake.Intents.all()
intents.message_content = True 

token = os.getenv('TOKEN')


#############################################

class BotNews(commands.Bot):

        async def on_ready(self) -> None:
                print(self.user)
    
##############################################
        
bot = BotNews(intents=intents, command_prefix='*')

## PROCESSAR OS ARQUIVOS DE COMANDOS SEPARADOS

def load_extensions(d, p):

    '''LOAD FILES''' 

    for filename in os.listdir(d):
        if filename.endswith('.py'):
            file = filename[:-3]
            bot.load_extension(f'{p}.{file}')


## CASO QUEIRA ADICIONAR COMANDOS NOVOS AO BOT, CHAME ESSA FUNÇÃO COM O CAMINHO DO ARQUIVO.py DESEJADO

load_extensions('./c', 'c')


bot.run(token)
