"""
PROGRAMA: Demostración de la puerta cuántica RX sobre |1⟩
==========================================
Este programa demuestra el efecto de la puerta RX sobre un qubit inicializado en |1⟩.
La puerta RX realiza una rotación del qubit alrededor del eje X de la esfera de Bloch.
Matriz RX(θ): [[cos(θ/2), -i·sin(θ/2)], [-i·sin(θ/2), cos(θ/2)]]
En este caso, θ = π/2, lo que produce una rotación de 90° sobre el eje X.
Esta puerta, a diferencia de PHASE/S/T, SÍ cambia las amplitudes de |0⟩ y |1⟩.
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: X (NOT) y RX (rotación sobre X)
from pyquil.gates import X,RX
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

# Añadir al programa la puerta RX con ángulo π/2 aplicada al qubit 0
# RX(π/2) rota el estado del qubit 90° alrededor del eje X
# RX(π/2)|1⟩ = -i·sin(π/4)|0⟩ + cos(π/4)|1⟩ ≈ -0.707i|0⟩ + 0.707|1⟩
# Esta puerta crea una superposición cuántica con componentes imaginarias
prog.inst(RX(math.pi/2,0))

# Ejecutar el programa completo (X + RX) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar RX(π/2, 0)
# Resultado esperado: (0-0.707j)|0⟩ + (0.707+0j)|1⟩
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de X):
(1+0j)|1⟩

Segunda impresión (después de RX):
(0-0.707j)|0⟩ + (0.707+0j)|1⟩  ó  aproximadamente (0-0.7071j)|0⟩ + (0.7071+0j)|1⟩

EXPLICACIÓN: La puerta RX(π/2) transforma el estado |1⟩ en una superposición cuántica.
El resultado es -i·sin(π/4)|0⟩ + cos(π/4)|1⟩ ≈ -0.707i|0⟩ + 0.707|1⟩.
Las probabilidades de medir |0⟩ o |1⟩ son iguales: |-0.707i|² = |0.707|² = 0.5 = 50%.
Nótese que la componente |0⟩ ahora tiene amplitud, a diferencia de las puertas de fase.
La componente |0⟩ tiene un factor -i (fase negativa imaginaria).
RX es una puerta de rotación fundamental en computación cuántica.
"""
