"""
PROGRAMA: Composición de puertas cuánticas - Relación ZX = iY sobre |0⟩
==========================================
Este programa demuestra una relación fundamental entre las puertas de Pauli:
la composición Z(X(|0⟩)) = iY|0⟩. Esto muestra que aplicar Z después de X es
equivalente a aplicar Y multiplicado por la fase global i (salvo una fase global).

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

# Añadir al programa la composición Z(0) seguido de X(0)
# Primero aplica Z a |0⟩ (no hace nada: Z|0⟩ = |0⟩)
# Luego aplica X a |0⟩ (invierte: X|0⟩ = |1⟩)
# El orden de ejecución es de izquierda a derecha, pero el efecto se lee Z∘X
prog.inst(Z(0),X(0))

# Ejecutar el programa completo (I + Z + X) y obtener la función de onda
result = qvm.wavefunction(prog)

# Imprimir la función de onda después de aplicar Z y X
# Resultado: -|1⟩ = (-1+0j)|1⟩
print(result)

# Multiplicar las amplitudes por i para demostrar la relación con Y
# result.amplitudes contiene el vector de estado [α, β] donde |ψ⟩ = α|0⟩ + β|1⟩
# Multiplicar por i = 0+1j transforma el resultado en iY|0⟩
print(1j*result.amplitudes)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de Z y X):
(-1+0j)|1⟩

Tercera impresión (amplitudes multiplicadas por i):
[0.+0.j 0.+1.j]

EXPLICACIÓN: Este programa demuestra una relación importante entre las puertas de Pauli.
Al aplicar Z seguido de X sobre |0⟩, obtenemos:

Paso 1: I|0⟩ = |0⟩ = [1, 0]
Paso 2: Z|0⟩ = |0⟩ (Z no afecta a |0⟩)
Paso 3: X|0⟩ = |1⟩ = [0, 1]
Pero con la fase de Z aplicada primero, el resultado es -|1⟩ = [0, -1]

Comparación con Y|0⟩:
Y|0⟩ = i|1⟩ = [0, i]

Multiplicando Z(X|0⟩) = -|1⟩ por i:
i × (-|1⟩) = -i|1⟩ = [0, -i]

La relación ZX = iY se cumple salvo una fase global (-1). En mecánica cuántica,
las fases globales no son observables, por lo que ZX y iY son físicamente equivalentes
cuando actúan sobre estados. Esta relación demuestra que las tres puertas de Pauli
están fundamentalmente relacionadas y forman un álgebra de Lie.

El vector [0, i] mostrado representa el estado i|1⟩, que es exactamente Y|0⟩.
"""
