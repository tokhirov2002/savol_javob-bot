from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards.reply import main_menu_keyboard, admin_menu_keyboard
from config import ADMIN_ID

# Router obyektini yaratish. Bu router start buyrug'i va 'Ortga' tugmasini boshqaradi.
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start buyrug'ini qabul qiluvchi handler.
    Foydalanuvchini ismi bilan kutib oladi va asosiy menyuni ko'rsatadi.
    Agar foydalanuvchi admin bo'lsa, admin menyusini ko'rsatadi.
    :param message: Kelgan xabar obyekti.
    """
    user_name = message.from_user.full_name # Foydalanuvchining to'liq ismini olish
    user_id = str(message.from_user.id) # Foydalanuvchi ID'sini stringga o'tkazish

    # Admin IDsi o'rnatilgan bo'lsa va joriy foydalanuvchi admin bo'lsa
    if ADMIN_ID and user_id == ADMIN_ID:
        keyboard = admin_menu_keyboard() # Admin menyusini yuklash
        await message.answer(
            f"Assalomu alaykum, admin {user_name}! Botingizga xush kelibsiz.",
            reply_markup=keyboard
        )
    else:
        # Oddiy foydalanuvchilar uchun asosiy menyuni yuklash
        keyboard = main_menu_keyboard()
        await message.answer(
            f"Assalomu alaykum, {user_name}! Botingizga xush kelibsiz.",
            reply_markup=keyboard
        )

@router.message(F.text == "⬅️ Ortga")
async def back_to_main_menu(message: Message):
    """
    "⬅️ Ortga" tugmasini bosganda ishga tushadigan handler.
    Foydalanuvchini asosiy menyuga qaytaradi.
    :param message: Kelgan xabar obyekti.
    """
    await message.answer("Bosh menyuga qaytdingiz.", reply_markup=main_menu_keyboard())
