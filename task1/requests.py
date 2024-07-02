import os
from dotenv import load_dotenv
import psycopg2

def get_connection():
    # Завантаження змінних середовища з файлу .env
    load_dotenv("db.env")

    # Підключення до бази даних
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST')
        )


def get_tasks_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def get_tasks_by_status(status_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM tasks 
    WHERE status_id = (SELECT id FROM status WHERE name = %s)
    """, (status_name,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def update_task_status(task_id, new_status_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s)
    WHERE id = %s
    """, (new_status_name, task_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_users_without_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)
    """)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def add_new_task(title, description, status_name, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tasks (title, description, status_id, user_id) 
    VALUES (%s, %s, (SELECT id FROM status WHERE name = %s), %s)
    """, (title, description, status_name, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_uncompleted_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM tasks 
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    """)
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()

def find_users_by_email(email_pattern):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def update_user_fullname(user_id, new_fullname):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET fullname = %s WHERE id = %s", (new_fullname, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def count_tasks_by_status():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT status.name, COUNT(tasks.id) 
    FROM tasks
    JOIN status ON tasks.status_id = status.id
    GROUP BY status.name
    """)
    count = cursor.fetchall()
    cursor.close()
    conn.close()
    return count

def get_users_by_email_domain(email_domain):
    conn = get_connection()
    cursor = conn.cursor()
    like_pattern = f"%{email_domain}%"
    cursor.execute("""
    SELECT * 
    FROM users
    WHERE email LIKE %s
    """, (like_pattern,))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_tasks_without_description():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE description IS NULL")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def get_users_with_in_progress_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT users.*, tasks.* 
    FROM users
    JOIN tasks ON users.id = tasks.user_id
    JOIN status ON tasks.status_id = status.id
    WHERE status.name = 'in progress'
    """)
    users_tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return users_tasks

def get_users_and_task_counts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT users.*, COUNT(tasks.id) as task_count 
    FROM users
    LEFT JOIN tasks ON users.id = tasks.user_id
    GROUP BY users.id
    """)
    users_task_counts = cursor.fetchall()
    cursor.close()
    conn.close()
    return users_task_counts

def get_tasks_by_user_email_domain(email_domain):
    conn = get_connection()
    cursor = conn.cursor()
    # Додайте символи підстановки до значення email_domain
    like_pattern = f"%{email_domain}%"
    cursor.execute("""
    SELECT tasks.* 
    FROM tasks
    JOIN users ON tasks.user_id = users.id
    WHERE users.email LIKE %s
    """, (like_pattern,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

# Отримати всі завдання для користувача з user_id = 31
tasks = get_tasks_by_user(31)
print(tasks)

# Додати нове завдання
#add_new_task('New Task','New description', 'new', 31)

# Оновити статус завдання з id = 51
#update_task_status(51, 'in progress')

# Кількість задач з різним статусом
print(count_tasks_by_status())

# Користувачі без статуса
print(get_users_without_tasks())
 
# Незавершені задачі
print(get_uncompleted_tasks())

# Видалити задачу з id = 95
#delete_task(95)

# Шукаємо користувачів з патерном example.com
users = get_users_by_email_domain("example.com")
print(users)

# Шукаємо задачі користувачів з патерном example.com
tasks = get_tasks_by_user_email_domain("example.com")
print(tasks)

# Задачі без опису
print(get_tasks_without_description())

# користувачі та кількість задач
print(get_users_and_task_counts())

# користувачі з задачами в статусі in progress
print(get_users_with_in_progress_tasks())