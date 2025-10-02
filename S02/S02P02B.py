"""
PROGRAMA: Simulación de 4 monedas cuánticas usando measure_all()
==========================================
Este programa demuestra el uso del método measure_all() como alternativa a medir
cada qubit individualmente. Se aplica la puerta Hadamard a 4 qubits diferentes,
creando un estado con 16 posibles resultados equiprobables. El método measure_all()
mide automáticamente todos los qubits que han sido manipulados en el circuito.

Matriz Hadamard: H = (1/√2) * [[1, 1], [1, -1]]
Estado inicial: |0000⟩
Después de H⊗H⊗H⊗H: |ψ⟩ = (1/4) Σ|i⟩ para i ∈ {0000, 0001, ..., 1111}
"""

# Importar la función para obtener un computador cuántico y el tipo Program
from pyquil import get_qc, Program
# Importar la puerta Hadamard (H) que crea superposición cuántica
from pyquil.gates import H

# Crear un programa cuántico que aplica H a los qubits 0, 1, 2 y 3
# Cada H crea una superposición independiente en cada qubit
# wrap_in_numshots_loop(50) configura el circuito para ejecutarse 50 veces
prog = Program(H(0),H(1),H(2),H(3)).wrap_in_numshots_loop(50)
# Declarar un registro clásico 'ro' de tipo BIT con 4 posiciones (una para cada qubit)
ro = prog.declare('ro','BIT',4)

# Imprimir el programa cuántico completo con el loop de 50 shots
print(prog)

# Medir todos los qubits automáticamente usando measure_all()
# Este método es equivalente a llamar prog.measure(i, ro[i]) para cada qubit usado
# Detecta automáticamente los qubits 0, 1, 2, 3 y los mide en el registro ro
prog.measure_all()

# Obtener una instancia del simulador cuántico (9q-square-qvm)
qvm = get_qc('9q-square-qvm')
# Ejecutar el programa compilado 50 veces y obtener todos los resultados
# result es una lista de 50 arrays, cada uno con 4 valores [ro[0], ro[1], ro[2], ro[3]]
result = qvm.run(qvm.compile(prog), 0).get_register_map().get("ro")

# Inicializar contadores para cara (0) y cruz (1)
cara = 0
cruz = 0
# Iterar sobre cada resultado de las 50 ejecuciones
for res in result:
    # Imprimir el resultado de los 4 qubits (ej: [0 1 0 1])
    print(res)

    # Contar el resultado del qubit 0
    if res[0] == 0:
        cara += 1
    else:
        cruz += 1

    # Contar el resultado del qubit 1
    if res[1] == 0:
        cara += 1
    else:
        cruz += 1

    # Contar el resultado del qubit 2
    if res[2] == 0:
        cara += 1
    else:
        cruz += 1

    # Contar el resultado del qubit 3
    if res[3] == 0:
        cara += 1
    else:
        cruz += 1

# Imprimir el total de caras obtenidas (máximo 200: 4 qubits × 50 ejecuciones)
print(cara)
# Imprimir el total de cruces obtenidas (máximo 200: 4 qubits × 50 ejecuciones)
print(cruz)
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
1. El circuito cuántico con 4 Hadamards y el loop de 50 shots
2. 50 líneas con arrays de 4 valores, cada uno mostrando el resultado de los 4 qubits
   Ejemplo: [0 1 1 0], [1 0 0 1], etc.
3. Total de caras (debería ser aproximadamente 100)
4. Total de cruces (debería ser aproximadamente 100)
5. El ganador del juego: "gana A", "gana B" o "empate"

Ejemplo de salida:
[1 0 1 0]
[0 1 0 1]
[1 1 1 0]
... (47 líneas más)
98
102
gana B

EXPLICACIÓN: El método measure_all() simplifica el código al medir automáticamente
todos los qubits que han sido manipulados, eliminando la necesidad de escribir
múltiples instrucciones prog.measure() individuales. El comportamiento es idéntico
a S02P02A.py: cada qubit tiene 50% de probabilidad de medir 0 o 1, resultando en
200 mediciones totales (50 ejecuciones × 4 qubits). Estadísticamente esperamos
aproximadamente 100 caras y 100 cruces, pero la variación puede favorecer a cualquier
jugador.
"""
