from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage # FSM holatlarini xotirada saqlash uchun
from config import BOT_TOKEN, DB_NAME
from database.db import Database

# Bot obyektini ishga tushirish. HTML parse_mode xabarlarda HTML teglarini ishlatish imkonini beradi.
bot = Bot(token=BOT_TOKEN)

# Dispatcher obyektini ishga tushirish.
# MemoryStorage FSM holatlarini bot xotirasida saqlash uchun ishlatiladi.
# Katta loyihalar uchun Redis yoki boshqa doimiy saqlash usullari tavsiya etiladi.
dp = Dispatcher(storage=MemoryStorage())

# Ma'lumotlar bazasi obyektini ishga tushirish
db = Database(DB_NAME)

# Bot ishga tushganda bajariladigan funksiya
async def on_startup():
    """
    Bot ishga tushganda ma'lumotlar bazasiga ulanishni amalga oshiradi.
    """
    db.connect()
    print("Ma'lumotlar bazasi ulandi va jadvallar tekshirildi.")

# Bot to'xtatilganda bajariladigan funksiya
async def on_shutdown():
    """
    Bot to'xtatilganda ma'lumotlar bazasi ulanishini yopadi.
    """
    db.close()
    print("Ma'lumotlar bazasi ulanishi yopildi.")
