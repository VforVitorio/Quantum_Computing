# Ejecutar en dos terminales antes de ejecutar el programa: quilc -P -S | qvm -S
# Version pyquil: pyquil==3.2.1

from pyquil import get_qc, Program  # Programa y compilador
from pyquil.gates import I  # Puertas

# Tipo de runner: función de onda o medida concreta en tiempo concreto
from pyquil.api import WavefunctionSimulator


# Definición del programa
# Construir un ordenador cuántico de 1 qbit sobre el que se va a ejecutar la función identidad
prog = Program(I(0))

# Ejecución del simulador
qvm = WavefunctionSimulator()

result = qvm.wavefunction(prog)
print(result)

"""
SALIDA ESPERADA:
================
(1+0j)|0⟩

EXPLICACIÓN:
La puerta identidad I no modifica el estado del qubit. Como el estado inicial
por defecto es |0⟩, la función de onda resultante es (1+0j)|0⟩, que representa
el estado |0⟩ con amplitud compleja 1+0j (probabilidad 100% de medir 0).
"""
