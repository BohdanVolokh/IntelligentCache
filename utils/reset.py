import os

from config import (
    LOGREG_CSV_PATH,
    LOGREG_MODEL_PATH
)

PERSIST_PATH = "persistent"
OBJECTS_FILE = os.path.join(PERSIST_PATH, "objects.pkl")
QTABLE_FILE = os.path.join(PERSIST_PATH, "q_table.pkl")


def reset_all():
    files_to_delete = [
        OBJECTS_FILE,
        QTABLE_FILE,
        LOGREG_CSV_PATH,
        LOGREG_MODEL_PATH
    ]

    for file in files_to_delete:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"[Reset] Видалено: {file}")
            else:
                print(f"[Reset] Не знайдено: {file}")
        except Exception as e:
            print(f"[Reset] Помилка при видаленні {file}: {e}")


if __name__ == "__main__":
    reset_all()