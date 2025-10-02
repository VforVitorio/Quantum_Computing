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
