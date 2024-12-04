import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os

Token = ''
bot = commands.Bot(command_prefix='\\', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Je viens de me réveiller. Je suis', bot.user.name)

@bot.command()
async def torrent(ctx):
    await ctx.send("lien du site pour installer qbitorrent : https://www.qbittorrent.org/download")

@bot.command()
async def fit(ctx, recherche : str):
    first = recherche.split('.')[0]
    print(first)
    recherche = recherche.replace('.', '+')
    #cherche
    url = f'https://fitgirl-repacks.site/?s={recherche}'
    await ctx.send(f'étape 1 : ok !')
    page_fit = requests.get(url)
    with open('page_fit.txt', 'w', encoding='utf-8') as file:
        file.write(page_fit.text)
    await ctx.send('étape 2 : ok !')
    #cherche lien de la page chercher
    with open('page_fit.txt', 'r', encoding='utf-8') as file:
        html_data = file.read()
        soup = BeautifulSoup(html_data, 'html.parser')
        lien = soup.find('a', href=lambda href: href and href.startswith(f'https://fitgirl-repacks.site/{first}'))
        if lien:
            await ctx.send(f'étape 3 : ok !')
            url_bis = f'{lien.get("href")}'
            await ctx.send(f'étape 4 : ok !')
            page_fit_bis = requests.get(url_bis)
            with open('page_fit_bis.txt', 'w', encoding='utf-8') as file:
                file.write(page_fit_bis.text)
            await ctx.send('étape 5 : ok !')
            with open('page_fit_bis.txt', 'r', encoding='utf-8') as file:
                html_data = file.read()
                soup = BeautifulSoup(html_data, 'html.parser')
                title = soup.title.string
                await ctx.send(f'nous avons trouver : {title}')
            with open('page_fit_bis.txt', 'r', encoding='utf-8') as file:
                html_data = file.read()
                soup = BeautifulSoup(html_data, 'html.parser')
                magnet_links = soup.find_all('a', href=lambda href: href and href.startswith('magnet:')and href.endswith('Fannounce'))
                if magnet_links:
                  for link in magnet_links:
                      # Créer un fichier texte avec le lien magnet
                      file_name = f"{recherche}.txt"
                      with open(file_name, 'w') as file:
                          file.write(link["href"])

                      # Envoi du fichier dans le chat
                      with open(file_name, 'rb') as f:
                          file = discord.File(f)
                          await ctx.send(f'Voici le lien magnet : ', file=file)

                      # Supprimer le fichier après l'avoir envoyé
                      os.remove(file_name)
                else:
                    await ctx.send('failed !')
        else:
            await ctx.send('étape 3 : failed !')

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'{amount} messages ont été supprimés.', delete_after=5)

bot.run(Token)
