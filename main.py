import sys
from estructuras import FileLinkedList
from modelos import TextFile, ConfigManager, SyntaxChecker, AIManager
from ordenamiento import Sorter

class IDEContext:
    def __init__(self):
        self.files = FileLinkedList()
        self.active_file = None
        self.config = ConfigManager()
        self.ai_manager = AIManager(self.config)
        self.diagnostics = [
             {"line": 10, "severity": 3, "msg": "Variable no usada"},
             {"line": 2, "severity": 1, "msg": "Falta punto y coma"}
        ]

# Patrón Comando
class Command:
    def execute(self, args, context): pass

class NewCommand(Command):
    def execute(self, args, context):
        if not args: return "Error: Especifique nombre de archivo."
        filename = args[0]
        new_file = TextFile(filename)
        context.files.append(new_file)
        context.active_file = new_file
        return f"Archivo '{filename}' creado en memoria y asignado como activo."

class ListCommand(Command):
    def execute(self, args, context):
        files = context.files.list_files()
        if not files: return "No hay archivos abiertos."
        return "Archivos abiertos:\n" + "\n".join([f" - {f} {'(Activo)' if context.active_file and context.active_file.name == f else ''}" for f in files])

class SwitchCommand(Command):
    def execute(self, args, context):
        if not args: return "Error: Especifique nombre de archivo."
        file_obj = context.files.find(args[0])
        if file_obj:
            context.active_file = file_obj
            return f"Cambiado al archivo '{args[0]}'."
        return "Archivo no encontrado."

class DeleteCommand(Command):
    def execute(self, args, context):
        if not args: return "Error: Especifique nombre de archivo."
        success = context.files.remove(args[0])
        if success:
            if context.active_file and context.active_file.name == args[0]:
                context.active_file = None
            return f"Archivo '{args[0]}' eliminado."
        return "Archivo no encontrado."

class ConfigCommand(Command):
    def execute(self, args, context):
        if not args: return "Error: Especifique ruta del JSON."
        success = context.config.load_config(args[0])
        return "Configuración cargada exitosamente." if success else "Error cargando archivo de configuración."

class CheckCommand(Command):
    def execute(self, args, context):
        if not context.active_file: return "No hay archivo activo."
        return SyntaxChecker.check(context.active_file.content)

class UndoCommand(Command):
    def execute(self, args, context):
        if not context.active_file: return "No hay archivo activo."
        return "Deshecho exitosamente." if context.active_file.undo() else "Nada que deshacer."

class RedoCommand(Command):
    def execute(self, args, context):
        if not context.active_file: return "No hay archivo activo."
        return "Rehecho exitosamente." if context.active_file.redo() else "Nada que rehacer."

class SortCommand(Command):
    def execute(self, args, context):
        if len(args) < 2: return "Uso: sort <line/severity> <mergesort/shellsort>"
        criterio, algoritmo = args[0], args[1]
        
        if algoritmo == "mergesort":
            Sorter.mergesort(context.diagnostics, criterio)
        elif algoritmo == "shellsort":
            Sorter.shellsort(context.diagnostics, criterio)
        else:
            return "Algoritmo no soportado."
        
        return "Diagnósticos ordenados:\n" + "\n".join([str(d) for d in context.diagnostics])

class QueueStatusCommand(Command):
    def execute(self, args, context):
        return f"Estado de la cola: {context.ai_manager.queue.size} peticiones pendientes."

class AnalyzeCommand(Command):
    def execute(self, args, context):
        if not context.active_file: return "No hay archivo activo."
        context.ai_manager.queue_request(context.active_file.content)
        return "Petición encolada. " + str(context.ai_manager.process_queue())

class CLIController:
    def __init__(self):
        self.context = IDEContext()
        self.commands = {
            "new": NewCommand(), "list": ListCommand(), "switch": SwitchCommand(),
            "delete": DeleteCommand(), "config": ConfigCommand(), "check": CheckCommand(),
            "undo": UndoCommand(), "redo": RedoCommand(), "sort": SortCommand(),
            "queue-status": QueueStatusCommand(), "analyze": AnalyzeCommand()
        }

    def run(self):
        print("Synthetix Studio CLI. Escriba 'exit' para salir.")
        while True:
            try:
                user_input = input(">> ").strip().split()
                if not user_input: continue
                cmd = user_input[0].lower()
                args = user_input[1:]
                
                if cmd == 'exit': break
                
                if cmd in self.commands:
                    print(self.commands[cmd].execute(args, self.context))
                else:
                    print("Comando no reconocido. Comandos sin menú permitidos.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    cli = CLIController()
    cli.run()