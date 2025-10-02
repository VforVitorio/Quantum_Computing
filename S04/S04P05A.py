"""
PROGRAMA: Demostración de la puerta cuántica RZ (Rotación sobre eje Z)
==========================================
Este programa demuestra el efecto de la puerta RZ sobre un qubit inicializado en |0⟩.
La puerta RZ realiza una rotación del qubit alrededor del eje Z de la esfera de Bloch.
Matriz RZ(θ): [[e^(-iθ/2), 0], [0, e^(iθ/2)]]
En este caso, θ = π/2, lo que produce una rotación de 90° sobre el eje Z.
RZ es similar a PHASE pero aplica una fase global adicional.
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad) y RZ (rotación sobre Z)
from pyquil.gates import I,RZ
# Importar el simulador de función de onda para ejecutar circuitos cuánticos
from pyquil.api import WavefunctionSimulator
# Importar el módulo math para usar constantes como pi
import math

# Crear un programa cuántico aplicando la puerta I (Identidad) al qubit 0
# Esto inicializa el qubit en el estado |0⟩ = (1, 0)
prog = Program(I(0))

# Crear una instancia del simulador de función de onda
qvm = WavefunctionSimulator()
# Ejecutar el programa y obtener la función de onda resultante
result = qvm.wavefunction(prog)

# Imprimir la función de onda después de aplicar I(0)
# Resultado esperado: (1+0j)|0⟩  (el qubit permanece en |0⟩)
print(result)

# Añadir al programa la puerta RZ con ángulo π/2 aplicada al qubit 0
# RZ(π/2) aplica e^(-iπ/4) a |0⟩ y e^(iπ/4) a |1⟩
# RZ(π/2)|0⟩ = e^(-iπ/4)|0⟩ ≈ (0.707 - 0.707i)|0⟩
# Esta es una fase global que técnicamente no es observable en mediciones
prog.inst(RZ(math.pi/2,0))

# Ejecutar el programa completo (I + RZ) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar RZ(π/2, 0)
# Resultado esperado: (0.707-0.707j)|0⟩  (fase global aplicada a |0⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de RZ):
(0.707-0.707j)|0⟩  ó  aproximadamente (0.7071-0.7071j)|0⟩

EXPLICACIÓN: La puerta RZ(π/2) aplica una rotación de fase alrededor del eje Z.
Para el estado |0⟩, aplica el factor e^(-iπ/4) ≈ 0.707 - 0.707i.
Esta es una fase GLOBAL sobre todo el estado, no una fase relativa entre |0⟩ y |1⟩.
DIFERENCIA con PHASE: PHASE solo afecta a |1⟩, mientras que RZ afecta a ambos estados
con fases opuestas (e^(-iθ/2) para |0⟩ y e^(iθ/2) para |1⟩).
RZ es útil en algoritmos cuánticos donde las fases relativas son importantes.
Junto con RX y RY, forma el conjunto de puertas de rotación de Pauli.
"""
