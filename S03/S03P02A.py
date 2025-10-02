"""
PROGRAMA: Demostración de la puerta cuántica Z sobre |0⟩
==========================================
Este programa demuestra el efecto de la puerta Z (phase-flip o puerta de Pauli Z)
sobre un qubit inicializado en |0⟩. La puerta Z deja |0⟩ sin cambios pero invierte
el signo de |1⟩, introduciendo un cambio de fase de π radianes (180°) en la componente |1⟩.

Matriz de la puerta Z: [[1, 0], [0, -1]]
Z|0⟩ = |0⟩
Z|1⟩ = -|1⟩
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad) y Z (phase-flip)
from pyquil.gates import I,Z
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

# Añadir al programa la puerta Z aplicada al qubit 0
# Z deja |0⟩ sin cambios: Z|0⟩ = |0⟩
prog.inst(Z(0))

# Ejecutar el programa completo (I + Z) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar Z(0)
# Resultado esperado: (1+0j)|0⟩ (el qubit permanece en |0⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de Z):
(1+0j)|0⟩

EXPLICACIÓN: La puerta Z es una de las tres puertas de Pauli (X, Y, Z). A diferencia
de X e Y, la puerta Z NO invierte el bit. En cambio, es una puerta de "phase-flip"
que introduce un cambio de fase de π radianes (180°) en la componente |1⟩ del estado.

Cuando se aplica a |0⟩, no tiene efecto visible porque |0⟩ no tiene componente |1⟩
que pueda ser afectada por el cambio de fase. Matemáticamente: Z|0⟩ = |0⟩.

Sin embargo, cuando se aplica a |1⟩, invierte su signo: Z|1⟩ = -|1⟩.
En superposiciones, Z cambia la fase relativa entre |0⟩ y |1⟩, lo cual es crucial
para algoritmos cuánticos. Por ejemplo: Z((|0⟩ + |1⟩)/√2) = (|0⟩ - |1⟩)/√2.
"""
