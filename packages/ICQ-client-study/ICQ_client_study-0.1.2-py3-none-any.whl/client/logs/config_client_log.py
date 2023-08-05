import logging
import sys
import os

sys.path.append(os.path.join(os.getcwd(), '..'))

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.log')

log = logging.getLogger('clientlog')
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s %(message)s')
file_hand = logging.FileHandler(path, encoding='utf-8')
file_hand.setFormatter(formatter)

log.addHandler(file_hand)
log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    log.debug('Отладочная информация')
    log.info('Информационное сообщение')
    log.warning('Предупреждение')
    log.error('Ошибка')
    log.critical('Критическая ошибка')
