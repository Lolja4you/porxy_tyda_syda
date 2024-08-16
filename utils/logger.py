import logging
import colorlog


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Создание форматтера с цветами для уровня логирования
formatter = colorlog.ColoredFormatter(
    '[%(asctime)s] %(log_color)s%(levelname)s:%(reset)s %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Создание обработчика для консоли
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)