from .databass.SQL_dm import add_todo, get_all_bypass, DEL_todo,get_todos
import discord
from discord import app_commands
from discord.ext import commands
class DoneSelect(discord.ui.Select):
    def __init__(self, todo_list, place):
        if not todo_list:
            options = [discord.SelectOption(label="清單是空的", value="empty")]
        else:
            options = [
                discord.SelectOption(
                    label=i[1],       # bypassname
                    value=str(i[0])  
                )
                for i in todo_list
            ]

        super().__init__(placeholder=place, options=options)
    
    async def callback(self, interaction: discord.Interaction):

        self.view.selected_id = int(self.values[0])  
        todo = await get_todos(self.view.user_id, self.view.selected_id)
        for option in self.options:
            option.default = option.value == self.values[0]
        for item in self.view.children:
            if isinstance(item, discord.ui.Button) and item.label == "刪除":
                item.disabled = False
        await interaction.response.edit_message(view=self.view)
        
class DoneView(discord.ui.View):
    def __init__(self, todo_list, user_id):
        super().__init__()
        self.user_id = user_id
        self.selected_id = None 
        self.add_item(DoneSelect(todo_list,"選擇項目"))
    @discord.ui.button(label="刪除", style=discord.ButtonStyle.red,disabled=True)
    async def del_confirm(self, interaction, button):
        if self.selected_id is None:
           return
        
        content = await get_todos(self.user_id,self.selected_id)
        test = content[0][0]
        
        await DEL_todo(self.user_id, self.selected_id)
        
        todo_list = await get_all_bypass(self.user_id)
        new_view = DoneView(todo_list, self.user_id)
        await interaction.response.edit_message(view=new_view)
        
        await interaction.followup.send(f"`{test}` is DEL✅")
class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addbypass", description="加入掠過名單(伺服器才可用)")
    async def addbypass(self,interaction):
        member = interaction.guild.get_member(interaction.user.id)
        game_id=None
        game_name=None
        for activity in member.activities:
            if hasattr(activity, 'application_id') and activity.application_id:
                game_id = activity.application_id
                game_name = activity.name
                break
        if not game_id:
            await interaction.response.send_message("❌ 沒有偵測到遊戲！")
            return
        await add_todo(interaction.user.id,game_id,game_name)
 
        await interaction.response.send_message(f"<@{interaction.user.id}>:\n 已加入{game_name}")
    @app_commands.command(name="remove", description="刪除BYPASSGAME")
    async def done(self,interaction):
        todo_list = await get_all_bypass(interaction.user.id)
        view = DoneView(todo_list, interaction.user.id)
        await interaction.response.send_message("選擇要完成或刪除的項目：", view=view)
async def setup(bot):
    await bot.add_cog(Todo(bot))