import tkinter as tk
from tkinter import ttk
from tkinter import *
# Глобальные переменные
CalcSyst = 'Гелиоцентрическая декартова'
CalcSpeed = 365 * 24 * 3600
file_name = 'info.txt'
start_date = '00:00:00/01/01/2000'
end_date = ''
now_date = start_date
setupdtime = 1
bodies = []

class Body:
    def __init__(self, name, x, y, z, Vx, Vy, Vz, ax, ay, az, radius, mass):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        self.ax = ax
        self.ay = ay
        self.az = az
        self.radius = radius
        self.mass = mass

def managment(q):
    global CalcSyst
    global CalcSpeed
    global file_name
    global start_date
    global end_date
    global now_date
    global bodies

    def update_gui():
        # Обновление информации о текущей дате
        set_datlbl.config(text=f"Текущая дата: {now_date}")
        window.after(1000, update_gui)  # Обновление каждую секунду

    def set_speed():
        global CalcSpeed
        try:
            CalcSpeed = int(speed_entry.get())
            speed_label.config(text=f"Скорость расчёта: {CalcSpeed} сек")
        except ValueError:
            speed_label.config(text="Ошибка: Введите число")

    def set_file():
        global file_name
        file_name = file_entry.get()
        file_label.config(text=f"Файл данных: {file_name}")

    def set_dates():
        global start_date
        global end_date
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        date_label.config(text=f"Дата: {start_date} - {end_date}")

    def add_body():
        name = name_entry.get()
        radius = float(radius_entry.get())
        x = float(x_entry.get())
        y = float(y_entry.get())
        z = float(z_entry.get())
        Vx = float(Vx_entry.get())
        Vy = float(Vy_entry.get())
        Vz = float(Vz_entry.get())
        new_body = Body(name, x, y, z, Vx, Vy, Vz, 0, 0, 0, radius, 0)
        bodies.append(new_body)
        body_listbox.insert(tk.END, name)

    # Создание окна
    window = tk.Tk()
    window.title("Управление моделью")
    window.geometry('1200x800')

    # Фрейм для настроек
    settings_frame = ttk.Frame(window, padding=10)
    settings_frame.grid(row=0, column=0, sticky="nsew")

    # Настройка системы координат
    ttk.Label(settings_frame, text="Система координат:").grid(row=0, column=0, sticky="w")
    coord_combo = ttk.Combobox(settings_frame, values=['Эклиптическая', 'Экваториальная', 'Гелиоцентрическая полярная', 'Гелиоцентрическая декартова'])
    coord_combo.grid(row=0, column=1, sticky="w")
    coord_combo.set(CalcSyst)

    # Настройка скорости расчёта
    ttk.Label(settings_frame, text="Скорость расчёта (сек):").grid(row=1, column=0, sticky="w")
    speed_entry = ttk.Entry(settings_frame, width=10)
    speed_entry.grid(row=1, column=1, sticky="w")
    ttk.Button(settings_frame, text="Установить", command=set_speed).grid(row=1, column=2, sticky="w")
    speed_label = ttk.Label(settings_frame, text=f"Скорость расчёта: {CalcSpeed} сек")
    speed_label.grid(row=1, column=3, sticky="w")

    # Настройка файла данных
    ttk.Label(settings_frame, text="Файл данных:").grid(row=2, column=0, sticky="w")
    file_entry = ttk.Entry(settings_frame, width=10)
    file_entry.grid(row=2, column=1, sticky="w")
    ttk.Button(settings_frame, text="Установить", command=set_file).grid(row=2, column=2, sticky="w")
    file_label = ttk.Label(settings_frame, text=f"Файл данных: {file_name}")
    file_label.grid(row=2, column=3, sticky="w")

    # Настройка даты
    ttk.Label(settings_frame, text="Стартовая дата (ЧЧ:ММ:СС/ДД/ММ/ГГГГ):").grid(row=3, column=0, sticky="w")
    start_date_entry = ttk.Entry(settings_frame, width=20)
    start_date_entry.grid(row=3, column=1, sticky="w")
    ttk.Label(settings_frame, text="Дата окончания:").grid(row=4, column=0, sticky="w")
    end_date_entry = ttk.Entry(settings_frame, width=20)
    end_date_entry.grid(row=4, column=1, sticky="w")
    ttk.Button(settings_frame, text="Установить", command=set_dates).grid(row=4, column=2, sticky="w")
    date_label = ttk.Label(settings_frame, text=f"Дата: {start_date} - {end_date}")
    date_label.grid(row=4, column=3, sticky="w")

    # Добавление нового объекта
    ttk.Label(settings_frame, text="Имя объекта:").grid(row=5, column=0, sticky="w")
    name_entry = ttk.Entry(settings_frame, width=10)
    name_entry.grid(row=5, column=1, sticky="w")
    ttk.Label(settings_frame, text="Радиус объекта:").grid(row=6, column=0, sticky="w")
    radius_entry = ttk.Entry(settings_frame, width=10)
    radius_entry.grid(row=6, column=1, sticky="w")
    ttk.Label(settings_frame, text="Координаты (x, y, z):").grid(row=7, column=0, sticky="w")
    x_entry = ttk.Entry(settings_frame, width=5)
    x_entry.grid(row=7, column=1, sticky="w")
    y_entry = ttk.Entry(settings_frame, width=5)
    y_entry.grid(row=7, column=2, sticky="w")
    z_entry = ttk.Entry(settings_frame, width=5)
    z_entry.grid(row=7, column=3, sticky="w")
    ttk.Label(settings_frame, text="Скорости (Vx, Vy, Vz):").grid(row=8, column=0, sticky="w")
    Vx_entry = ttk.Entry(settings_frame, width=5)
    Vx_entry.grid(row=8, column=1, sticky="w")
    Vy_entry = ttk.Entry(settings_frame, width=5)
    Vy_entry.grid(row=8, column=2, sticky="w")
    Vz_entry = ttk.Entry(settings_frame, width=5)
    Vz_entry.grid(row=8, column=3, sticky="w")
    ttk.Button(settings_frame, text="Добавить объект", command=add_body).grid(row=9, column=0, columnspan=4, sticky="w")

    # Список объектов
    body_listbox = tk.Listbox(settings_frame, height=5)
    body_listbox.grid(row=10, column=0, columnspan=4, sticky="nsew")

    # Отображение текущей даты
    set_datlbl = ttk.Label(settings_frame, text=f"Текущая дата: {now_date}")
    set_datlbl.grid(row=11, column=0, columnspan=4, sticky="w")
    window.mainloop()
# Пример запуска GUI
def managment_initiator(q):
    global now_date
    global bodies

    managment(q)

    def update_gui():
        global window
        global now_date
        # Проверяем очередь на наличие новых данных
        while not q.empty():
            command, data = q.get()
            if command == "update_date":
                now_date = data
            elif command == "update_bodies":
                bodies.clear()
                for body_data in data:
                    bodies.append(Body(*body_data))
            q.put(("update_file", file_name))
            q.put(("update_speed", CalcSpeed))
        # Обновляем интерфейс каждые 100 мс
        window.after(100, update_gui)

    # Запускаем обновление интерфейса
    update_gui()