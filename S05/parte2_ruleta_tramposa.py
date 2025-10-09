"""
================================================================================
RULETA FRANCESA CUÁNTICA - PARTE 2: JUEGO CON TRAMPAS (OPTIMIZADO)
================================================================================

Asignatura: Computación Cuántica y Natural
Actividad: S05 - La Ruleta Francesa
Alumno: Víctor Vega Sobral

DESCRIPCIÓN:
------------
Implementación de la Ruleta Francesa Cuántica donde el croupier hace trampas.
Este archivo extiende la funcionalidad de la Parte 1, importando las clases
base (Jugador, Croupier, JuegoRuleta) y el diccionario de colores desde el
archivo parte1_ruleta_justa.py. Define dos nuevas clases:

- CroupierTramposo: Hereda de Croupier y añade la capacidad de hacer trampas
  espiando a un jugador aleatorio y modificando un qubit del resultado si 
  ese jugador ganaría.
  
- JuegoRuletaTramposa: Hereda de JuegoRuleta y gestiona el juego con el
  croupier tramposo, registrando estadísticas sobre los intentos de trampa
  y su tasa de éxito.

La trampa no siempre funciona debido a la incertidumbre cuántica, lo que
demuestra cómo la aleatoriedad cuántica persiste incluso al intentar manipularla.

ESTRUCTURA:
-----------
- Importa: numeros_colores, Jugador, Croupier, JuegoRuleta de parte1
- Define: CroupierTramposo (hereda de Croupier)
- Define: JuegoRuletaTramposa (hereda de JuegoRuleta)

MECÁNICA DE LA TRAMPA:
-----------------------
1. El croupier genera un número normalmente (con 6 qubits)
2. Elige aleatoriamente a un jugador para espiar
3. Verifica si ese jugador ganaría con el número actual
4. Si el jugador ganaría, el croupier hace trampa:
   - Cambia aleatoriamente UNO de sus 6 qubits
   - Recalcula el número resultante
   - Si el nuevo número es válido (0-36), lo usa
   - Si es inválido (>36), mantiene el original (trampa fallida)

REQUISITOS:
-----------
pip install pyquil==3.2.1

IMPORTANTE:
-----------
Este archivo requiere que parte1_ruleta_justa.py esté en el mismo directorio.
================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================
from pyquil import Program, get_qc
from pyquil.gates import H, MEASURE
import random

# Importar clases base y configuración de la Parte 1
from parte1_ruleta_justa import numeros_colores, Jugador, Croupier, JuegoRuleta


# ============================================================================
# CLASE CROUPIER TRAMPOSO (hereda de Croupier)
# ============================================================================
class CroupierTramposo(Croupier):
    """
    Croupier que hace trampas espiando a los jugadores.

    HERENCIA:
    ---------
    Hereda de Croupier y añade:
    - Capacidad de generar números guardando el estado de bits
    - Capacidad de cambiar un qubit específico
    - Lógica para espiar y decidir cuándo hacer trampa

    ATRIBUTOS ADICIONALES:
    ----------------------
    - numero_original: Guarda el número y bits originales
    - numero_trampa: Guarda el número modificado (si hay trampa)
    - hizo_trampa: Indica si se hizo trampa en la ronda actual
    - jugador_espiado: Guarda qué jugador fue espiado (para verificar éxito)

    ESTRATEGIA DE TRAMPA:
    ---------------------
    1. Generar número normalmente
    2. Espiar a un jugador aleatorio
    3. Si ese jugador ganaría:
       a. Cambiar aleatoriamente uno de los 6 qubits
       b. Recalcular el número
       c. Validar si está en rango (0-36)
       d. Usar el nuevo número o mantener el original
    """

    def __init__(self, monedas_iniciales=20):
        """
        Inicializa el croupier tramposo.
        Llama al constructor de la clase padre (Croupier).
        """
        super().__init__(monedas_iniciales)
        self.numero_original = None
        self.numero_trampa = None
        self.hizo_trampa = False
        self.jugador_espiado = None  # NUEVO: guardar qué jugador fue espiado

    def girar_ruleta_con_trampa(self, jugadores, apuestas):
        """
        Gira la ruleta con capacidad de hacer trampas.

        PROCESO DETALLADO:
        ------------------
        1. Generar número cuántico con estado de bits guardado
        2. Elegir un jugador aleatorio para espiar
        3. Verificar si ese jugador ganaría con el número actual
        4. Si ganaría, intentar hacer trampa:
           - Elegir aleatoriamente uno de los 6 qubits
           - Invertir su estado (0→1 o 1→0)
           - Recalcular el número resultante
           - Validar si es válido (0-36)
        5. Retornar el número final (original o modificado)

        Args:
            jugadores: Lista de jugadores
            apuestas: Diccionario {nombre_jugador: apuesta}

        Returns:
            int: Número final de la ruleta (0-36)
        """
        # PASO 1: Generar número original con estado de bits
        self.numero_original = self._generar_numero_cuantico_con_estado(6)
        while self.numero_original['numero'] > 36:
            self.numero_original = self._generar_numero_cuantico_con_estado(6)

        # PASO 2: Elegir un jugador aleatorio para espiar
        jugador_espiado = random.choice(jugadores)
        self.jugador_espiado = jugador_espiado  # GUARDAR para verificar después
        apuesta_espiada = apuestas[jugador_espiado.nombre]

        # PASO 3: Verificar si el jugador ganaría con el número actual
        ganaria = self._verificar_apuesta_rapida(apuesta_espiada,
                                                 self.numero_original['numero'])

        # PASO 4: Si el jugador ganaría, intentar hacer trampa
        if ganaria:
            print(f"  [TRAMPA] Croupier espía a {jugador_espiado.nombre}")
            print(f"  [TRAMPA] Apuesta espiada: {apuesta_espiada}")
            print(
                f"  [TRAMPA] Número original: {self.numero_original['numero']}")

            # Cambiar aleatoriamente uno de los 6 qubits (0-5)
            qubit_a_cambiar = random.randint(0, 5)

            # Invertir el bit: 0→1 o 1→0
            self.numero_original['bits'][qubit_a_cambiar] = \
                1 - self.numero_original['bits'][qubit_a_cambiar]

            # Recalcular el número con el bit modificado
            numero_nuevo = sum([self.numero_original['bits'][i] * (2 ** i)
                               for i in range(6)])

            # VALIDACIÓN: Solo usar el nuevo número si está en rango válido
            if numero_nuevo <= 36:
                # Trampa exitosa
                print(f"  [TRAMPA] Cambiando qubit {qubit_a_cambiar}: " +
                      f"{self.numero_original['numero']} → {numero_nuevo}")
                self.numero_trampa = numero_nuevo
                self.hizo_trampa = True
                return numero_nuevo
            else:
                # Trampa fallida: el nuevo número está fuera de rango
                print(f"  [TRAMPA] Cambio inválido: qubit {qubit_a_cambiar} " +
                      f"genera {numero_nuevo} (>36)")
                print(f"  [TRAMPA] Manteniendo número original")
                self.hizo_trampa = False
                return self.numero_original['numero']
        else:
            # El jugador no ganaría, no hay necesidad de hacer trampa
            self.hizo_trampa = False
            self.jugador_espiado = None  # No hubo espionaje efectivo
            return self.numero_original['numero']

    def _generar_numero_cuantico_con_estado(self, n_qubits):
        """
        Genera un número aleatorio y GUARDA el estado de los bits.

        DIFERENCIA CON MÉTODO PADRE:
        ----------------------------
        El método normal solo retorna el número.
        Este método retorna un diccionario con:
        - 'numero': el valor decimal
        - 'bits': lista con el valor de cada bit

        Esto permite modificar bits individuales después.

        Args:
            n_qubits: Número de qubits a usar

        Returns:
            dict: {
                'numero': int (0 a 2^n_qubits - 1),
                'bits': list[int] (estado de cada qubit)
            }

        Ejemplo:
            Para el número 25 con 6 qubits:
            25 en binario = 011001
            bits = [1, 0, 0, 1, 1, 0]  (little-endian)
            numero = 1×2^0 + 0×2^1 + 0×2^2 + 1×2^3 + 1×2^4 + 0×2^5 = 25
        """
        programa = Program()

        # Declarar memoria clásica (PyQuil 3.x)
        ro = programa.declare('ro', 'BIT', n_qubits)

        # Crear superposición en todos los qubits
        for i in range(n_qubits):
            programa += H(i)

        # Medir todos los qubits (PyQuil 3.x)
        for i in range(n_qubits):
            programa += MEASURE(i, ro[i])

        programa.wrap_in_numshots_loop(1)

        resultado = self.qc.run(programa)

        # Acceso a resultados en PyQuil 3.x
        resultado_bits = resultado.readout_data['ro']

        # Guardar el estado de cada bit
        bits = [resultado_bits[0][i] for i in range(n_qubits)]

        # Calcular el número decimal
        numero = sum([bits[i] * (2 ** i) for i in range(n_qubits)])

        return {"numero": numero, "bits": bits}

    def _verificar_apuesta_rapida(self, apuesta, numero):
        """
        Verifica rápidamente si una apuesta ganaría con un número dado.

        Este método es necesario para que el croupier pueda decidir
        si hacer trampa ANTES de mostrar el resultado.

        Args:
            apuesta: dict {"tipo": str, "valor": int/str}
            numero: int (0-36)

        Returns:
            bool: True si la apuesta ganaría, False si no
        """
        if apuesta["tipo"] == "numero":
            return apuesta["valor"] == numero

        elif apuesta["tipo"] == "paridad":
            if numero == 0:
                return False
            if apuesta["valor"] == "par":
                return numero % 2 == 0
            else:
                return numero % 2 == 1

        elif apuesta["tipo"] == "rango":
            if numero == 0:
                return False
            if apuesta["valor"] == "manque":
                return 1 <= numero <= 18
            else:
                return 19 <= numero <= 36

        elif apuesta["tipo"] == "color":
            color_ganador = numeros_colores[numero]
            if color_ganador == "verde":
                return False
            return apuesta["valor"] == color_ganador

        return False


# ============================================================================
# CLASE JUEGO RULETA TRAMPOSA (hereda de JuegoRuleta)
# ============================================================================
class JuegoRuletaTramposa(JuegoRuleta):
    """
    Juego de ruleta donde el croupier puede hacer trampas.

    HERENCIA:
    ---------
    Hereda de JuegoRuleta y modifica:
    - jugar_ronda(): Usa girar_ruleta_con_trampa() en lugar de girar_ruleta()
    - jugar(): Añade estadísticas de trampas al final

    ATRIBUTOS ADICIONALES:
    ----------------------
    - total_trampas: Contador de intentos de trampa
    - trampas_exitosas: Contador de trampas donde el jugador ESPIADO perdió

    ESTADÍSTICAS:
    -------------
    Al final del juego se muestra:
    - Total de veces que el croupier intentó hacer trampa
    - Cuántas trampas fueron exitosas (el jugador ESPIADO específicamente perdió)
    - Tasa de éxito de las trampas

    NOTA IMPORTANTE SOBRE "TRAMPA EXITOSA":
    ----------------------------------------
    Una trampa se considera exitosa SOLO si:
    1. El croupier hizo trampa (cambió un qubit)
    2. El jugador ESPIADO específicamente perdió su apuesta

    La trampa puede fallar por tres razones:
    1. El nuevo número es >36 (inválido, se mantiene el original)
    2. El nuevo número sigue beneficiando al jugador espiado
    3. El cambio de un qubit aleatorio tiene consecuencias impredecibles

    Esto refleja la incertidumbre cuántica inherente al sistema.
    """

    def __init__(self, jugador1, jugador2, croupier_tramposo):
        """
        Inicializa el juego con trampas.

        Args:
            jugador1: Instancia de Jugador
            jugador2: Instancia de Jugador
            croupier_tramposo: Instancia de CroupierTramposo
        """
        super().__init__(jugador1, jugador2, croupier_tramposo)
        self.total_trampas = 0
        self.trampas_exitosas = 0

    def jugar_ronda(self, numero_ronda):
        """
        Ejecuta una ronda donde el croupier puede hacer trampa.

        DIFERENCIAS CON LA CLASE PADRE:
        --------------------------------
        1. Usa girar_ruleta_con_trampa() en lugar de girar_ruleta()
        2. Registra si se hizo trampa
        3. Cuenta las trampas exitosas (cuando el jugador espiado pierde)
        """
        print(f"\n{'='*60}")
        print(f"RONDA {numero_ronda}")
        print(f"{'='*60}")

        # Cada jugador genera su apuesta
        apuestas = {}
        for jugador in self.jugadores:
            apuesta = jugador.generar_apuesta()
            apuestas[jugador.nombre] = apuesta
            print(
                f"{jugador.nombre} apuesta: {apuesta['tipo']} = {apuesta['valor']}")

        # El croupier gira la ruleta CON POSIBILIDAD DE TRAMPA
        numero_ganador = self.croupier.girar_ruleta_con_trampa(self.jugadores,
                                                               apuestas)
        color_ganador = numeros_colores[numero_ganador]
        print(f"\n🎰 Resultado FINAL: {numero_ganador} ({color_ganador})")

        # Registrar si se intentó hacer trampa
        if self.croupier.hizo_trampa:
            self.total_trampas += 1

        # Verificar apuestas y actualizar monedas
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

                # CORRECCIÓN: Solo cuenta como trampa exitosa si el jugador ESPIADO perdió
                if self.croupier.hizo_trampa and jugador == self.croupier.jugador_espiado:
                    self.trampas_exitosas += 1

        print(f"\nCroupier - Monedas: {self.croupier.monedas}")

    def jugar(self, num_rondas=10):
        """
        Ejecuta el juego completo con trampas y muestra estadísticas.

        DIFERENCIAS CON LA CLASE PADRE:
        --------------------------------
        - Título indica que hay trampas
        - Al final muestra estadísticas de trampas
        """
        print("="*60)
        print("RULETA FRANCESA CUÁNTICA - CON TRAMPAS 🎭")
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

        # ESTADÍSTICAS DE TRAMPAS
        print(f"\n📊 ESTADÍSTICAS DE TRAMPAS:")
        print(f"  Total de intentos de trampa: {self.total_trampas}")
        print(
            f"  Trampas exitosas (jugador espiado perdió): {self.trampas_exitosas}")
        if self.total_trampas > 0:
            tasa_exito = (self.trampas_exitosas / self.total_trampas) * 100
            print(f"  Tasa de éxito: {tasa_exito:.1f}%")
            print(
                f"  Trampas fallidas: {self.total_trampas - self.trampas_exitosas}")

        # ANÁLISIS
        print(f"\n💡 ANÁLISIS:")
        if self.total_trampas == 0:
            print("  No hubo oportunidades para hacer trampa.")
        else:
            print(
                f"  El croupier intentó hacer trampa {self.total_trampas} veces.")
            if self.trampas_exitosas < self.total_trampas:
                print(f"  Algunas trampas fallaron debido a la incertidumbre cuántica:")
                print(f"  - El nuevo número podría ser >36 (inválido)")
                print(
                    f"  - El nuevo número podría seguir beneficiando al jugador espiado")
                print(
                    f"  - Cambiar un solo qubit aleatoriamente no garantiza perjudicar al jugador")
            if self.trampas_exitosas == 0 and self.total_trampas > 0:
                print(
                    f"  ¡Ninguna trampa fue exitosa! La incertidumbre cuántica protegió a los jugadores.")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================
if __name__ == "__main__":
    """
    Punto de entrada del programa.

    Crea los participantes con el croupier tramposo y ejecuta el juego.
    """
    print("\n" + "="*60)
    print("INICIANDO SIMULACIÓN DE RULETA FRANCESA CUÁNTICA CON TRAMPAS")
    print("="*60)

    # Crear jugadores con 10 monedas cada uno
    jugador1 = Jugador("Alice", 10)
    jugador2 = Jugador("Bob", 10)

    # Crear croupier TRAMPOSO con 20 monedas
    croupier_tramposo = CroupierTramposo(20)

    # Crear e iniciar el juego CON TRAMPAS
    juego = JuegoRuletaTramposa(jugador1, jugador2, croupier_tramposo)
    juego.jugar(num_rondas=10)

    print("\n" + "="*60)
    print("SIMULACIÓN COMPLETADA")
    print("="*60)
    print("\nOBSERVACIÓN:")
    print("Las trampas no siempre funcionan debido a la incertidumbre cuántica.")
    print("Cambiar un solo qubit puede generar números inválidos o seguir")
    print("beneficiando al jugador espiado, demostrando la naturaleza")
    print("probabilística de la mecánica cuántica.")
    print("\nUna trampa se considera 'exitosa' SOLO cuando el jugador ESPIADO")
    print("pierde su apuesta. Esto demuestra que incluso haciendo trampas,")
    print("la incertidumbre cuántica puede proteger a los jugadores.")
