class ColaMisiones:
    def __init__(self):
        self.misiones = [] # Lista para almacenar las misiones

    def enqueue(self, mission):
        # Añade una misión al final de la cola.
        self.misiones.append(mission)

    def dequeue(self):
        # Elimina la primera misión de la cola.
        if self.is_empty():
            return None
        return self.misiones.pop(0)

    def first(self):
        # Ve la primera mision sin remover
        if self.is_empty():
            return None
        return self.misiones[0]
    
    def is_empty(self):
        # Verifica si la cola esta vacia
        return len(self.misiones) == 0

    def size(self):
        # Obtiene la cantidad de misiones
        return len(self.misiones)