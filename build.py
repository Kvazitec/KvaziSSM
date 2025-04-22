from multiprocessing import Process, Queue
from threading import Thread
from datetime import datetime, timedelta
import time
#import pygame

# Импорты из других файлов проекта
from calculating_advanced import num_integr, Body, bodies  # Функция численного интегрирования
from new_gui import managment_initiator  # Функция графического интерфейса
ifstart = False
#from visualization_module import visualization  # Функция визуализации

# Глобальные переменные
now_date = "00:00:00/01/01/2000"  # Текущая дата
current_date = datetime.strptime(now_date, "%H:%M:%S/%d/%m/%Y")  # Начальная дата
end_date = ''
calc_speed = 365 * 24 * 3600  # Скорость расчета (в секундах)
step = 3600
file = 'info.txt'
q = Queue()  # Очередь для обмена данными
qifs = Queue()
qed = Queue()
# Функция для запуска численного интегрирования
def run_num_integr():
    global calc_speed
    global ifstart
    last_time = time.time()
    while True:
        if ifstart and now_date != end_date and time.time() - last_time > step / calc_speed:
            num_integr(step, q)  # Вызов функции интегрирования с шагом step
            last_time = time.time()

# Функция для запуска обновления даты
def run_date():
    global now_date
    global current_date
    global calc_speed
    global end_date
    lasttime = time.time()
    ifstart1 = False
    while True:
        if not qifs.empty():
            command1, data1 = qifs.get()
            if command1 == "update_ifstart":
                ifstart1 = data1
        #print(ifstart1, now_date != end_date, time.time() - lasttime > step / calc_speed)
        if ifstart1 and now_date != end_date and time.time() - lasttime > step/calc_speed:
            current_date += timedelta(seconds=step)
            now_date = current_date.strftime("%H:%M:%S/%d/%m/%Y")
            q.put(("update_date", now_date))  # Отправка новой даты в очередь
            if not qed.empty():
                command1, data1 = qed.get()
                if command1 == "update_end_date":
                    end_date = data1
            if end_date:
                if type(end_date) == str:
                    end_date = datetime.strptime(end_date, "%H:%M:%S/%d/%m/%Y")
                if current_date.timestamp() > end_date.timestamp():
                    q.put(("update_ifstart", False))

# Основной блок для сборки проекта
if __name__ == "__main__":
    # Создание процессов
    process_date = Process(target=run_date)  # Процесс для обновления даты
    process_gui = Process(target=managment_initiator, args=(q,))  # Процесс для GUI
    #process_visualization = Process(target=visualization, args=(q,))  # Процесс для визуализации

    # Запуск процессов
    process_gui.start()
    #process_visualization.start()
    process_date.start()
    # Запуск численного интегрирования в отдельном потоке
    thread_num_integr = Thread(target=run_num_integr)
    thread_num_integr.start()
    # Основной цикл для обработки данных из очереди
    while True:
        if not q.empty():
            command, data = q.get()
            if command == "update_ifstart":
                ifstart = data
                qifs.put(("update_ifstart", ifstart))
            elif command == "update_date":
                now_date = data  # Обновление текущей даты
            elif command == "update_end_date":
                end_date = data  # Обновление текущей даты
                qed.put(("update_end_date", end_date))
            elif command == "update_bodies":
                bodies.clear()
                for body_data in data:
                    bodies.append(Body(*body_data))  # Обновление списка тел
            elif command == "update_speed":
                calc_speed = data
            elif command == "update_file":
                file = data
            elif command == "update_step":
                step = data
