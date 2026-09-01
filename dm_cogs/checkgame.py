from discord.ext import tasks, commands
import discord
from .databass.SQL_dm import add_todo, get_all_bypass, DEL_todo



from .cogs.databass.SQL import get_all_game_check, check, get_todos, get_all_todos
from datetime import datetime 
class BypassGameId(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = 1490737355202760804 # ← 指定伺服器
        self.bypassgameid.start()

    def cog_unload(self):
        self.bypassgameid.cancel()  

    @tasks.loop(seconds=10)
    async def bypassgameid(self):
        
        try:
            now = datetime.now().strftime("%H:%M")
            
            
            todo_list = await get_all_game_check(now)
            
            id_list = []
            for i  in todo_list:
                id_list.append(i[1])
            
            guild = self.bot.get_guild(self.guild_id)
            if not guild:
                return
        except Exception as e:
            print(f"錯誤: {e}")
            if not guild:
                return

        for member in guild.members:
            if member.bot:
                continue  
            
            for activity in member.activities:
                if isinstance(activity, discord.CustomActivity):
                    continue 
               # print(member.id)
               # print(id_list)
                if hasattr(activity, 'application_id') and activity.application_id and member.id in id_list:
                    game_name = activity.name
                    game_id = activity.application_id
                    bypassid =await get_all_bypass(member.id)
                    bypass_game_ids = [i[0] for i in bypassid]  
                    if game_id not in bypass_game_ids:
                            try:
                                await member.send(f"偵測到遊戲：**{game_name}**\n遊戲 ID：`{game_id}`")
                                print(f"send{game_name}")
                            except discord.Forbidden:
                                print(f"無法傳送給 {member.name}（關閉私訊）")

    @bypassgameid.before_loop
    async def before_bypassgameid(self):
        await self.bot.wait_until_ready()
async def setup(bot):
    await bot.add_cog(BypassGameId(bot))