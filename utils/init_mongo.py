
from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["intelligent_cache"]

# 1. Пошкоджені будівлі (розширено)
damaged_buildings = db["damaged_buildings"]
damaged_buildings.insert_one({
    "building_id": "B001",
    "location": {
        "city": "Київ",
        "district": "район_1",
        "street": "вул. Прикладна, 12",
        "coordinates": {"lat": 50.45, "lon": 30.52}
    },
    "type": "житлова",
    "damage_date": datetime.datetime(2022, 5, 10),
    "media_files": ["https://example.com/photo1.jpg"],
    "info_source": "волонтерська група",
    "contact": {
        "name": "Іван Іванов",
        "role": "свідок",
        "email": "ivan@example.com",
        "phone": "+380931112233",
        "organization": "Громадська ініціатива"
    },
    "damage_description": "руйнування даху і вікон",
    "damage_level": "суттєві",
    "damage_causes": ["обстріл"],
    "technical_condition": "нестабільний",
    "inspected": True
})

# 2. Користувачі
users = db["users"]
users.insert_one({
    "user_id": "U123",
    "name": "Олександра Коваль",
    "role": "експерт",
    "organization": "МБФ Відновлення",
    "email": "oleksandra@example.com",
    "registration_date": datetime.datetime(2023, 2, 1),
    "active": True
})

# 3. Історія запитів
request_history = db["request_history"]
request_history.insert_one({
    "request_id": "R001",
    "user_id": "U123",
    "timestamp": datetime.datetime.now(),
    "request_type": "читання",
    "building_id": "B001",
    "object_type": "школа",
    "location": "Київ"
})

# 4. Статистика пошкоджень
city_stats = db["city_stats"]
city_stats.insert_one({
    "city": "Київ",
    "damaged_percentage": 27.5,
    "destroyed_percentage": 12.0,
    "estimated_loss_uah": 126000000,
    "victims_count": 14,
    "deaths_count": 3
})

# 5. Q-таблиця
q_table = db["q_table"]
q_table.insert_one({
    "s": "12.3.1.0.2.3",
    "a": 1,
    "q_value": 0.75
})

# 6. Навчальні приклади
lr_training_examples = db["lr_training_examples"]
lr_training_examples.insert_one({
    "x": [12, 50, 1, 24, 2, 3],
    "y": 1
})

# 7. Параметри моделі
lr_model_params = db["lr_model_params"]
lr_model_params.insert_one({
    "w": [0.1, -0.05, 0.3, 0.2, -0.1, 0.05],
    "b": 0.0
})

print("✅ MongoDB initialized with full structured example data.")
