import discord
import os
import asyncio
from discord.ext import commands
from dm_cogs.cogs.databass.SQL import init_db,del_all
from dm_cogs.databass.SQL_dm import dm_init_db
from dm_cogs.cogs.databass.SQL_done import done_init_db
from discord import app_commands
class MyBot(commands.Bot):
    def __init__(self):
        # 1. 設定 Intents (存取權限)
        intents = discord.Intents.default()
        intents.message_content = True  # 讀取訊息內容權限
        intents.members = True    # ← 加這行，否則看不到別人的 activities
        intents.presences = True  
        super().__init__(
            command_prefix="!", 
            intents=intents,
            help_command=None # 停用預設 Help 以便未來製作精美的 Help
        )
        
        @commands.command()
        async def reloud(ctx,extension):
            await self.reload_extension(f"cogs.{extension}")
            await ctx.send(f"ReLoaded {extension} done.")
        @commands.command()
        async def reloud_all(ctx):
        
            await self.setup_hook()
            await self.cocomand()
            await ctx.send(f"ReLoaded all done.")
        @commands.command()
        async def reset(ctx):
            await del_all()
            await ctx.send(f"all reset")
        self.add_command(reloud)
        self.add_command(reloud_all)
        self.add_command(reset)
    async def on_message(self, message):
        ctx = await self.get_context(message)
        if ctx.command:
            try:
                await ctx.command.invoke(ctx)
            except Exception as e:
                print(f"執行錯誤: {e}")
    async def setup_hook(self):
    # 取得 main.py 所在的資料夾絕對路徑
        self.tree.allowed_installs = app_commands.AppInstallationType(guild=True, user=True)
        self.tree.allowed_contexts = app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True)
        base_path = os.path.dirname(os.path.abspath(__file__))
        cogs_path = os.path.join(base_path, 'dm_cogs','cogs')
        await init_db()
        await done_init_db()
        for filename in os.listdir(cogs_path):
            if filename.endswith('.py'):
                try:
                    await self.reload_extension(f'dm_cogs.cogs.{filename[:-3]}')
                except commands.ExtensionNotLoaded:
                    await self.load_extension(f'dm_cogs.cogs.{filename[:-3]}')
                except Exception as e:  # 這個要放最後
                    print(f'❌ 載入失敗: {filename} | {e}')
                    try:
                        await self.load_extension(f'dm_cogs.cogs.{filename[:-3]}')
                        print(f'✅ 已載入模組: {filename}')
                    except:
                        await self.reload_extension(f'dm_cogs.cogs. {filename[:-3]}')
                        print(f'✅ 已載入模組: {filename}')
                    
                 
    async def cocomand(self):
                try:
                    synced = await self.tree.sync()
                    print(f'🌐 已同步 {len(synced)} 個斜線指令')
                    for cmd in synced:
                        print(f"  - {cmd.name}") 
                except Exception as e:
                    print(f'❌ 指令同步失敗: {e}')

    async def on_ready(self):
        print(f'---')
        print(f'🤖 機器人名稱: {self.user.name}')
        print(f'🆔 機器人 ID: {self.user.id}')
        
        activity = discord.Activity(type=discord.ActivityType.listening, name="test bot")
        await self.change_presence(status=discord.Status.do_not_disturb, activity=activity)
        await self.cocomand()

        print(f'---')
        print(self.commands) 
    
class dmbot(commands.Bot):
    def __init__(self):
        
        intents = discord.Intents.default()
        intents.message_content = True  # 讀取訊息內容權限
        intents.members = True        # ← 加這行，否則看不到別人的 activities
        intents.presences = True  
        super().__init__(
            command_prefix="?", 
            intents=intents,
            help_command=None 
        )
      
        @commands.command()
        async def dm_reloud_all(ctx):
        
            await self.setup_hook()
            await self.cocomand()
            await ctx.send(f"ReLoaded all done.")
       
        self.add_command(dm_reloud_all)
    async def on_message(self, message):
        ctx = await self.get_context(message)
        if ctx.command:
            try:
                await ctx.command.invoke(ctx)
            except Exception as e:
                print(f"執行錯誤: {e}")
    async def setup_hook(self):
        self.tree.allowed_installs = app_commands.AppInstallationType(guild=True, user=True)
        self.tree.allowed_contexts = app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True)
        base_path = os.path.dirname(os.path.abspath(__file__))
        cogs_path = os.path.join(base_path, 'dm_cogs')
        await dm_init_db()
        
        for filename in os.listdir(cogs_path):
            if filename.endswith('.py'):
                try:
                    await self.reload_extension(f'dm_cogs.{filename[:-3]}')
                except commands.ExtensionNotLoaded:
                    await self.load_extension(f'dm_cogs.{filename[:-3]}')
                except Exception as e:  # 這個要放最後
                    print(f'❌ 載入失敗: {filename} | {e}')
                    try:
                        await self.load_extension(f'dm_cogs.{filename[:-3]}')
                        print(f'✅ 已載入模組: {filename}')
                    except:
                        await self.reload_extension(f'dm_cogs.{filename[:-3]}')
                        print(f'✅ 已載入模組: {filename}')
                    
                 
    async def cocomand(self):
                try:
                    synced = await self.tree.sync()
                    print(f'🌐 已同步 {len(synced)} 個斜線指令')
                    for cmd in synced:
                        print(f"  - {cmd.name}") 
                except Exception as e:
                    print(f'❌ 指令同步失敗: {e}')

    async def on_ready(self):
        print(f'---')
        print(f'🤖 機器人名稱: {self.user.name}')
        print(f'🆔 機器人 ID: {self.user.id}')
        
        
        await self.cocomand()

        print(f'---')
        print(self.commands) 

async def main():
    TOKEN = "MTQ4ODU2ODg3OTYzNzcyOTYxMg.GyR0x2.8tGhmsm8AaJ4ZJerwxObhc4eAAX3wYDF0Du178"
    DM_token = "MTQ5MDk5NDUyMDQ0MjAxMTY0OA.GsfNuP.95WZHvSxO6rBgW7sPZHmZ4y8JQP_Ab7JnaEOHk"
    
    bot = MyBot()
    dm_bot = dmbot()
    
    await asyncio.gather(
        bot.start(TOKEN),
        dm_bot.start(DM_token)
    )

if __name__ == "__main__":
    asyncio.run(main())
    