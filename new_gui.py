import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QComboBox, QPushButton,
                             QFormLayout, QGroupBox, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt

# Значения по умолчанию (как в оригинале)
DEFAULT_CALC_SYST = 'Гелиоцентрическая декартова'
DEFAULT_SPEED = str(365 * 24 * 3600)
DEFAULT_STEP = '3600'
DEFAULT_FILE = 'info.txt'
DEFAULT_START_DATE = '00:00:00/12/04/2021'


class ControlWindow(QWidget):
    def __init__(self, q, qnewb):
        super().__init__()
        self.q = q
        self.qnewb = qnewb
        self.setWindowTitle("Управление моделью")
        self.resize(600, 550)

        self.setup_ui()

    def setup_ui(self):
        # Основной вертикальный контейнер
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # --- Группа настроек ---
        settings_group = QGroupBox("Настройки симуляции")
        settings_layout = QFormLayout()

        # Система координат
        self.coord_combo = QComboBox()
        self.coord_combo.addItems(['Эклиптическая', 'Экваториальная',
                                   'Гелиоцентрическая полярная', 'Гелиоцентрическая декартова'])
        self.coord_combo.setCurrentText(DEFAULT_CALC_SYST)
        settings_layout.addRow("Система координат:", self.coord_combo)

        # Скорость расчёта
        self.speed_entry = QLineEdit(DEFAULT_SPEED)
        settings_layout.addRow("Скорость расчёта (сек):", self.speed_entry)

        # Шаг интегрирования
        self.step_entry = QLineEdit(DEFAULT_STEP)
        settings_layout.addRow("Шаг интегрирования (сек):", self.step_entry)

        # Файл данных
        self.file_entry = QLineEdit(DEFAULT_FILE)
        settings_layout.addRow("Файл данных:", self.file_entry)

        # Даты
        self.start_date_entry = QLineEdit(DEFAULT_START_DATE)
        self.start_date_entry.setPlaceholderText("ЧЧ:MM:СС/ДД/ММ/ГГГГ")
        settings_layout.addRow("Стартовая дата:", self.start_date_entry)

        self.end_date_entry = QLineEdit()
        self.end_date_entry.setPlaceholderText("ЧЧ:MM:СС/ДД/ММ/ГГГГ")
        settings_layout.addRow("Дата окончания:", self.end_date_entry)

        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        # --- Кнопки управления расчётом ---
        btn_layout = QHBoxLayout()

        self.btn_start = QPushButton("Начать расчёт")
        self.btn_start.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.btn_start.clicked.connect(self.starter)

        self.btn_stop = QPushButton("Остановить расчёт")
        self.btn_stop.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        self.btn_stop.clicked.connect(self.stopper)

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        main_layout.addLayout(btn_layout)

        # Лейбл для статуса
        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # --- Группа добавления объекта ---
        obj_group = QGroupBox("Меню добавления объекта")
        obj_layout = QVBoxLayout()

        # Форма для основных параметров
        obj_form = QFormLayout()
        self.name_entry = QLineEdit()
        obj_form.addRow("Имя объекта:", self.name_entry)

        self.radius_entry = QLineEdit()
        obj_form.addRow("Радиус объекта (м):", self.radius_entry)

        self.mass_entry = QLineEdit()
        obj_form.addRow("Масса объекта (кг):", self.mass_entry)
        obj_layout.addLayout(obj_form)

        # Сетка для координат и скоростей
        grid_vals = QGridLayout()

        grid_vals.addWidget(QLabel("Координаты (м):"), 0, 0)
        self.x_entry = QLineEdit();
        self.x_entry.setPlaceholderText("X")
        self.y_entry = QLineEdit();
        self.y_entry.setPlaceholderText("Y")
        self.z_entry = QLineEdit();
        self.z_entry.setPlaceholderText("Z")
        grid_vals.addWidget(self.x_entry, 0, 1)
        grid_vals.addWidget(self.y_entry, 0, 2)
        grid_vals.addWidget(self.z_entry, 0, 3)

        grid_vals.addWidget(QLabel("Скорости (м/с):"), 1, 0)
        self.vx_entry = QLineEdit();
        self.vx_entry.setPlaceholderText("Vx")
        self.vy_entry = QLineEdit();
        self.vy_entry.setPlaceholderText("Vy")
        self.vz_entry = QLineEdit();
        self.vz_entry.setPlaceholderText("Vz")
        grid_vals.addWidget(self.vx_entry, 1, 1)
        grid_vals.addWidget(self.vy_entry, 1, 2)
        grid_vals.addWidget(self.vz_entry, 1, 3)

        obj_layout.addLayout(grid_vals)

        # Кнопки для объектов
        self.btn_add_obj = QPushButton("Добавить объект")
        self.btn_add_obj.setStyleSheet("background-color: blue; color: white;")
        self.btn_add_obj.clicked.connect(self.add_body)

        self.btn_save_data = QPushButton("Сохранить текущие данные в файл")
        self.btn_save_data.setStyleSheet("background-color: blue; color: white;")
        self.btn_save_data.clicked.connect(self.save_data)

        obj_layout.addWidget(self.btn_add_obj)
        obj_layout.addWidget(self.btn_save_data)

        obj_group.setLayout(obj_layout)
        main_layout.addWidget(obj_group)

    def starter(self):
        """Логика запуска расчёта"""
        start_date = self.start_date_entry.text()
        end_date = self.end_date_entry.text()

        # Валидация
        if not start_date:
            self.status_label.setText("Ошибка: Введите стартовую дату")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            return

        if not end_date:
            self.status_label.setText("Ошибка: Введите дату окончания")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            return

        # Отправка данных в очередь
        self.q.put(("update_calcsyst", self.coord_combo.currentText()))

        if self.speed_entry.text():
            try:
                self.q.put(("update_speed", float(self.speed_entry.text())))
            except ValueError:
                pass  # Или обработка ошибки числа

        if self.step_entry.text():
            try:
                self.q.put(("update_step", float(self.step_entry.text())))
            except ValueError:
                pass

        if self.file_entry.text():
            self.q.put(("update_file", self.file_entry.text()))

        self.q.put(("update_start_date", start_date))
        self.q.put(("update_end_date", end_date))

        # Успешный запуск
        self.q.put(('update_ifstart', True))
        self.status_label.setText("Расчёт запущен")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")

    def stopper(self):
        """Логика остановки"""
        self.q.put(('update_ifstart', False))
        self.status_label.setText("Расчёт остановлен")
        self.status_label.setStyleSheet("color: red;")

    def add_body(self):
        """Добавление нового тела"""
        try:
            name = self.name_entry.text()
            radius = float(self.radius_entry.text())
            mass = float(self.mass_entry.text())
            x = float(self.x_entry.text())
            y = float(self.y_entry.text())
            z = float(self.z_entry.text())
            vx = float(self.vx_entry.text())
            vy = float(self.vy_entry.text())
            vz = float(self.vz_entry.text())

            # Кортеж данных (структура из вашего примера)
            new_body = (name, x, y, z, vx, vy, vz, 0, 0, 0, radius, mass)

            # В оригинале new_body никуда не отправлялся, здесь отправляем в qnewb
            self.qnewb.put(new_body)

            self.status_label.setText(f"Объект '{name}' добавлен")
            self.status_label.setStyleSheet("color: blue;")

            # Очистка полей (опционально)
            # self.name_entry.clear()

        except ValueError:
            self.status_label.setText("Ошибка: Проверьте числовые поля")
            self.status_label.setStyleSheet("color: red;")

    def save_data(self):
        """Сохранение данных"""
        # В оригинале эта кнопка вызывала add_body, что скорее всего было ошибкой.
        # Здесь отправляем сигнал на сохранение, если это предусмотрено логикой симуляции.
        self.q.put("save_current_data")
        self.status_label.setText("Запрос на сохранение отправлен")
        self.status_label.setStyleSheet("color: black;")


def managment(q, qnewb):
    """Функция-обертка для запуска Qt приложения"""
    # Создаем экземпляр приложения.
    # sys.argv нужен для обработки аргументов командной строки Qt
    app = QApplication(sys.argv)

    # Применяем стиль Fusion для одинакового вида на всех ОС
    app.setStyle('Fusion')

    window = ControlWindow(q, qnewb)
    window.show()

    # Запускаем цикл событий.
    # В Python 3.14+ и современных PyQt используется .exec() вместо .exec_()
    sys.exit(app.exec())


# Для тестирования интерфейса отдельно от основной программы раскомментируйте строки ниже:
"""if __name__ == "__main__":
    from queue import Queue

    # Заглушки очередей для теста
    q_test = Queue()
    qnewb_test = Queue()
    managment(q_test, qnewb_test)"""