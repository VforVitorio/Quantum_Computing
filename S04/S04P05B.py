"""
PROGRAMA: Demostración de la puerta cuántica RZ sobre |1⟩
==========================================
Este programa demuestra el efecto de la puerta RZ sobre un qubit inicializado en |1⟩.
La puerta RZ realiza una rotación del qubit alrededor del eje Z de la esfera de Bloch.
Matriz RZ(θ): [[e^(-iθ/2), 0], [0, e^(iθ/2)]]
En este caso, θ = π/2, lo que produce una rotación de 90° sobre el eje Z.
RZ es similar a PHASE pero aplica una fase global adicional.
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: X (NOT) y RZ (rotación sobre Z)
from pyquil.gates import X,RZ
# Importar el simulador de función de onda para ejecutar circuitos cuánticos
from pyquil.api import WavefunctionSimulator
# Importar el módulo math para usar constantes como pi
import math

# Crear un programa cuántico aplicando la puerta X al qubit 0
# X es la puerta NOT cuántica, que convierte |0⟩ en |1⟩
# Esto inicializa el qubit en el estado |1⟩ = (0, 1)
prog = Program(X(0))

# Crear una instancia del simulador de función de onda
qvm = WavefunctionSimulator()
# Ejecutar el programa y obtener la función de onda resultante
result = qvm.wavefunction(prog)

# Imprimir la función de onda después de aplicar X(0)
# Resultado esperado: (1+0j)|1⟩  (el qubit está en |1⟩)
print(result)

# Añadir al programa la puerta RZ con ángulo π/2 aplicada al qubit 0
# RZ(π/2) aplica e^(-iπ/4) a |0⟩ y e^(iπ/4) a |1⟩
# RZ(π/2)|1⟩ = e^(iπ/4)|1⟩ ≈ (0.707 + 0.707i)|1⟩
# Esta es la fase opuesta a la que se aplica a |0⟩
prog.inst(RZ(math.pi/2,0))

# Ejecutar el programa completo (X + RZ) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar RZ(π/2, 0)
# Resultado esperado: (0.707+0.707j)|1⟩  (fase e^(iπ/4) aplicada a |1⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de X):
(1+0j)|1⟩

Segunda impresión (después de RZ):
(0.707+0.707j)|1⟩  ó  aproximadamente (0.7071+0.7071j)|1⟩

EXPLICACIÓN: La puerta RZ(π/2) aplica una rotación de fase alrededor del eje Z.
Para el estado |1⟩, aplica el factor e^(iπ/4) ≈ 0.707 + 0.707i.
Nótese que este resultado es IDÉNTICO al de PHASE(π/4)|1⟩, pero conceptualmente diferente:
- PHASE solo afecta |1⟩, dejando |0⟩ sin cambios
- RZ afecta ambos estados con fases OPUESTAS: e^(-iπ/4) para |0⟩ y e^(iπ/4) para |1⟩

Esta diferencia es importante en superposiciones: si tenemos α|0⟩ + β|1⟩,
RZ(θ) produce: e^(-iθ/2)α|0⟩ + e^(iθ/2)β|1⟩, creando una fase RELATIVA de θ entre ambos.
RZ es una puerta fundamental en algoritmos cuánticos y circuitos variacionales.
"""
