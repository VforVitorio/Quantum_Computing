"""
PROGRAMA: S01P02.py - Estado de Bell (entrelazamiento cuántico)

RESUMEN:
Este programa crea uno de los estados de Bell más básicos, demostrando el entrelazamiento
cuántico entre dos qubits. Utiliza una compuerta Hadamard para crear superposición
y una compuerta CNOT para entrelazar los qubits.

FUNCIONAMIENTO:
1. Declara un registro clásico de 2 bits para almacenar mediciones
2. Aplica compuerta Hadamard (H) al qubit 0 (crea superposición |0⟩+|1⟩)/√2
3. Aplica CNOT con qubit 0 como control y qubit 1 como target
4. Mide ambos qubits y almacena los resultados
5. Repite el experimento 100 veces

SALIDA ESPERADA:
La salida muestra 100 mediciones de los dos qubits entrelazados. Cada línea muestra:
[medición_qubit_0, medición_qubit_1]
Debido al entrelazamiento, los resultados serán correlacionados:
- Aproximadamente 50% de las veces: [0, 0]
- Aproximadamente 50% de las veces: [1, 1]
- Nunca se observará [0, 1] ni [1, 0] debido al entrelazamiento perfecto

CONCEPTOS DE FÍSICA CUÁNTICA:

1. COMPUERTA HADAMARD (H):
   - Crea superposición equiprobable desde estados base
   - Matriz: H = (1/√2)[[1,1],[1,-1]]
   - Efectos: H|0⟩ = (|0⟩ + |1⟩)/√2, H|1⟩ = (|0⟩ - |1⟩)/√2
   - Rotación de 180° alrededor del eje (X+Z)/√2 en la esfera de Bloch
   - Fundamental para crear algoritmos cuánticos

2. SUPERPOSICIÓN CUÁNTICA:
   - Principio fundamental: un qubit puede estar en múltiples estados simultáneamente
   - Estado H|0⟩ = (|0⟩ + |1⟩)/√2 existe en ambos |0⟩ y |1⟩ hasta la medición
   - No es mezcla estadística clásica, sino coherencia cuántica real
   - Permite paralelismo cuántico exponencial

3. ESTADOS DE BELL:
   - Cuatro estados entrelazados maximalmente de dos qubits:
   - |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 (creado por este programa)
   - |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
   - |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
   - |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
   - Base de Bell: estados no separables, fundamentales en información cuántica

4. ENTRELAZAMIENTO CUÁNTICO:
   - Correlación cuántica no clásica entre qubits
   - El estado no puede escribirse como producto tensorial: ψ ≠ ψ₁ ⊗ ψ₂
   - Medición de un qubit instantáneamente determina el estado del otro
   - Einstein lo llamó "acción fantasmal a distancia"
   - Violación de desigualdades de Bell demuestra su naturaleza no local

5. CORRELACIONES CUÁNTICAS:
   - Más fuertes que cualquier correlación clásica posible
   - En |Φ⁺⟩: mediciones siempre correlacionadas (ambos 0 o ambos 1)
   - Probabilidad P(0,0) = P(1,1) = 1/2, P(0,1) = P(1,0) = 0
   - Base para protocolos como teleportación cuántica y criptografía cuántica

6. ESFERA DE BLOCH:
   - Representación geométrica del estado de un qubit
   - |0⟩ en polo norte, |1⟩ en polo sur
   - Estados de superposición en el ecuador y interior
   - (|0⟩ + |1⟩)/√2 se ubica en el ecuador del eje X
"""

# Importa las funciones necesarias para crear y ejecutar circuitos cuánticos
from pyquil import get_qc, Program
# Importa las compuertas: CNOT (controlled-NOT), H (Hadamard), MEASURE
from pyquil.gates import CNOT, H, MEASURE
# Importa Declare para declarar registros de memoria clásica
from pyquil.quilbase import Declare

# Crea el programa cuántico para generar un estado de Bell
prog = Program(
    # Declara un registro clásico llamado "ro" de tipo BIT con 2 posiciones
    # para almacenar los resultados de medición de ambos qubits
    Declare("ro", "BIT", 2),
    # Aplica compuerta Hadamard al qubit 0
    # Transforma |0⟩ → (|0⟩ + |1⟩)/√2, creando una superposición equiprobable
    H(0),
    # Aplica compuerta CNOT con qubit 0 como control y qubit 1 como target
    # Esto crea entrelazamiento: si qubit 0 está en superposición, el sistema
    # evoluciona al estado entrelazado (|00⟩ + |11⟩)/√2
    CNOT(0, 1),
    # Mide el qubit 0 y almacena el resultado en la posición 0 del registro "ro"
    # El colapso de la función de onda determinará si el resultado es 0 o 1
    MEASURE(0, ("ro", 0)),
    # Mide el qubit 1 y almacena el resultado en la posición 1 del registro "ro"
    # Debido al entrelazamiento, este resultado será idéntico al del qubit 0
    MEASURE(1, ("ro", 1)),
# Repite todo el experimento 100 veces para observar la distribución estadística
).wrap_in_numshots_loop(100)

# Obtiene una conexión al simulador cuántico virtual
qvm = get_qc('9q-square-qvm')
# Compila y ejecuta el programa cuántico
result = qvm.run(qvm.compile(prog))
# Extrae los datos de medición del registro "ro"
measurements = result.readout_data['ro']

# Itera sobre todas las mediciones e imprime los resultados
for res in measurements:
    # Imprime cada par de mediciones [qubit_0, qubit_1]
    # Esperamos ver solo [0,0] y [1,1] debido al entrelazamiento
    print(res)
