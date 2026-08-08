from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

class MultiBloxySelectorUI(QMainWindow):
    def __init__(self, window_manager, hotkey_handler):
        super().__init__()
        self.window_manager = window_manager
        self.hotkey_handler = hotkey_handler
        
        self.init_ui()
        self.setup_timer()
    
    def init_ui(self):
        """Инициализировать пользовательский интерфейс"""
        self.setWindowTitle('MultiBloxy - Roblox Multi-Window Manager')
        self.setGeometry(100, 100, 650, 550)
        self.setStyleSheet("background-color: #f0f0f0;")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Заголовок
        title = QLabel('🎮 MultiBloxy')
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2196F3;")
        main_layout.addWidget(title)
        
        # Статус
        self.status_label = QLabel('Status: Inactive')
        status_font = QFont()
        status_font.setPointSize(12)
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet('color: red;')
        main_layout.addWidget(self.status_label)
        
        # Информация об окнах
        self.windows_label = QLabel('Roblox Windows: 0')
        windows_font = QFont()
        windows_font.setPointSize(11)
        self.windows_label.setFont(windows_font)
        self.windows_label.setStyleSheet("color: #555;")
        main_layout.addWidget(self.windows_label)
        
        # Список окон
        windows_group = QGroupBox('Detected Roblox Windows')
        windows_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
        """)
        windows_layout = QVBoxLayout()
        self.windows_list = QListWidget()
        self.windows_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
        """)
        self.refresh_windows_list()
        windows_layout.addWidget(self.windows_list)
        windows_group.setLayout(windows_layout)
        main_layout.addWidget(windows_group)
        
        # Горячие клавиши
        hotkey_group = QGroupBox('⌨️ Hotkey Settings')
        hotkey_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        hotkey_layout = QHBoxLayout()
        
        self.hotkey_label = QLabel('Current Hotkey: Not set')
        hotkey_label_font = QFont()
        hotkey_label_font.setPointSize(10)
        self.hotkey_label.setFont(hotkey_label_font)
        self.hotkey_label.setStyleSheet("color: #333;")
        hotkey_layout.addWidget(self.hotkey_label)
        
        self.set_hotkey_btn = QPushButton('Set Hotkey')
        self.set_hotkey_btn.clicked.connect(self.on_set_hotkey)
        self.set_hotkey_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        self.set_hotkey_btn.setMaximumWidth(150)
        hotkey_layout.addWidget(self.set_hotkey_btn)
        
        hotkey_group.setLayout(hotkey_layout)
        main_layout.addWidget(hotkey_group)
        
        # Управление
        control_group = QGroupBox('Control')
        control_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton('▶️ Start')
        self.start_btn.clicked.connect(self.on_start)
        self.start_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                font-size: 12px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        self.start_btn.setMinimumHeight(40)
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton('⏹️ Stop')
        self.stop_btn.clicked.connect(self.on_stop)
        self.stop_btn.setStyleSheet('''
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                font-size: 12px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        ''')
        self.stop_btn.setMinimumHeight(40)
        control_layout.addWidget(self.stop_btn)
        
        self.disable_all_btn = QPushButton('⛔ Disable All')
        self.disable_all_btn.clicked.connect(self.on_disable_all)
        self.disable_all_btn.setStyleSheet('''
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                font-size: 12px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        ''')
        self.disable_all_btn.setMinimumHeight(40)
        control_layout.addWidget(self.disable_all_btn)
        
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        central_widget.setLayout(main_layout)
        
        self.hotkey_handler.on_hotkey_changed = self.update_hotkey_label
    
    def setup_timer(self):
        """Установить таймер для обновления информации"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(500)
    
    def on_start(self):
        """Обработчик кнопки Start"""
        if self.window_manager.get_windows_count() < 2:
            QMessageBox.warning(self, 'Warning', 'Need at least 2 Roblox windows open!')
            return
        
        if not self.hotkey_handler.current_hotkey:
            QMessageBox.warning(self, 'Warning', 'Please set a hotkey first!')
            return
        
        self.window_manager.activate_control()
        QMessageBox.information(self, 'Success', f'✅ Multi-window control activated!\n\nPress "{self.hotkey_handler.get_hotkey()}" to toggle.')
    
    def on_stop(self):
        """Обработчик кнопки Stop"""
        self.window_manager.deactivate_control()
    
    def on_disable_all(self):
        """Обработчик кнопки Disable All"""
        self.window_manager.deactivate_control()
        QMessageBox.information(self, 'Info', '✅ All windows disabled!')
    
    def on_set_hotkey(self):
        """Обработчик кнопки Set Hotkey"""
        self.set_hotkey_btn.setText('Press any key...')
        self.set_hotkey_btn.setEnabled(False)
        self.hotkey_handler.start_listening_for_hotkey(self.on_hotkey_set)
    
    def on_hotkey_set(self):
        """Горячая клавиша установлена"""
        self.set_hotkey_btn.setText('Set Hotkey')
        self.set_hotkey_btn.setEnabled(True)
    
    def update_hotkey_label(self, hotkey):
        """Обновить метку горячей клавиши"""
        self.hotkey_label.setText(f'Current Hotkey: {hotkey}')
    
    def refresh_windows_list(self):
        """Обновить список окон Roblox"""
        self.windows_list.clear()
        windows = self.window_manager.roblox_windows
        
        if not windows:
            item = QListWidgetItem('❌ No Roblox windows found')
            item.setForeground(QColor('red'))
            self.windows_list.addItem(item)
        else:
            for i, window in enumerate(windows, 1):
                title = window['title'][:50] + '...' if len(window['title']) > 50 else window['title']
                item = QListWidgetItem(f'✓ {i}. {title}')
                item.setForeground(QColor('green'))
                self.windows_list.addItem(item)
    
    def update_status(self):
        """Обновить статус"""
        count = self.window_manager.get_windows_count()
        self.windows_label.setText(f'Roblox Windows: {count}')
        self.refresh_windows_list()
        
        if self.window_manager.is_active:
            self.status_label.setText('Status: 🟢 ACTIVE')
            self.status_label.setStyleSheet('color: green; font-weight: bold;')
        else:
            self.status_label.setText('Status: ⚫ Inactive')
            self.status_label.setStyleSheet('color: red; font-weight: bold;')
    
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        self.window_manager.stop()
        self.hotkey_handler.stop()
        self.timer.stop()
        event.accept()
