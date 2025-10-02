"""
PROGRAMA: S01P03.py - Estado de Bell modificado con inicialización X

RESUMEN:
Este programa crea un estado de Bell modificado, comenzando con una compuerta X
seguida de Hadamard y CNOT. Demuestra cómo diferentes inicializaciones afectan
el estado entrelazado final.

FUNCIONAMIENTO:
1. Declara un registro clásico de 2 bits para almacenar mediciones
2. Aplica compuerta X al qubit 0 (cambia |0⟩ a |1⟩)
3. Aplica compuerta Hadamard al qubit 0 (crea superposición desde |1⟩)
4. Aplica CNOT con qubit 0 como control y qubit 1 como target
5. Mide ambos qubits y almacena los resultados
6. Repite el experimento 10 veces

SALIDA ESPERADA:
La salida muestra 10 mediciones de los dos qubits entrelazados. Cada línea muestra:
[medición_qubit_0, medición_qubit_1]
El estado final es (|01⟩ + |10⟩)/√2, por lo que esperamos:
- Aproximadamente 50% de las veces: [0, 1]
- Aproximadamente 50% de las veces: [1, 0]
- Nunca se observará [0, 0] ni [1, 1] debido al patrón anti-correlacionado

CONCEPTOS DE FÍSICA CUÁNTICA:

1. ESTADO DE BELL |Ψ⁺⟩:
   - Este programa crea el estado |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
   - Uno de los cuatro estados de Bell maximalmente entrelazados
   - Caracterizado por anti-correlación perfecta entre qubits
   - También llamado "estado singlete" en sistemas de spin

2. EVOLUCIÓN DE ESTADO POR PASOS:
   - Inicial: |00⟩
   - Después de X(0): |10⟩
   - Después de H(0): (|00⟩ - |10⟩)/√2 = (|0⟩ - |1⟩)/√2 ⊗ |0⟩
   - Después de CNOT(0,1): (|01⟩ + |10⟩)/√2
   - Nota: H|1⟩ = (|0⟩ - |1⟩)/√2 incluye una fase relativa

3. FASES RELATIVAS EN SUPERPOSICIÓN:
   - H|1⟩ = (|0⟩ - |1⟩)/√2 tiene fase negativa en |1⟩
   - Las fases relativas afectan la interferencia cuántica
   - CNOT convierte la fase en el control a correlación anti-paralela
   - Fase global vs. fase relativa: solo las relativas son observables

4. ANTI-CORRELACIÓN CUÁNTICA:
   - Qubits están perfectamente anti-correlacionados
   - P(0,1) = P(1,0) = 1/2, P(0,0) = P(1,1) = 0
   - Más fuerte que correlación clásica máxima
   - Fundamental para aplicaciones como codificación superdensa

5. TRANSFORMACIONES UNITARIAS COMPUESTAS:
   - Secuencia de operaciones: U = CNOT₀₁ · H₀ · X₀
   - Cada operación es reversible y preserva norma
   - El orden de aplicación importa (matrices no commutan)
   - Circuito equivale a una sola transformación unitaria 4×4

6. MEDICIÓN PROYECTIVA:
   - Medición en base computacional {|0⟩, |1⟩}
   - Proyecta estado entrelazado a estados producto
   - Colapso instantáneo: medir un qubit determina el otro
   - Conserva la anti-correlación estadística
"""

# Importa las funciones necesarias para crear y ejecutar circuitos cuánticos
from pyquil import get_qc, Program
# Importa las compuertas: CNOT (controlled-NOT), H (Hadamard), MEASURE, X (Pauli-X)
from pyquil.gates import CNOT, H, MEASURE, X
# Importa Declare para declarar registros de memoria clásica
from pyquil.quilbase import Declare

# Crea el programa cuántico para generar un estado de Bell anti-correlacionado
prog = Program(
    # Declara un registro clásico llamado "ro" de tipo BIT con 2 posiciones
    Declare("ro", "BIT", 2),
    # Aplica compuerta X (Pauli-X) al qubit 0
    # Cambia el estado inicial de |0⟩ a |1⟩
    X(0),
    # Aplica compuerta Hadamard al qubit 0 (que ahora está en |1⟩)
    # Transforma |1⟩ → (|0⟩ - |1⟩)/√2, creando superposición con fase relativa
    H(0),
    # Aplica compuerta CNOT con qubit 0 como control y qubit 1 como target
    # Esto crea el estado entrelazado (|01⟩ + |10⟩)/√2
    # Los qubits estarán anti-correlacionados (siempre opuestos)
    CNOT(0, 1),
    # Mide el qubit 0 y almacena el resultado en la posición 0 del registro "ro"
    MEASURE(0, ("ro", 0)),
    # Mide el qubit 1 y almacena el resultado en la posición 1 del registro "ro"
    # Debido al entrelazamiento, este resultado será opuesto al del qubit 0
    MEASURE(1, ("ro", 1)),
# Repite el experimento 10 veces para observar la anti-correlación
).wrap_in_numshots_loop(10)

# Obtiene una conexión al simulador cuántico virtual
qvm = get_qc('9q-square-qvm')
# Compila y ejecuta el programa cuántico
result = qvm.run(qvm.compile(prog))
# Extrae los datos de medición del registro "ro"
measurements = result.readout_data['ro']

# Itera sobre todas las mediciones e imprime los resultados
for res in measurements:
    # Imprime cada par de mediciones [qubit_0, qubit_1]
    # Esperamos ver solo [0,1] y [1,0] debido al entrelazamiento anti-correlacionado
    print(res)
