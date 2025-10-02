"""
PROGRAMA: Simulación de 50 lanzamientos de moneda cuántica con wrap_in_numshots_loop
==========================================
Este programa demuestra cómo realizar múltiples mediciones (shots) de un circuito cuántico
usando el método wrap_in_numshots_loop(). Se simula un juego donde dos jugadores (A y B)
compiten: A gana con cara (0), B gana con cruz (1). La puerta Hadamard crea una
superposición equitativa |ψ⟩ = (|0⟩ + |1⟩)/√2.

Matriz Hadamard: H = (1/√2) * [[1, 1], [1, -1]]
H|0⟩ = (1/√2)(|0⟩ + |1⟩)
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar la puerta Hadamard (H) que crea superposición cuántica
from pyquil.gates import H

# Crear un programa cuántico que aplica H al qubit 0 y lo envuelve en un loop de 50 ejecuciones
# wrap_in_numshots_loop(50) configura el circuito para ejecutarse 50 veces automáticamente
prog = Program(H(0)).wrap_in_numshots_loop(50)
# Declarar un registro clásico 'ro' (read-out) para almacenar los resultados de las mediciones
ro = prog.declare('ro')

# Imprimir el programa cuántico completo con el loop de 50 shots
print(prog)

# Medir el qubit 0 y almacenar el resultado en ro[0]
# Esta medición se ejecutará 50 veces debido al wrap_in_numshots_loop
prog.measure(0,ro[0])

# Obtener una instancia del simulador cuántico (9q-square-qvm)
qvm = get_qc('9q-square-qvm')
# Ejecutar el programa compilado y obtener todos los resultados (50 mediciones)
# El resultado es una lista de 50 valores, cada uno con el resultado de una medición
result = qvm.run(qvm.compile(prog), 0).get_register_map().get("ro")

# Inicializar contadores para cara (0) y cruz (1)
cara = 0
cruz = 0
# Iterar sobre cada resultado de las 50 mediciones
for res in result:
    # Imprimir el resultado individual (será [0] o [1])
    print(res)
    # Si el resultado es 0, incrementar contador de cara (jugador A)
    if res[0] == 0:
        cara += 1
    # Si el resultado es 1, incrementar contador de cruz (jugador B)
    else:
        cruz += 1

# Determinar el ganador comparando los contadores
# Si hay más caras que cruces, gana el jugador A
if cara > cruz:
    print("gana A")
# Si hay igual cantidad de caras y cruces, es empate
elif cara == cruz:
    print("empate")
# Si hay más cruces que caras, gana el jugador B
else:
    print("gana B")

"""
SALIDA ESPERADA:
================
El programa imprime:
1. El circuito cuántico con el loop de 50 shots
2. 50 líneas, cada una mostrando el resultado de una medición: [0] o [1]
3. El ganador del juego: "gana A", "gana B" o "empate"

Ejemplo de salida:
[0]
[1]
[0]
[1]
... (46 líneas más)
gana A (o "gana B" o "empate")

EXPLICACIÓN: El método wrap_in_numshots_loop(50) optimiza la ejecución al configurar
el circuito para que se ejecute 50 veces en una sola llamada al simulador. Cada medición
colapsa la superposición a 0 o 1 con 50% de probabilidad. Estadísticamente, esperamos
aproximadamente 25 caras y 25 cruces, lo que resultaría en empate, pero la variación
estadística puede favorecer a cualquier jugador.
"""
