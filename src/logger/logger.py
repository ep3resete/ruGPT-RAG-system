import logging
from datetime import datetime
from config import logs_dir

def update_config(dir_of_logs: str) -> None:
    """ Функция для обновления пути """
    # Хэндлеры логов
    file_log = logging.FileHandler(dir_of_logs)
    console_out = logging.StreamHandler()

    # Конфигурация логгера
    logging.basicConfig(level=logging.INFO, handlers=(file_log, console_out))

# Функция для установки дефолтных настроек
set_base_config = lambda: update_config(logs_dir)
# Самая первая установка дефолтных логов
set_base_config()

# Функции для шаблонного логгирования разного уровня
loginfo = lambda x: logging.info(f"[{datetime.now()}] {x}")
logwarn = lambda x: logging.warning(f"[{datetime.now()}] {x}")
logerr = lambda x: logging.error(f"[{datetime.now()}] {x}")
logcritical = lambda x: logging.critical(f"[{datetime.now()}] {x}")
