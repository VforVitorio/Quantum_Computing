"""
PROGRAMA: Demostración de la puerta cuántica S sobre |1⟩
==========================================
Este programa demuestra el efecto de la puerta S sobre un qubit inicializado en |1⟩.
La puerta S es una puerta de fase especial que aplica un cambio de fase de π/2 radianes.
Es equivalente a PHASE(π/2).
Matriz S: [[1, 0], [0, i]]  (donde i = e^(iπ/2))
La puerta S también se conoce como "raíz cuadrada de Z".
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: X (NOT) y S (puerta de fase π/2)
from pyquil.gates import X,S
# Importar el simulador de función de onda para ejecutar circuitos cuánticos
from pyquil.api import WavefunctionSimulator

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

# Añadir al programa la puerta S aplicada al qubit 0
# S multiplica la componente |1⟩ por i (equivalente a e^(iπ/2))
# S|0⟩ = |0⟩  (no afecta al estado |0⟩)
# S|1⟩ = i|1⟩  (añade fase de 90° al estado |1⟩)
prog.inst(S(0))

# Ejecutar el programa completo (X + S) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar S(0)
# Resultado esperado: (0+1j)|1⟩ = i|1⟩  (fase de 90° aplicada a |1⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de X):
(1+0j)|1⟩

Segunda impresión (después de S):
(0+1j)|1⟩  ó  1j|1⟩

EXPLICACIÓN: Como el qubit está en el estado |1⟩, la puerta S multiplica su amplitud
por i (el número imaginario). Esto representa una rotación de fase de 90° en el plano complejo.
El estado pasa de |1⟩ a i|1⟩, que se representa como (0+1j)|1⟩.
Matemáticamente: S|1⟩ = i|1⟩, donde i = e^(iπ/2) = cos(π/2) + i·sin(π/2) = 0 + 1i.
"""
