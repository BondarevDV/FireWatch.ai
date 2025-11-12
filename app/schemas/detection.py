
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Эта модель описывает один обнаруженный объект
class DetectionResult(BaseModel):
    class_name: str = Field(..., description="Название обнаруженного класса (e.g., 'fire', 'smoke')")
    confidence: float = Field(..., gt=0.0, le=1.0, description="Уверенность модели от 0.0 до 1.0")

# Эта модель описывает полный ответ нашего API
class DetectionResponse(BaseModel):
    filename: str = Field(..., description="Имя обработанного файла")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Время детекции (UTC)")
    detections: List[DetectionResult] = Field(..., description="Список обнаруженных объектов")