from discord.ext import tasks
from discord.ext import commands
from datetime import datetime
import discord
from .databass.SQL  import get_all_check,check,get_todos,get_all_todos
class CheckView(discord.ui.View):
    def __init__(self, user_id,user_todo_id):
        super().__init__()
        self.user_id = user_id
        self.user_todo_id = user_todo_id
        
    @discord.ui.button(label="check", style=discord.ButtonStyle.green,disabled=False)
    async def check_confirm(self, interaction,button):
        
        await check(self.user_id, self.user_todo_id)
        
        content = await get_todos(self.user_id,self.user_todo_id)
        
        test = content[0][0]
        await interaction.response.send_message(content=f"`{test}` is check✅")
        
class CheckDate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_due_dates.start()

    @tasks.loop(seconds=10)
    async def check_due_dates(self):
        now = datetime.now().strftime("%H:%M")
  
        todo_list = await get_all_check(now)
        
        for todo in todo_list:
            content = todo[0]
            user_id = todo[1]
            user_todo_id = todo[4]
            time=todo[3]
            user = await self.bot.fetch_user(user_id)
            view = CheckView(user_id, user_todo_id)
            await user.send(f"<@{user_id}>`{content}` 時間到了！結束時間{time}",view=view)
                

async def setup(bot):
    await bot.add_cog(CheckDate(bot))