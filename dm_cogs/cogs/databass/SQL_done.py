import aiosqlite
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "done.db")

async def done_init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS dones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                weekday INTEGER,
                week INTEGER,    -- 第几周 (1-52)
                accomplish INTEGER DEFAULT 0,
                undone INTEGER DEFAULT 0,
                UNIQUE(user_id, weekday, week)
            )
        """)
        await db.commit()

async def addone(user_id):
    now = datetime.now()
    weekday = now.isoweekday()
    week = now.isocalendar()[1]   # 第几周
   
    print(weekday)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO dones (user_id, weekday, week, accomplish) VALUES (?, ?, ?, 1)
            ON CONFLICT(user_id, weekday, week) DO UPDATE SET accomplish = accomplish + 1
        """, (user_id, weekday, week))
        await db.commit()
async def get_weekly_data(user_id):
    now = datetime.now()
    week = now.isocalendar()[1] 


    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT weekday, accomplish,undone FROM dones WHERE user_id = ? AND week = ? ",
            (user_id, week)
        )
        rows = await cursor.fetchall()
    return {row[0]: row[1] for row in rows}
async def del_dones(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM dones WHERE user_id = ?", (user_id,))
        await db.commit()
async def addundone(user_id,undone):
    now = datetime.now()
    weekday = now.isoweekday()
    week = now.isocalendar()[1]   
  
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO dones (user_id, weekday, week, undone) VALUES (?, ?,  ?, ?)
        """, (user_id, weekday, week,undone))
        await db.commit()