class Node:
    """Clase Nodo para una lista doblemente enlazada."""
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class Queue:
    """Clase Queue implementada como lista doblemente enlazada."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, item):
        """Añadir un elemento al final de la cola."""
        new_node = Node(item)
        if not self.tail:  # Cola vacía
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        """Eliminar y devolver el elemento del inicio de la cola."""
        if not self.head:  # Cola vacía
            return None
        removed_node = self.head
        self.head = self.head.next
        if self.head:  # Si hay más elementos
            self.head.prev = None
        else:  # La cola está ahora vacía
            self.tail = None
        self.size -= 1
        return removed_node.data

    def peek(self):
        """Obtener el elemento al inicio de la cola sin eliminarlo."""
        return self.head.data if self.head else None

    def is_empty(self):
        """Verificar si la cola está vacía."""
        return self.size == 0

    def __len__(self):
        """Devolver el tamaño de la cola."""
        return self.size

    def __iter__(self):
        """Hacer la cola iterable."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __repr__(self):
        """Representación legible de la cola."""
        elements = [repr(node.data) for node in self]
        return "Queue([" + ", ".join(elements) + "])"