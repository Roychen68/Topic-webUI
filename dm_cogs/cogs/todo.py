from discord.ext import commands
from discord.ui import Select, View
import discord
from datetime import datetime, timedelta
from discord import app_commands
from .databass.SQL  import add_todo, get_todos, done_todo, DEL_todo,get_all_todos
from .databass.SQL_done import addone,del_dones,addundone
from .databass.picture import get_weekly_chart
class AddTodoModal(discord.ui.Modal, title="新增代辦"):
    content_input = discord.ui.TextInput(
        label="代辦事項",
        max_length=4000,
        required=True
    )
    starthour_input = discord.ui.TextInput(
        label="幾點開始(時)",
        style=discord.TextStyle.short,
        placeholder='23',
        required=True
    )
    startmin_input = discord.ui.TextInput(
        label="幾點開始(分)",
        style=discord.TextStyle.short,
        placeholder='00',
        required=True
    )
    hour_input = discord.ui.TextInput(
        label="持續幾個小時",
        style=discord.TextStyle.short,
        placeholder='1(非必填)',
        required=False
    )
    min_input = discord.ui.TextInput(
        label="持續幾分鐘",
        style=discord.TextStyle.short,
        placeholder='30(非必填)',
        required=False
    )
    async def on_submit(self, interaction: discord.Interaction):
        try:
            content = self.content_input.value
            hour = int(self.starthour_input.value)
            min = int(self.startmin_input.value)
            if(self.hour_input.value!=""):
                how_long_hour = int(self.hour_input.value)
            else:
                how_long_hour=0
            if(self.min_input.value!=""):
                how_long_min = int(self.min_input.value)
            else:
                how_long_min=0


        except:
            await interaction.response.send_message(f"格式錯誤請重新輸入")
            return
        start_point = datetime.now().replace(hour=hour, minute=min)
        long = how_long_hour*60+how_long_min
        future_time = start_point + timedelta(minutes=long)
        todo_list = await get_all_todos(interaction.user.id)
        for i in todo_list:
            existing_start = datetime.strptime(i[3], "%H:%M").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            existing_end = datetime.strptime(i[4], "%H:%M").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
            if start_point < existing_end and future_time > existing_start:
                await interaction.response.send_message("時間不可重疊")
                return
        if future_time.day-start_point.day  !=0:
            await interaction.response.send_message("時間不可超過今天")
            return
        due_date = start_point.strftime("%H:%M")
        finensh_time = future_time.strftime("%H:%M")
        await add_todo(interaction.user.id,content,due_date,finensh_time)
        todo_list = await get_all_todos(interaction.user.id)
        view = DoneView(todo_list, interaction.user.id)
        await interaction.response.send_message(f"新增了`{content}`", view=view,ephemeral=True)
class DoneSelect(discord.ui.Select):
    def __init__(self, todo_list, place):
        if not todo_list:
            options = [discord.SelectOption(label="清單是空的", value="empty")]
        else:
            options = [
                discord.SelectOption(
                    label=f"{i[1]} {'✅' if i[2] else '❌'} start:{i[3]}",
                    value=str(i[0])
                )
                for i in todo_list
            ]

        super().__init__(placeholder=place, options=options)
    
    async def callback(self, interaction: discord.Interaction):

        self.view.selected_id = int(self.values[0])  # 存到 View 裡
        todo = await get_todos(self.view.user_id, self.view.selected_id)
        for option in self.options:
            option.default = option.value == self.values[0]
        is_done = todo[0][1]  # done 欄位
        if(is_done):
            self.view.check_confirm.label = "已完成" 
        else:
            self.view.check_confirm.label = "確認完成" 
        self.view.check_confirm.disabled = is_done

        self.view.del_confirm.disabled = False 
        await interaction.response.edit_message(view=self.view)
        
class DoneView(discord.ui.View):
    def __init__(self, todo_list, user_id):
        super().__init__()
        self.user_id = user_id
        self.selected_id = None  # 先空著
        self.add_item(DoneSelect(todo_list,"選擇項目"))
    
    @discord.ui.button(label="請選擇", style=discord.ButtonStyle.green,disabled=True)
    async def check_confirm(self, interaction, button):
        if self.selected_id is None:
           return
        await done_todo(self.user_id, self.selected_id)    
        try:
           
            await addone(self.user_id)
        except Exception as e :
            print(e)
        content = await get_todos(self.user_id,self.selected_id)
        test = content[0][0]
        todo_list = await get_all_todos(self.user_id)
        new_view = DoneView(todo_list, self.user_id)
        await interaction.response.edit_message(content=f"`{test}` is done✅", view=new_view)
    @discord.ui.button(label="刪除", style=discord.ButtonStyle.red,disabled=True)
    async def del_confirm(self, interaction, button):
        if self.selected_id is None:
           return
        
        content = await get_todos(self.user_id,self.selected_id)
        test = content[0][0]
        
        await DEL_todo(self.user_id, self.selected_id)
        
        todo_list = await get_all_todos(self.user_id)
        new_view = DoneView(todo_list, self.user_id)
        await interaction.response.edit_message(view=new_view)
        
        await interaction.followup.send(f"`{test}` is DEL✅",ephemeral=True)
class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="add", description="新增待辦事項")
    async def add(self,interaction):
        await interaction.response.send_modal(AddTodoModal())
    @app_commands.command(name="get_list", description="列出清單")
    async def get_list(self,interaction):
        try:
            user = interaction.user
            todo_list=await get_all_todos(interaction.user.id)
            
            result = "\n".join(
            f" ```diff\n+ {i[1]}\n``` ✅    **start:{i[3]} **  |  **end:{i[4]} ** \n" if i[2] else f"```diff\n- {i[1]}\n``` ❌    **start:{i[3]} **  |  **end:{i[4]} ** \n"
            for i in todo_list
            )
            #cont =await get_undone(self.user_id)
            if(result!=""):
                embed = discord.Embed(
                title=f"{user.display_name}的代辦事項",
                color=0xFFF1BC)
                embed.set_thumbnail(url=user.display_avatar.url)

                embed.set_image(url=await get_weekly_chart(user.id))
                embed.add_field(name="項目", value=result, inline=True)
                timew = datetime.now().strftime("%Y年%m月%d日 %H:%M")
                embed.set_footer(text=timew)
                await interaction.response.send_message(embed=embed,ephemeral=True)
            else:
                
                await interaction.response.send_message(f"<@{interaction.user.id}>:\n"+"查無資料",ephemeral=True)
        except Exception as a:
                print(a)
    @app_commands.command(name="done", description="選擇要刪除或完成項目")
    async def done(self,interaction):
        todo_list = await get_all_todos(interaction.user.id)
        view = DoneView(todo_list, interaction.user.id)
        await interaction.response.send_message("選擇要完成或刪除的項目：", view=view,ephemeral=True)
    @app_commands.command(name="del", description="刪除")
    async def Del_todo(self,interaction,id:int):
        todo_list=await get_todos(interaction.user.id,id)
        content = todo_list[0][0]  
        await DEL_todo(interaction.user.id, id)
        await interaction.response.send_message(f"user:<@{interaction.user.id}> {content} is del",ephemeral=True)
async def setup(bot):
    await bot.add_cog(Todo(bot))