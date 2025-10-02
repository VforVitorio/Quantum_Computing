"""
PROGRAMA: Demostración de la puerta cuántica Y sobre |0⟩
==========================================
Este programa demuestra el efecto de la puerta Y (puerta de Pauli Y) sobre un qubit
inicializado en |0⟩. La puerta Y combina un bit-flip (como X) con un cambio de fase,
introduciendo un factor imaginario i. Es equivalente a aplicar iXZ o iZX.

Matriz de la puerta Y: [[0, -i], [i, 0]]
Y|0⟩ = i|1⟩
Y|1⟩ = -i|0⟩
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad) y Y (puerta de Pauli Y)
from pyquil.gates import I,Y
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

# Añadir al programa la puerta Y aplicada al qubit 0
# Y transforma |0⟩ en i|1⟩ (invierte el bit y añade fase imaginaria)
prog.inst(Y(0))

# Ejecutar el programa completo (I + Y) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar Y(0)
# Resultado esperado: i|1⟩ = (0+1j)|1⟩ (qubit en |1⟩ con amplitud imaginaria i)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de Y):
(0+1j)|1⟩

EXPLICACIÓN: La puerta Y es una de las tres puertas de Pauli (X, Y, Z). Cuando se
aplica a |0⟩, lo transforma en i|1⟩, que tiene una amplitud puramente imaginaria de i.
Esto significa que el qubit está en el estado |1⟩ con una fase de π/2 radianes (90°).
La puerta Y combina un bit-flip (como X) con un phase-flip (como Z), introduciendo
el factor imaginario i. Matemáticamente: Y|0⟩ = i|1⟩ y Y|1⟩ = -i|0⟩.
La amplitud (0+1j) representa una probabilidad de |i|² = 1 (100%) de medir 1.
"""
