from multiprocessing import Process, Queue
from threading import Thread
from datetime import datetime, timedelta
import time
#import pygame

# Импорты из других файлов проекта
from calculating_advanced import num_integr, Body, bodies  # Функция численного интегрирования
from new_gui import managment_initiator  # Функция графического интерфейса
#from visualization_module import visualization  # Функция визуализации

# Глобальные переменные
now_date = "00:00:00/01/01/2000"  # Текущая дата
start_date = datetime.strptime(now_date, "%H:%M:%S/%d/%m/%Y")  # Начальная дата
calc_speed = 365 * 24 * 3600  # Скорость расчета (в секундах)
file = 'info.txt'
q = Queue()  # Очередь для обмена данными

# Функция для запуска численного интегрирования
def run_num_integr():
    global calc_speed
    last_time = time.time()
    while True:
        if time.time() - last_time > 1 / calc_speed:
            num_integr(3600, q)  # Вызов функции интегрирования с шагом 3600 секунд
            last_time = time.time()

# Функция для запуска обновления даты
def run_date():
    global now_date
    global start_date
    global calc_speed
    current_date = start_date
    lasttime = time.time()
    while True:
        if time.time() - lasttime > 3600:
            current_date += timedelta(seconds=3600)
            now_date = current_date.strftime("%H:%M:%S/%d/%m/%Y")
            q.put(("update_date", now_date))  # Отправка новой даты в очередь
            print(now_date)
# Основной блок для сборки проекта
if __name__ == "__main__":
    # Создание процессов
    process_date = Process(target=run_date)  # Процесс для обновления даты
    process_gui = Process(target=managment_initiator, args=(q,))  # Процесс для GUI
    #process_visualization = Process(target=visualization, args=(q,))  # Процесс для визуализации

    # Запуск процессов
    process_date.start()
    process_gui.start()
    #process_visualization.start()
    # Запуск численного интегрирования в отдельном потоке
    thread_num_integr = Thread(target=run_num_integr)
    thread_num_integr.start()
    # Основной цикл для обработки данных из очереди
    while True:
        if not q.empty():
            command, data = q.get()
            if command == "update_date":
                now_date = data  # Обновление текущей даты
            elif command == "update_bodies":
                bodies.clear()
                for body_data in data:
                    bodies.append(Body(*body_data))  # Обновление списка тел
            elif command == "update_speed":
                calc_speed = data
            elif command == "update_file":
                file = data
        print(now_date)