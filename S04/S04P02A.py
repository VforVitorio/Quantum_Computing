"""
PROGRAMA: Demostración de la puerta cuántica T (π/8 Gate)
==========================================
Este programa demuestra el efecto de la puerta T sobre un qubit inicializado en |0⟩.
La puerta T es una puerta de fase especial que aplica un cambio de fase de π/4 radianes.
Es equivalente a PHASE(π/4).
Matriz T: [[1, 0], [0, e^(iπ/4)]]  (donde e^(iπ/4) ≈ 0.707 + 0.707i)
La puerta T también se conoce como "raíz cuadrada de S" o "π/8 gate".
"""

# Importar la función para obtener un computador cuántico
from pyquil import get_qc, Program
# Importar las puertas cuánticas: I (Identidad) y T (puerta de fase π/4)
from pyquil.gates import I,T
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

# Añadir al programa la puerta T aplicada al qubit 0
# T multiplica la componente |1⟩ por e^(iπ/4) ≈ 0.707 + 0.707i
# T|0⟩ = |0⟩  (no afecta al estado |0⟩)
# T|1⟩ = e^(iπ/4)|1⟩  (añade fase de 45° al estado |1⟩)
prog.inst(T(0))

# Ejecutar el programa completo (I + T) y obtener la función de onda
result = qvm.wavefunction(prog)
# Imprimir la función de onda después de aplicar T(0)
# Resultado esperado: (1+0j)|0⟩  (T no afecta a |0⟩)
print(result)

"""
SALIDA ESPERADA:
================
Primera impresión (después de I):
(1+0j)|0⟩

Segunda impresión (después de T):
(1+0j)|0⟩

EXPLICACIÓN: Como el qubit está en el estado |0⟩, la puerta T no tiene efecto visible
porque T solo modifica la componente |1⟩ del estado cuántico (multiplicándola por e^(iπ/4)).
En este caso, la amplitud de |1⟩ es 0, por lo que no hay cambio observable.
La puerta T es un caso particular de PHASE con θ = π/4, y también es la raíz cuadrada de S.
Relación: T² = S  (aplicar T dos veces equivale a aplicar S una vez).
"""
