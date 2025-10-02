"""
PROGRAMA: Demostración de la puerta cuántica Y sobre |1⟩
==========================================
Este programa demuestra el efecto de la puerta Y (puerta de Pauli Y) sobre un qubit
inicializado en |1⟩. Primero se prepara el estado |1⟩ usando I y X, luego se aplica Y.
La puerta Y combina un bit-flip con un cambio de fase negativo cuando actúa sobre |1⟩.

Matriz de la puerta Y: [[0, -i], [i, 0]]
Y|0⟩ = i|1⟩
Y|1⟩ = -i|0⟩
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad), X (NOT cuántico) y Y (puerta de Pauli Y)
from pyquil.gates import I,X,Y
# Importar el simulador de función de onda para ejecutar circuitos cuánticos
from pyquil.api import WavefunctionSimulator

# Crear un programa cuántico aplicando I(0) seguido de X(0)
# I(0) inicializa el qubit en |0⟩, luego X(0) lo invierte a |1⟩
prog = Program(I(0),X(0))

# Crear una instancia del simulador de función de onda
qvm = WavefunctionSimulator()
# Ejecutar el programa y obtener la función de onda resultante
result = qvm.wavefunction(prog)

# Imprimir la función de onda después de aplicar I y X
# Resultado esperado: (1+0j)|1⟩ (el qubit está en |1⟩)
print(result)

# Añadir al programa la puerta Y aplicada al qubit 0
# Y transforma |1⟩ en -i|0⟩ (invierte el bit y añade fase imaginaria negativa)
prog.inst(Y(0))

# Ejecutar el programa completo (I + X + Y) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar Y(0)
# Resultado esperado: -i|0⟩ = (0-1j)|0⟩ (qubit en |0⟩ con amplitud -i)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I + X):
(1+0j)|1⟩

Segunda impresión (después de Y):
(-0-1j)|0⟩

EXPLICACIÓN: Este programa demuestra la acción de la puerta Y sobre el estado |1⟩.
Primero, se prepara el qubit en |1⟩ aplicando X a |0⟩. Luego, al aplicar Y, el
qubit se transforma en -i|0⟩, que es el estado |0⟩ con una amplitud imaginaria
negativa -i. La notación (-0-1j)|0⟩ es equivalente a -i|0⟩.

La puerta Y aplicada a |1⟩ realiza dos operaciones simultáneas:
1. Invierte el bit: |1⟩ → |0⟩
2. Introduce una fase de -π/2 radianes (-90°), representada por el factor -i

La amplitud (-0-1j) = -i representa una probabilidad de |-i|² = 1 (100%) de medir 0.
La diferencia con Y|0⟩ = i|1⟩ es el signo: Y introduce +i cuando actúa sobre |0⟩
y -i cuando actúa sobre |1⟩.
"""
