from fastapi.testclient import TestClient
import io

def test_detect_fire_success(client: TestClient):
    """
    Тест успешного обнаружения: отправляем "изображение", ожидаем статус 200.
    """
    # Создаем фейковый файл изображения в памяти
    fake_image_bytes = b"fake_image_data_here"
    file = ("test_image.jpg", io.BytesIO(fake_image_bytes), "image/jpeg")

    # Отправляем запрос на эндпоинт
    response = client.post("/api/v1/detect", files={"file": file})

    # Проверяем результат
    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert data["filename"] == "test_image.jpg"
    assert "detections" in data
    assert isinstance(data["detections"], list) # Проверяем, что detections - это список



def test_detect_invalid_file_type(client: TestClient):
    """
    Тест с невалидным файлом: отправляем текстовый файл, ожидаем ошибку 422.
    """
    # Создаем фейковый текстовый файл
    fake_text_bytes = b"this is not an image"
    file = ("test.txt", io.BytesIO(fake_text_bytes), "text/plain")

    # Отправляем запрос
    response = client.post("/api/v1/detect", files={"file": file})

    # FastAPI вернет 422 Unprocessable Entity, если тип файла не совпадает с ожидаемым
    # (если мы указали, что принимаем только image/*)
    # или 400, если мы сами проверяем тип и возвращаем ошибку.
    # Для нашего кастомного обработчика (ниже) будем ожидать 400.
    assert response.status_code == 400 
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Invalid file type. Please upload an image."