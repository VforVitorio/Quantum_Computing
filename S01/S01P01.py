"""
PROGRAMA: S01P01.py - Circuito cuántico con compuertas X y CNOT

RESUMEN:
Este programa demuestra el uso de compuertas cuánticas básicas (X y CNOT) en un circuito
de dos qubits. Aplica compuertas X (NOT cuántico) a ambos qubits, luego una compuerta CNOT
y finalmente mide uno de los qubits para observar el resultado.

FUNCIONAMIENTO:
1. Declara un registro clásico de 2 bits para almacenar mediciones
2. Aplica compuerta X al qubit 0 (lo cambia de |0⟩ a |1⟩)
3. Aplica compuerta X al qubit 1 (lo cambia de |0⟩ a |1⟩)
4. Aplica CNOT con qubit 1 como control y qubit 0 como target
5. Mide el qubit 1 y almacena el resultado
6. Repite el experimento 100 veces

SALIDA ESPERADA:
La salida muestra 100 mediciones del qubit 1. Cada línea tiene el formato:
Shot X: [medición_qubit_0, medición_qubit_1]
Donde medición_qubit_1 debería ser consistentemente 1, y medición_qubit_0 será 0
(ya que no se mide el qubit 0 pero se inicializa en 0 en el registro).

CONCEPTOS DE FÍSICA CUÁNTICA:

1. COMPUERTA PAULI-X (Compuerta NOT cuántica):
   - Análogo cuántico de la compuerta NOT clásica
   - Matriz: X = [[0,1],[1,0]]
   - Efectos: X|0⟩ = |1⟩ y X|1⟩ = |0⟩
   - Representa una rotación de 180° alrededor del eje X en la esfera de Bloch
   - También llamada "bit flip" porque invierte el estado computacional

2. COMPUERTA CNOT (Controlled-NOT):
   - Compuerta de dos qubits: un control y un target
   - Si control = |0⟩, target permanece sin cambios
   - Si control = |1⟩, target se invierte (aplica X al target)
   - Matriz 4×4: CNOT = [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]
   - Operaciones: |00⟩→|00⟩, |01⟩→|01⟩, |10⟩→|11⟩, |11⟩→|10⟩

3. SISTEMAS DE DOS QUBITS:
   - El espacio de estados es producto tensorial: ℂ² ⊗ ℂ² = ℂ⁴
   - Estados base: |00⟩, |01⟩, |10⟩, |11⟩
   - Estado general: α|00⟩ + β|01⟩ + γ|10⟩ + δ|11⟩
   - Evolución del circuito: |00⟩ X⊗X→ |11⟩ CNOT(1,0)→ |10⟩

4. MEDICIÓN CUÁNTICA:
   - Proceso que colapsa el estado cuántico a un estado clásico
   - Resultado probabilístico basado en |amplitud|²
   - Destruye la superposición cuántica
   - Solo el qubit medido colapsa (medición parcial)

5. OPERACIONES UNITARIAS:
   - Todas las compuertas cuánticas son matrices unitarias (U†U = I)
   - Preservan la norma del estado cuántico
   - Representan evolución reversible del sistema cuántico
   - Las mediciones son el único proceso irreversible
"""

# Importa las funciones necesarias para crear y ejecutar circuitos cuánticos
from pyquil import get_qc, Program
# Importa las compuertas cuánticas: CNOT (controlled-NOT), X (Pauli-X), MEASURE
from pyquil.gates import CNOT, X, MEASURE
# Importa Declare para declarar registros de memoria clásica
from pyquil.quilbase import Declare

# Crea el programa cuántico
prog = Program(
    # Declara un registro clásico llamado "ro" (readout) de tipo BIT con 2 posiciones
    # Este registro almacenará los resultados de las mediciones
    Declare("ro", "BIT", 2),
    # Aplica compuerta X (NOT cuántico) al qubit 0, cambiándolo de |0⟩ a |1⟩
    X(0),
    # Aplica compuerta X (NOT cuántico) al qubit 1, cambiándolo de |0⟩ a |1⟩
    X(1),
    # Aplica compuerta CNOT con qubit 1 como control y qubit 0 como target
    # Si control=|1⟩, entonces target se invierte; si control=|0⟩, target no cambia
    # Estado antes: |11⟩, después: |10⟩ (el qubit 0 se invierte porque qubit 1 = |1⟩)
    CNOT(1, 0),
    # Mide el qubit 1 y almacena el resultado en la posición 1 del registro "ro"
    # El qubit 1 permanece en |1⟩, por lo que la medición debería dar 1
    MEASURE(1, ("ro", 1)),
# Repite todo el circuito 100 veces para obtener estadísticas
).wrap_in_numshots_loop(100)

# Obtiene una conexión al simulador cuántico virtual (9 qubits en configuración cuadrada)
qvm = get_qc('9q-square-qvm')
# Compila el programa para el hardware específico y lo ejecuta
result = qvm.run(qvm.compile(prog))

# Extrae los datos de medición del registro "ro"
measurements = result.readout_data['ro']

# Itera sobre todas las mediciones y las imprime
for i, measurement in enumerate(measurements):
    # Imprime cada medición con formato "Shot X: [bit0, bit1]"
    # bit1 debería ser siempre 1, bit0 siempre 0 (no se mide, valor por defecto)
    print(f"Shot {i}: {measurement}")