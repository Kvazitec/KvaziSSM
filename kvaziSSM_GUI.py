import time
from kvazi_dts import datasearch
from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Separator
CalcSyst = ''
CalcSystdoub = CalcSyst
CalcSpeed = 365*24*3600
file_name ='info.txt'
start_date = '00:00:00/01/01/2000'
end_date = ''
now_date = ''
ifnew = True
Name = ''
Radius = 0
setupdtime = 1
mcombo = 0
bodies = []
x = 0
y = 0
z = 0
Vx = 0
Vy = 0
Vz = 0
def managment():
    global CalcSyst
    global CalcSystdoub
    global CalcSpeed
    global file_name
    global ifnew
    global mcombo
    global bodies
    def creatmenu(row0):
        def new(loc_name, loc_radius, loc_x, loc_y, loc_z, loc_Vx, loc_Vy, loc_Vz):
            global Name
            global Radius
            global x
            global y
            global z
            global Vx
            global Vy
            global Vz
            global ifnew
            ifnew = True
            Name = loc_name
            Radius = loc_radius
            x = loc_x
            y = loc_y
            z = loc_z
            Vx = loc_Vx
            Vy = loc_Vy
            Vz = loc_Vz

        lbl1 = Label(window, text="Добавление нового объекта")
        lbl1.grid(column=0, row=row0)
        namelbl = Label(window, text="Имя объекта: ")
        namelbl.grid(column=0, row=row0 + 1)
        namelbl_txt = Entry(window, width=10)
        namelbl_txt.grid(column=1, row=row0 + 1)
        radiuslbl = Label(window, text="Радиус объекта: ")
        radiuslbl.grid(column=0, row=row0+2)
        radiuslbl_txt = Entry(window, width=10)
        radiuslbl_txt.grid(column=1, row=row0+2)
        poslbl = Label(window, text="Начальные координаты объекта: ")
        poslbl.grid(column=0, row=row0+3)
        poslbl_x = Label(window, text="x: ")
        poslbl_x.grid(column=1, row=row0+3)
        poslbl_x_txt = Entry(window, width=10)
        poslbl_x_txt.grid(column=2, row=row0+3)
        poslbl_y = Label(window, text="y: ")
        poslbl_y.grid(column=1, row=row0+4)
        poslbl_y_txt = Entry(window, width=10)
        poslbl_y_txt.grid(column=2, row=row0+4)
        poslbl_z = Label(window, text="z: ")
        poslbl_z.grid(column=1, row=row0+5)
        poslbl_z_txt = Entry(window, width=10)
        poslbl_z_txt.grid(column=2, row=row0+5)
        speedlbl = Label(window, text="Проекции начальной скорости объекта: ")
        speedlbl.grid(column=0, row=row0+6)
        speedlbl_x = Label(window, text="Vx: ")
        speedlbl_x.grid(column=1, row=row0+6)
        speedlbl_x_txt = Entry(window, width=10)
        speedlbl_x_txt.grid(column=2, row=row0+6)
        speedlbl_y = Label(window, text="Vy: ")
        speedlbl_y.grid(column=1, row=row0+7)
        speedlbl_y_txt = Entry(window, width=10)
        speedlbl_y_txt.grid(column=2, row=row0+7)
        speedlbl_z = Label(window, text="Vz: ")
        speedlbl_z.grid(column=1, row=row0+8)
        speedlbl_z_txt = Entry(window, width=10)
        speedlbl_z_txt.grid(column=2, row=row0+8)
        initnewb = Button(window, text="Добавить", command=lambda: new(namelbl_txt.get(), radiuslbl_txt.get(), poslbl_x_txt.get(), poslbl_y_txt.get(), poslbl_z_txt.get(), speedlbl_x_txt.get(), speedlbl_y_txt.get(), speedlbl_z_txt.get()))
        initnewb.grid(column=0, row=row0+9)
    def speed_set(get):
        global CalcSpeed
        CalcSpeed = get
    def file_set(get):
        global file_name
        file_name = get
    def setupupd(get):
        global setupdtime
        setupdtime = float(get)
    def date_set(start, end):
        global start_date
        global end_date
        start_date = start
        end_date = end
    window = Tk()
    window.title(f"Управление моделью {datasearch(file_name, 'General', 'system_name')}")
    window.geometry('1700x500')
    Separator(
        window,
        takefocus=0,
        orient=VERTICAL
    ).place(x=620, y=0, relheight=1)
    lbl = Label(window, text="Настройка расчётной модели: ", font="TkHeadingFont")
    lbl.grid(column=0, row=0)
    mode_lbl = Label(window, text="    Режим: ")
    mode_lbl.grid(column=0, row=1)
    mcombo = Combobox(window, width=27)
    mcombo['values'] = ('Расчёт координат для даты', 'Проверка столкновений')
    mcombo.current(0)  # установите вариант по умолчанию
    mcombo.grid(column=1, row=1)
    coord_lbl = Label(window, text="    Система координат: ")
    coord_lbl.grid(column=0, row=2)
    combo = Combobox(window, width = 27)
    combo['values'] = ('Эклиптическая', 'Экваториальная', 'Гелиоцентрическая полярная', 'Гелиоцентрическая декартова')
    combo.current(2)  # установите вариант по умолчанию
    combo.grid(column=1, row=2)
    speedlbl = Label(window, text=f"Скорость расчёта: ")
    speedlbl.grid(column=0, row=4)
    speedlbl_txt = Entry(window, width=10)
    speedlbl_txt.grid(column=1, row=4)
    speedbut = Button(window, text="Установить", command=lambda: speed_set(speedlbl_txt.get()))
    speedbut.grid(column=2, row=4)
    updspeed = Label(window, text="Скорость обновления: ")
    updspeed.grid(column=0, row=5)
    updspeed_txt = Entry(window, width=10)
    updspeed_txt.grid(column=1, row=5)
    updspbut = Button(window, text="Установить", command=lambda: setupupd(updspeed_txt.get()))
    updspbut.grid(column=2, row=5)
    filelbl = Label(window, text="Файл данных: ")
    filelbl.grid(column=0, row=6)
    filelbl_txt = Entry(window, width=10)
    filelbl_txt.grid(column=1, row=6)
    filebut = Button(window, text="Установить", command=lambda: file_set(filelbl_txt.get()))
    filebut.grid(column=2, row=6)
    initnewb = Button(window, text="Добавить новый объект", command=lambda: creatmenu(8))
    initnewb.grid(column=0, row=7)
    statelbl = Label(window, text="                         Текущее состояние модели: ", font="TkHeadingFont")
    statelbl.grid(column=3, row=0)
    set_systemlbl = Label(window, text=f"                             Система координат: ")
    set_systemlbl.grid(column=3, row=1)
    set_speedlbl = Label(window, text=f"                             Скорость расчёта: ")
    set_speedlbl.grid(column=3, row=2)
    set_filelbl = Label(window, text=f"                             Файл данных: ")
    set_filelbl.grid(column=3, row=3)
    set_datlbl = Label(window, text=f"                             Дата: ")
    set_datlbl.grid(column=3, row=4)
    statelbl = Label(window, text="         Параметры объектов: ", font="TkHeadingFont")
    statelbl.grid(column=3, row=5)
    Separator(
    window,
    takefocus=0,
    orient=VERTICAL
    ).place(x=620, y=0, relheight=1)
    timeupd = time.time()
    while True:
            if time.time() - timeupd > setupdtime:
                lenc = len(CalcSyst)
                if lenc < 27:
                    set_systemlbl1 = Label(window, text='   ' * ((27 - lenc) // 2) + CalcSyst + '   ' * (
                            27 - ((27 - lenc) // 2) - lenc))
                    set_systemlbl1.grid(column=4, row=1)
                else:
                    set_systemlbl1 = Label(window, text=CalcSyst)
                    set_systemlbl1.grid(column=4, row=1)
                set_datlbl = Label(window, text=f"{now_date}")
                set_datlbl.grid(column=4, row=4)
                set_speedlbl = Label(window, text=CalcSpeed)
                set_speedlbl.grid(column=4, row=2)
                set_filelbl = Label(window,
                                    text=file_name)
                set_filelbl.grid(column=4, row=3)
                datelbl = Label(window, text=f"Стартовая дата: ")
                datelbl.place(x=15, y=68)
                datelbl_txt = Entry(window, width=10)
                datelbl_txt.place(x=130, y=68)
                datelbl = Label(window, text=f"Дата окончания: ")
                datelbl.place(x=225, y=68)
                dateelbl_txt = Entry(window, width=10)
                dateelbl_txt.place(x=345, y=68)
                datebut = Button(window, text="Установить", command=lambda: date_set(datelbl_txt.get(), dateelbl_txt.get()))
                datebut.place(x=453, y=60)
                for i in range(0, int(datasearch(file_name, 'General', 'NUM_BODIES'))):
                    if ifnew:
                        lbl1 = Label(window,
                                     text=f"                             Объект {datasearch(file_name, f'Body_{i}', 'name')}: ",
                                     font="TkHeadingFont")
                        lbl1.grid(column=3, row=6 + 4 * i)
                        lbl2 = Label(window, text=f"                             Координаты объекта: ")
                        lbl2.grid(column=3, row=7 + 4 * i)
                        lbl3 = Label(window, text=f"                             Проекции скорости объекта: ")
                        lbl3.grid(column=6, row=7 + 4 * i)
                        axlbl = Label(window, text=f"                             Проекции ускорений объекта: ")
                        axlbl.grid(column=10, row=7 + 4 * i)
                    CalcSyst = combo.get()
                    if CalcSystdoub != CalcSyst:
                        if CalcSyst == 'Гелиоцентрическая декартова':
                            marks = ["x: ", "y: ", "z: ", "Vx: ", "Vy: ", "Vz: ", "ax: ", "ay: ", "az: "]
                            for j in range(0, len(marks)):
                                pos = Label(window, text=marks[j])
                                if j < 3:
                                    pos.grid(column=4, row=j + 7 + 4 * i)
                                elif j < 6:
                                    pos.grid(column=8, row=j + 4 + 4 * i)
                                else:
                                    pos.grid(column=11, row=j + 1 + 4 * i)
                            del j
                        elif CalcSyst == 'Гелиоцентрическая полярная' or CalcSyst == 'Эклиптическая':
                            marks = ["λ: ", "β: ", "r: ", "Vλ: ", "Vβ: ", "Vr: ", "aλ: ", "aβ: ", "ar: "]
                            for j in range(0, len(marks)):
                                pos = Label(window, text=marks[j])
                                if j < 3:
                                    pos.grid(column=4, row=j + 7 + 4 * i)
                                elif j < 6:
                                    pos.grid(column=8, row=j + 4 + 4 * i)
                                else:
                                    pos.grid(column=11, row=j + 1 + 4 * i)
                            del j
                        elif CalcSyst == 'Экваториальная':
                            marks = ["α: ", "δ: ", "r: ", "Vα: ", "Vδ: ", "Vr: ", "aα: ", "aδ: ", "ar: "]
                            for j in range(0, len(marks)):
                                pos = Label(window, text=marks[j])
                                if j < 3:
                                    pos.grid(column=4, row=j + 7 + 4 * i)
                                elif j < 6:
                                    pos.grid(column=8, row=j + 4 + 4 * i)
                                else:
                                    pos.grid(column=11, row=j + 1 + 4 * i)
                            del j
                    values = [round(bodies[i].x/149597870700, 8), round(bodies[i].y/149597870700, 8), round(bodies[i].z/149597870700, 8), 0, 0, 0, 0, 0, 0]
                    print(values)
                    for j in range(0, len(values)):
                        pos = Label(window, text=values[j])
                        if j < 3:
                            pos.grid(column=5, row=j + 7 + 4 * i)
                        elif j < 6:
                            pos.grid(column=9, row=j + 4 + 4 * i)
                        else:
                            pos.grid(column=12, row=j + 1 + 4 * i)
                    del j
                ifnew = False
                CalcSystdoub = CalcSyst
                timeupd = time.time()
            Separator(
                window,
                takefocus=0,
                orient=VERTICAL
            ).place(x=620, y=0, relheight=1)
            window.update()
            window.update_idletasks()
def managment_initiator(bodies_in):
    global bodies
    bodies = bodies_in
    managment()