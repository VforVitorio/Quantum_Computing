"""
PROGRAMA: Demostración de la puerta cuántica Z sobre |1⟩
==========================================
Este programa demuestra el efecto de la puerta Z (phase-flip) sobre un qubit
inicializado en |1⟩. Primero se prepara el estado |1⟩ usando I y X, luego se aplica Z.
La puerta Z invierte el signo de |1⟩, introduciendo una fase de π radianes (180°).

Matriz de la puerta Z: [[1, 0], [0, -1]]
Z|0⟩ = |0⟩
Z|1⟩ = -|1⟩
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad), X (NOT cuántico) y Z (phase-flip)
from pyquil.gates import I,X,Z
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

# Añadir al programa la puerta Z aplicada al qubit 0
# Z invierte el signo de |1⟩: Z|1⟩ = -|1⟩
prog.inst(Z(0))

# Ejecutar el programa completo (I + X + Z) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar Z(0)
# Resultado esperado: -|1⟩ = (-1+0j)|1⟩ (qubit en |1⟩ con amplitud negativa)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I + X):
(1+0j)|1⟩

Segunda impresión (después de Z):
(-1+0j)|1⟩

EXPLICACIÓN: Este programa demuestra el efecto de la puerta Z sobre el estado |1⟩.
Primero, se prepara el qubit en |1⟩ aplicando X a |0⟩. Luego, al aplicar Z, el
qubit se transforma en -|1⟩, que es el estado |1⟩ con amplitud negativa.

La puerta Z es una puerta de "phase-flip" que introduce un cambio de fase de π
radianes (180°) en la componente |1⟩. A diferencia de X e Y, Z NO cambia el estado
base del qubit (sigue siendo |1⟩), solo invierte su signo.

Puntos clave:
- La amplitud cambia de +1 a -1
- La probabilidad de medir 1 permanece en |-1|² = 1 (100%)
- El estado sigue siendo |1⟩, pero con fase opuesta
- Esta fase es observable cuando el qubit está en superposición

Comparación con Z|0⟩:
- Z|0⟩ = |0⟩ (sin cambio)
- Z|1⟩ = -|1⟩ (cambio de signo)

Esta asimetría hace que Z sea útil para manipular fases relativas en superposiciones.
"""
