"""
PROGRAMA: Demostración de la puerta cuántica PHASE
==========================================
Este programa demuestra el efecto de la puerta PHASE sobre un qubit inicializado en |0⟩.
La puerta PHASE aplica un cambio de fase de θ radianes a la componente |1⟩ del estado cuántico.
Matriz PHASE(θ): [[1, 0], [0, e^(iθ)]]
En este caso, θ = π/4, por lo que e^(iπ/4) = cos(π/4) + i·sin(π/4) ≈ 0.707 + 0.707i
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad) y PHASE (cambio de fase)
from pyquil.gates import I,PHASE
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

# Añadir al programa la puerta PHASE con ángulo π/4 aplicada al qubit 0
# PHASE(θ) modifica la fase del estado |1⟩ multiplicándola por e^(iθ)
prog.inst(PHASE(math.pi/4,0))

# Ejecutar el programa completo (I + PHASE) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar PHASE(π/4, 0)
# Resultado esperado: (1+0j)|0⟩  (PHASE no afecta a |0⟩, solo a |1⟩)
# La fase global no es observable, por lo que el estado sigue siendo |0⟩
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de PHASE):
(1+0j)|0⟩

EXPLICACIÓN: Como el qubit está en el estado |0⟩, la puerta PHASE no tiene efecto visible
porque PHASE solo modifica la componente |1⟩ del estado cuántico. En este caso, la amplitud
de |1⟩ es 0, por lo que no hay cambio observable en la función de onda.
"""
