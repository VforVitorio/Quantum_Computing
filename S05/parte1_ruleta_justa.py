"""
================================================================================
RULETA FRANCESA CUÁNTICA - PARTE 1: JUEGO JUSTO
================================================================================

Asignatura: Computación Cuántica y Natural
Actividad: S05 - La Ruleta Francesa
Profesor: Yago González Rozas

DESCRIPCIÓN:
------------
Implementación de un juego de ruleta francesa usando circuitos cuánticos
para generar aleatoriedad verdadera. En esta versión, todos los participantes
son independientes y el juego es completamente justo.

REGLAS:
-------
- La ruleta tiene 37 números (0-36)
- 2 jugadores empiezan con 10 monedas cada uno
- El croupier empieza con 20 monedas
- Se gana/pierde 1 moneda por ronda

TIPOS DE APUESTAS:
------------------
1. Número específico (0-36)
2. Par o Impar
3. Manque (1-18) o Passe (19-36)
4. Rojo o Negro

ASPECTOS CUÁNTICOS:
-------------------
- Se usan 6 qubits para representar números 0-36 (2^6 = 64 posibles)
- Cada circuito cuántico es independiente
- Se usa la puerta Hadamard (H) para crear superposición
- La medición colapsa el estado a un valor definido

REQUISITOS:
-----------
pip install pyquil==3.2.1
================================================================================
"""

from pyquil import Program, get_qc
from pyquil.gates import H, MEASURE


# ============================================================================
# CONFIGURACIÓN DE COLORES
# ============================================================================
# En la ruleta francesa:
# - El 0 es verde (ni rojo ni negro)
# - Los números pares son negros
# - Los números impares son rojos

numeros_colores = {}
numeros_colores[0] = "verde"

for i in range(1, 37):
    if i % 2 == 0:
        numeros_colores[i] = "negro"
    else:
        numeros_colores[i] = "rojo"


# ============================================================================
# CLASE JUGADOR
# ============================================================================
class Jugador:
    """
    Representa un jugador de la ruleta.

    Cada jugador:
    - Genera apuestas aleatorias usando circuitos cuánticos
    - Mantiene su propio simulador cuántico (independiente)
    - Gestiona su cantidad de monedas

    Estrategia de qubits:
    - 2 qubits para elegir tipo de apuesta (4 tipos posibles: 2^2 = 4)
    - 6 qubits para números específicos (0-63, filtrados a 0-36)
    - 1 qubit para valores binarios (par/impar, rojo/negro, manque/passe)
    """

    def __init__(self, nombre, monedas_iniciales=10):
        """
        Inicializa un jugador.

        Args:
            nombre: Nombre del jugador
            monedas_iniciales: Cantidad inicial de monedas (default: 10)
        """
        self.nombre = nombre
        self.monedas = monedas_iniciales
        self.qc = get_qc('9q-square-qvm')  # Simulador cuántico independiente

    def generar_apuesta(self):
        """
        Genera una apuesta aleatoria usando circuitos cuánticos.

        Proceso:
        1. Usa 2 qubits en superposición para elegir tipo (0-3)
        2. Según el tipo, genera el valor específico de la apuesta

        Returns:
            dict: {"tipo": str, "valor": int/str}
                tipo: "numero", "paridad", "rango", o "color"
                valor: el valor específico de la apuesta
        """
        # PASO 1: Elegir tipo de apuesta con 2 qubits
        # Creamos superposición en ambos qubits
        programa_tipo = Program()

        # Declarar memoria clásica para 2 bits (PyQuil 3.x)
        ro = programa_tipo.declare('ro', 'BIT', 2)

        programa_tipo += H(0)  # Qubit 0 en superposición: |0⟩ + |1⟩
        programa_tipo += H(1)  # Qubit 1 en superposición: |0⟩ + |1⟩

        # Medir qubits en memoria clásica (PyQuil 3.x)
        programa_tipo += MEASURE(0, ro[0])
        programa_tipo += MEASURE(1, ro[1])

        # Envolver en loop de 1 shot AL FINAL (PyQuil 3.x)
        programa_tipo.wrap_in_numshots_loop(1)

        resultado_tipo = self.qc.run(programa_tipo)

        # Acceso a resultados en PyQuil 3.x
        bits = resultado_tipo.readout_data['ro']
        tipo_apuesta = bits[0][0] + 2 * bits[0][1]

        # PASO 2: Generar valor según el tipo elegido

        if tipo_apuesta == 0:  # NÚMERO ESPECÍFICO (0-36)
            # Usamos 6 qubits para generar números de 0 a 63
            numero = self._generar_numero_cuantico(6)
            # Si el número es mayor que 36, repetimos hasta obtener uno válido
            while numero > 36:
                numero = self._generar_numero_cuantico(6)
            return {"tipo": "numero", "valor": numero}

        elif tipo_apuesta == 1:  # PAR o IMPAR
            # Un solo qubit: |0⟩ = par, |1⟩ = impar
            programa = Program()
            ro = programa.declare('ro', 'BIT', 1)
            programa += H(0)
            programa += MEASURE(0, ro[0])
            programa.wrap_in_numshots_loop(1)
            resultado = self.qc.run(programa)
            bits = resultado.readout_data['ro']
            valor = "par" if bits[0][0] == 0 else "impar"
            return {"tipo": "paridad", "valor": valor}

        elif tipo_apuesta == 2:  # MANQUE (1-18) o PASSE (19-36)
            # Un solo qubit: |0⟩ = manque, |1⟩ = passe
            programa = Program()
            ro = programa.declare('ro', 'BIT', 1)
            programa += H(0)
            programa += MEASURE(0, ro[0])
            programa.wrap_in_numshots_loop(1)
            resultado = self.qc.run(programa)
            bits = resultado.readout_data['ro']
            valor = "manque" if bits[0][0] == 0 else "passe"
            return {"tipo": "rango", "valor": valor}

        else:  # ROJO o NEGRO (tipo_apuesta == 3)
            # Un solo qubit: |0⟩ = rojo, |1⟩ = negro
            programa = Program()
            ro = programa.declare('ro', 'BIT', 1)
            programa += H(0)
            programa += MEASURE(0, ro[0])
            programa.wrap_in_numshots_loop(1)
            resultado = self.qc.run(programa)
            bits = resultado.readout_data['ro']
            valor = "rojo" if bits[0][0] == 0 else "negro"
            return {"tipo": "color", "valor": valor}

    def _generar_numero_cuantico(self, n_qubits):
        """
        Genera un número aleatorio usando n qubits.

        Proceso cuántico:
        1. Aplica Hadamard a cada qubit (superposición)
        2. Mide todos los qubits
        3. Convierte la cadena de bits a número decimal

        Args:
            n_qubits: Número de qubits a usar (rango: 2^n)

        Returns:
            int: Número aleatorio entre 0 y (2^n_qubits - 1)
        """
        programa = Program()

        # Declarar memoria clásica para n_qubits bits (PyQuil 3.x)
        ro = programa.declare('ro', 'BIT', n_qubits)

        # Aplicar Hadamard a todos los qubits
        for i in range(n_qubits):
            programa += H(i)

        # Medir todos los qubits en memoria clásica (PyQuil 3.x)
        for i in range(n_qubits):
            programa += MEASURE(i, ro[i])

        # Envolver en loop de 1 shot AL FINAL (PyQuil 3.x)
        programa.wrap_in_numshots_loop(1)

        resultado = self.qc.run(programa)

        # Acceso a resultados en PyQuil 3.x
        bits = resultado.readout_data['ro']

        # Convertir bits a número decimal
        # Ejemplo: [1,0,1] = 1×2^0 + 0×2^1 + 1×2^2 = 1 + 0 + 4 = 5
        numero = sum([bits[0][i] * (2 ** i) for i in range(n_qubits)])
        return numero

    def ganar(self, cantidad=1):
        """Incrementa las monedas del jugador"""
        self.monedas += cantidad

    def perder(self, cantidad=1):
        """Decrementa las monedas del jugador"""
        self.monedas -= cantidad


# ============================================================================
# CLASE CROUPIER
# ============================================================================
class Croupier:
    """
    Representa al croupier (encargado de la ruleta).

    El croupier:
    - Genera el número ganador usando un circuito cuántico
    - Es independiente de los jugadores
    - Gestiona sus propias monedas (gana cuando los jugadores pierden)

    Estrategia:
    - Usa 6 qubits para generar números 0-63
    - Filtra resultados para obtener solo números válidos (0-36)
    """

    def __init__(self, monedas_iniciales=20):
        """
        Inicializa el croupier.

        Args:
            monedas_iniciales: Cantidad inicial de monedas (default: 20)
        """
        self.monedas = monedas_iniciales
        self.qc = get_qc('9q-square-qvm')  # Simulador cuántico independiente

    def girar_ruleta(self):
        """
        Gira la ruleta y obtiene un número aleatorio (0-36).

        Proceso:
        1. Genera un número con 6 qubits (rango 0-63)
        2. Si el número > 36, repite el proceso
        3. Retorna un número válido (0-36)

        ¿Por qué 6 qubits?
        - 5 qubits: 2^5 = 32 (insuficiente para 37 números)
        - 6 qubits: 2^6 = 64 (suficiente, filtramos a 0-36)

        Returns:
            int: Número ganador entre 0 y 36
        """
        numero = self._generar_numero_cuantico(6)

        # Repetir hasta obtener un número válido (0-36)
        while numero > 36:
            numero = self._generar_numero_cuantico(6)

        return numero

    def _generar_numero_cuantico(self, n_qubits):
        """
        Genera un número aleatorio usando n qubits.

        (Mismo proceso que en la clase Jugador)

        Args:
            n_qubits: Número de qubits a usar

        Returns:
            int: Número aleatorio entre 0 y (2^n_qubits - 1)
        """
        programa = Program()

        # Declarar memoria clásica para n_qubits bits (PyQuil 3.x)
        ro = programa.declare('ro', 'BIT', n_qubits)

        for i in range(n_qubits):
            programa += H(i)

        # Medir todos los qubits (PyQuil 3.x)
        for i in range(n_qubits):
            programa += MEASURE(i, ro[i])

        programa.wrap_in_numshots_loop(1)

        resultado = self.qc.run(programa)

        # Acceso a resultados en PyQuil 3.x
        bits = resultado.readout_data['ro']
        numero = sum([bits[0][i] * (2 ** i) for i in range(n_qubits)])
        return numero

    def ganar(self, cantidad=1):
        """Incrementa las monedas del croupier"""
        self.monedas += cantidad

    def perder(self, cantidad=1):
        """Decrementa las monedas del croupier"""
        self.monedas -= cantidad


# ============================================================================
# CLASE JUEGO RULETA
# ============================================================================
class JuegoRuleta:
    """
    Maneja la lógica completa del juego de ruleta.

    Responsabilidades:
    - Coordinar las rondas del juego
    - Recoger las apuestas de los jugadores
    - Obtener el número ganador del croupier
    - Verificar qué apuestas ganaron
    - Actualizar las monedas de todos los participantes
    - Mostrar los resultados

    Reglas de verificación:
    - Número: debe coincidir exactamente
    - Paridad: el 0 no cuenta como par ni impar
    - Rango: el 0 no está en ningún rango
    - Color: el 0 (verde) no es ni rojo ni negro
    """

    def __init__(self, jugador1, jugador2, croupier):
        """
        Inicializa el juego.

        Args:
            jugador1: Primera instancia de Jugador
            jugador2: Segunda instancia de Jugador
            croupier: Instancia de Croupier
        """
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.croupier = croupier
        self.jugadores = [jugador1, jugador2]

    def verificar_apuesta(self, apuesta, numero_ganador):
        """
        Verifica si una apuesta ganó según el número de la ruleta.

        Args:
            apuesta: dict con {"tipo": str, "valor": int/str}
            numero_ganador: int entre 0 y 36

        Returns:
            bool: True si la apuesta ganó, False si perdió
        """
        if apuesta["tipo"] == "numero":
            # Coincidencia exacta del número
            return apuesta["valor"] == numero_ganador

        elif apuesta["tipo"] == "paridad":
            # El 0 no cuenta como par ni impar
            if numero_ganador == 0:
                return False

            if apuesta["valor"] == "par":
                return numero_ganador % 2 == 0
            else:  # impar
                return numero_ganador % 2 == 1

        elif apuesta["tipo"] == "rango":
            # El 0 no está en ningún rango
            if numero_ganador == 0:
                return False

            if apuesta["valor"] == "manque":
                return 1 <= numero_ganador <= 18
            else:  # passe
                return 19 <= numero_ganador <= 36

        elif apuesta["tipo"] == "color":
            color_ganador = numeros_colores[numero_ganador]

            # El 0 (verde) no es ni rojo ni negro
            if color_ganador == "verde":
                return False

            return apuesta["valor"] == color_ganador

        return False

    def jugar_ronda(self, numero_ronda):
        """
        Ejecuta una ronda completa del juego.

        Proceso:
        1. Cada jugador genera su apuesta (independientemente)
        2. El croupier gira la ruleta (independientemente)
        3. Se verifican las apuestas contra el resultado
        4. Se actualizan las monedas:
           - Jugador gana: +1 moneda (croupier -1)
           - Jugador pierde: -1 moneda (croupier +1)

        Args:
            numero_ronda: Número de la ronda actual
        """
        print(f"\n{'='*60}")
        print(f"RONDA {numero_ronda}")
        print(f"{'='*60}")

        # PASO 1: Cada jugador genera su apuesta
        apuestas = {}
        for jugador in self.jugadores:
            apuesta = jugador.generar_apuesta()
            apuestas[jugador.nombre] = apuesta
            print(
                f"{jugador.nombre} apuesta: {apuesta['tipo']} = {apuesta['valor']}")

        # PASO 2: El croupier gira la ruleta
        numero_ganador = self.croupier.girar_ruleta()
        color_ganador = numeros_colores[numero_ganador]
        print(f"\n🎰 Resultado: {numero_ganador} ({color_ganador})")

        # PASO 3: Verificar apuestas y actualizar monedas
        print(f"\nResultados:")
        for jugador in self.jugadores:
            apuesta = apuestas[jugador.nombre]
            gano = self.verificar_apuesta(apuesta, numero_ganador)

            if gano:
                jugador.ganar(1)
                self.croupier.perder(1)
                print(f"  ✓ {jugador.nombre} GANA - Monedas: {jugador.monedas}")
            else:
                jugador.perder(1)
                self.croupier.ganar(1)
                print(
                    f"  ✗ {jugador.nombre} PIERDE - Monedas: {jugador.monedas}")

        print(f"\nCroupier - Monedas: {self.croupier.monedas}")

    def jugar(self, num_rondas=10):
        """
        Ejecuta el juego completo con el número especificado de rondas.

        Args:
            num_rondas: Cantidad de rondas a jugar (default: 10)
        """
        print("="*60)
        print("RULETA FRANCESA CUÁNTICA - JUEGO JUSTO")
        print("="*60)
        print(f"\nMonedas iniciales:")
        print(f"  {self.jugador1.nombre}: {self.jugador1.monedas}")
        print(f"  {self.jugador2.nombre}: {self.jugador2.monedas}")
        print(f"  Croupier: {self.croupier.monedas}")

        # Ejecutar todas las rondas
        for i in range(1, num_rondas + 1):
            self.jugar_ronda(i)

        # Mostrar resultados finales
        print(f"\n{'='*60}")
        print("RESULTADOS FINALES")
        print(f"{'='*60}")
        print(f"{self.jugador1.nombre}: {self.jugador1.monedas} monedas")
        print(f"{self.jugador2.nombre}: {self.jugador2.monedas} monedas")
        print(f"Croupier: {self.croupier.monedas} monedas")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================
if __name__ == "__main__":
    """
    Punto de entrada del programa.

    Crea los participantes y ejecuta el juego por 10 rondas.
    """
    print("\n" + "="*60)
    print("INICIANDO SIMULACIÓN DE RULETA FRANCESA CUÁNTICA")
    print("="*60)

    # Crear jugadores con 10 monedas cada uno
    jugador1 = Jugador("Alice", 10)
    jugador2 = Jugador("Bob", 10)

    # Crear croupier con 20 monedas
    croupier = Croupier(20)

    # Crear e iniciar el juego
    juego = JuegoRuleta(jugador1, jugador2, croupier)
    juego.jugar(num_rondas=10)

    print("\n" + "="*60)
    print("SIMULACIÓN COMPLETADA")
    print("="*60)
