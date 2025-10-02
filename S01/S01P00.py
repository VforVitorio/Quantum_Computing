"""
PROGRAMA: S01P00.py - Simulación básica de qubit con compuerta identidad

RESUMEN:
Este programa demuestra el uso básico de PyQuil para crear y simular un circuito cuántico
simple. Aplica una compuerta identidad (I) a un qubit inicializado en |0⟩ y obtiene
la función de onda del estado resultante.

FUNCIONAMIENTO:
1. Crea un programa cuántico con una compuerta identidad aplicada al qubit 0
2. Usa el simulador de función de onda para obtener el estado cuántico exacto
3. Imprime la función de onda, que debería ser |0⟩ = [1+0j, 0+0j]

SALIDA ESPERADA:
La salida muestra la función de onda como un array de amplitudes complejas:
- [1+0j, 0+0j]: representa el estado |0⟩ (qubit en estado fundamental)
- El primer elemento (1+0j) es la amplitud para |0⟩
- El segundo elemento (0+0j) es la amplitud para |1⟩

CONCEPTOS DE FÍSICA CUÁNTICA:

1. QUBIT (Quantum Bit):
   - Unidad básica de información cuántica, análogo cuántico del bit clásico
   - Puede existir en estados |0⟩, |1⟩ o cualquier superposición α|0⟩ + β|1⟩
   - Los coeficientes α y β son amplitudes complejas que satisfacen |α|² + |β|² = 1
   - |α|² y |β|² representan las probabilidades de medir 0 y 1 respectivamente

2. NOTACIÓN BRA-KET (Notación de Dirac):
   - |ψ⟩ (ket): representa un estado cuántico como vector columna
   - |0⟩ = [1, 0]ᵀ y |1⟩ = [0, 1]ᵀ son los estados base computacionales
   - Estados fundamentales análogos a los bits clásicos 0 y 1

3. FUNCIÓN DE ONDA:
   - Descripción matemática completa del estado cuántico de un sistema
   - Contiene toda la información sobre las probabilidades de medición
   - En este caso: ψ = 1·|0⟩ + 0·|1⟩ = |0⟩

4. COMPUERTA IDENTIDAD (I):
   - Operación que no modifica el estado del qubit
   - Matriz identidad 2×2: I = [[1,0],[0,1]]
   - Útil para sincronización temporal en circuitos complejos
   - I|0⟩ = |0⟩ e I|1⟩ = |1⟩

5. AMPLITUDES COMPLEJAS:
   - Los estados cuánticos se describen con números complejos
   - La fase relativa entre amplitudes tiene efectos físicos medibles
   - En este ejemplo simple, todas las amplitudes son reales
"""

# Importa la clase Program para crear programas cuánticos
from pyquil import Program
# Importa la compuerta identidad (I) que no modifica el estado del qubit
from pyquil.gates import I
# Importa el simulador de función de onda para obtener estados cuánticos exactos
from pyquil.api import WavefunctionSimulator

# Crea un programa cuántico que aplica la compuerta identidad al qubit 0
# La compuerta I no cambia el estado del qubit (|0⟩ permanece como |0⟩, |1⟩ permanece como |1⟩)
prog = Program(I(0))

# Inicializa el simulador de función de onda
# Este simulador calcula la función de onda exacta del sistema cuántico
qvm = WavefunctionSimulator()
# Ejecuta la simulación del programa y obtiene la función de onda resultante
# Como el qubit inicia en |0⟩ y aplicamos identidad, el resultado sigue siendo |0⟩
result = qvm.wavefunction(prog)
# Imprime la función de onda como array de amplitudes complejas
# [1+0j, 0+0j] indica que el qubit está completamente en el estado |0⟩
print(result)

# Importa la compuerta X (Pauli-X o NOT cuántico)
from pyquil.gates import X

# Añade al programa existente la compuerta X aplicada al qubit 0
# X es la compuerta NOT cuántica: invierte |0⟩ a |1⟩ y viceversa
prog.inst(X(0))

# Ejecuta nuevamente la simulación con el programa modificado (I seguido de X)
# Como I(0) no hace nada, el resultado es equivalente a solo aplicar X(0)
result = qvm.wavefunction(prog)
# Imprime la nueva función de onda
# [0+0j, 1+0j] indica que el qubit ahora está en el estado |1⟩
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión:
(1+0j)|0⟩

Segunda impresión:
(1+0j)|1⟩

EXPLICACIÓN:
El programa primero aplica la puerta identidad I(0), que no modifica el estado inicial |0⟩.
Luego añade la puerta X(0) (NOT cuántico) al programa, que invierte el qubit de |0⟩ a |1⟩.
La puerta X es el análogo cuántico de la compuerta NOT clásica, realizando un "bit-flip"
del estado cuántico.
"""
