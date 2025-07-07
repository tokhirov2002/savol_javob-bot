from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Asosiy menyu tugmalarini yaratuvchi funksiya
def main_menu_keyboard():
    """
    Foydalanuvchiga asosiy menyuni ko'rsatish uchun ReplyKeyboardMarkup yaratadi.
    """
    kb = ReplyKeyboardMarkup(
        keyboard=[
            # Birinchi qator tugmalar
            [KeyboardButton(text="ℹ️ Bot haqida"), KeyboardButton(text="🛍 Mahsulotlar")],
            # Ikkinchi qator tugmalar
            [KeyboardButton(text="🕘 Ish vaqti"), KeyboardButton(text="📍 Manzil")],
            # Uchinchi qator tugmalar
            [KeyboardButton(text="🎧 Qo‘llab-quvvatlash"), KeyboardButton(text="❓ FAQ")],
            # To'rtinchi qator tugmalar
            [KeyboardButton(text="✍️ Erkin savol berish"), KeyboardButton(text="🌐 Rasmiy sayt")],
            # Beshinchi qator tugma
            [KeyboardButton(text="📞 Aloqa")]
        ],
        resize_keyboard=True,  # Tugmalarni klaviatura o'lchamiga moslashtirish
        input_field_placeholder="Menuga o'tish uchun tugmani tanlang..." # Kiritish maydonchasida ko'rsatiladigan matn
    )
    return kb

# Mahsulot kategoriyalari uchun tugmalarni yaratuvchi funksiya
def products_categories_keyboard(categories):
    """
    Mahsulot kategoriyalarini ko'rsatish uchun ReplyKeyboardMarkup yaratadi.
    :param categories: Kategoriya nomlari ro'yxati.
    """
    # Kategoriyalar uchun tugmalarni dinamik ravishda yaratish
    category_buttons = [[KeyboardButton(text=category)] for category in categories]
    
    # "Ortga" tugmasini alohida qatorga qo'shish
    back_button = [KeyboardButton(text="⬅️ Ortga")]
    
    # Barcha tugmalarni birlashtirib, ReplyKeyboardMarkup ga berish
    kb = ReplyKeyboardMarkup(
        keyboard=category_buttons + [back_button], # Barcha kategoriya tugmalari va "Ortga" tugmasi
        resize_keyboard=True,
        input_field_placeholder="Kategoriyani tanlang..."
    )
    return kb

# Admin menyusi tugmalarini yaratuvchi funksiya
def admin_menu_keyboard():
    """
    Adminlar uchun maxsus menyuni ko'rsatish uchun ReplyKeyboardMarkup yaratadi.
    """
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔄 Savol-javob qo‘shish"), KeyboardButton(text="❌ Savol o‘chirish")],
            [KeyboardButton(text="📝 Mahsulot qo‘shish"), KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="⬅️ Ortga")] # Asosiy menyuga qaytish tugmasi
        ],
        resize_keyboard=True,
        input_field_placeholder="Admin menyusi..."
    )
    return kb








# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# # Asosiy menyu tugmalarini yaratuvchi funksiya
# def main_menu_keyboard():
#     """
#     Foydalanuvchiga asosiy menyuni ko'rsatish uchun ReplyKeyboardMarkup yaratadi.
#     """
#     kb = ReplyKeyboardMarkup(
#         keyboard=[
#             # Birinchi qator tugmalar
#             [KeyboardButton(text="ℹ️ Bot haqida"), KeyboardButton(text="🛍 Mahsulotlar")],
#             # Ikkinchi qator tugmalar
#             [KeyboardButton(text="🕘 Ish vaqti"), KeyboardButton(text="📍 Manzil")],
#             # Uchinchi qator tugmalar
#             [KeyboardButton(text="🎧 Qo‘llab-quvvatlash"), KeyboardButton(text="❓ FAQ")],
#             # To'rtinchi qator tugmalar
#             [KeyboardButton(text="✍️ Erkin savol berish"), KeyboardButton(text="🌐 Rasmiy sayt")],
#             # Beshinchi qator tugma
#             [KeyboardButton(text="📞 Aloqa")]
#         ],
#         resize_keyboard=True,  # Tugmalarni klaviatura o'lchamiga moslashtirish
#         input_field_placeholder="Menuga o'tish uchun tugmani tanlang..." # Kiritish maydonchasida ko'rsatiladigan matn
#     )
#     return kb

# # Mahsulot kategoriyalari uchun tugmalarni yaratuvchi funksiya
# def products_categories_keyboard(categories):
#     """
#     Mahsulot kategoriyalarini ko'rsatish uchun ReplyKeyboardMarkup yaratadi.
#     :param categories: Kategoriya nomlari ro'yxati.
#     """
#     kb = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Kategoriyani tanlang...")
#     for category in categories:
#         kb.add(KeyboardButton(text=category)) # Har bir kategoriya uchun tugma qo'shish
#     kb.add(KeyboardButton(text="⬅️ Ortga")) # Asosiy menyuga qaytish tugmasi
#     return kb

# # Admin menyusi tugmalarini yaratuvchi funksiya
# def admin_menu_keyboard():
#     """
#     Adminlar uchun maxsus menyuni ko'rsatish uchun ReplyKeyboardMarkup yaratadi.
#     """
#     kb = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text="🔄 Savol-javob qo‘shish"), KeyboardButton(text="❌ Savol o‘chirish")],
#             [KeyboardButton(text="📝 Mahsulot qo‘shish"), KeyboardButton(text="📊 Statistika")],
#             [KeyboardButton(text="⬅️ Ortga")] # Asosiy menyuga qaytish tugmasi
#         ],
#         resize_keyboard=True,
#         input_field_placeholder="Admin menyusi..."
#     )
#     return kb
