import os
from dotenv import load_dotenv
from faker import Faker
import psycopg2

# Завантаження змінних середовища з файлу .env
load_dotenv("db.env")

# Підключення до бази даних
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST')
)
cursor = conn.cursor()

# Ініціалізація Faker
fake = Faker('uk_UA')

# Заповнення таблиці users
for _ in range(20):
    fullname = fake.name()
    email = fake.email()
    cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

# Заповнення таблиці status
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cursor.execute("INSERT INTO status (name) VALUES (%s)", (status,))

# Отримання ID користувачів та статусів
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM status")
status_ids = [row[0] for row in cursor.fetchall()]

# Заповнення таблиці tasks
for _ in range(50):
    title = fake.sentence()
    description = fake.text()
    status_id = fake.random_element(elements=status_ids)
    user_id = fake.random_element(elements=user_ids)
    cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (title, description, status_id, user_id))

# Збереження змін
conn.commit()

# Закриття з'єднання
cursor.close()
conn.close()
