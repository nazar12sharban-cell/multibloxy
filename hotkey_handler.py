from pynput import keyboard
import threading

class HotkeyHandler:
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.current_hotkey = None
        self.listener = None
        self.is_listening_for_hotkey = False
        self.on_hotkey_changed = None
    
    def start_listening_for_hotkey(self, callback=None):
        """Начать прослушивание для установки горячей клавиши"""
        self.is_listening_for_hotkey = True
        self.on_hotkey_changed = callback
        
        def on_press(key):
            if self.is_listening_for_hotkey:
                self.set_hotkey(key)
                self.is_listening_for_hotkey = False
                if self.listener:
                    self.listener.stop()
        
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
    
    def set_hotkey(self, key):
        """Установить горячую клавишу"""
        try:
            if hasattr(key, 'name'):
                self.current_hotkey = key.name
            else:
                self.current_hotkey = str(key).strip("'")
            
            if self.on_hotkey_changed:
                self.on_hotkey_changed(self.current_hotkey)
            
            self._start_hotkey_listener()
        except:
            pass
    
    def _start_hotkey_listener(self):
        """Слушать горячую клавишу для включения/отключения"""
        if self.listener:
            self.listener.stop()
        
        def on_press(key):
            try:
                key_name = None
                if hasattr(key, 'name'):
                    key_name = key.name
                else:
                    key_name = str(key).strip("'")
                
                if key_name == self.current_hotkey:
                    if self.window_manager.is_active:
                        self.window_manager.deactivate_control()
                    else:
                        self.window_manager.activate_control()
            except:
                pass
        
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
    
    def get_hotkey(self):
        """Получить текущую горячую клавишу"""
        return self.current_hotkey if self.current_hotkey else "Not set"
    
    def stop(self):
        """Остановить обработчик"""
        if self.listener:
            self.listener.stop()
