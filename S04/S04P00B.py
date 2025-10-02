"""
PROGRAMA: Demostración de la puerta cuántica PHASE sobre |1⟩
==========================================
Este programa demuestra el efecto de la puerta PHASE sobre un qubit inicializado en |1⟩.
La puerta PHASE aplica un cambio de fase de θ radianes a la componente |1⟩ del estado cuántico.
Matriz PHASE(θ): [[1, 0], [0, e^(iθ)]]
En este caso, θ = π/4, por lo que e^(iπ/4) = cos(π/4) + i·sin(π/4) ≈ 0.707 + 0.707i
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: X (NOT) y PHASE (cambio de fase)
from pyquil.gates import X,PHASE
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

# Añadir al programa la puerta PHASE con ángulo π/4 aplicada al qubit 0
# PHASE(θ) modifica la fase del estado |1⟩ multiplicándola por e^(iθ)
# En este caso, |1⟩ → e^(iπ/4)|1⟩
prog.inst(PHASE(math.pi/4,0))

# Ejecutar el programa completo (X + PHASE) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar PHASE(π/4, 0)
# Resultado esperado: (0.707+0.707j)|1⟩  (fase e^(iπ/4) aplicada a |1⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de X):
(1+0j)|1⟩

Segunda impresión (después de PHASE):
(0.707+0.707j)|1⟩

EXPLICACIÓN: Como el qubit está en el estado |1⟩, la puerta PHASE(π/4) multiplica su amplitud
por e^(iπ/4) ≈ 0.707 + 0.707i. Este cambio de fase SÍ es observable en este caso porque
afecta directamente a la componente |1⟩ del estado. El factor de fase e^(iπ/4) modifica
tanto la parte real como la imaginaria de la amplitud.
"""
