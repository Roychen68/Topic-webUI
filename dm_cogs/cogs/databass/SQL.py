import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.db")
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE )
        
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_todo_id INTEGER,
        user_fk INTEGER,
        content TEXT,
        done INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date TIMESTAMP,
        finensh_time TIMESTAMP,
        is_check INTEGER DEFAULT 0,
        FOREIGN KEY (user_fk) REFERENCES users(id))
        """)
        await db.commit()
async def get_or_create_user(db, user_id):
    
    cursor = await db.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
    row = await cursor.fetchone()
    
    if row is None:
        
        await db.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()
        cursor = await db.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        row = await cursor.fetchone()
    
    return row[0]  
async def add_todo(user_id, content,due_date,finensh_time):
    async with aiosqlite.connect(DB_PATH) as db:
        user_fk = await get_or_create_user(db, user_id)
        cursor = await db.execute("SELECT COUNT(*) FROM todos WHERE user_fk = ?", (user_fk,))
        row = await cursor.fetchone()
        user_todo_id = row[0] + 1  # 加1就是新的編號
        
        # 再插入
        await db.execute("""
            INSERT INTO todos (user_fk, user_todo_id, content, done,due_date,finensh_time) VALUES (?, ?, ?, 0,?,?)
        """, (user_fk, user_todo_id, content,due_date,finensh_time))
        
        await db.commit()
        return user_todo_id
async def get_all_todos(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        
        user_fk =await get_or_create_user(db,user_id)
      # value= await db.execute("SELECT content FROM todos WHERE user_id=?",(user_id,))
        
        
        value = await db.execute("SELECT user_todo_id, content, done,due_date,finensh_time FROM todos WHERE user_fk=? ORDER BY due_date ASC", (user_fk,))
        rows= await value.fetchall()
        
        return rows
async def get_todos(user_id, user_todo_id):
    async with aiosqlite.connect(DB_PATH) as db:
       user_fk =await get_or_create_user(db,user_id)
       value= await db.execute("SELECT content,done,due_date,finensh_time FROM todos WHERE user_fk=? AND  user_todo_id=? ",(user_fk, user_todo_id))
       return await value.fetchall()
async def done_todo(user_id, user_todo_id):
    async with aiosqlite.connect(DB_PATH) as db:
        user_fk =await get_or_create_user(db,user_id)
        await db.execute("""
            UPDATE todos SET done=1 WHERE user_fk = ? AND user_todo_id=?                 
        """,(user_fk,user_todo_id))
        await db.commit()
async def DEL_todo(user_id, user_todo_id):
    async with aiosqlite.connect(DB_PATH) as db:
        user_fk =await get_or_create_user(db,user_id)
        await db.execute("""
            DELETE FROM todos WHERE user_fk = ? AND user_todo_id=?                   
        """,(user_fk,user_todo_id))
        await db.execute(""" UPDATE todos SET user_todo_id = user_todo_id - 1 WHERE user_fk = ? AND user_todo_id > ?""", (user_fk, user_todo_id))
        await db.commit()
async def get_all_date(today):
    async with aiosqlite.connect(DB_PATH) as db:
       value= await db.execute("SELECT todos.content, users.user_id ,todos.done,todos.finensh_time FROM todos JOIN users ON todos.user_fk = users.id WHERE todos.due_date = ? AND todos.is_check=0",(today,))
       return await value.fetchall()
async def check(user_id, user_todo_id):
    async with aiosqlite.connect(DB_PATH) as db:
        user_fk =await get_or_create_user(db,user_id)
        await db.execute("""
            UPDATE todos SET is_check=1 WHERE user_fk = ? AND user_todo_id=?                 
        """,(user_fk,user_todo_id))
        await db.commit()
async def get_all_check(today):
    async with aiosqlite.connect(DB_PATH) as db:
        value = await db.execute("""
        SELECT todos.content, users.user_id, todos.done, todos.finensh_time, todos.user_todo_id
        FROM todos JOIN users ON todos.user_fk = users.id 
        WHERE (todos.due_date = ? OR todos.due_date < ?) AND todos.is_check = 0 AND todos.done=0
        """, (today, today))
        return await value.fetchall()

async def get_all_game_check(today):
    async with aiosqlite.connect(DB_PATH) as db:
        value = await db.execute("""
        SELECT todos.content, users.user_id, todos.done, todos.finensh_time, todos.user_todo_id
        FROM todos JOIN users ON todos.user_fk = users.id 
        WHERE ((todos.due_date = ? OR (todos.due_date < ? AND ? < todos.finensh_time)) AND todos.finensh_time != todos.due_date)
        """, (today, today,today))
        return await value.fetchall()
async def get_end_time(today):
    async with aiosqlite.connect(DB_PATH) as db:
        value = await db.execute("""
        SELECT todos.content, users.user_id, todos.done, todos.finensh_time, todos.user_todo_id
        FROM todos JOIN users ON todos.user_fk = users.id 
        WHERE (todos.finensh_time = ? OR todos.finensh_time < ?) AND todos.done=0 AND todos.finensh_time != todos.due_date
        """, (today, today))
        return await value.fetchall()
async def add_time(user_id, user_todo_id, time):
    async with aiosqlite.connect(DB_PATH) as db:
        user_fk =await get_or_create_user(db,user_id)
        await db.execute("UPDATE todos SET finensh_time=? WHERE user_fk=? AND user_todo_id=?", (time, user_fk, user_todo_id))
        await db.commit()

# async def get_undone(user_id):
#     async with aiosqlite.connect(DB_PATH) as db:
        
#         user_fk =await get_or_create_user(db,user_id)

        
#         value = await db.execute("SELECT user_todo_id, content, done FROM todos WHERE user_fk=? AND done=0 ", (user_fk,))
#         rows= await value.fetchall()
        
#         return rows
async def del_all():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM todos")
        await db.execute("DELETE FROM sqlite_sequence WHERE name='todos'")
        await db.commit()