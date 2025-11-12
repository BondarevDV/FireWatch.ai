# Расположение: /fire_detection_api/app/api/v1/endpoints/detect.py

# Добавляем импорт HTTPException
from fastapi import APIRouter, File, UploadFile, Depends, BackgroundTasks, HTTPException, status
from app.services.ml_model import FireDetectionModel, get_model
from app.schemas.detection import DetectionResponse
from app.crud.crud_detection import save_detection_result
from app.db.session import get_db_session
from app.services.queue_producer import QueueProducer, get_queue_producer
from app.core.exceptions import InvalidFileTypeError
import logging

router = APIRouter()


# Получаем логгер для текущего модуля. Это лучшая практика.
logger = logging.getLogger(__name__)

#  1. Определим разрешенные типы файлов
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/bmp"]

@router.post(
    "/detect",
    summary="Обнаружение огня и дыма на изображении",
    description="Загрузите изображение (JPEG, PNG), чтобы получить список обнаруженных объектов ('fire', 'smoke') и их координаты.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Успешное обнаружение",
            "content": {
                "application/json": {
                    "example": {
                        "filename": "image.jpg",
                        "detections": [
                            {"box": [100, 150, 180, 220], "class": "fire", "confidence": 0.92}
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Неверный тип файла",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid file type. Please upload an image."}
                }
            },
        },
    }
)

async def detect_fire_from_image(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="Изображение для анализа"),
    model: FireDetectionModel = Depends(get_model),
    db_session: str = Depends(get_db_session),
    queue: QueueProducer = Depends(get_queue_producer)
):
    """
    Принимает изображение, анализирует его на наличие огня/дыма 
    и возвращает результат.
    """


    #  2. Добавляем проверку типа файла
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        error_detail = (
            f"Недопустимый тип файла: '{file.content_type}'. "
            f"Пожалуйста, загрузите изображение одного из следующих форматов: "
            f"{', '.join(type.split('/')[1] for type in ALLOWED_IMAGE_TYPES)}."
        )
        logger.warning(f"Попытка загрузки файла с неверным типом: {file.filename} ({file.content_type})")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Недопустимый тип файла: {file.content_type}. "
                   f"Пожалуйста, загрузите изображение одного из следующих форматов: "
                   f"{', '.join(type.split('/')[1] for type in ALLOWED_IMAGE_TYPES)}"
        )
    try:
        # 3. Читаем байты и логируем информацию о файле
        image_bytes = await file.read()
        file_size_kb = len(image_bytes) / 1024
        file_extension = file.filename.split('.')[-1]

        print(f"\n--- FILE INFO ---")
        print(f"Имя файла: {file.filename}")
        print(f"Тип файла (MIME): {file.content_type}")
        print(f"Расширение: {file_extension}")
        print(f"Размер: {file_size_kb:.2f} KB")
        print(f"--- END FILE INFO ---\n")
        
        detection_results = model.predict(image_bytes)
    except Exception as e:
        # Ловим ЛЮБУЮ непредвиденную ошибку (ошибка в модели, битый файл и т.д.)
        logger.error(
            f"Произошла внутренняя ошибка при обработке файла {file.filename}: {e}", 
            exc_info=True  # exc_info=True добавит полный traceback ошибки в лог
        )
        # Возвращаем пользователю общую ошибку 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла внутренняя ошибка при обработке изображения."
        )

    response = DetectionResponse(
        filename=file.filename,
        detections=detection_results
    )
    
    background_tasks.add_task(
        save_detection_result, 
        db_session, 
        response
    )
    if response.detections:
        background_tasks.add_task(
            queue.send_notification,
            {"filename": response.filename, "detections_count": len(response.detections)}
        )
    logger.info(f"Обработка файла {file.filename} завершена успешно.")    
    return response
