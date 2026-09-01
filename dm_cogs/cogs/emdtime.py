from discord.ext import tasks
from discord.ext import commands
from datetime import datetime
from datetime import datetime, timedelta
import discord
from .databass.SQL  import get_end_time,add_time,get_todos
class Check(discord.ui.View):
    def __init__(self, user_id,user_todo_id):
        super().__init__()
        self.user_id = user_id
        self.user_todo_id = user_todo_id
    @discord.ui.button(label="add 10 min", style=discord.ButtonStyle.green,disabled=False)
    async def check_confirm(self, interaction,button):
        content = await get_todos(self.user_id,self.user_todo_id)
        test = content[0][0]
        time = content[0][3]
  
        t = datetime.strptime(time, "%H:%M")
        new_time = (t + timedelta(minutes=10)).strftime("%H:%M")
        print(new_time)
        await add_time(self.user_id,self.user_todo_id,new_time)
        
        await interaction.response.send_message(content=f"`{test}` has been add 10 min end time ")
class addtime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_due_dates.start()

    @tasks.loop(seconds=10)
    async def check_due_dates(self):
        now = datetime.now().strftime("%H:%M")
  
        todo_list = await get_end_time(now)
        
        for todo in todo_list:
            content = todo[0]
            user_id = todo[1]
            user_todo_id = todo[4]
            user = await self.bot.fetch_user(user_id)
            view = Check(user_id, user_todo_id)
            await user.send(f"<@{user_id}>`{content}` 已經結束了 ",view=view)
                

async def setup(bot):
    await bot.add_cog(addtime(bot))