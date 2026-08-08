import sys
from PyQt5.QtWidgets import QApplication
from ui import MultiBloxySelectorUI
from window_manager import RobloxWindowManager
from hotkey_handler import HotkeyHandler

def main():
    app = QApplication(sys.argv)
    
    # Инициализируем менеджер окон
    window_manager = RobloxWindowManager()
    
    # Инициализируем обработчик горячих клавиш
    hotkey_handler = HotkeyHandler(window_manager)
    
    # Создаем UI
    ui = MultiBloxySelectorUI(window_manager, hotkey_handler)
    ui.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
