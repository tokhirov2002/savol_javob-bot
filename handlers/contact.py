from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import support_inline_keyboard, website_inline_keyboard
from config import OFFICIAL_WEBSITE_URL

# Router obyektini yaratish. Bu router aloqa va ma'lumot bo'limlarini boshqaradi.
router = Router()

@router.message(F.text == "📞 Aloqa")
async def show_contact_info(message: Message):
    """
    "📞 Aloqa" tugmasini bosganda ishga tushadigan handler.
    Aloqa ma'lumotlarini ko'rsatadi va qo'llab-quvvatlash tugmalarini taklif qiladi.
    :param message: Kelgan xabar obyekti.
    """
    await message.answer(
        "Biz bilan bog'lanish:\n\n"
        "Telefon: +998 90 123 45 67\n"
        "Email: info@example.com\n"
        "Ish vaqti: Dushanba-Juma, 9:00-18:00",
        reply_markup=support_inline_keyboard() # Qo'llab-quvvatlash inline tugmalarini ko'rsatish
    )

@router.message(F.text == "🕘 Ish vaqti")
async def show_working_hours(message: Message):
    """
    "🕘 Ish vaqti" tugmasini bosganda ishga tushadigan handler.
    Ish vaqtini ko'rsatadi.
    :param message: Kelgan xabar obyekti.
    """
    await message.answer("Bizning ish vaqtimiz:\nDushanba-Juma: 09:00 - 18:00\nShanba-Yakshanba: Dam olish kuni")

@router.message(F.text == "📍 Manzil")
async def show_address(message: Message):
    """
    "📍 Manzil" tugmasini bosganda ishga tushadigan handler.
    Kompaniyaning manzilini ko'rsatadi.
    :param message: Kelgan xabar obyekti.
    """
    await message.answer("Bizning manzilimiz: Toshkent shahri, Mustaqillik shoh ko'chasi, 1-uy.")
    # Agar xohlasangiz, Telegramning joylashuv funksiyasidan foydalanishingiz mumkin:
    # await message.answer_location(latitude=41.2825, longitude=69.2163) # Toshkent, Mustaqillik maydoni taxminiy koordinatalari

@router.message(F.text == "🌐 Rasmiy sayt")
async def show_website(message: Message):
    """
    "🌐 Rasmiy sayt" tugmasini bosganda ishga tushadigan handler.
    Rasmiy saytga o'tish tugmasini ko'rsatadi.
    :param message: Kelgan xabar obyekti.
    """
    await message.answer("Bizning rasmiy saytimiz:", reply_markup=website_inline_keyboard(OFFICIAL_WEBSITE_URL))

@router.message(F.text == "ℹ️ Bot haqida")
async def about_bot(message: Message):
    """
    "ℹ️ Bot haqida" tugmasini bosganda ishga tushadigan handler.
    Bot haqida qisqacha ma'lumot beradi.
    :param message: Kelgan xabar obyekti.
    """
    await message.answer("Bu bot sizga mahsulotlarimiz, tez-tez so'raladigan savollar va aloqa ma'lumotlari haqida ma'lumot berish uchun yaratilgan.")

@router.callback_query(F.data == "contact_operator")
async def contact_operator_callback(callback_query: CallbackQuery):
    """
    "Operator bilan bog'lanish" inline tugmasi bosilganda ishga tushadigan handler.
    Foydalanuvchiga xabar yuborishni taklif qiladi. Haqiqiy loyihada bu yerda adminlarga xabar yuborish mumkin.
    :param callback_query: Kelgan callback query obyekti.
    """
    await callback_query.answer("Sizning so'rovingiz qabul qilindi. Operatorimiz tez orada siz bilan bog'lanadi.", show_alert=True)
    await callback_query.message.answer(
        "Operatorimiz tez orada siz bilan bog'lanadi. Iltimos, savolingizni to'liq yozib qoldiring."
    )

@router.callback_query(F.data == "go_to_faq")
async def go_to_faq_callback(callback_query: CallbackQuery):
    """
    "Tez-tez so'raladigan savollar" inline tugmasi bosilganda ishga tushadigan handler.
    Foydalanuvchini FAQ bo'limiga yo'naltiradi.
    :param callback_query: Kelgan callback query obyekti.
    """
    await callback_query.answer("FAQ bo'limiga o'tmoqdasiz...", show_alert=False)
    # FAQ handlerini chaqirish uchun, "❓ FAQ" matnini qayta yuborish (bu text_handler.py ga tushadi)
    # Yoki to'g'ridan-to'g'ri FAQ handler funksiyasini chaqirish mumkin, agar u import qilingan bo'lsa.
    # Hozircha, foydalanuvchiga "❓ FAQ" tugmasini bosishni taklif qilamiz.
    await callback_query.message.answer(
        "Siz FAQ bo'limiga yo'naltirildingiz. Iltimos, '❓ FAQ' tugmasini bosing yoki savolingizni yozing."
    )
