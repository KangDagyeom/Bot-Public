import discord
from discord.ext import commands
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from discord import Embed
import asyncio

sys.stdout.reconfigure(encoding='utf-8')

# Khai báo intents
intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.messages = True 
intents.message_content = True

# Cấu hình Spotipy
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id='6149cde1f3984bec84bea00a767327c5', client_secret='2b5a3398dc834697a50e2fd2f9a16a0b'))
client = commands.Bot(command_prefix='/', intents=intents)




@client.command()
async def play(ctx, *, song_name):
    await ctx.send('🎵 **Dưới đây là những bài hát mà có thể bạn đang tìm kiếm** 🎵')
    results = spotify.search(q=song_name, limit=5)  

    if results['tracks']['items']:
        for item in results['tracks']['items']:
            song_name = item['name']
            song_url = item['external_urls']['spotify']
            await ctx.send(f'🎶 **Bài hát:** {song_name}\n🔗 **Link đến bài hát:** {song_url}')
    else:
        await ctx.send('❌ **Không tìm thấy bài hát, hãy thử tìm kiếm cả tên nghệ sĩ và một số dấu hiệu nhận biết khác**')


# Khóa API RapidAPI
RAPIDAPI_KEY = "79e9925fedmsh5ece400febbd5d0p1e7721jsna398b5210fa7"

#Youtbe
@client.command()
async def video(ctx, *, video_name):
    embed=Embed(
        title='Youtube',
        description='Xem video và short video !',
        color=0xff0000
    )
    embed.set_thumbnail(url='https://inkythuatso.com/uploads/images/2021/10/youtube-logo-inkythuatso-01-27-14-06-56.jpg')
    await ctx.send(embed=embed)
    try:
        # Tìm kiếm video trên YouTube
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            'q': video_name,
            'part': 'snippet',
            'key': 'AIzaSyCthyv70U7bJ0XgYhRSBz6BTDaNG3WVSY0',
            'maxResults': 3  
        }
        response = requests.get(search_url, params=params)
        data = response.json()

        # Lấy URL của video đầu tiên trong kết quả
        video_urls = [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in data['items']]

        # Gửi URL của video cho người dùng
        await ctx.send(f"This is the video you want: {video_urls}")
    except Exception as e:
        await ctx.send("Có lỗi xảy ra khi tìm kiếm video.")
#Chat GPT
@client.command(name='gpt')
async def chatgpt_command(ctx, *, question):
    try:
        url = "https://chatgpt-best-price.p.rapidapi.com/v1/chat/completions"

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "chatgpt-best-price.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                chat_gpt_response = data['choices'][0]['message']['content']
                await ctx.send(f'Bot: {chat_gpt_response}')
            else:
                await ctx.send("Không có phản hồi từ ChatGPT.")
        else:
            await ctx.send(f"Lỗi: HTTP status code {response.status_code}")
    
    except Exception as e:
        await ctx.send(f"Lỗi: {str(e)}")
#Text
@client.command()
async def text(ctx):
    text = (
        "Bold: **Text** hoặc __Text__\n"
        "Ví dụ: Bold Text\n\n"

        "Italic: *Text* hoặc _Text_\n"
        "Ví dụ: Italic Text\n\n"

        "Underline: __Text__\n"
        "Ví dụ: Underline Text\n\n"

        "Strikethrough: ~~Text~~\n"
        "Ví dụ: Strikethrough Text\n\n"

        "Bold Italic: ***Text*** hoặc ___Text___\n"
        "Ví dụ: Bold Italic Text\n\n"

        "Monospace: `Text`\n"
        "Ví dụ: Monospace Text"
    )
    await ctx.send(text)
@client.command()
async def ping(ctx):
    embed=Embed(
        title='Pong !',
        description='Xin chào đây là Musix bot #1455',
        color=0xffffff
    )
    embed.set_thumbnail(url='https://i.pinimg.com/564x/c3/01/26/c30126b804adc5e61f6c10f2be6706cc.jpg')
    await ctx.send(embed=embed)
#tier list
@client.command()
async def checktier(ctx):
    embed=Embed(
        title='Game8',
        description='Xếp hạng tất cả nhân vật Honkai Starrail !',
        color=0xffff00
    )
    embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_FmfS2q96FldhDgcKkukiT9vvXM4s1hfEsNxfkUMIyA&s')
    await ctx.send(embed=embed)
    # URL của trang web chứa thông tin xếp hạng nhân vật
    await ctx.send('https://game8.co/games/Honkai-Star-Rail/archives/409604')

#Welcome
@client.event
async def on_member_join(member):
    channel = member.guild.system_channel  # Lấy kênh hệ thống của server
    if channel is not None:
        await channel.send(f"Chào mừng {member.mention} đã tham gia server!")
    else:
        print("Không tìm thấy kênh hệ thống.")
@client.command()
async def pick_roles(ctx):
    # Gửi tin nhắn với emoji và tên vai trò
    message = await ctx.send("Pick your roles:\n"
                             ":boy: - Boy\n"
                             ":girl: - Girl\n"
                             ":rainbow_flag: - LGBTQ+")

    # Thêm emoji vào tin nhắn để người dùng có thể phản ứng
    await message.add_reaction('👦')  # Emoji cho Boy
    await message.add_reaction('👧')  # Emoji cho Girl
    await message.add_reaction('🏳️‍🌈')  # Emoji cho LGBTQ+

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['👦', '👧', '🏳️‍🌈']

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=None, check=check)

        # Thêm vai trò tương ứng cho người dùng
        if str(reaction.emoji) == '👦':
            role = discord.utils.get(ctx.guild.roles, name='Boy')
        elif str(reaction.emoji) == '👧':
            role = discord.utils.get(ctx.guild.roles, name='Girl')
        elif str(reaction.emoji) == '🏳️‍🌈':
            role = discord.utils.get(ctx.guild.roles, name='LGBTQ+')

        await ctx.author.add_roles(role)
        private_channel = await ctx.author.create_dm()
        await private_channel.send(f"You've been assigned the role: {role.name}")
    except asyncio.TimeoutError:
        private_channel = await ctx.author.create_dm()
        await private_channel.send("Timeout: (Troll, bot not have timeout :))")

#help
@client.command()
async def guide(ctx):
    embed = discord.Embed(
        title="Guide of Musix bot",
        description="All commands of bot",
        color=discord.Color.brand_red()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1226077250622062663/1255523098644451460/vecteezy_discord-app-logo-in-big-sur-style-3d-render-icon-design_35746042.jpg?ex=667d7081&is=667c1f01&hm=1a838ba65b85f83d5997e19962e1888b5aa0173f7279ac4b7a5908d104c72ee3&")
    message = (
        "**/ping - to ping bot**\n\n"
        "**/play [Your_Song_Name] - listening to music on Spotify**\n\n"
        "**/video [Your_Video_Name] - watching video on Youtube**\n\n"
        "**/text - view text change on Discord**\n\n"
        "**/gpt [Your_QUESTION] - ask chat Gpt 3.5 turbo**\n\n"
        "**/checktier - Check tier list characters in Honkai Star Rail**\n"
    )
    embed.add_field(name="Commands", value=message)
    await ctx.send(embed = embed)

# Sự kiện khi bot đã sẵn sàng
@client.event
async def on_ready():
    
    await client.change_presence(status=discord.Status.idle, activity=discord.Streaming(name='Game with 3,325,566 people in Valorant | !help', url='https://www.twitch.tv/directory/category/valorant'))
    print(f'{client.user} đã sẵn sàng và đang hoạt động trên các máy chủ:')
    for guild in client.guilds:
        print(f'- {guild.name} (ID: {guild.id})')

# Chạy bot với token của bạn
client.run('')