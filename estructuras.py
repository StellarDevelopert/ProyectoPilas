class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class Stack:
    """Pila para validación de sintaxis y el historial Undo/Redo."""
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node

    def pop(self):
        if not self.top:
            return None
        popped = self.top.data
        self.top = self.top.next
        return popped

    def peek(self):
        return self.top.data if self.top else None

    def is_empty(self):
        return self.top is None

class Queue:
    """Cola FIFO para administrar las solicitudes de análisis hacia la API de IA."""
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return temp.data

    def is_empty(self):
        return self.front is None

class FileLinkedList:
    """Lista Enlazada donde cada nodo representa un archivo abierto en la sesión."""
    def __init__(self):
        self.head = None

    def append(self, file_obj):
        new_node = Node(file_obj)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.prev = last

    def remove(self, filename):
        current = self.head
        while current:
            if current.data.name == filename:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                return True
            current = current.next
        return False

    def find(self, filename):
        current = self.head
        while current:
            if current.data.name == filename:
                return current.data
            current = current.next
        return None

    def list_files(self):
        current = self.head
        files = []
        while current:
            files.append(current.data.name)
            current = current.next
        return files