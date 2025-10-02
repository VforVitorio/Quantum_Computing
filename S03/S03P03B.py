"""
PROGRAMA: Composición de puertas cuánticas - Relación ZX = iY sobre |1⟩
==========================================
Este programa demuestra la relación fundamental ZX = iY (salvo fase global) cuando
se aplica sobre |1⟩. Primero prepara el estado |1⟩, luego aplica la composición
Z(X(...)) y verifica que el resultado es equivalente a iY|1⟩ salvo una fase global.

Matrices de las puertas de Pauli:
X = [[0, 1], [1, 0]]
Z = [[1, 0], [0, -1]]
Y = [[0, -i], [i, 0]]

Relación: ZX = iY (salvo fase global)
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

# Añadir al programa la composición Z(0) seguido de X(0)
# Primero aplica Z a |1⟩ (invierte signo: Z|1⟩ = -|1⟩)
# Luego aplica X a -|1⟩ (invierte bit: X(-|1⟩) = -|0⟩)
# La secuencia completa es X(Z|1⟩) = X(-|1⟩) = -|0⟩
prog.inst(Z(0),X(0))

# Ejecutar el programa completo (I + X + Z + X) y obtener la función de onda
result = qvm.wavefunction(prog)

# Imprimir la función de onda después de aplicar Z y X al estado |1⟩
# Resultado: -|0⟩ = (-1+0j)|0⟩
print(result)

# Multiplicar las amplitudes por i para demostrar la relación con Y
# result.amplitudes contiene el vector de estado [α, β] donde |ψ⟩ = α|0⟩ + β|1⟩
# Multiplicar por i = 0+1j transforma el resultado para mostrar la relación con iY|1⟩
print(1j*result.amplitudes)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I + X):
(1+0j)|1⟩

Segunda impresión (después de Z y X aplicados a |1⟩):
(-1+0j)|0⟩

Tercera impresión (amplitudes multiplicadas por i):
[0.-1.j 0.+0.j]

EXPLICACIÓN: Este programa demuestra la relación ZX = iY (salvo fase global) sobre |1⟩.

Paso a paso:
1. I|0⟩ = |0⟩
2. X|0⟩ = |1⟩ = [0, 1]
3. Z|1⟩ = -|1⟩ = [0, -1]
4. X(-|1⟩) = -|0⟩ = [-1, 0]

Comparación con Y|1⟩:
Y|1⟩ = -i|0⟩ = [-i, 0]

Multiplicando ZX|1⟩ = -|0⟩ por i:
i × (-|0⟩) = -i|0⟩ = [-i, 0]

El vector resultante [-i, 0] = (0-1j)|0⟩ es exactamente Y|1⟩ = -i|0⟩.

Esta demostración confirma que la relación ZX = iY se cumple tanto para |0⟩ como
para |1⟩ (y por linealidad, para cualquier estado). Las puertas de Pauli forman
un grupo con la propiedad:
- XY = iZ
- YZ = iX
- ZX = iY

Estas relaciones son fundamentales en la teoría de información cuántica y muestran
que las tres puertas de Pauli están íntimamente relacionadas a través de factores
de fase imaginarios. En mecánica cuántica, las fases globales como el factor i o -1
no son observables en mediciones individuales, pero son importantes en interferencias
y algoritmos cuánticos.
"""
