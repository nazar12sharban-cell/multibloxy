import win32gui
import win32con
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import threading
import time

class RobloxWindowManager:
    def __init__(self):
        self.roblox_windows = []
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.is_active = False
        self.stop_monitoring = False
        self.monitor_thread = None
        self.control_thread = None
        self.listeners = []
        
        self.find_roblox_windows()
        self.start_monitoring()
    
    def find_roblox_windows(self):
        """Найти все окна Roblox"""
        self.roblox_windows = []
        
        def enum_windows(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                # Ищем только окна которые содержат только "Roblox" и не содержат других слов
                if window_title == 'Roblox':
                    self.roblox_windows.append({
                        'hwnd': hwnd,
                        'title': window_title
                    })
            return True
        
        win32gui.EnumWindows(enum_windows, None)
        return self.roblox_windows
    
    def get_windows_count(self):
        """Получить количество окон Roblox"""
        return len(self.roblox_windows)
    
    def start_monitoring(self):
        """Запустить мониторинг новых окон"""
        self.stop_monitoring = False
        self.monitor_thread = threading.Thread(target=self._monitor_windows, daemon=True)
        self.monitor_thread.start()
    
    def _monitor_windows(self):
        """Мониторить новые окна Roblox"""
        while not self.stop_monitoring:
            self.find_roblox_windows()
            time.sleep(1)
    
    def activate_control(self):
        """Активировать управление всеми окнами"""
        self.is_active = True
        if self.control_thread is None or not self.control_thread.is_alive():
            self.control_thread = threading.Thread(target=self._control_windows, daemon=True)
            self.control_thread.start()
    
    def deactivate_control(self):
        """Деактивировать управление всеми окнами"""
        self.is_active = False
    
    def _control_windows(self):
        """Контролировать все окна Roblox"""
        
        def on_mouse_move(x, y):
            if not self.is_active or not self.roblox_windows:
                return
            
            for window in self.roblox_windows:
                try:
                    rect = win32gui.GetWindowRect(window['hwnd'])
                    window_x, window_y = rect[0], rect[1]
                    window_width = rect[2] - rect[0]
                    window_height = rect[3] - rect[1]
                    
                    rel_x = x - window_x
                    rel_y = y - window_y
                    
                    if 0 <= rel_x < window_width and 0 <= rel_y < window_height:
                        win32gui.PostMessage(window['hwnd'], win32con.WM_MOUSEMOVE, 
                                           0, self._make_lparam(int(rel_x), int(rel_y)))
                except:
                    pass
        
        def on_mouse_click(x, y, button, pressed):
            if not self.is_active or not self.roblox_windows:
                return
            
            for window in self.roblox_windows:
                try:
                    if button.name == 'left':
                        msg_down = win32con.WM_LBUTTONDOWN
                        msg_up = win32con.WM_LBUTTONUP
                    elif button.name == 'right':
                        msg_down = win32con.WM_RBUTTONDOWN
                        msg_up = win32con.WM_RBUTTONUP
                    else:
                        continue
                    
                    rect = win32gui.GetWindowRect(window['hwnd'])
                    window_x, window_y = rect[0], rect[1]
                    rel_x = x - window_x
                    rel_y = y - window_y
                    
                    if pressed:
                        win32gui.PostMessage(window['hwnd'], msg_down, 0, 
                                           self._make_lparam(int(rel_x), int(rel_y)))
                    else:
                        win32gui.PostMessage(window['hwnd'], msg_up, 0, 
                                           self._make_lparam(int(rel_x), int(rel_y)))
                except:
                    pass
        
        def on_press(key):
            if not self.is_active or not self.roblox_windows:
                return
            
            try:
                key_code = self._get_key_code(key)
                if key_code:
                    for window in self.roblox_windows:
                        try:
                            win32gui.PostMessage(window['hwnd'], win32con.WM_KEYDOWN, key_code, 0)
                        except:
                            pass
            except:
                pass
        
        def on_release(key):
            if not self.is_active or not self.roblox_windows:
                return
            
            try:
                key_code = self._get_key_code(key)
                if key_code:
                    for window in self.roblox_windows:
                        try:
                            win32gui.PostMessage(window['hwnd'], win32con.WM_KEYUP, key_code, 0)
                        except:
                            pass
            except:
                pass
        
        mouse_listener = MouseListener(on_move=on_mouse_move, on_click=on_mouse_click)
        keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
        
        self.listeners = [mouse_listener, keyboard_listener]
        
        mouse_listener.start()
        keyboard_listener.start()
        
        while self.is_active:
            time.sleep(0.1)
        
        try:
            mouse_listener.stop()
        except:
            pass
        try:
            keyboard_listener.stop()
        except:
            pass
    
    def _make_lparam(self, x, y):
        """Создать LPARAM для отправки координат мыши"""
        return (y << 16) | (x & 0xffff)
    
    def _get_key_code(self, key):
        """Получить код клавиши Windows"""
        try:
            if hasattr(key, 'vk'):
                return key.vk
        except:
            pass
        return None
    
    def stop(self):
        """Остановить менеджер окон"""
        self.stop_monitoring = True
        self.deactivate_control()
        for listener in self.listeners:
            try:
                listener.stop()
            except:
                pass
