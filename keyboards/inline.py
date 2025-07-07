from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OFFICIAL_WEBSITE_URL

# FAQ bo'limi uchun inline tugma yaratuvchi funksiya
def faq_inline_keyboard(question_id):
    """
    FAQ savoli uchun "Ko'proq o'qish" inline tugmasini yaratadi.
    Callback data orqali qaysi savolga tegishli ekanligi aniqlanadi.
    :param question_id: Savolning noyob identifikatori.
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ko‘proq o‘qish", callback_data=f"faq_read_more_{question_id}")]
    ])
    return kb

# Mahsulotlar uchun inline tugma yaratuvchi funksiya
def product_inline_keyboard(details_url=None):
    """
    Mahsulot uchun "Batafsil ma'lumot" inline tugmasini yaratadi.
    Agar details_url berilgan bo'lsa, URL tugmasi qo'shiladi.
    :param details_url: Mahsulot haqida batafsil ma'lumot beruvchi URL.
    """
    # Inline tugmalar ro'yxati
    buttons = []
    if details_url:
        buttons.append(InlineKeyboardButton(text="Batafsil ma’lumot", url=details_url))
    
    # InlineKeyboardMarkup ni to'g'ri Aiogram v3 sintaksisi bilan yaratish
    kb = InlineKeyboardMarkup(inline_keyboard=[buttons]) if buttons else None
    return kb

# Qo'llab-quvvatlash bo'limi uchun inline tugmalar yaratuvchi funksiya
def support_inline_keyboard():
    """
    Qo'llab-quvvatlash bo'limi uchun "Operator bilan bog'lanish" va
    "Tez-tez so'raladigan savollar" inline tugmalarini yaratadi.
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Operator bilan bog'lanish", callback_data="contact_operator")],
        [InlineKeyboardButton(text="Tez-tez so'raladigan savollar", callback_data="go_to_faq")]
    ])
    return kb

# Rasmiy sayt uchun inline tugma yaratuvchi funksiya
def website_inline_keyboard(url=OFFICIAL_WEBSITE_URL):
    """
    Rasmiy saytga o'tish uchun inline URL tugmasini yaratadi.
    :param url: Rasmiy saytning URL'i.
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Rasmiy saytga o'tish", url=url)]
    ])
    return kb



# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from config import OFFICIAL_WEBSITE_URL

# # FAQ bo'limi uchun inline tugma yaratuvchi funksiya
# def faq_inline_keyboard(question_id):
#     """
#     FAQ savoli uchun "Ko'proq o'qish" inline tugmasini yaratadi.
#     Callback data orqali qaysi savolga tegishli ekanligi aniqlanadi.
#     :param question_id: Savolning noyob identifikatori.
#     """
#     kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Ko‘proq o‘qish", callback_data=f"faq_read_more_{question_id}")]
#     ])
#     return kb

# # Mahsulotlar uchun inline tugma yaratuvchi funksiya
# def product_inline_keyboard(details_url=None):
#     """
#     Mahsulot uchun "Batafsil ma'lumot" inline tugmasini yaratadi.
#     Agar details_url berilgan bo'lsa, URL tugmasi qo'shiladi.
#     :param details_url: Mahsulot haqida batafsil ma'lumot beruvchi URL.
#     """
#     kb = InlineKeyboardMarkup(inline_keyboard=[])
#     if details_url:
#         kb.add(InlineKeyboardButton(text="Batafsil ma’lumot", url=details_url))
#     return kb

# # Qo'llab-quvvatlash bo'limi uchun inline tugmalar yaratuvchi funksiya
# def support_inline_keyboard():
#     """
#     Qo'llab-quvvatlash bo'limi uchun "Operator bilan bog'lanish" va
#     "Tez-tez so'raladigan savollar" inline tugmalarini yaratadi.
#     """
#     kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Operator bilan bog'lanish", callback_data="contact_operator")],
#         [InlineKeyboardButton(text="Tez-tez so'raladigan savollar", callback_data="go_to_faq")]
#     ])
#     return kb

# # Rasmiy sayt uchun inline tugma yaratuvchi funksiya
# def website_inline_keyboard(url=OFFICIAL_WEBSITE_URL):
#     """
#     Rasmiy saytga o'tish uchun inline URL tugmasini yaratadi.
#     :param url: Rasmiy saytning URL'i.
#     """
#     kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="Rasmiy saytga o'tish", url=url)]
#     ])
#     return kb
