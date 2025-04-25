import tkinter as tk
from tkinter import ttk
# Глобальные переменные
CalcSyst = 'Гелиоцентрическая декартова'
CalcSpeed = 365 * 24 * 3600
file_name = 'info.txt'
start_date = '00:00:00/01/01/2000'
end_date = ''
now_date = start_date
setupdtime = 1
bodies = []
step = 3600
ifstart = False
mess = 1
window = ''

def managment(q, qnewb):
    global CalcSyst
    global CalcSpeed
    global file_name
    global start_date
    global end_date
    global now_date
    global bodies
    global window

    def starter():
        iferror = False
        global ifstart
        global mess
        mess = 1
        ttk.Label(settings_frame, text="Сообщения:").grid(row=17, column=0, sticky='W')
        q.put(("update_calcsyst", coord_combo.get()))
        if speed_entry.get():
            q.put("update_speed", float(speed_entry.get()))
        if step_entry.get():
            q.put(("update_step", float(step_entry.get())))
        if file_entry.get():
            q.put(("update_file", file_entry.get()))
        if start_date_entry.get():
            q.put(("update_start_date", start_date_entry.get()))
        else:
            iferror = True
            tk.Label(settings_frame, text='Введите стартовую дату        ', bg='red', fg='white').grid(row=17, column=mess, sticky='W')
            mess += 1
        if end_date_entry.get():
            q.put(('update_end_date', end_date_entry.get()))
        else:
            iferror = True
            tk.Label(settings_frame, text='Введите дату окончания', bg='red', fg='white').grid(row=17, column=mess, sticky='W')
            mess += 1
        if not iferror:
            tk.Label(settings_frame, text='Запущена подготовка к расчёту', bg='green', fg='white').grid(row=17, column=mess, sticky='W')
            mess += 1
            tk.Label(settings_frame, text='                             ').grid(row=17, column=mess, sticky='W')
            mess += 1
            ifstart = True
        q.put(('update_ifstart', ifstart))
    def stopper():
        q.put(('update_ifstart', False))
    def add_body():
        name = name_entry.get()
        radius = float(radius_entry.get())
        mass = float(mass_entry.get())
        x = float(x_entry.get())
        y = float(y_entry.get())
        z = float(z_entry.get())
        Vx = float(Vx_entry.get())
        Vy = float(Vy_entry.get())
        Vz = float(Vz_entry.get())
        new_body = (name, x, y, z, Vx, Vy, Vz, 0, 0, 0, radius, mass)
    # Создание окна
    window = tk.Tk()
    window.title("Управление моделью")
    window.geometry('600x450')
    # Фрейм для настроек
    settings_frame = ttk.Frame(window, padding=10)
    settings_frame.grid(row=0, column=0, sticky="nsew")

    # Настройка системы координат
    ttk.Label(settings_frame, text="Система координат:").grid(row=0, column=0, sticky="w")
    coord_combo = ttk.Combobox(settings_frame, values=['Эклиптическая', 'Экваториальная', 'Гелиоцентрическая полярная', 'Гелиоцентрическая декартова'])
    coord_combo.grid(row=0, column=1, sticky="w")
    coord_combo.set(CalcSyst)

    ttk.Label(settings_frame, text="Файл данных:").grid(row=3, column=0, sticky="w")
    file_entry = ttk.Entry(settings_frame, width=10)
    file_entry.grid(row=3, column=1, sticky="w")

    # Настройка скорости расчёта
    ttk.Label(settings_frame, text="Скорость расчёта (сек):").grid(row=1, column=0, sticky="w")
    speed_entry = ttk.Entry(settings_frame, width=10)
    speed_entry.grid(row=1, column=1, sticky="w")
    # Шаг интегрирования
    ttk.Label(settings_frame, text="Шаг интегрирования (сек):").grid(row=2, column=0, sticky="w")
    step_entry = ttk.Entry(settings_frame, width=10)
    step_entry.grid(row=2, column=1, sticky="w")
    # Настройка даты
    ttk.Label(settings_frame, text="Стартовая дата:").grid(row=4, column=0, sticky="w")
    ttk.Label(settings_frame, text="ЧЧ:MM:СС/ДД/ММ/ГГГГ").grid(row=4, column=2, sticky="w")
    start_date_entry = ttk.Entry(settings_frame, width=20)
    start_date_entry.grid(row=4, column=1, sticky="w")
    ttk.Label(settings_frame, text="Дата окончания:").grid(row=5, column=0, sticky="w")
    end_date_entry = ttk.Entry(settings_frame, width=20)
    end_date_entry.grid(row=5, column=1, sticky="w")
    ttk.Label(settings_frame, text="").grid(row=6, column=0, sticky="w")
    tk.Button(settings_frame, bg="green", fg = "white", text="Начать расчёт", command=starter).grid(row=7, column=0, sticky="w")
    tk.Button(settings_frame, bg="red", fg = "white", text="Остановить расчёт", command=stopper).grid(row=7, column=1, sticky="w")
    ttk.Label(settings_frame, text="").grid(row=8, column=0, sticky="w")
    # Добавление нового объекта
    ttk.Label(settings_frame, text="Меню добавления объекта").grid(row=9, column=0, sticky="w")
    ttk.Label(settings_frame, text="Имя объекта:").grid(row=10, column=0, sticky="w")
    name_entry = ttk.Entry(settings_frame, width=10)
    name_entry.grid(row=10, column=1, sticky="w")
    ttk.Label(settings_frame, text="Радиус объекта (м):").grid(row=11, column=0, sticky="w")
    radius_entry = ttk.Entry(settings_frame, width=10)
    radius_entry.grid(row=11, column=1, sticky="w")
    ttk.Label(settings_frame, text="Масса объекта (кг):").grid(row=12, column=0, sticky="w")
    mass_entry = ttk.Entry(settings_frame, width=10)
    mass_entry.grid(row=12, column=1, sticky="w")
    ttk.Label(settings_frame, text="Координаты (x, y, z ) (м):").grid(row=13, column=0, sticky="w")
    x_entry = ttk.Entry(settings_frame, width=5)
    x_entry.grid(row=13, column=1, sticky="w")
    y_entry = ttk.Entry(settings_frame, width=5)
    y_entry.grid(row=13, column=2, sticky="w")
    z_entry = ttk.Entry(settings_frame, width=5)
    z_entry.grid(row=13, column=3, sticky="w")
    ttk.Label(settings_frame, text="Скорости (Vx, Vy, Vz) (м/c):").grid(row=14, column=0, sticky="w")
    Vx_entry = ttk.Entry(settings_frame, width=5)
    Vx_entry.grid(row=14, column=1, sticky="w")
    Vy_entry = ttk.Entry(settings_frame, width=5)
    Vy_entry.grid(row=14, column=2, sticky="w")
    Vz_entry = ttk.Entry(settings_frame, width=5)
    Vz_entry.grid(row=14, column=3, sticky="w")
    tk.Button(settings_frame, text="Добавить объект", command=add_body, bg='blue', fg='white').grid(row=15, column=0, columnspan=4, sticky="w")
    tk.Button(settings_frame, text="Сохранить текущие данные в файл", command=add_body, bg='blue', fg='white').grid(row=16, column=0, columnspan=4, sticky="w")
    window.mainloop()

