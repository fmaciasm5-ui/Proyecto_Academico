from datetime import date


class ModeloBase:

    def __init__(self, id_registro):
        self.id = int(id_registro)

    @classmethod
    def desde_diccionario(cls, datos):
        datos = dict(datos)
        id_registro = datos.pop("id")
        return cls(id_registro, **datos)

    def a_diccionario(self):
        return {"id": self.id}

    def etiqueta(self):
        return f"registro {self.id}"

    def __str__(self):
        return f"[{self.id}] {self.etiqueta()}"


class Persona(ModeloBase):

    def __init__(self, id_registro, nombre, apellido, email):
        super().__init__(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["apellido"] = self.apellido
        datos["email"] = self.email
        return datos

    def etiqueta(self):
        return self.nombre_completo()


class Socio(Persona):

    def __init__(self, id_registro, nombre, apellido, email, numero, fecha):
        super().__init__(id_registro, nombre, apellido, email)
        self.numero = numero
        self.fecha = fecha

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["numero"] = self.numero
        datos["fecha"] = self.fecha
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · {self.numero} · {self.fecha or 'sin fecha'}"


class Juego(ModeloBase):

    COPIAS_MAXIMAS = 5
    totaljuegos = 0

    def __init__(self, id_registro, nombre, categoria, copias = 0):
        super().__init__(id_registro)
        self.nombre = nombre
        self.categoria = categoria
        self.copias = int(copias)
        Juego.totaljuegos += 1

    @staticmethod
    def es_fecha_valida(valor):
        try:
            fecha = int(valor)
            return 0 <= fecha <= 31
        except (TypeError, ValueError):
            return False

    def hay_copia_disponible(self):
        return self.copias > 0

    def prestar_copia(self):
        self.copias -= 1

    def devolver_copia(self):
        self.copias += 1

    def copias_bajas(self):
        return self.copias <= 5

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["nombre"] = self.nombre
        datos["categoria"] = self.categoria
        datos["copias"] = self.copias
        return datos

    def etiqueta(self):
        alerta = " ⚠ copias bajas" if self.copias_bajas() else ""
        return f"{self.nombre} · {self.categoria} categoria · copias {self.copias}{alerta}"


class Prestamo(ModeloBase):

    def __init__(self, id_registro, socio_id, juego_id, fecha_prestamo, devuelto=False, fecha_devolucion=""):
        super().__init__(id_registro)
        self.socio_id = int(socio_id)
        self.juego_id = int(juego_id)
        self.fecha_prestamo = fecha_prestamo
        self.devuelto = devuelto 
        self.fecha_devolucion = fecha_devolucion 

    def estado(self):
        if self.devuelto:
            return "Devuelto"

        fecha_inicio = date.fromisoformat(self.fecha_prestamo)
        dias = (date.today() - fecha_inicio).days

        if dias > 7:
            return "Atrasado"

        return "Prestado"

    def devolver(self):
        if self.devuelto:
            return False

        self.devuelto = True
        self.fecha_devolucion = date.today().isoformat()
        return True

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["socio_id"] = self.socio_id
        datos["juego_id"] = self.juego_id
        datos["fecha_prestamo"] = self.fecha_prestamo
        datos["fecha_devolucion"] = self.fecha_devolucion
        datos["devuelto"] = self.devuelto
        return datos

    def etiqueta(self):
        return (f"Socio {self.socio_id} · Juego {self.juego_id} · "
                f"Fecha préstamo: {self.fecha_prestamo} · "
                f"Estado: {self.estado()}")

if __name__ == "__main__":

    prestamo1 = Prestamo(
        1,
        10,
        3,
        "2026-10-10"
    )

    print("=== PRUEBA DE PRÉSTAMO ===")

    print("ID:", prestamo1.id)
    print("Socio:", prestamo1.socio_id)
    print("Juego:", prestamo1.juego_id)
    print("Fecha préstamo:", prestamo1.fecha_prestamo)
    print("Fecha devolución:", prestamo1.fecha_devolucion)
    print("Devuelto:", prestamo1.devuelto)
    print("Estado:", prestamo1.estado())

    print("\n=== DEVOLVER JUEGO ===")

    prestamo1.devolver()

    print("Fecha devolución:", prestamo1.fecha_devolucion)
    print("Devuelto:", prestamo1.devuelto)
    print("Estado:", prestamo1.estado())

    print("\n=== DICCIONARIO ===")

    print(prestamo1.a_diccionario())