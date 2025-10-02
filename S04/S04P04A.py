"""
PROGRAMA: Demostración de la puerta cuántica RY (Rotación sobre eje Y)
==========================================
Este programa demuestra el efecto de la puerta RY sobre un qubit inicializado en |0⟩.
La puerta RY realiza una rotación del qubit alrededor del eje Y de la esfera de Bloch.
Matriz RY(θ): [[cos(θ/2), -sin(θ/2)], [sin(θ/2), cos(θ/2)]]
En este caso, θ = π/2, lo que produce una rotación de 90° sobre el eje Y.
A diferencia de RX, RY genera amplitudes REALES (sin componentes imaginarias).
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad) y RY (rotación sobre Y)
from pyquil.gates import I,RY
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

# Añadir al programa la puerta RY con ángulo π/2 aplicada al qubit 0
# RY(π/2) rota el estado del qubit 90° alrededor del eje Y
# RY(π/2)|0⟩ = cos(π/4)|0⟩ + sin(π/4)|1⟩ ≈ 0.707|0⟩ + 0.707|1⟩
# Esta puerta crea una superposición cuántica balanceada con amplitudes reales
prog.inst(RY(math.pi/2,0))

# Ejecutar el programa completo (I + RY) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar RY(π/2, 0)
# Resultado esperado: (0.707+0j)|0⟩ + (0.707+0j)|1⟩
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de RY):
(0.707+0j)|0⟩ + (0.707+0j)|1⟩  ó  aproximadamente (0.7071+0j)|0⟩ + (0.7071+0j)|1⟩

EXPLICACIÓN: La puerta RY(π/2) transforma el estado |0⟩ en una superposición cuántica balanceada.
El resultado es cos(π/4)|0⟩ + sin(π/4)|1⟩ ≈ 0.707|0⟩ + 0.707|1⟩.
Las probabilidades de medir |0⟩ o |1⟩ son iguales: |0.707|² = 0.5 = 50%.
DIFERENCIA CLAVE con RX: RY genera amplitudes REALES (sin componentes imaginarias),
mientras que RX genera amplitudes imaginarias. Ambas puertas crean superposiciones,
pero con diferentes fases en el espacio de Hilbert.
RY es especialmente útil para preparar estados de superposición simétricos.
"""
