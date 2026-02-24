import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
from pynput import keyboard
import sys


class MacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Макрос для клавиши Ё")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Переменная для отслеживания состояния макроса
        self.running = False
        self.listener = None

        # Настройка интерфейса
        self.setup_ui()

        # Запуск слушателя клавиш в отдельном потоке
        self.start_key_listener()

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Макрос для клавиши Ё",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Информационная панель
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(info_frame, text="Состояние:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.status_label = tk.Label(info_frame, text="Ожидание нажатия Ё",
                                     fg="green", font=("Arial", 10, "bold"))
        self.status_label.grid(row=0, column=1, sticky="w", padx=10)

        # Описание действий
        actions_frame = tk.LabelFrame(self.root, text="Действия макроса", padx=10, pady=10)
        actions_frame.pack(pady=10, padx=20, fill="both", expand=True)

        actions_text = """1. Перемещает курсор в x850 y670 и кликает ЛКМ
2. Перемещает в x854 y477 и кликает ЛКМ
3. Перемещает в x850 y870 и кликает ЛКМ
4. Перемещает в x950 y483 и кликает ЛКМ
5. Перемещает в x1064 y484 и кликает Shift+ЛКМ

Задержка между действиями: 0.3 секунды"""

        tk.Label(actions_frame, text=actions_text, justify="left",
                 font=("Arial", 9)).pack(anchor="w")

        # Кнопки управления
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Активировать макрос",
                                       command=self.toggle_macro)
        self.start_button.pack(side="left", padx=5)

        ttk.Button(button_frame, text="Выход",
                   command=self.on_closing).pack(side="left", padx=5)

        # Подсказка
        tk.Label(self.root, text="Нажмите клавишу Ё для выполнения макроса",
                 font=("Arial", 9, "italic")).pack(pady=5)

    def start_key_listener(self):
        """Запуск слушателя клавиш в отдельном потоке"""

        def on_press(key):
            try:
                if key == keyboard.KeyCode.from_char('ё') or key == keyboard.KeyCode.from_char('`'):
                    if not self.running:
                        self.execute_macro()
            except:
                pass

        def start_listener():
            with keyboard.Listener(on_press=on_press) as listener:
                self.listener = listener
                listener.join()

        thread = threading.Thread(target=start_listener, daemon=True)
        thread.start()

    def execute_macro(self):
        """Выполнение последовательности действий макроса"""
        self.running = True
        self.root.after(0, self.update_status, "Выполняется...")

        # Координаты для действий
        positions = [
            (850, 670, "left", False),  # x850 y670, ЛКМ
            (854, 477, "left", False),  # x854 y477, ЛКМ
            (890, 670, "left", False),  # x850 y870, ЛКМ
            (950, 483, "left", False),  # x950 y483, ЛКМ
            (1064, 484, "left", True),  # x1064 y484, Shift+ЛКМ
        ]

        # Выполнение каждого действия
        for x, y, button, use_shift in positions:
            # Плавное перемещение курсора
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.1)

            # Клик с Shift или без
            if use_shift:
                pyautogui.keyDown('shift')
                pyautogui.click(button=button)
                pyautogui.keyUp('shift')
            else:
                pyautogui.click(button=button)

            # Задержка между действиями
            time.sleep(0.2)

        self.running = False
        self.root.after(0, self.update_status, "Ожидание нажатия Ё")

    def update_status(self, text):
        """Обновление статуса в интерфейсе"""
        self.status_label.config(text=text)

    def toggle_macro(self):
        """Переключение состояния макроса (для кнопки)"""
        if not self.running:
            self.execute_macro()

    def on_closing(self):
        """Обработка закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            if self.listener:
                self.listener.stop()
            self.root.destroy()
            sys.exit()


def main():
    root = tk.Tk()
    app = MacroApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()