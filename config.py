import os
from dotenv import load_dotenv

# .env faylidan atrof-muhit o'zgaruvchilarini yuklash
load_dotenv()

# Bot tokenini .env faylidan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Admin ID'sini .env faylidan olish (ixtiyoriy, admin funksiyalari uchun)
# Bu ID orqali bot adminni aniqlaydi va unga qo'shimcha buyruqlarni ko'rsatadi.
ADMIN_ID = os.getenv("ADMIN_ID")

# Ma'lumotlar bazasi faylining joylashuvi
# Loyiha ildiz katalogidagi 'data' papkasida 'qa.db' faylini yaratadi.
DB_NAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'qa.db')

# Agar BOT_TOKEN topilmasa, xatolik berish
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida topilmadi. Iltimos, uni sozlang.")

# Foydalanuvchiga ko'rsatiladigan rasmiy sayt URL'i
# MUHIM: Bu yerga o'zingizning haqiqiy veb-saytingiz URL'ini kiriting.
# Hozircha xato bermasligi uchun Google.com manzilini qo'ydim.
OFFICIAL_WEBSITE_URL = "https://www.google.com"



# import os
# from dotenv import load_dotenv

# # .env faylidan atrof-muhit o'zgaruvchilarini yuklash
# load_dotenv()

# # Bot tokenini .env faylidan olish
# BOT_TOKEN = os.getenv("BOT_TOKEN")

# # Admin ID'sini .env faylidan olish (ixtiyoriy, admin funksiyalari uchun)
# # Bu ID orqali bot adminni aniqlaydi va unga qo'shimcha buyruqlarni ko'rsatadi.
# ADMIN_ID = os.getenv("ADMIN_ID")

# # Ma'lumotlar bazasi faylining joylashuvi
# # Loyiha ildiz katalogidagi 'data' papkasida 'qa.db' faylini yaratadi.
# DB_NAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'qa.db')

# # Agar BOT_TOKEN topilmasa, xatolik berish
# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN .env faylida topilmadi. Iltimos, uni sozlang.")

# # Foydalanuvchiga ko'rsatiladigan rasmiy sayt URL'i
# OFFICIAL_WEBSITE_URL = "[https://example.com](https://example.com)" # O'zingizning rasmiy saytingiz URL'ini kiriting
