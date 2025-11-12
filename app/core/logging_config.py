import logging
from logging.handlers import RotatingFileHandler
from app.core.config import settings  # 👈 Импортируем наш объект настроек

# ... (фильтр InfoLevelFilter остается без изменений) ...
class InfoLevelFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.WARNING

def setup_logging():
    """
    Настраивает логирование для записи в разные файлы в зависимости от уровня.
    Уровень логирования берется из конфигурационного файла (.env).
    """
    # --- Получаем уровень логирования из конфига ---
    log_level_str = settings.LOG_LEVEL.upper()
    
    # Словарь для преобразования строки в константу logging
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    
    # Получаем соответствующий уровень. Если в конфиге указано что-то не то,
    # по умолчанию ставим INFO.
    log_level = log_levels.get(log_level_str, logging.INFO)
    print("===============", log_level)
    # Получаем корневой логгер
    logger = logging.getLogger()
    logger.setLevel(log_level)  # 👈 Устанавливаем уровень из конфига!

    if logger.hasHandlers():
        logger.handlers.clear()

    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
    )

    # --- 1. Обработчик для INFO логов ---
    info_handler = RotatingFileHandler('logs/info.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
    info_handler.setLevel(logging.INFO) # Этот файл всегда будет от INFO и выше
    info_handler.setFormatter(log_format)
    info_handler.addFilter(InfoLevelFilter())

    # --- 2. Обработчик для ERROR логов ---
    error_handler = RotatingFileHandler('logs/error.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)

    # --- 3. Обработчик для вывода в консоль ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level) # 👈 Консоль будет показывать логи с тем же уровнем, что и в конфиге
    console_handler.setFormatter(log_format)
    
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    # Логируем сообщение с новым уровнем для проверки
    logging.info(f"Система логирования настроена. Установлен уровень: {log_level_str}")