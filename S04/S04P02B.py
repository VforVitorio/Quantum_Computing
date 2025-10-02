"""
PROGRAMA: Demostración de la puerta cuántica T sobre |1⟩
==========================================
Este programa demuestra el efecto de la puerta T sobre un qubit inicializado en |1⟩.
La puerta T es una puerta de fase especial que aplica un cambio de fase de π/4 radianes.
Es equivalente a PHASE(π/4).
Matriz T: [[1, 0], [0, e^(iπ/4)]]  (donde e^(iπ/4) ≈ 0.707 + 0.707i)
La puerta T también se conoce como "raíz cuadrada de S" o "π/8 gate".
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: X (NOT) y T (puerta de fase π/4)
from pyquil.gates import X,T
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

# Añadir al programa la puerta T aplicada al qubit 0
# T multiplica la componente |1⟩ por e^(iπ/4) ≈ 0.707 + 0.707i
# T|0⟩ = |0⟩  (no afecta al estado |0⟩)
# T|1⟩ = e^(iπ/4)|1⟩  (añade fase de 45° al estado |1⟩)
prog.inst(T(0))

# Ejecutar el programa completo (X + T) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar T(0)
# Resultado esperado: (0.707+0.707j)|1⟩  (fase e^(iπ/4) aplicada a |1⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de X):
(1+0j)|1⟩

Segunda impresión (después de T):
(0.707+0.707j)|1⟩  ó  aproximadamente (0.7071+0.7071j)|1⟩

EXPLICACIÓN: Como el qubit está en el estado |1⟩, la puerta T multiplica su amplitud
por e^(iπ/4) = cos(π/4) + i·sin(π/4) ≈ 0.707 + 0.707i.
Esto representa una rotación de fase de 45° en el plano complejo.
El estado pasa de |1⟩ a e^(iπ/4)|1⟩, que se representa como (0.707+0.707j)|1⟩.
La puerta T es fundamental en computación cuántica porque, junto con H y CNOT,
forma un conjunto universal de puertas cuánticas.
"""
