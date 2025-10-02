"""
PROGRAMA: Demostración de la puerta cuántica S (Phase Gate)
==========================================
Este programa demuestra el efecto de la puerta S sobre un qubit inicializado en |0⟩.
La puerta S es una puerta de fase especial que aplica un cambio de fase de π/2 radianes.
Es equivalente a PHASE(π/2).
Matriz S: [[1, 0], [0, i]]  (donde i = e^(iπ/2))
La puerta S también se conoce como "raíz cuadrada de Z".
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad) y S (puerta de fase π/2)
from pyquil.gates import I,S
# Importar el simulador de función de onda para ejecutar circuitos cuánticos
from pyquil.api import WavefunctionSimulator

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

# Añadir al programa la puerta S aplicada al qubit 0
# S multiplica la componente |1⟩ por i (equivalente a e^(iπ/2))
# S|0⟩ = |0⟩  (no afecta al estado |0⟩)
# S|1⟩ = i|1⟩  (añade fase de 90° al estado |1⟩)
prog.inst(S(0))

# Ejecutar el programa completo (I + S) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar S(0)
# Resultado esperado: (1+0j)|0⟩  (S no afecta a |0⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de S):
(1+0j)|0⟩

EXPLICACIÓN: Como el qubit está en el estado |0⟩, la puerta S no tiene efecto visible
porque S solo modifica la componente |1⟩ del estado cuántico (multiplicándola por i).
En este caso, la amplitud de |1⟩ es 0, por lo que no hay cambio observable.
La puerta S es un caso particular de PHASE con θ = π/2.
"""
