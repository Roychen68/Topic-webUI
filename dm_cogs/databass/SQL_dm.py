import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game.db")
async def dm_init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        bypassgame_id INTEGER,
        bypassname TEXT)
        """)
        await db.commit()

async def add_todo(user_id,bypassgame_id,bypassname):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO todos (user_id,bypassgame_id,bypassname) VALUES (?, ?,?)
        """, (user_id,bypassgame_id,bypassname))
        await db.commit()
async def get_all_bypass(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        value = await db.execute("SELECT bypassgame_id,bypassname FROM todos WHERE user_id=? ", (user_id,))
        rows= await value.fetchall()
        
        return rows

async def DEL_todo(user_id, bypassgame_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            DELETE FROM todos WHERE user_id = ? AND bypassgame_id=?
        """, (user_id, bypassgame_id))
        await db.commit()

async def get_todos(user_id, selected_id):
    async with aiosqlite.connect(DB_PATH) as db:
        value = await db.execute(
            "SELECT bypassgame_id, bypassname FROM todos WHERE user_id=? AND bypassgame_id=?", 
            (user_id, selected_id)
        )
        rows = await value.fetchall()
        return rows