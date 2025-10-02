from pyquil import get_qc, Program
from pyquil.gates import H, Z, MEASURE
from pyquil.quilbase import Declare

# Circuito 1: H en q0, medición en ambos
prog1 = Program(
    Declare("ro", "BIT", 2),
    H(0),
    MEASURE(0, ("ro", 0)),
    MEASURE(1, ("ro", 1))
).wrap_in_numshots_loop(100)

# Circuito 2: H en q0, dos mediciones en q1
prog2 = Program(
    Declare("ro", "BIT", 3),  # 3 bits para 3 mediciones
    H(0),
    MEASURE(1, ("ro", 0)),    # Primera medición q1
    MEASURE(1, ("ro", 1)),    # Segunda medición q1
    MEASURE(0, ("ro", 2))     # Medición q0
).wrap_in_numshots_loop(100)

# Circuito 3: H+Z en q0, Z en q1, mediciones
prog3 = Program(
    Declare("ro", "BIT", 3),
    H(0),
    Z(0),
    Z(1),
    MEASURE(1, ("ro", 0)),    # Primera medición q1
    MEASURE(1, ("ro", 1)),    # Segunda medición q1
    MEASURE(0, ("ro", 2))     # Medición q0
).wrap_in_numshots_loop(100)

# Ejecutar cualquier circuito
qvm = get_qc('9q-square-qvm')

print("Circuito 1:")
result1 = qvm.run(qvm.compile(prog1)).readout_data.get("ro")
for i, res in enumerate(result1[:5]):  # Solo primeros 5 resultados
    print(f"Shot {i+1}: q0={res[0]}, q1={res[1]}")

print("\nCircuito 2:")
result2 = qvm.run(qvm.compile(prog2)).readout_data.get("ro")
for i, res in enumerate(result2[:5]):
    print(f"Shot {i+1}: q1_med1={res[0]}, q1_med2={res[1]}, q0={res[2]}")

print("\nCircuito 3:")
result3 = qvm.run(qvm.compile(prog3)).readout_data.get("ro")
for i, res in enumerate(result3[:5]):
    print(f"Shot {i+1}: q1_med1={res[0]}, q1_med2={res[1]}, q0={res[2]}")

"""
SALIDA ESPERADA:
================
Circuito 1:
Shot 1: q0=0 (o 1), q1=0
Shot 2: q0=1 (o 0), q1=0
...
El qubit 0 estará en superposición (50% de 0 o 1), el qubit 1 siempre será 0.

Circuito 2:
Shot 1: q1_med1=0, q1_med2=0, q0=0 (o 1)
Shot 2: q1_med1=0, q1_med2=0, q0=1 (o 0)
...
Las dos mediciones consecutivas de q1 siempre darán 0 (colapso del estado).
El qubit 0 está en superposición.

Circuito 3:
Shot 1: q1_med1=0, q1_med2=0, q0=0 (o 1)
Shot 2: q1_med1=0, q1_med2=0, q0=1 (o 0)
...
Las compuertas Z introducen cambios de fase pero no afectan las probabilidades
de medición en la base computacional. El resultado es idéntico al Circuito 2.

EXPLICACIÓN:
Estos tres circuitos demuestran conceptos fundamentales:
- Circuito 1: Superposición de q0, q1 permanece en |0⟩ (no hay entrelazamiento)
- Circuito 2: Mediciones consecutivas del mismo qubit siempre dan el mismo resultado (colapso)
- Circuito 3: Las compuertas Z no cambian probabilidades en la base {|0⟩,|1⟩}, solo fases relativas
"""
