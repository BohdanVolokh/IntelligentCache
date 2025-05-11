from generator.object_generator import ObjectGenerator
from generator.request_generator import RequestGenerator
from db.in_memory_db import InMemoryStorage

from threading import Event
logreg_reload_flag = Event()

# Ініціалізація генераторів та сховища
object_generator = ObjectGenerator()
storage = InMemoryStorage()

# Генеруємо об'єкти
objects = object_generator.generate_batch(count=10)
for obj in objects:
    storage.add(obj)

# Ініціалізуємо генератор запитів із доступними object_id
object_ids = list(storage.storage.keys())
request_generator = RequestGenerator(object_ids=object_ids)

# Генеруємо запити
requests = request_generator.generate_requests(count=20)

# Виводимо результат запитів
for req in requests:
    obj = storage.get(req["object_id"])
    if obj:
        print(f"[HIT] Object {req['object_id']} found.")
    else:
        print(f"[MISS] Object {req['object_id']} not found.")