from estructuras import Stack, Queue
import json
import requests

class TextFile:
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        
    def write(self, new_content):
        self.undo_stack.push(self.content)
        self.content = new_content
        self.redo_stack = Stack() # Limpiar redo al escribir

    def undo(self):
        if not self.undo_stack.is_empty():
            self.redo_stack.push(self.content)
            self.content = self.undo_stack.pop()
            return True
        return False

    def redo(self):
        if not self.redo_stack.is_empty():
            self.undo_stack.push(self.content)
            self.content = self.redo_stack.pop()
            return True
        return False

class SyntaxChecker:
    @staticmethod
    def check(code):
        stack = Stack()
        pairs = {')': '(', '}': '{', ']': '['}
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for char_pos, char in enumerate(line, 1):
                if char in "({[":
                    stack.push((char, line_num, char_pos))
                elif char in ")}]":
                    if stack.is_empty():
                        return f"Error: '{char}' inesperado en línea {line_num}, carácter {char_pos}."
                    top_char, _, _ = stack.pop()
                    if pairs[char] != top_char:
                        return f"Error de balanceo: se esperaba cerrar '{top_char}' pero se encontró '{char}' en línea {line_num}."
        if not stack.is_empty():
            top_char, l_num, c_pos = stack.pop()
            return f"Error: '{top_char}' sin cerrar en línea {l_num}, carácter {c_pos}."
        return "Sintaxis correcta. Símbolos balanceados."

class ConfigManager:
    def __init__(self):
        self.backup_path = ""
        self.log_path = ""
        self.api_url = ""

    def load_config(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.backup_path = data.get("backup_dir", "./backups")
                self.log_path = data.get("log_dir", "./logs")
                self.api_url = data.get("api_endpoint", "http://localhost:5000/analyze")
            return True
        except Exception as e:
            return False

class AIManager:
    def __init__(self, config):
        self.config = config
        self.queue = Queue()

    def queue_request(self, code):
        self.queue.enqueue(code)
        
    def process_queue(self):
        if self.queue.is_empty():
            return "La cola de peticiones está vacía."
        
        code = self.queue.dequeue()
        try:
            # Petición HTTP a la API simulada
            response = requests.post(self.config.api_url, json={"code": code})
            if response.status_code == 200:
                return response.json()
            return "Error en la respuesta de la API."
        except requests.exceptions.RequestException:
            return "No se pudo conectar con el endpoint de IA configurado."