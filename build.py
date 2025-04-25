from multiprocessing import Process, Queue
from threading import Thread
from datetime import datetime, timedelta
import time

# Импорты из других файлов проекта
from calculating_advanced import num_integr, Body, bodies, downloader  # Функция численного интегрирования
from new_gui import managment, end_date  # Функция графического интерфейса
ifstart = False
from kvazissm_visual import visualization  # Функция визуализации
# Глобальные переменные
start_date = datetime.strptime("00:00:00/01/01/2000", "%H:%M:%S/%d/%m/%Y")
now_date = "00:00:00/01/01/2000"  # Текущая дата
current_date = datetime.strptime(now_date, "%H:%M:%S/%d/%m/%Y")  # Начальная дата
calc_speed = 365 * 24 * 3600  # Скорость расчета (в секундах)
step = 3600
file = 'info.txt'
q = Queue()  # Очередь для обмена данными
qifs = Queue()
qvis = Queue()
qbod = Queue()
qvis_date = Queue()
qnewb = Queue()
data = []
# Функция для запуска численного интегрирования
# Функция для запуска обновления даты
def run_num_integr():
    global now_date
    global current_date
    global calc_speed
    global end_date
    global step
    global ifstart
    global file
    lasttime = time.time()
    lasttime2 = time.time()
    while True:
        if not q.empty():
            command, data = q.get()
            if command == "update_ifstart":
                ifstart = data
                if ifstart:
                    current_date = start_date
                    downloader()
            elif command == "update_date":
                now_date = data  # Обновление начальной даты
            elif command == "update_end_date":
                end_date = datetime.strptime(data,   "%H:%M:%S/%d/%m/%Y")# Обновление конечной даты
            elif command == "update_speed":
                calc_speed = data
            elif command == "update_file":
                file = data
            elif command == "update_step":
                step = data
        #print(ifstart, now_date != end_date, time.time() - lasttime > step / calc_speed)
        if ifstart and current_date.timestamp() <= end_date.timestamp() and time.time() - lasttime > step/calc_speed:
            num_integr(step, qbod, qnewb, ifstart)  # Вызов функции интегрирования с шагом step
            current_date += timedelta(seconds=step)
            now_date = current_date.strftime("%H:%M:%S/%d/%m/%Y")
            qvis.put(("update_end_date", end_date))
            qvis.put(("update_step", step))
            qvis.put(("update_file", file))
            if end_date:
                if current_date.timestamp() >= end_date.timestamp():
                    ifstart = False
            lasttime = time.time()
            if time.time() - lasttime2 > 0.02 or ifstart == False:
                qvis_date.put(now_date)  # Отправка новой даты в очередь
                lasttime2 = time.time()
# Основной блок для сборки проекта
if __name__ == "__main__":
    # Создание процессов
    process_integ = Process(target=run_num_integr)  # Процесс для обновления даты
    process_gui = Process(target=managment, args=(q, qnewb))  # Процесс для GUI
    process_visualization = Process(target=visualization, args=(qbod, qvis, qvis_date,))  # Процесс для визуализации

    # Запуск процессов
    process_gui.start()
    process_visualization.start()
    process_integ.start()
    # Основной цикл для обработки данных из очереди
