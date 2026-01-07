import sys
import vtk
import time

from calculating_advanced import Body
import calculating_advanced


class SolarSystemVisualizer:
    def __init__(self, qbod, qvis, qvis_date):
        self.qbod = qbod
        self.qvis = qvis
        self.qvis_date = qvis_date

        # --- Переменные состояния ---
        self.bodies_data = []  # Список объектов Body
        self.actors = {}  # Словарь {имя_тела: vtkActor} (сами сферы)
        self.labels = {}  # Словарь {имя_тела: vtkCaptionActor2D} (подписи)
        self.now_date = "00:00:00/12/04/2021"
        self.end_date = ""
        self.calc_speed = 365 * 24 * 3600
        self.step = 3600
        self.file_name = 'info.txt'

        # --- Масштабирование ---
        # VTK плохо работает с числами порядка 10^11, приводим к условным единицам
        self.COORD_SCALE = 1.0e-9

        # Визуальное увеличение радиусов, иначе планеты будут невидимыми точками
        self.RADIUS_SCALE_SUN = self.COORD_SCALE * 60
        self.RADIUS_SCALE_PLANET = self.COORD_SCALE * 1500

        # --- Настройка VTK ---
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.05, 0.05, 0.1)  # Темно-синий космос

        self.render_window = vtk.vtkRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        self.render_window.SetSize(1200, 900)
        self.render_window.SetWindowName("KvaziSSM 3D Model Visualisation")

        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.render_window)

        # Стиль камеры: левая кнопка - вращение, колесо - зум, средняя/shift - панорамирование
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)
        camera = self.renderer.GetActiveCamera()
        camera.Dolly(0.001)
        # Текстовая информация (HUD) - статический текст в углу экрана
        self.text_actor = vtk.vtkTextActor()
        self.text_actor.GetTextProperty().SetFontSize(14)
        self.text_actor.GetTextProperty().SetColor(0.8, 0.8, 0.8)
        self.text_actor.SetPosition(10, 10)
        self.renderer.AddActor2D(self.text_actor)

        # Инициализация таймера для цикла обновления (примерно 60 FPS)
        self.interactor.Initialize()
        self.interactor.CreateRepeatingTimer(16)
        self.interactor.AddObserver("TimerEvent", self.update_scene)
        self.interactor.AddObserver("InteractionEvent", self.update_scene)

    def get_color_by_name(self, name):
        """Возвращает RGB цвет в зависимости от имени объекта"""
        name = name.lower()
        if 'sun' in name or 'солнце' in name: return (1.0, 0.9, 0.0)  # Желтый
        if 'earth' in name or 'земля' in name: return (0.1, 0.4, 0.9)  # Синий
        if 'mars' in name or 'марс' in name: return (1.0, 0.3, 0.2)  # Красный
        if 'venus' in name or 'венера' in name: return (0.9, 0.8, 0.6)
        if 'mercury' in name or 'меркурий' in name: return (0.6, 0.6, 0.6)
        if 'jupiter' in name or 'юпитер' in name: return (0.8, 0.6, 0.4)
        if 'saturn' in name or 'сатурн' in name: return (0.9, 0.8, 0.5)
        return (0.8, 0.8, 0.8)  # Серый по умолчанию

    def create_body_actor(self, body):
        """Создает сферу и 2D-подпись фиксированного размера для нового тела"""

        # 1. Геометрия сферы
        sphere = vtk.vtkSphereSource()
        sphere.SetThetaResolution(40)  # Детализация
        sphere.SetPhiResolution(40)

        # Выбор масштаба радиуса
        rad_scale = self.RADIUS_SCALE_SUN if body.name in ['Sun', 'Солнце'] else self.RADIUS_SCALE_PLANET
        sphere.SetRadius(body.radius * rad_scale)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Настройка цвета и свечения
        r, g, b = self.get_color_by_name(body.name)
        actor.GetProperty().SetColor(r, g, b)

        if body.name in ['Sun', 'Солнце']:
            actor.GetProperty().SetAmbient(1.0)  # Солнце светится само
            actor.GetProperty().SetDiffuse(0.0)
        else:
            actor.GetProperty().SetAmbient(0.1)  # Планеты тусклые в тени
            actor.GetProperty().SetDiffuse(0.8)  # Отражают свет

        # 2. Текстовая метка (CaptionActor2D)
        # Этот объект отображает текст поверх 3D сцены, размер шрифта не зависит от зума
        label = vtk.vtkCaptionActor2D()
        label.SetCaption(body.name)
        label.ThreeDimensionalLeaderOff()  # Убедиться, что он работает в 2D режиме
        label.SetPadding(0)  # Убрать отступы вокруг текста
        label.SetHeight(0.001)
        # Настройка шрифта
        text_prop = label.GetCaptionTextProperty()
        text_prop.SetColor(1, 1, 1)  # Белый текст
        text_prop.BoldOff()
        text_prop.ItalicOff()

        # Отключаем "лидер" (линию) и рамку, оставляем только текст
        label.LeaderOff()
        label.BorderOff()
        

        # Смещение текста, чтобы он не перекрывал планету (в пикселях экрана)
        # Position управляет положением текста относительно точки привязки
        # label.SetPosition(...) - здесь можно подстроить, если текст "сидит" на планете

        return actor, label

    def update_scene(self, obj, event):
        """Основной цикл обновления данных и графики"""

        # --- 1. Обработка очередей управления ---
        if not self.qvis_date.empty():
            self.now_date = self.qvis_date.get()

        if not self.qvis.empty():
            try:
                # Читаем все доступные команды, чтобы не было задержек
                while not self.qvis.empty():
                    command, data = self.qvis.get_nowait()
                    if command == "update_end_date":
                        self.end_date = data
                    elif command == "update_speed":
                        self.calc_speed = data
                    elif command == "update_step":
                        self.step = data
                    elif command == "update_file":
                        self.file_name = data
            except:
                pass

        # --- 2. Получение данных о телах ---
        has_new_data = False
        if not self.qbod.empty():
            # Берем только самый последний кадр, пропуская промежуточные, если рендер не успевает
            while not self.qbod.empty():
                bod_data_raw = self.qbod.get_nowait()

            # Распаковка данных в объекты Body
            self.bodies_data = [Body(*b) for b in bod_data_raw]
            has_new_data = True

        # Если данных нет вообще (первый запуск), пробуем загрузить дефолтные
        if not self.bodies_data and not has_new_data:
            try:
                calculating_advanced.downloader()
                self.bodies_data = calculating_advanced.bodies
            except:
                pass  # Ждем данных от процесса расчета

        # --- 3. Обновление 3D объектов ---
        for body in self.bodies_data:
            # Применяем масштаб координат
            x = body.x * self.COORD_SCALE
            y = body.y * self.COORD_SCALE
            z = body.z * self.COORD_SCALE

            # Если для этого тела еще нет актера, создаем его
            if body.name not in self.actors:
                actor, label = self.create_body_actor(body)
                self.renderer.AddActor(actor)
                self.renderer.AddActor(label)
                self.actors[body.name] = actor
                self.labels[body.name] = label

            # Обновляем позицию сферы
            self.actors[body.name].SetPosition(x, y, z)

            # Обновляем точку привязки текста
            self.labels[body.name].SetAttachmentPoint(x, y, z)

        # --- 4. Обновление интерфейса (HUD) ---
        info_text = (
            f"Date: {self.now_date}\n"
            f"End Date: {self.end_date}\n"
            f"Calc Speed: {self.calc_speed}\n"
            f"Step: {self.step}\n"
            f"Objects: {len(self.bodies_data)}\n"
        )
        self.text_actor.SetInput(info_text)

        # Рендер текущего кадра
        self.render_window.Render()

    def start(self):
        """Запуск цикла визуализации"""
        # Сброс камеры на объекты при старте
        self.renderer.ResetCamera()
        cam = self.renderer.GetActiveCamera()
        cam.Zoom(0.8)  # Немного отдаляем

        self.render_window.Render()
        self.interactor.Start()


def visualization(qbod, qvis, qvis_date):
    """Точка входа для мультипроцессинга"""
    viz = SolarSystemVisualizer(qbod, qvis, qvis_date)
    viz.start()