from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database.db import Database
from keyboards.inline import faq_inline_keyboard

# Router obyektini yaratish. Bu router FAQ bo'limini boshqaradi.
router = Router()

@router.message(F.text == "❓ FAQ")
async def show_faq(message: Message, db: Database):
    """
    "❓ FAQ" tugmasini bosganda ishga tushadigan handler.
    Ma'lumotlar bazasidan tez-tez so'raladigan savol-javoblarni oladi va ko'rsatadi.
    Agar baza bo'sh bo'lsa, ba'zi dastlabki savol-javoblarni qo'shadi.
    :param message: Kelgan xabar obyekti.
    :param db: Ma'lumotlar bazasi obyekti (loader orqali yuboriladi).
    """
    # Dastlabki savol-javoblarni qo'shish (agar baza bo'sh bo'lsa)
    initial_faqs = [
        ("Bot nima ish qiladi?", "Bu bot sizning savollaringizga javob beradi va mahsulotlar haqida ma'lumot beradi."),
        ("Mahsulotlarni qayerdan ko'rishim mumkin?", "Mahsulotlar bo'limida kategoriyalar bo'yicha ko'rishingiz mumkin."),
        ("Qo'llab-quvvatlash xizmati bormi?", "Ha, 'Qo'llab-quvvatlash' bo'limida operator bilan bog'lanishingiz mumkin.")
    ]
    for q, a in initial_faqs:
        # Faqatgina savol bazada mavjud bo'lmasa qo'shish
        if not db.get_answer(q):
            db.add_qa(q, a)

    # Ma'lumotlar bazasidagi barcha savol-javoblarni olish
    all_qa = db.get_all_qa()

    if not all_qa:
        await message.answer("Hozircha tez-tez so'raladigan savollar mavjud emas.")
        return

    response_text = "Tez-tez so'raladigan savollar:\n\n"
    # Har bir savol-javobni formatlab javob matniga qo'shish
    for i, (q, a) in enumerate(all_qa):
        response_text += f"<b>{i+1}. {q}</b>\nJavob: {a}\n\n"
        # "Ko'proq o'qish" tugmasi hozircha faqat joy egallaydi, chunki javob to'liq ko'rsatilgan.
        # Agar javoblar qisqartirib ko'rsatilishi kerak bo'lsa, bu yerda o'zgarishlar kiritiladi.
        # await message.answer(f"<b>{i+1}. {q}</b>", reply_markup=faq_inline_keyboard(i+1), parse_mode="HTML")
        # await message.answer(f"Javob: {a}", parse_mode="HTML")

    await message.answer(response_text, parse_mode="HTML")

@router.callback_query(F.data.startswith("faq_read_more_"))
async def faq_read_more_callback(callback_query: CallbackQuery, db: Database):
    """
    "Ko'proq o'qish" inline tugmasi bosilganda ishga tushadigan handler.
    Hozircha faqat xabarni tasdiqlaydi. Haqiqiy loyihada bu yerda to'liq javob ko'rsatiladi.
    :param callback_query: Kelgan callback query obyekti.
    :param db: Ma'lumotlar bazasi obyekti.
    """
    # Callback data'dan savol ID'sini ajratib olish
    question_id = int(callback_query.data.split("_")[-1])
    # Haqiqiy stsenariyda, bu yerda question_id yordamida bazadan to'liq javob olinadi
    # va foydalanuvchiga yuboriladi.
    await callback_query.answer("Batafsil ma'lumot shu yerda ko'rsatiladi.", show_alert=True)
    # Agar xohlasangiz, xabarni tahrirlab to'liq javobni ko'rsatishingiz mumkin:
    # all_qa = db.get_all_qa()
    # if question_id <= len(all_qa):
    #     q, a = all_qa[question_id - 1]
    #     await callback_query.message.edit_text(f"<b>{q}</b>\nTo'liq javob: {a}", parse_mode="HTML")
