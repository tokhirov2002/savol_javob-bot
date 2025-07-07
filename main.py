import asyncio
import sys
import os

# Loyiha ildiz katalogini PYTHONPATH ga qo'shish
# Bu, bot/main.py dan boshqa modullarni import qilish imkonini beradi.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Loader faylidan bot, dispatcher, startup/shutdown funksiyalari va db obyektini import qilish
from loader import dp, bot, on_startup, on_shutdown, db

# Handler modullarini import qilish
# Har bir handler fayli o'zining router obyektini o'z ichiga oladi.
from handlers import start, faq, products, contact, text_handler

async def main():
    """
    Botning asosiy ishga tushirish funksiyasi.
    Startup/shutdown hook'larni ro'yxatdan o'tkazadi, routerlarni qo'shadi
    va botni ishga tushiradi.
    """
    # Bot ishga tushganda va to'xtatilganda bajariladigan funksiyalarni ro'yxatdan o'tkazish
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Handler routerlarini dispatcherga qo'shish
    # Xabarlar kelganida, dispatcher ularni ro'yxatdan o'tgan routerlar orqali qayta ishlaydi.
    dp.include_router(start.router)
    dp.include_router(faq.router)
    dp.include_router(products.router)
    dp.include_router(contact.router)
    # text_handler.router eng oxirida qo'shilishi kerak, chunki u boshqa hech bir handler tomonidan
    # qayta ishlanmagan barcha matnli xabarlarni tutadi.
    dp.include_router(text_handler.router)

    # Ma'lumotlar bazasi obyektini dispatcherga yuborish
    # Bu, handlerlarda 'db' nomli argument orqali ma'lumotlar bazasiga kirish imkonini beradi.
    dp["db"] = db

    # Botni ishga tushirish va kelgan yangilanishlarni (polling) qabul qilishni boshlash
    print("Bot ishga tushirishga tayyorlanmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Loyihani asosiy fayl sifatida ishga tushirish
    try:
        asyncio.run(main()) # Asosiy funksiyani asinxron tarzda ishga tushirish
    except KeyboardInterrupt:
        # Foydalanuvchi Ctrl+C bosganda botni to'xtatish
        print("\nBot foydalanuvchi tomonidan to'xtatildi.")
    except Exception as e:
        # Boshqa kutilmagan xatoliklarni qayta ishlash
        print(f"Kutilmagan xatolik yuz berdi: {e}")
