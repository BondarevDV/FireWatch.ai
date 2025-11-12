import logging
from logging.handlers import RotatingFileHandler

# --- Создаем кастомный фильтр ---
# Он будет пропускать только логи определенного уровня и ниже.
class InfoLevelFilter(logging.Filter):
    def filter(self, record):
        # Пропускаем только записи с уровнем INFO и WARNING
        # Уровень DEBUG=10, INFO=20, WARNING=30, ERROR=40, CRITICAL=50
        return record.levelno <= logging.WARNING

def setup_logging():
    """
    Настраивает логирование для записи в разные файлы в зависимости от уровня.
    """
    # Получаем корневой логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Устанавливаем минимальный уровень для логгера

    # Если обработчики уже были добавлены (например, при перезагрузке uvicorn), очищаем их
    if logger.hasHandlers():
        logger.handlers.clear()

    # --- Создаем форматтер ---
    # Определяет, как будет выглядеть строка лога
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
    )

    # --- 1. Обработчик для INFO логов (info.log) ---
    # RotatingFileHandler автоматически будет ротировать файлы, когда они достигнут 5MB
    info_handler = RotatingFileHandler('logs/info.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(log_format)
    info_handler.addFilter(InfoLevelFilter()) # Применяем наш фильтр

    # --- 2. Обработчик для ERROR логов (error.log) ---
    error_handler = RotatingFileHandler('logs/error.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
    error_handler.setLevel(logging.ERROR) # Этот обработчик будет ловить только ERROR и CRITICAL
    error_handler.setFormatter(log_format)

    # --- 3. Обработчик для вывода в консоль (удобно для разработки) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    
    # --- Добавляем все обработчики к корневому логгеру ---
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    logging.info("Система логирования успешно настроена.")