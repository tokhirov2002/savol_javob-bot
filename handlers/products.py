from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.db import Database
from keyboards.reply import products_categories_keyboard
from keyboards.inline import product_inline_keyboard
from handlers.text_handler import ProductStates # Yangi FSM holatini import qilish

# Router obyektini yaratish. Bu router mahsulotlar bo'limini boshqaradi.
router = Router()

@router.message(F.text == "🛍 Mahsulotlar")
async def show_products_menu(message: Message, db: Database, state: FSMContext):
    """
    "🛍 Mahsulotlar" tugmasini bosganda ishga tushadigan handler.
    Mahsulot kategoriyalarini ko'rsatadi va foydalanuvchiga tanlashni taklif qiladi.
    Agar baza bo'sh bo'lsa, ba'zi dastlabki mahsulotlarni qo'shadi.
    Va `ProductStates.waiting_for_category_selection` holatini o'rnatadi.
    :param message: Kelgan xabar obyekti.
    :param db: Ma'lumotlar bazasi obyekti.
    :param state: FSM kontekst obyekti.
    """
    # Dastlabki mahsulotlarni ma'lumotlar bazasiga qo'shish (agar mavjud bo'lmasa)
    initial_products = [
        ("Smartfonlar", "Samsung Galaxy S24", "Eng so'nggi Samsung flagmani, ajoyib kamera va kuchli protsessorga ega.", "https://placehold.co/200x200/000/FFF?text=Samsung+S24", "https://www.samsung.com/uz/smartphones/galaxy-s24-ultra/"),
        ("Smartfonlar", "iPhone 15 Pro", "Apple'ning eng kuchli smartfoni, A17 Bionic chipi va titanium korpusiga ega.", "https://placehold.co/200x200/000/FFF?text=iPhone+15", "https://www.apple.com/iphone-15-pro/"),
        ("Aksessuarlar", "Bluetooth quloqchinlar", "Yuqori sifatli simsiz quloqchinlar, uzoq batareya quvvati bilan.", "https://placehold.co/200x200/000/FFF?text=Quloqchinlar", None),
        ("Aksessuarlar", "Smart soat", "Pulsni o'lchash, qadam hisoblash va bildirishnomalar funksiyasiga ega.", "https://placehold.co/200x200/000/FFF?text=Smart+Soat", None),
        ("Noutbuklar", "MacBook Air M3", "Yangi M3 chipiga ega yengil va ixcham noutbuk, yuqori unumdorlik bilan.", "https://placehold.co/200x200/000/FFF?text=MacBook+Air", "https://www.apple.com/macbook-air/"),
        ("Noutbuklar", "Lenovo ThinkPad X1 Carbon", "Biznes uchun mo'ljallangan ishonchli va kuchli noutbuk.", "https://placehold.co/200x200/000/FFF?text=ThinkPad", None)
    ]
    for cat, name, desc, img, url in initial_products:
        # Mahsulotni takroriy qo'shmaslik uchun tekshirish
        existing_products = db.get_products_by_category(cat)
        if not any(p[0] == name for p in existing_products):
            db.add_product(cat, name, desc, img, url)

    # Ma'lumotlar bazasidan barcha noyob kategoriyalarni olish
    categories = db.get_all_categories()
    if not categories:
        await message.answer("Hozircha mahsulotlar mavjud emas.")
        return

    # Kategoriyalarni ReplyKeyboardMarkup orqali ko'rsatish
    await message.answer(
        "Mahsulotlar kategoriyasini tanlang:",
        reply_markup=products_categories_keyboard(categories)
    )
    # Mahsulot kategoriyasini tanlash holatini o'rnatish
    await state.set_state(ProductStates.waiting_for_category_selection)

# show_products_by_category handler'i endi text_handler.py ichida joylashgan
# chunki u FSM holatiga bog'liq va barcha matnli xabarlarni qayta ishlaydigan
# text_handler.py da bo'lishi mantiqan to'g'ri.



# from aiogram import Router, F
# from aiogram.types import Message
# from database.db import Database
# from keyboards.reply import products_categories_keyboard
# from keyboards.inline import product_inline_keyboard
# from aiogram.fsm.context import FSMContext
# from handlers.text_handler import ProductStates 

# # Router obyektini yaratish. Bu router mahsulotlar bo'limini boshqaradi.
# router = Router()


# @router.message(F.text == "🛍 Mahsulotlar")
# async def show_products_menu(message: Message, db: Database, state: FSMContext):
#     """
#     "🛍 Mahsulotlar" tugmasini bosganda ishga tushadigan handler.
#     Mahsulot kategoriyalarini ko'rsatadi va foydalanuvchiga tanlashni taklif qiladi.
#     Agar baza bo'sh bo'lsa, ba'zi dastlabki mahsulotlarni qo'shadi.
#     Va `ProductStates.waiting_for_category_selection` holatini o'rnatadi.
#     :param message: Kelgan xabar obyekti.
#     :param db: Ma'lumotlar bazasi obyekti.
#     :param state: FSM kontekst obyekti.
#     """
#     # Dastlabki mahsulotlarni ma'lumotlar bazasiga qo'shish (agar mavjud bo'lmasa)
#     initial_products = [
#         ("Smartfonlar", "Samsung Galaxy S24", "Eng so'nggi Samsung flagmani, ajoyib kamera va kuchli protsessorga ega.", "https://placehold.co/200x200/000/FFF?text=Samsung+S24", "https://www.samsung.com/uz/smartphones/galaxy-s24-ultra/"),
#         ("Smartfonlar", "iPhone 15 Pro", "Apple'ning eng kuchli smartfoni, A17 Bionic chipi va titanium korpusiga ega.", "https://placehold.co/200x200/000/FFF?text=iPhone+15", "https://www.apple.com/iphone-15-pro/"),
#         ("Aksessuarlar", "Bluetooth quloqchinlar", "Yuqori sifatli simsiz quloqchinlar, uzoq batareya quvvati bilan.", "https://placehold.co/200x200/000/FFF?text=Quloqchinlar", None),
#         ("Aksessuarlar", "Smart soat", "Pulsni o'lchash, qadam hisoblash va bildirishnomalar funksiyasiga ega.", "https://placehold.co/200x200/000/FFF?text=Smart+Soat", None),
#         ("Noutbuklar", "MacBook Air M3", "Yangi M3 chipiga ega yengil va ixcham noutbuk, yuqori unumdorlik bilan.", "https://placehold.co/200x200/000/FFF?text=MacBook+Air", "https://www.apple.com/macbook-air/"),
#         ("Noutbuklar", "Lenovo ThinkPad X1 Carbon", "Biznes uchun mo'ljallangan ishonchli va kuchli noutbuk.", "https://placehold.co/200x200/000/FFF?text=ThinkPad", None)
#     ]
#     for cat, name, desc, img, url in initial_products:
#         # Mahsulotni takroriy qo'shmaslik uchun tekshirish
#         existing_products = db.get_products_by_category(cat)
#         if not any(p[0] == name for p in existing_products):
#             db.add_product(cat, name, desc, img, url)

#     # Ma'lumotlar bazasidan barcha noyob kategoriyalarni olish
#     categories = db.get_all_categories()
#     if not categories:
#         await message.answer("Hozircha mahsulotlar mavjud emas.")
#         return

#     # Kategoriyalarni ReplyKeyboardMarkup orqali ko'rsatish
#     await message.answer(
#         "Mahsulotlar kategoriyasini tanlang:",
#         reply_markup=products_categories_keyboard(categories)
#     )
#     # Mahsulot kategoriyasini tanlash holatini o'rnatish
#     await state.set_state(ProductStates.waiting_for_category_selection)
# # Mahsulot kategoriyalari uchun umumiy handler (yangi kategoriyalar qo'shilsa ham ishlaydi)

# @router.message(F.text.in_(lambda text, db: text in db.get_all_categories(), db_factory=lambda: Database(None))) # Dinamik kategoriya tekshiruvi
# async def show_products_by_category(message: Message, db: Database):
#     """
#     Kategoriya tugmasini bosganda ishga tushadigan handler.
#     Tanlangan kategoriyadagi mahsulotlarni ko'rsatadi.
#     :param message: Kelgan xabar obyekti.
#     :param db: Ma'lumotlar bazasi obyekti.
#     """
#     category = message.text # Foydalanuvchi tanlagan kategoriya matni
#     products = db.get_products_by_category(category) # Bazadan mahsulotlarni olish

#     if not products:
#         await message.answer(f"'{category}' kategoriyasida mahsulotlar topilmadi.")
#         return

#     # Har bir mahsulotni rasm va tavsif bilan yuborish
#     for product in products:
#         name, description, image_url, details_url = product
#         text = f"<b>{name}</b>\n{description}"
#         keyboard = product_inline_keyboard(details_url) # Inline tugmani yaratish

#         if image_url:
#             # Agar rasm URL'i mavjud bo'lsa, rasmni caption bilan yuborish
#             await message.answer_photo(photo=image_url, caption=text, reply_markup=keyboard, parse_mode="HTML")
#         else:
#             # Agar rasm URL'i mavjud bo'lmasa, faqat matnni yuborish
#             await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

