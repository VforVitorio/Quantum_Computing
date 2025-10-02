"""
PROGRAMA: Simulación de 50 lanzamientos de moneda cuántica con loop manual
==========================================
Este programa demuestra cómo realizar múltiples mediciones de un circuito cuántico
usando un loop for manual. A diferencia de wrap_in_numshots_loop(), aquí se ejecuta
el circuito 50 veces de forma explícita. Se simula un juego donde dos jugadores (A y B)
compiten: A gana con cara (0), B gana con cruz (1).

Matriz Hadamard: H = (1/√2) * [[1, 1], [1, -1]]
H|0⟩ = (1/√2)(|0⟩ + |1⟩)
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar la puerta Hadamard (H) que crea superposición cuántica
from pyquil.gates import H

# Crear un programa cuántico que aplica la puerta Hadamard al qubit 0
# H transforma |0⟩ en una superposición equitativa (|0⟩ + |1⟩)/√2
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

# Inicializar contadores para cara (0) y cruz (1)
cara = 0
cruz = 0
# Loop manual que ejecuta el circuito 50 veces
for number in range(50):
    # Ejecutar el programa compilado y obtener el resultado de esta medición individual
    # Cada iteración ejecuta el circuito completo desde el inicio
    result = qvm.run(qvm.compile(prog), 0).get_register_map().get("ro")
    # Imprimir el resultado individual (será [0] o [1])
    print(result[0])
    # Si el resultado es 0, incrementar contador de cara (jugador A)
    if result[0] == 0:
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
1. El circuito cuántico (sin loop visible en el código)
2. 50 líneas, cada una mostrando el resultado de una medición: [0] o [1]
3. El ganador del juego: "gana A", "gana B" o "empate"

Ejemplo de salida:
H 0
DECLARE ro BIT[1]
MEASURE 0 ro[0]
[0]
[1]
[1]
[0]
... (46 líneas más)
gana B (o "gana A" o "empate")

EXPLICACIÓN: Este enfoque ejecuta el circuito 50 veces usando un loop for explícito.
Cada iteración compila y ejecuta el circuito de forma independiente, lo que es menos
eficiente que wrap_in_numshots_loop() pero más flexible si se necesita procesar
resultados entre ejecuciones. Cada medición colapsa la superposición con 50% de
probabilidad para cada resultado. Estadísticamente, esperamos aproximadamente 25 caras
y 25 cruces, pero la variación aleatoria puede favorecer a cualquier jugador.
"""
