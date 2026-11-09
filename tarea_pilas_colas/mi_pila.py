from pasajero import Pasajero


class MiPila:
    """Pila (LIFO) hecha a mano sobre un arreglo de tamaño fijo.
    datos -> [fondo, ..., TOPE, None, None]
    TOPE  -> datos[cantidad - 1]  (el último que entró: el único que se ve y el único que sale)
    ⛔ Mismas prohibiciones que MiLista: sin append, pop, insert, remove, index,
       sort, reverse, copy, len(), in, slicing ni comprensiones.
    """

    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    def apilar(self, pasajero):                      # ✅ resuelto (= añadir de MiLista)
        if self.cantidad == self.capacidad:
            print("  ⚠ La pila está llena")
            return False
        if self.buscar(pasajero.numero) != -1:        # mejora: no permitir números repetidos
            print("  ⚠ Ya existe un pasajero con ese número")
            return False
        self.datos[self.cantidad] = pasajero          # el nuevo queda encima: es el TOPE
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):                                 # ✅ EJEMPLO: del TOPE al FONDO
        if self.cantidad == 0:
            print("  (pila vacía)")
            return
        for i in range(self.cantidad - 1, -1, -1):    # cantidad-1, ..., 1, 0  (hacia atrás)
            if i == self.cantidad - 1:
                print(f"  [{i}] {self.datos[i]}  ← TOPE")
            elif i == 0:
                print(f"  [{i}] {self.datos[i]}  ← FONDO")
            else:
                print(f"  [{i}] {self.datos[i]}")

    # ------- ✍ IMPLEMENTA (tabla 3) · recorre SIEMPRE del tope al fondo -------
    def desapilar(self):
        if self.cantidad == 0:
            return None
        tope = self.datos[self.cantidad - 1]          # el único que puede salir
        self.datos[self.cantidad - 1] = None           # dejamos ese cajón vacío
        self.cantidad = self.cantidad - 1              # restamos cantidad, no corremos nada
        return tope

    def ver_tope(self):
        if self.cantidad == 0:
            return None
        return self.datos[self.cantidad - 1]           # mira el tope sin sacarlo

    def buscar(self, numero):
        for i in range(self.cantidad - 1, -1, -1):     # del tope al fondo
            if self.datos[i].numero == numero:
                return i
        return -1

    def modificar(self, numero, nuevo_destino, nuevo_asiento):
        pos = self.buscar(numero)                      # buscar ya recorre en el sentido correcto
        if pos == -1:
            return False
        self.datos[pos].destino = nuevo_destino         # nadie cambia de lugar
        self.datos[pos].asiento = nuevo_asiento
        return True

    def eliminar_por_numero(self, numero):
        # ⚠ no se puede sacar del medio: desapilamos hacia una pila auxiliar
        # hasta encontrarlo, lo descartamos y volvemos a apilar los de la auxiliar
        if self.buscar(numero) == -1:
            return False
        auxiliar = MiPila(self.capacidad)
        encontrado = False
        while self.cantidad > 0:
            pasajero = self.desapilar()
            if pasajero.numero == numero:
                encontrado = True
                break                                   # lo descartamos (no se vuelve a apilar)
            auxiliar.apilar(pasajero)
        while auxiliar.cantidad > 0:                    # devolvemos los demás a su lugar
            self.apilar(auxiliar.desapilar())
        return encontrado

    def copiar(self):
        nueva = MiPila(self.capacidad)
        for i in range(self.cantidad):                 # del fondo al tope: el tope sigue siendo el mismo
            nueva.apilar(self.datos[i])
        return nueva

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0
