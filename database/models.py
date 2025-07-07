# Bu fayl ma'lumotlar bazasi jadvallarini yaratish uchun SQL so'rovlarini saqlaydi.
# ORM (Object-Relational Mapping) ishlatilmagan, to'g'ridan-to'g'ri SQLite3 bilan ishlash uchun.

# 'qa' jadvalini yaratish uchun SQL so'rovi
# Bu jadval savol-javob juftliklarini saqlaydi.
CREATE_QA_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS qa (
    question TEXT,
    answer TEXT
);
"""

# 'products' jadvalini yaratish uchun SQL so'rovi
# Bu jadval mahsulotlar haqidagi ma'lumotlarni saqlaydi.
CREATE_PRODUCTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    name TEXT,
    description TEXT,
    image_url TEXT,
    details_url TEXT
);
"""

# 'logs' jadvalini yaratish uchun SQL so'rovi
# Bu jadval foydalanuvchilarning bot bilan o'zaro aloqalarini (xabarlarini) saqlaydi.
CREATE_LOGS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    message_text TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""
