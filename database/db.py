import sqlite3
import os
from .models import CREATE_QA_TABLE_SQL, CREATE_PRODUCTS_TABLE_SQL, CREATE_LOGS_TABLE_SQL

# Ma'lumotlar bazasi bilan ishlash uchun yordamchi sinf
class Database:
    def __init__(self, db_name):
        """
        Database sinfini ishga tushirish.
        :param db_name: SQLite ma'lumotlar bazasi faylining nomi (yo'li).
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._ensure_data_directory_exists()

    def _ensure_data_directory_exists(self):
        """
        Ma'lumotlar bazasi fayli joylashadigan 'data' papkasini yaratish.
        """
        data_dir = os.path.dirname(self.db_name)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def connect(self):
        """
        Ma'lumotlar bazasiga ulanish va jadvallarni yaratish (agar mavjud bo'lmasa).
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self._create_tables()
            print(f"Ma'lumotlar bazasi '{self.db_name}' ga ulanildi.")
        except sqlite3.Error as e:
            print(f"Ma'lumotlar bazasiga ulanishda xatolik: {e}")

    def _create_tables(self):
        """
        Ma'lumotlar bazasi jadvallarini yaratish.
        """
        try:
            self.cursor.execute(CREATE_QA_TABLE_SQL)
            self.cursor.execute(CREATE_PRODUCTS_TABLE_SQL)
            self.cursor.execute(CREATE_LOGS_TABLE_SQL)
            self.conn.commit()
            print("Jadvallar muvaffaqiyatli yaratildi/tekshirildi.")
        except sqlite3.Error as e:
            print(f"Jadvallarni yaratishda xatolik: {e}")

    def close(self):
        """
        Ma'lumotlar bazasi ulanishini yopish.
        """
        if self.conn:
            self.conn.close()
            print("Ma'lumotlar bazasi ulanishi yopildi.")

    # --- QA (Savol-Javob) operatsiyalari ---

    def add_qa(self, question, answer):
        """
        Yangi savol-javob juftligini ma'lumotlar bazasiga qo'shish.
        :param question: Savol matni.
        :param answer: Javob matni.
        """
        try:
            self.cursor.execute("INSERT INTO qa (question, answer) VALUES (?, ?)", (question, answer))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Savol-javob qo'shishda xatolik: {e}")
            return False

    def get_answer(self, user_question):
        """
        Foydalanuvchi savoliga mos javobni ma'lumotlar bazasidan topish.
        Savolga qisman (LIKE operatori bilan) va katta/kichik harflarga e'tibor bermasdan (LOWER funksiyasi bilan) mos keladi.
        :param user_question: Foydalanuvchi tomonidan berilgan savol matni.
        :return: Topilgan javob matni yoki None agar topilmasa.
        """
        try:
            # LOWER funksiyasi savolni kichik harflarga o'tkazadi
            # LIKE operatori qisman moslikni tekshiradi
            self.cursor.execute(
                "SELECT answer FROM qa WHERE LOWER(question) LIKE LOWER(?)",
                (f"%{user_question}%",)
            )
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Javobni olishda xatolik: {e}")
            return None

    def get_all_qa(self):
        """
        Barcha savol-javob juftliklarini ma'lumotlar bazasidan olish.
        :return: (savol, javob) kortejlar ro'yxati.
        """
        try:
            self.cursor.execute("SELECT question, answer FROM qa")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Barcha savol-javoblarni olishda xatolik: {e}")
            return []

    def delete_qa(self, question):
        """
        Berilgan savolga mos savol-javob juftligini o'chirish.
        :param question: O'chiriladigan savol matni.
        :return: True agar muvaffaqiyatli o'chirilsa, False aks holda.
        """
        try:
            self.cursor.execute("DELETE FROM qa WHERE question = ?", (question,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Savol-javobni o'chirishda xatolik: {e}")
            return False

    # --- Product (Mahsulot) operatsiyalari ---

    def add_product(self, category, name, description, image_url=None, details_url=None):
        """
        Yangi mahsulotni ma'lumotlar bazasiga qo'shish.
        :param category: Mahsulot kategoriyasi.
        :param name: Mahsulot nomi.
        :param description: Mahsulot tavsifi.
        :param image_url: Mahsulot rasmining URL'i (ixtiyoriy).
        :param details_url: Mahsulot haqida batafsil ma'lumot URL'i (ixtiyoriy).
        """
        try:
            self.cursor.execute(
                "INSERT INTO products (category, name, description, image_url, details_url) VALUES (?, ?, ?, ?, ?)",
                (category, name, description, image_url, details_url)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Mahsulot qo'shishda xatolik: {e}")
            return False

    def get_products_by_category(self, category):
        """
        Berilgan kategoriyadagi barcha mahsulotlarni olish.
        :param category: Mahsulot kategoriyasi.
        :return: (nomi, tavsifi, rasm_url, batafsil_url) kortejlar ro'yxati.
        """
        try:
            self.cursor.execute(
                "SELECT name, description, image_url, details_url FROM products WHERE category = ?",
                (category,)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Kategoriya bo'yicha mahsulotlarni olishda xatolik: {e}")
            return []

    def get_all_categories(self):
        """
        Barcha noyob mahsulot kategoriyalarini olish.
        :return: Kategoriya nomlari ro'yxati.
        """
        try:
            self.cursor.execute("SELECT DISTINCT category FROM products")
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Barcha kategoriyalarni olishda xatolik: {e}")
            return []

    # --- Log (Jurnal) operatsiyalari ---

    def log_message(self, user_id, username, first_name, last_name, message_text):
        """
        Foydalanuvchi xabarini loglash.
        :param user_id: Foydalanuvchi ID'si.
        :param username: Foydalanuvchi nomi (agar mavjud bo'lsa).
        :param first_name: Foydalanuvchi ismi.
        :param last_name: Foydalanuvchi familiyasi (agar mavjud bo'lsa).
        :param message_text: Yuborilgan xabar matni.
        """
        try:
            self.cursor.execute(
                "INSERT INTO logs (user_id, username, first_name, last_name, message_text) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, first_name, last_name, message_text)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Xabarni loglashda xatolik: {e}")

    def get_log_stats(self):
        """
        Loglar bo'yicha statistikani olish.
        :return: Umumiy xabarlar soni va eng faol foydalanuvchilar ro'yxatini o'z ichiga olgan lug'at.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM logs")
            total_messages = self.cursor.fetchone()[0]

            # Eng ko'p xabar yuborgan 5 ta foydalanuvchini olish
            self.cursor.execute(
                "SELECT user_id, COUNT(*) FROM logs GROUP BY user_id ORDER BY COUNT(*) DESC LIMIT 5"
            )
            top_users = self.cursor.fetchall()
            return {"total_messages": total_messages, "top_users": top_users}
        except sqlite3.Error as e:
            print(f"Log statistikasini olishda xatolik: {e}")
            return {"total_messages": 0, "top_users": []}

