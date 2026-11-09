from pasajero import Pasajero


class MiLista:
    """Lista construida a mano sobre un arreglo de tamaño fijo.
    datos     -> [p1, p2, p3, None, None, ...]
    capacidad -> total de cajones     cantidad -> cajones ocupados
    ⛔ Sin append, insert, pop, remove, sort, reverse, copy, len, in, slicing.
    """

    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    def añadir(self, pasajero):                      # ✅ resuelto
        if self.cantidad == self.capacidad:
            print("  ⚠ La lista está llena")
            return False
        if self.buscar(pasajero.numero) != -1:
            print("  ⚠ Ya existe un pasajero con ese número")
            return False
        self.datos[self.cantidad] = pasajero          # primer cajón libre
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):                                 # ✅ resuelto
        if self.cantidad == 0:
            print("  (lista vacía)")
            return
        for i in range(self.cantidad):
            print(f"  [{i}] {self.datos[i]}")

    # ---------------- ✍ IMPLEMENTACIÓN DE OPERACIONES ----------------
    def insertar(self, posicion, pasajero):
        if self.cantidad == self.capacidad:
            print("  ⚠ La lista está llena")
            return False
        if posicion < 0 or posicion > self.cantidad:
            print("  ⚠ Posición fuera de rango")
            return False
        if self.buscar(pasajero.numero) != -1:
            print("  ⚠ Ya existe un pasajero con ese número")
            return False

        # Desplazar a la derecha (de atrás hacia adelante)
        i = self.cantidad
        while i > posicion:
            self.datos[i] = self.datos[i - 1]
            i -= 1

        self.datos[posicion] = pasajero
        self.cantidad += 1
        return True

    def buscar(self, numero):
        for i in range(self.cantidad):
            if self.datos[i].numero == numero:
                return i
        return -1

    def buscar_binaria(self, numero):
        izq = 0
        der = self.cantidad - 1
        while izq <= der:
            medio = (izq + der) // 2
            if self.datos[medio].numero == numero:
                return medio
            elif self.datos[medio].numero < numero:
                izq = medio + 1
            else:
                der = medio - 1
        return -1

    def modificar(self, numero, nuevo_destino, nuevo_asiento):
        pos = self.buscar(numero)
        if pos != -1:
            self.datos[pos].destino = nuevo_destino
            self.datos[pos].asiento = nuevo_asiento
            return True
        return False

    def eliminar_por_posicion(self, posicion):
        if posicion < 0 or posicion >= self.cantidad:
            return None
        eliminado = self.datos[posicion]

        # Desplazar a la izquierda
        for i in range(posicion, self.cantidad - 1):
            self.datos[i] = self.datos[i + 1]

        self.datos[self.cantidad - 1] = None
        self.cantidad -= 1
        return eliminado

    def eliminar_por_valor(self, numero):
        pos = self.buscar(numero)
        if pos != -1:
            self.eliminar_por_posicion(pos)
            return True
        return False

    def ordenar_asc(self):
        # Algoritmo de Burbuja (Ascendente)
        for i in range(self.cantidad - 1):
            for j in range(self.cantidad - 1 - i):
                if self.datos[j].numero > self.datos[j + 1].numero:
                    aux = self.datos[j]
                    self.datos[j] = self.datos[j + 1]
                    self.datos[j + 1] = aux

    def ordenar_desc(self):
        # Algoritmo de Burbuja (Descendente)
        for i in range(self.cantidad - 1):
            for j in range(self.cantidad - 1 - i):
                if self.datos[j].numero < self.datos[j + 1].numero:
                    aux = self.datos[j]
                    self.datos[j] = self.datos[j + 1]
                    self.datos[j + 1] = aux

    def reversar(self):
        izq = 0
        der = self.cantidad - 1
        while izq < der:
            aux = self.datos[izq]
            self.datos[izq] = self.datos[der]
            self.datos[der] = aux
            izq += 1
            der -= 1

    def copiar(self):
        nueva = MiLista(self.capacidad)
        for i in range(self.cantidad):
            nueva.añadir(self.datos[i])
        return nueva

    def longitud(self):
        return self.cantidad