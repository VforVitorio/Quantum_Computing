"""
PROGRAMA: S01P04.py - Estado de Bell con inicialización X en el segundo qubit

RESUMEN:
Este programa crea otro tipo de estado de Bell, aplicando Hadamard al primer qubit
y X al segundo qubit antes del entrelazamiento con CNOT. Demuestra cómo la
inicialización de diferentes qubits afecta el estado entrelazado resultante.

FUNCIONAMIENTO:
1. Declara un registro clásico de 2 bits para almacenar mediciones
2. Aplica compuerta Hadamard al qubit 0 (crea superposición |0⟩+|1⟩)/√2
3. Aplica compuerta X al qubit 1 (cambia |0⟩ a |1⟩)
4. Aplica CNOT con qubit 0 como control y qubit 1 como target
5. Mide ambos qubits y almacena los resultados
6. Repite el experimento 100 veces

SALIDA ESPERADA:
La salida muestra 100 mediciones de los dos qubits entrelazados. Cada línea muestra:
[medición_qubit_0, medición_qubit_1]
El estado final es (|01⟩ + |10⟩)/√2, por lo que esperamos:
- Aproximadamente 50% de las veces: [0, 1]
- Aproximadamente 50% de las veces: [1, 0]
- Los qubits estarán anti-correlacionados debido a la inicialización del qubit 1

CONCEPTOS DE FÍSICA CUÁNTICA:

1. DIFERENTES RUTAS AL MISMO ESTADO DE BELL:
   - Este programa también crea |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
   - Misma superposición que S01P03.py pero con diferente construcción
   - Demuestra equivalencia de circuitos cuánticos diferentes
   - Múltiples formas de preparar el mismo estado cuántico

2. EVOLUCIÓN DE ESTADO ALTERNATIVA:
   - Inicial: |00⟩
   - Después de H(0): (|0⟩ + |1⟩)/√2 ⊗ |0⟩ = (|00⟩ + |10⟩)/√2
   - Después de X(1): (|01⟩ + |11⟩)/√2
   - Después de CNOT(0,1): (|01⟩ + |10⟩)/√2
   - Resultado idéntico a S01P03 por ruta diferente

3. OPERACIONES CONMUTATIVAS Y NO CONMUTATIVAS:
   - H(0) y X(1) conmutan: actúan en qubits diferentes
   - Orden H(0),X(1) vs X(1),H(0) no afecta el resultado
   - CNOT debe aplicarse después para crear entrelazamiento
   - Demostración: [H₀ ⊗ I₁][I₀ ⊗ X₁] = [I₀ ⊗ X₁][H₀ ⊗ I₁]

4. PRODUCTO TENSORIAL EN SISTEMAS COMPUESTOS:
   - Estado inicial factorizable: |0⟩ ⊗ |0⟩ = |00⟩
   - Después de H,X: (|0⟩ + |1⟩)/√2 ⊗ |1⟩ (aún factorizable)
   - CNOT crea entrelazamiento: estado no factorizable
   - Transición de estado separable a entrelazado

5. COMPILACIÓN DE CIRCUITOS:
   - Circuitos se optimizan para hardware específico
   - Compilador puede reordenar operaciones conmutativas
   - Puede fusionar operaciones consecutivas
   - Mapeo de qubits lógicos a físicos

6. ESTADÍSTICAS DE MEDICIÓN:
   - 100 repeticiones revelan distribución probabilística
   - Ley de grandes números: frecuencias → probabilidades
   - Fluctuaciones estadísticas esperadas (~10% para 100 shots)
   - Verificación experimental de predicciones teóricas
"""

# Importa las funciones necesarias para crear y ejecutar circuitos cuánticos
from pyquil import get_qc, Program
# Importa las compuertas: CNOT (controlled-NOT), H (Hadamard), MEASURE, X (Pauli-X)
from pyquil.gates import CNOT, H, MEASURE, X
# Importa Declare para declarar registros de memoria clásica
from pyquil.quilbase import Declare

# Crea el programa cuántico con inicialización X en el segundo qubit
prog = Program(
    # Declara un registro clásico llamado "ro" de tipo BIT con 2 posiciones
    Declare("ro", "BIT", 2),
    # Aplica compuerta Hadamard al qubit 0
    # Crea superposición: |0⟩ → (|0⟩ + |1⟩)/√2
    H(0),
    # Aplica compuerta X al qubit 1
    # Inicializa el qubit 1 en estado |1⟩ (en lugar del |0⟩ por defecto)
    X(1),
    # Aplica compuerta CNOT con qubit 0 como control y qubit 1 como target
    # El estado antes del CNOT: (|0⟩ + |1⟩)/√2 ⊗ |1⟩ = (|01⟩ + |11⟩)/√2
    # Después del CNOT: (|01⟩ + |10⟩)/√2 (anti-correlacionado)
    CNOT(0, 1),
    # Mide el qubit 0 y almacena el resultado en la posición 0 del registro "ro"
    MEASURE(0, ("ro", 0)),
    # Mide el qubit 1 y almacena el resultado en la posición 1 del registro "ro"
    # Los resultados serán anti-correlacionados: cuando uno es 0, el otro es 1
    MEASURE(1, ("ro", 1)),
# Repite el experimento 100 veces para observar la distribución estadística
).wrap_in_numshots_loop(100)

# Obtiene una conexión al simulador cuántico virtual
qvm = get_qc('9q-square-qvm')

# Compila el programa cuántico para el hardware específico
# El paso de compilación optimiza el circuito para la arquitectura del simulador
executable = qvm.compile(prog)
# Ejecuta el programa compilado
result = qvm.run(executable)

# Extrae los datos de medición del registro "ro" usando el método .get()
ro_data = result.readout_data.get("ro")
# Itera sobre todas las mediciones e imprime los resultados
for res in ro_data:
    # Imprime cada par de mediciones [qubit_0, qubit_1]
    # Esperamos ver solo [0,1] y [1,0] debido al entrelazamiento anti-correlacionado
    print(res)
