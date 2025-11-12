# Расположение: /fire_detection_api/app/crud/crud_detection.py

import time
from app.schemas.detection import DetectionResponse

def save_detection_result(db_session: str, result: DetectionResponse):
    """
    Имитирует сохранение результата детекции в базу данных.
    """
    print(f"\n--- [BACKGROUND TASK] ---")
    print(f"Получен '{db_session}' для сохранения данных.")
    print("Имитация медленной записи в БД...")
    time.sleep(3) # Имитация задержки
    print(f"Сохранение результата для файла: {result.filename}")
    print(f"Обнаружено: {result.detections}")
    print(f"--- [BACKGROUND TASK FINISHED] ---\n")
    return True