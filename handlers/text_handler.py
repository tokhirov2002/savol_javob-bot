from aiogram import Router, F
from aiogram.types import Message
from database.db import Database
from config import ADMIN_ID
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import main_menu_keyboard
from keyboards.inline import product_inline_keyboard

# Router obyektini yaratish. Bu router erkin matnli xabarlar va admin buyruqlarini boshqaradi.
router = Router()

# Admin funksiyalari uchun holat mashinasi (FSM - Finite State Machine)
class AdminStates(StatesGroup):
    # Savol-javob qo'shish holatlari
    waiting_for_qa_question = State()
    waiting_for_qa_answer = State()
    # Savol-javob o'chirish holati
    waiting_for_delete_qa_question = State()
    # Mahsulot qo'shish holatlari
    waiting_for_product_category = State()
    waiting_for_product_name = State()
    waiting_for_product_description = State()
    waiting_for_product_image_url = State()
    waiting_for_product_details_url = State()

# Mahsulot kategoriyasini tanlash holati
class ProductStates(StatesGroup):
    waiting_for_category_selection = State()


@router.message(F.text == "✍️ Erkin savol berish")
async def free_question_prompt(message: Message, state: FSMContext):
    """
    "✍️ Erkin savol berish" tugmasini bosganda ishga tushadigan handler.
    Foydalanuvchiga savol yozishni taklif qiladi va FSM holatini tozalaydi.
    :param message: Kelgan xabar obyekti.
    :param state: FSM kontekst obyekti.
    """
    await state.clear() # Boshqa FSM holatidan chiqish
    await message.answer("Iltimos, savolingizni yozing. Men bazadan javob topishga harakat qilaman.")

@router.message(F.text)
async def handle_text_messages(message: Message, db: Database, state: FSMContext):
    """
    Barcha kelgan matnli xabarlarni qabul qiluvchi handler.
    1. Xabarni loglaydi.
    2. Agar foydalanuvchi admin bo'lsa, admin buyruqlarini tekshiradi va bajaradi.
    3. Agar FSM holati mahsulot kategoriyasini kutayotgan bo'lsa, uni qayta ishlaydi.
    4. Agar hech qanday maxsus buyruq yoki FSM holati bo'lmasa, savol-javob bazasidan javob qidiradi.
    :param message: Kelgan xabar obyekti.
    :param db: Ma'lumotlar bazasi obyekti.
    :param state: FSM kontekst obyekti.
    """
    # 1. Barcha kelgan xabarlarni loglash
    user = message.from_user
    db.log_message(
        user.id,
        user.username if user.username else "Noma'lum",
        user.first_name if user.first_name else "Noma'lum",
        user.last_name if user.last_name else "",
        message.text
    )

    current_state = await state.get_state() # Joriy FSM holatini olish

    # 2. Agar foydalanuvchi admin bo'lsa, admin buyruqlarini tekshirish
    if ADMIN_ID and str(message.from_user.id) == ADMIN_ID:
        # --- Savol-javob qo'shish ---
        if message.text == "🔄 Savol-javob qo‘shish":
            await message.answer("Iltimos, yangi savolni kiriting:")
            await state.set_state(AdminStates.waiting_for_qa_question) # Holatni o'rnatish
            return
        elif current_state == AdminStates.waiting_for_qa_question:
            await state.update_data(new_question=message.text) # Savolni saqlash
            await message.answer("Iltimos, savolga javobni kiriting:")
            await state.set_state(AdminStates.waiting_for_qa_answer) # Keyingi holatga o'tish
            return
        elif current_state == AdminStates.waiting_for_qa_answer:
            user_data = await state.get_data() # Oldingi ma'lumotlarni olish
            question = user_data.get("new_question")
            answer = message.text
            if db.add_qa(question, answer):
                await message.answer(f"Savol-javob muvaffaqiyatli qo'shildi:\n<b>Savol:</b> {question}\n<b>Javob:</b> {answer}", parse_mode="HTML")
            else:
                await message.answer("Savol-javobni qo'shishda xatolik yuz berdi.")
            await state.clear() # Holatni tozalash
            return

        # --- Savol-javob o'chirish ---
        elif message.text == "❌ Savol o‘chirish":
            await message.answer("O'chirmoqchi bo'lgan savolni to'liq kiriting:")
            await state.set_state(AdminStates.waiting_for_delete_qa_question)
            return
        elif current_state == AdminStates.waiting_for_delete_qa_question:
            question_to_delete = message.text
            if db.delete_qa(question_to_delete):
                await message.answer(f"Savol '<b>{question_to_delete}</b>' muvaffaqiyatli o'chirildi.", parse_mode="HTML")
            else:
                await message.answer(f"Savol '<b>{question_to_delete}</b>' topilmadi. Iltimos, savolni to'liq va to'g'ri kiriting.", parse_mode="HTML")
            await state.clear()
            return

        # --- Mahsulot qo'shish ---
        elif message.text == "📝 Mahsulot qo‘shish":
            await message.answer("Mahsulot kategoriyasini kiriting (masalan: Smartfonlar):")
            await state.set_state(AdminStates.waiting_for_product_category)
            return
        elif current_state == AdminStates.waiting_for_product_category:
            await state.update_data(product_category=message.text)
            await message.answer("Mahsulot nomini kiriting:")
            await state.set_state(AdminStates.waiting_for_product_name)
            return
        elif current_state == AdminStates.waiting_for_product_name:
            await state.update_data(product_name=message.text)
            await message.answer("Mahsulot tavsifini kiriting:")
            await state.set_state(AdminStates.waiting_for_product_description)
            return
        elif current_state == AdminStates.waiting_for_product_description:
            await state.update_data(product_description=message.text)
            await message.answer("Mahsulot rasmi URL'ini kiriting (agar yo'q bo'lsa 'yoq' deb yozing):")
            await state.set_state(AdminStates.waiting_for_product_image_url)
            return
        elif current_state == AdminStates.waiting_for_product_image_url:
            image_url = message.text if message.text.lower() != 'yoq' else None
            await state.update_data(product_image_url=image_url)
            await message.answer("Mahsulot batafsil ma'lumot URL'ini kiriting (agar yo'q bo'lsa 'yoq' deb yozing):")
            await state.set_state(AdminStates.waiting_for_product_details_url)
            return
        elif current_state == AdminStates.waiting_for_product_details_url:
            details_url = message.text if message.text.lower() != 'yoq' else None
            user_data = await state.get_data()
            category = user_data.get("product_category")
            name = user_data.get("product_name")
            description = user_data.get("product_description")
            image_url = user_data.get("product_image_url")

            if db.add_product(category, name, description, image_url, details_url):
                await message.answer(f"Mahsulot '<b>{name}</b>' muvaffaqiyatli qo'shildi.", parse_mode="HTML")
            else:
                await message.answer("Mahsulotni qo'shishda xatolik yuz berdi.")
            await state.clear()
            return

        # --- Statistika ---
        elif message.text == "📊 Statistika":
            stats = db.get_log_stats()
            response = f"<b>Umumiy xabarlar soni:</b> {stats['total_messages']}\n\n"
            response += "<b>Eng faol foydalanuvchilar (ID, Xabarlar soni):</b>\n"
            if stats['top_users']:
                for user_id, count in stats['top_users']:
                    response += f"- <code>{user_id}</code>: {count} ta xabar\n"
            else:
                response += "Ma'lumotlar mavjud emas.\n"
            await message.answer(response, parse_mode="HTML")
            return

    # 3. Agar FSM holati mahsulot kategoriyasini kutayotgan bo'lsa
    if current_state == ProductStates.waiting_for_category_selection:
        category = message.text
        all_categories = db.get_all_categories()
        if category in all_categories:
            products = db.get_products_by_category(category)
            if not products:
                await message.answer(f"'{category}' kategoriyasida mahsulotlar topilmadi.")
            else:
                for product in products:
                    name, description, image_url, details_url = product
                    text = f"<b>{name}</b>\n{description}"
                    keyboard = product_inline_keyboard(details_url)
                    if image_url:
                        await message.answer_photo(photo=image_url, caption=text, reply_markup=keyboard, parse_mode="HTML")
                    else:
                        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
            await state.clear() # Kategoriyani tanlagandan keyin holatni tozalash
            return
        else:
            await message.answer("Kechirasiz, bunday kategoriya topilmadi. Iltimos, ro'yxatdan tanlang yoki '⬅️ Ortga' tugmasini bosing.")
            return # Boshqa handlerlarga o'tmasin

    # 4. Agar hech qanday maxsus buyruq yoki FSM holati bo'lmasa, savol-javob bazasidan javob qidirish
    # Bu qism faqatgina FSM holati bo'sh bo'lganda va yuqoridagi shartlar bajarilmaganda ishlaydi.
    if not current_state: # FSM holati mavjud emasligini tekshirish
        answer = db.get_answer(message.text)
        if answer:
            await message.answer(answer)
        else:
            await message.answer("Kechirasiz, bu savolga javob topilmadi.")

