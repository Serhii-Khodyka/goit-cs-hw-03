import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB через змінну середовища
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client['cat_database']
collection = db['cats']

# Створення документа
def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    result = collection.insert_one(cat)
    print(f"Кіт доданий з _id: {result.inserted_id}")

# Читання всіх документів
def read_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)

# Читання документа за ім'ям
def read_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"Кіт з ім'ям {name} не знайдений.")

# Оновлення віку кота за ім'ям
def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count > 0:
        print(f"Вік кота {name} оновлено.")
    else:
        print(f"Кіт з ім'ям {name} не знайдений.")

# Додавання нової характеристики
def add_feature_to_cat(name, feature):
    result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
    if result.matched_count > 0:
        print(f"Характеристика додана коту {name}.")
    else:
        print(f"Кіт з ім'ям {name} не знайдений.")

# Видалення документа за ім'ям
def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кіт з ім'ям {name} видалений.")
    else:
        print(f"Кіт з ім'ям {name} не знайдений.")

# Видалення всіх документів
def delete_all_cats():
    result = collection.delete_many({})
    print(f"Видалено {result.deleted_count} котів.")


# Приклад використання функцій
if __name__ == "__main__":
    # Створення нового кота
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("Cat", 5, ["ходить і стрибає", "не дає себе гладити", "білий"])
    create_cat("my_cat", 7, ["ходить в капці", "дає себе гладити", "рудий"])
    
    # Читання всіх котів
    print("Всі коти в колекції:")
    read_all_cats()
    
    # Читання кота за ім'ям
    print("Кіт з ім'ям barsik:")
    read_cat_by_name("barsik")
    
    # Оновлення віку кота
    update_cat_age("barsik", 4)
    
    # Додавання нової характеристики
    add_feature_to_cat("barsik", "любить гратися")
    
    # Видалення кота за ім'ям
    delete_cat_by_name("barsik")
    
    # Видалення всіх котів
    delete_all_cats()
