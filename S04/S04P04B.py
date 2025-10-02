"""
PROGRAMA: Demostración de la puerta cuántica RY sobre |1⟩
==========================================
Este programa demuestra el efecto de la puerta RY sobre un qubit inicializado en |1⟩.
La puerta RY realiza una rotación del qubit alrededor del eje Y de la esfera de Bloch.
Matriz RY(θ): [[cos(θ/2), -sin(θ/2)], [sin(θ/2), cos(θ/2)]]
En este caso, θ = π/2, lo que produce una rotación de 90° sobre el eje Y.
A diferencia de RX, RY genera amplitudes REALES (sin componentes imaginarias).
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: X (NOT) y RY (rotación sobre Y)
from pyquil.gates import X,RY
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

# Añadir al programa la puerta RY con ángulo π/2 aplicada al qubit 0
# RY(π/2) rota el estado del qubit 90° alrededor del eje Y
# RY(π/2)|1⟩ = -sin(π/4)|0⟩ + cos(π/4)|1⟩ ≈ -0.707|0⟩ + 0.707|1⟩
# Esta puerta crea una superposición cuántica con amplitudes reales
prog.inst(RY(math.pi/2,0))

# Ejecutar el programa completo (X + RY) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar RY(π/2, 0)
# Resultado esperado: (-0.707+0j)|0⟩ + (0.707+0j)|1⟩
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de X):
(1+0j)|1⟩

Segunda impresión (después de RY):
(-0.707+0j)|0⟩ + (0.707+0j)|1⟩  ó  aproximadamente (-0.7071+0j)|0⟩ + (0.7071+0j)|1⟩

EXPLICACIÓN: La puerta RY(π/2) transforma el estado |1⟩ en una superposición cuántica.
El resultado es -sin(π/4)|0⟩ + cos(π/4)|1⟩ ≈ -0.707|0⟩ + 0.707|1⟩.
Las probabilidades de medir |0⟩ o |1⟩ son iguales: |-0.707|² = |0.707|² = 0.5 = 50%.
Nótese que todas las amplitudes son REALES (sin componentes imaginarias).
La componente |0⟩ tiene signo negativo, lo que representa una diferencia de fase de 180°.
DIFERENCIA con RX: RY mantiene amplitudes reales, mientras que RX introduce factores i.
Esta propiedad hace que RY sea útil para ciertas operaciones de superposición.
"""
