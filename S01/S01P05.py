"""
PROGRAMA: S01P05.py - Estado de Bell con compuertas Z (cambio de fase)

RESUMEN:
Este programa crea un estado de Bell modificado que incluye compuertas Z (Pauli-Z)
para introducir cambios de fase. Demuestra cómo las compuertas de fase afectan
los estados entrelazados sin cambiar las probabilidades de medición en la base computacional.

FUNCIONAMIENTO:
1. Declara un registro clásico de 2 bits para almacenar mediciones
2. Aplica compuerta Hadamard al qubit 0 (crea superposición)
3. Aplica compuerta X al qubit 1 (inicializa en |1⟩)
4. Aplica compuertas Z a ambos qubits (introduce cambios de fase)
5. Aplica CNOT para crear entrelazamiento
6. Mide ambos qubits y almacena los resultados
7. Repite el experimento 100 veces

SALIDA ESPERADA:
La salida muestra 100 mediciones de los dos qubits entrelazados. Cada línea muestra:
[medición_qubit_0, medición_qubit_1]
Las compuertas Z no afectan las probabilidades de medición en la base |0⟩,|1⟩, por lo que:
- Aproximadamente 50% de las veces: [0, 1]
- Aproximadamente 50% de las veces: [1, 0]
- Mismo comportamiento que S01P04.py (las fases no son observables en esta base)

CONCEPTOS DE FÍSICA CUÁNTICA:

1. COMPUERTA PAULI-Z (Flip de fase):
   - Matriz: Z = [[1,0],[0,-1]]
   - Efectos: Z|0⟩ = |0⟩, Z|1⟩ = -|1⟩
   - No cambia probabilidades en base computacional: |⟨0|Z|ψ⟩|² = |⟨0|ψ⟩|²
   - Rotación de 180° alrededor del eje Z en la esfera de Bloch
   - También llamada "phase flip"

2. FASES GLOBALES VS. FASES RELATIVAS:
   - Fase global: multiplica todo el estado por e^(iφ)
   - Fases globales son físicamente inobservables
   - Fases relativas entre componentes SÍ son observables
   - Z introduce fases relativas, no globales

3. INVARIANZA DE MEDICIÓN EN BASE COMPUTACIONAL:
   - Mediciones en base {|0⟩, |1⟩} solo dependen de |amplitud|²
   - Z preserva |α|² y |β|² para estado α|0⟩ + β|1⟩
   - Fases aparecen en mediciones de otras bases (ej: base {|+⟩, |-⟩})
   - Demostración de separación entre información clásica y cuántica

4. EVOLUCIÓN COMPLETA CON FASES:
   - Inicial: |00⟩
   - H(0): (|00⟩ + |10⟩)/√2
   - X(1): (|01⟩ + |11⟩)/√2
   - Z(0): (|01⟩ - |11⟩)/√2
   - Z(1): (-|01⟩ + |11⟩)/√2 = -(|01⟩ - |11⟩)/√2
   - CNOT(0,1): -(|01⟩ - |10⟩)/√2
   - Fase global -1 es inobservable

5. GRUPO DE PAULI:
   - Cuatro matrices: I, X, Y, Z (Y = iXZ)
   - Generan todas las rotaciones de un qubit
   - Anticommutan: XZ = -ZX
   - Base para corrección de errores cuánticos
   - X: bit flip, Z: phase flip, Y: bit+phase flip

6. INTERFERENCIA CUÁNTICA Y FASES:
   - Fases determinan interferencia constructiva vs. destructiva
   - En este circuito, las fases no afectan la medición final
   - En circuitos con más Hadamards, las fases serían cruciales
   - Ejemplo: algoritmo de Deutsch-Jozsa depende de interferencia de fases

7. EQUIVALENCIA DE CIRCUITOS MÓDULO FASES GLOBALES:
   - Este circuito es equivalente a S01P04 módulo fase global
   - Dos circuitos son equivalentes si difieren solo en fase global
   - Clase de equivalencia importante en diseño de algoritmos cuánticos
"""

# Importa las funciones necesarias para crear y ejecutar circuitos cuánticos
from pyquil import get_qc, Program
# Importa las compuertas: CNOT, H (Hadamard), MEASURE, X (Pauli-X), Z (Pauli-Z)
from pyquil.gates import CNOT, H, MEASURE, X, Z
# Importa Declare para declarar registros de memoria clásica
from pyquil.quilbase import Declare

# Crea el programa cuántico con compuertas de fase Z
prog = Program(
    # Declara un registro clásico llamado "ro" de tipo BIT con 2 posiciones
    Declare("ro", "BIT", 2),
    # Aplica compuerta Hadamard al qubit 0
    # Crea superposición: |0⟩ → (|0⟩ + |1⟩)/√2
    H(0),
    # Aplica compuerta X al qubit 1
    # Inicializa el qubit 1 en estado |1⟩
    X(1),
    # Aplica compuerta Z (Pauli-Z) al qubit 0
    # Introduce un cambio de fase: |0⟩ → |0⟩, |1⟩ → -|1⟩
    # Transforma (|0⟩ + |1⟩)/√2 → (|0⟩ - |1⟩)/√2
    Z(0),
    # Aplica compuerta Z al qubit 1
    # Como el qubit 1 está en |1⟩, se convierte en -|1⟩
    Z(1),
    # Aplica compuerta CNOT con qubit 0 como control y qubit 1 como target
    # Crea entrelazamiento. El estado final incluye las fases introducidas por Z
    CNOT(0, 1),
    # Mide el qubit 0 y almacena el resultado en la posición 0 del registro "ro"
    # Las fases globales no afectan las probabilidades de medición
    MEASURE(0, ("ro", 0)),
    # Mide el qubit 1 y almacena el resultado en la posición 1 del registro "ro"
    # Los resultados seguirán siendo anti-correlacionados como en S01P04
    MEASURE(1, ("ro", 1)),
# Repite el experimento 100 veces para observar la distribución estadística
).wrap_in_numshots_loop(100)

# Obtiene una conexión al simulador cuántico virtual
qvm = get_qc('9q-square-qvm')

# Compila el programa cuántico para optimizarlo para el hardware específico
executable = qvm.compile(prog)
# Ejecuta el programa compilado
result = qvm.run(executable)
# Extrae los datos de medición del registro "ro"
ro_data = result.readout_data.get("ro")

# Itera sobre todas las mediciones e imprime los resultados
for res in ro_data:
    # Imprime cada par de mediciones [qubit_0, qubit_1]
    # Las compuertas Z no cambian las probabilidades, solo las fases relativas
    # Esperamos el mismo patrón que S01P04: [0,1] y [1,0] con 50% cada uno
    print(res)