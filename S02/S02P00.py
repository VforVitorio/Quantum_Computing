"""
PROGRAMA: Simulación de lanzamiento de moneda cuántica
==========================================
Este programa demuestra el uso de la puerta Hadamard (H) para crear superposición
y simular el lanzamiento de una moneda cuántica. La puerta H transforma el estado
|0⟩ en una superposición equitativa (|0⟩ + |1⟩)/√2.
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar la puerta Hadamard (H) que crea superposición
from pyquil.gates import H

# Crear un programa cuántico que aplica la puerta Hadamard al qubit 0
# H(0) transforma |0⟩ en (|0⟩ + |1⟩)/√2, creando una superposición equitativa
prog = Program(H(0))
# Declarar un registro clásico 'ro' (read-out) para almacenar el resultado de la medición
ro = prog.declare('ro')

# Imprimir el programa cuántico (muestra las instrucciones del circuito)
print(prog)

# Medir el qubit 0 y almacenar el resultado en ro[0]
# La medición colapsa la superposición a |0⟩ o |1⟩ con 50% de probabilidad cada uno
prog.measure(0,ro[0])

# Obtener una instancia del simulador cuántico (9q-square-qvm)
qvm = get_qc('9q-square-qvm')
# Ejecutar el programa compilado y obtener el resultado de la medición
result = qvm.run(qvm.compile(prog), 0).get_register_map().get("ro")

# Imprimir el resultado de la medición (0 o 1)
print(result[0])
# Interpretar el resultado como cara (0) o cruz (1)
if result[0] == 0:
 print("cara")
else:
 print("cruz")

"""
SALIDA ESPERADA:
================
El programa imprime:
1. El circuito cuántico
2. El resultado de la medición (0 o 1)
3. "cara" si el resultado es 0, "cruz" si es 1

EXPLICACIÓN:
La puerta Hadamard crea una superposición perfecta del qubit, donde al medir
se obtiene 0 o 1 con igual probabilidad (50% cada uno). Esto simula un
lanzamiento de moneda cuántico perfectamente justo.
"""
