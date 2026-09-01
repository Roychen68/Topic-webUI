import discord
from discord.ext import commands
from discord import app_commands # 用於斜線指令
from datetime import datetime
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 事件監聽器 (例如：成員加入、訊息發送)
    @commands.Cog.listener()
    async def on_ready(self):
        print('General 模組已就緒')

    # 標準前綴指令 (例如：!ping)
    @commands.command(name="ping")
    async def ping_cmd(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 延遲：{latency}ms")

   
   
    @app_commands.command(name="echo", description="讓機器人重複你說的話")
    async def echo(self, interaction: discord.Interaction):
        user = interaction.user
        embed = discord.Embed(
        title=f"{user.display_name}的代辦事項",
        color=0x00ff00 
    )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_image(url=user.display_avatar.url)
        embed.add_field(name="項目", value="```diff\n+ OPERATIONAL\n```", inline=True)
        timew = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        embed.set_footer(text=timew)
        await interaction.response.send_message(embed=embed)

# 必須要有這個 setup 函數，main.py 才能正確載入
async def setup(bot):
    await bot.add_cog(General(bot))