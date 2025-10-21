import disnake
import os
import aiohttp
import datetime

from aiohttp import request
from disnake.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

# CHAVE DA API 
key = os.getenv('KEY_NYT')


## ESSE LINK PODE FICAR DESATUALIZADO, PORTANTO, ANTES DE EXECUTAR É BOM TESTA-LO
## LEMBRANDO QUE A DOCUMENTAÇÃO DA API DISPONIBILIZA ESSA E OUTRA INFORMAÇÕES RELEVANTES PARA O PROJETO.

n = (f'https://api.nytimes.com/svc/news/v3/content/nyt/technology.json?api-key={key}')

class PostTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # INICIALIZAÇÃO DAS TASKS
        self.very.start()
        self.news_publi = set()
        

    # O LOOP ESTÁ DEFINIDO A CADA 30 MINUTOS
    @tasks.loop(minutes=30)
    async def very(self):

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(n, headers={}) as response:
                    data = await response.json()
                    news_list = data["results"]

            for news in news_list:
                
                # SUBSTITUA PELO ID DO CANAL DESEJADO 
                channel_id = 1430188743712837682

                if news["published_date"] not in self.news_publi:
                    post = self.bot.get_channel(channel_id)

                    # ESSA PARTE DO EMBED, PERSONALIZE DA FORMA QUE DESEJAR
                    e = disnake.Embed(
                        title= news["title"],
                        url=news["url"], 
                        description= news["abstract"],
                        colour= disnake.Colour.from_rgb(158, 17, 29),
                        timestamp=datetime.datetime.now()
                        )

                    multimedia = news.get("multimedia")

                    news_img = multimedia[0]["url"]
                    news_copyright = data["copyright"]
                    news_date = datetime.datetime.now()

                    logo =  'https://www.familialiteraria.com.br/files/fotos/mega_noticias/mid/28.jpg'
                    logo_two = 'https://static01.nyt.com/vi-assets/images/share/1200x1200_t.png'


                    e.set_author(
                        name= news["byline"], 
                        icon_url= logo
                        )

                    e.set_image(news_img)
                    e.set_footer(text=news_copyright, icon_url=logo_two)

                    # PRINT OPCIONAL
                    print(f'Novo post - {news_date}')
                    
                    await post.send(embed=e)
                    self.news_publi.add(news["published_date"])

        except Exception as e:
            print(e)


    @very.before_loop
    async def before_verificar_noticias(self):
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot):
    bot.add_cog(PostTask(bot))