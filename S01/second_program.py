from pyquil import get_qc, Program
from pyquil.gates import CNOT, H, MEASURE
from pyquil.quilbase import Declare

prog = Program(
    Declare("ro", "BIT", 2),
    H(0),
    CNOT(0, 1),
    MEASURE(0, ("ro", 0)),
    MEASURE(1, ("ro", 1)),
).wrap_in_numshots_loop(100)

qvm = get_qc('9q-square-qvm')
result = qvm.run(qvm.compile(prog)).readout_data.get("ro")
for res in result:
    print(res)

"""
SALIDA ESPERADA:
================
100 líneas con mediciones, aproximadamente:
[0 0]  (≈50 veces)
[1 1]  (≈50 veces)

EXPLICACIÓN:
Este programa crea un estado de Bell |Φ⁺⟩ = (|00⟩ + |11⟩)/√2 mediante H y CNOT.
Los qubits quedan perfectamente entrelazados: cuando se mide el qubit 0, el qubit 1
siempre tendrá el mismo valor. Las probabilidades son 50% para [0,0] y 50% para [1,1].
Nunca se observará [0,1] ni [1,0] debido al entrelazamiento cuántico.
"""
