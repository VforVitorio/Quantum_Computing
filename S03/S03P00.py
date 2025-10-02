"""
PROGRAMA: Demostración de la puerta cuántica X (NOT cuántico)
==========================================
Este programa demuestra el efecto de la puerta X (también llamada NOT cuántico o
bit-flip) sobre un qubit inicializado en |0⟩. La puerta X intercambia las amplitudes
de |0⟩ y |1⟩, análoga a la puerta NOT clásica pero operando sobre superposiciones.

Matriz de la puerta X: [[0, 1], [1, 0]]
X|0⟩ = |1⟩
X|1⟩ = |0⟩
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad) y X (NOT cuántico)
from pyquil.gates import I,X
# Importar el simulador de función de onda para ejecutar circuitos cuánticos
from pyquil.api import WavefunctionSimulator

# Crear un programa cuántico aplicando la puerta I (Identidad) al qubit 0
# Esto inicializa explícitamente el qubit en el estado |0⟩ = (1, 0)
prog = Program(I(0))

# Crear una instancia del simulador de función de onda
qvm = WavefunctionSimulator()
# Ejecutar el programa y obtener la función de onda resultante
result = qvm.wavefunction(prog)

# Imprimir la función de onda después de aplicar I(0)
# Resultado esperado: (1+0j)|0⟩ (el qubit está en |0⟩)
print(result)

# Añadir al programa la puerta X aplicada al qubit 0
# X invierte el estado: |0⟩ → |1⟩
prog.inst(X(0))

# Ejecutar el programa completo (I + X) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar X(0)
# Resultado esperado: (1+0j)|1⟩ (el qubit ha sido invertido a |1⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de X):
(1+0j)|1⟩

EXPLICACIÓN: La puerta X es el equivalente cuántico de la puerta NOT clásica.
Cuando se aplica a |0⟩, lo transforma en |1⟩ con amplitud 1 (probabilidad 100%).
La puerta X invierte el estado del qubit intercambiando las amplitudes de las
componentes |0⟩ y |1⟩. Matemáticamente: X|0⟩ = |1⟩ y X|1⟩ = |0⟩.
Esta es una de las puertas de Pauli, junto con Y y Z, que forman la base de
muchas operaciones cuánticas.
"""
