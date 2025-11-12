
import time
import random

class FireDetectionModel:
    def __init__(self, model_path: str = "path/to/fake_model.onnx"):
        # Имитация долгой загрузки модели в память
        print(f"--- LOADING FAKE MODEL: {model_path} ---")
        time.sleep(2) 
        self._model_path = model_path
        self.possible_results = ["fire", "smoke", "neutral"]
        print("--- FAKE MODEL LOADED ---")

    def predict(self, image_bytes: bytes) -> list[dict]:
        """
        Имитирует предсказание на основе байтов изображения.
        Возвращает случайный результат.
        """
        print(f"Received {len(image_bytes)} bytes for prediction.")
        # Имитация работы модели
        time.sleep(0.5) 
        
        # Генерируем случайный ответ
        num_detections = random.randint(0, 2)
        if num_detections == 0:
            return []

        results = []
        for _ in range(num_detections):
            result = {
                "class_name": random.choice(self.possible_results),
                "confidence": round(random.uniform(0.75, 0.99), 2)
            }
            # Убедимся, что не выдаем "neutral" как тревогу
            if result["class_name"] != "neutral":
                results.append(result)
        
        print(f"Prediction result: {results}")
        return results
    

model_instance = FireDetectionModel()

def get_model() -> FireDetectionModel:
    """
    Эта функция-зависимость будет возвращать один и тот же 
    экземпляр модели при каждом вызове.
    """
    return model_instance