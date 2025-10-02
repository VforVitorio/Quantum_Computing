# Resumen: Introducción a PyQuil y Estados de Bell

## Conceptos Fundamentales de Computación Cuántica

### Qubits vs Bits Clásicos
Los qubits son la unidad básica de información cuántica. A diferencia de los bits clásicos que solo pueden estar en 0 o 1, los qubits pueden estar en:
- Estado |0⟩ (equivalente al 0 clásico)
- Estado |1⟩ (equivalente al 1 clásico)
- **Superposición**: una combinación de ambos estados simultáneamente

La analogía útil es pensar en una moneda: normalmente está cara o cruz, pero cuando la lanzas al aire y está girando, está en "ambos estados a la vez" hasta que cae.

### Inicialización del Sistema
En PyQuil, todos los qubits siempre empiezan en el estado |0⟩. Esta es una regla fundamental que nunca cambia.

## Las Puertas Cuánticas Básicas

### Puerta X (NOT Cuántico)
La puerta X es el equivalente cuántico de la puerta NOT clásica:
- X|0⟩ → |1⟩ (voltea 0 a 1)
- X|1⟩ → |0⟩ (voltea 1 a 0)

En código PyQuil: `X(0)` aplica la puerta X al qubit 0.

### Puerta H (Hadamard)
La puerta H crea superposición, es decir, "lanza la moneda al aire":
- H|0⟩ → crea superposición (|0⟩ + |1⟩)/√2
- H|1⟩ → crea superposición (|0⟩ - |1⟩)/√2

**Descubrimiento importante**: H no crea la misma superposición para |0⟩ y |1⟩. La diferencia está en el signo (+ vs -), que representa una "fase cuántica" diferente.

### Puerta CNOT (Control-NOT)
La puerta CNOT opera sobre dos qubits:
```
CNOT(control, target)
```

**Regla**: Si el qubit control está en |1⟩, entonces voltea el qubit target. Si el control está en |0⟩, no hace nada.

Ejemplo: `CNOT(0,1)` usa el qubit 0 como control y el qubit 1 como target.

### Puerta Z (Cambio de Fase)
La puerta Z es la más abstracta:
- Z|0⟩ = |0⟩ (no cambia nada)
- Z|1⟩ = -|1⟩ (añade fase negativa invisible)

**Característica clave**: Si mides un qubit individualmente después de aplicar Z, obtienes los mismos resultados que sin Z. Sin embargo, Z afecta cómo el qubit interactúa con otros qubits, especialmente en sistemas entrelazados.

## El Efecto de H después de X

Cuando aplicas una secuencia X seguida de H:
```python
X(0)  # |0⟩ → |1⟩
H(0)  # |1⟩ → (|0⟩ - |1⟩)/√2
```

Esto crea una superposición con fase negativa, diferente a aplicar solo H sobre |0⟩. Experimentalmente, esto puede producir distribuciones de resultados ligeramente diferentes cuando hay entrelazamiento, debido a efectos de interferencia cuántica.

## Entrelazamiento Cuántico

El entrelazamiento es un fenómeno donde dos qubits quedan "conectados" de tal manera que medir uno instantáneamente determina el estado del otro, sin importar la distancia entre ellos.

**Características del entrelazamiento:**
- Los resultados individuales son aleatorios
- Los resultados están perfectamente correlacionados
- Einstein lo llamaba "acción fantasmal a distancia"

### Creación de Entrelazamiento
El patrón básico para crear entrelazamiento:
1. Poner un qubit en superposición con H
2. Usar CNOT para correlacionar ambos qubits

Ejemplo básico:
```python
H(0)        # Crear superposición en qubit 0
CNOT(0,1)   # Entrelazar qubit 0 con qubit 1
```

## Estados de Bell

Los estados de Bell son los cuatro estados de máximo entrelazamiento posible entre dos qubits. Son estados especiales donde los qubits están completamente correlacionados.

### Los Cuatro Estados de Bell

**|Φ⁺⟩ = (|00⟩ + |11⟩)/√2**
- Circuito: H(0) → CNOT(0,1)
- Resultados: 50% [0,0] y 50% [1,1]
- Nunca obtienes [0,1] o [1,0]

**|Φ⁻⟩ = (|00⟩ - |11⟩)/√2**
- Similar al anterior pero con fase negativa
- Experimentalmente da los mismos resultados que |Φ⁺⟩
- La diferencia de fase afecta interacciones con otras operaciones

**|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2**
- Resultados: 50% [0,1] y 50% [1,0]
- Nunca obtienes [0,0] o [1,1]

**|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2**
- Similar al anterior pero con fase negativa

### ¿Por qué Son Especiales?

Los estados de Bell representan correlación perfecta entre qubits. En estados entrelazados normales, los qubits pueden tener correlaciones parciales, pero los estados de Bell tienen la máxima correlación posible.

**Característica distintiva**: En un estado de Bell, si mides un qubit y obtienes un resultado específico, automáticamente sabes con certeza absoluta qué resultado obtendrás al medir el segundo qubit.

## Configuración del Entorno PyQuil

### Servicios Necesarios
Antes de ejecutar cualquier programa PyQuil, es fundamental lanzar dos servicios en terminales separados:

**Terminal 1:**
```bash
quilc -P -S
```
Este comando inicia el compilador cuántico (quilc) que traduce tu código PyQuil a instrucciones optimizadas para el hardware cuántico o simulador.

**Terminal 2:**
```bash
qvm -S
```
Este comando inicia la máquina virtual cuántica (QVM) que simula el comportamiento de un procesador cuántico real.

**¿Por qué dos terminales separados?** Estos son dos servicios independientes que trabajan en conjunto. El compilador traduce tu código, mientras que el simulador ejecuta las instrucciones compiladas. Mantenerlos en terminales separados te permite ver los mensajes de estado de cada servicio y reiniciar uno sin afectar el otro si surgen problemas.

Una vez que ambos servicios están corriendo, puedes ejecutar tus programas PyQuil desde un tercer terminal o desde tu entorno de desarrollo preferido.

## Estructura del Código PyQuil

### Declaración de Memoria Clásica
```python
Declare("ro", "BIT", 2)  # Crea 2 espacios de memoria clásica
```

### Medición
```python
MEASURE(0, ("ro", 0))  # Mide qubit 0, guarda en ro[0]
MEASURE(1, ("ro", 1))  # Mide qubit 1, guarda en ro[1]
```

### Ejecución
```python
qvm = get_qc('9q-square-qvm')  # Simulador cuántico virtual
result = qvm.run(qvm.compile(prog))
measurements = result.readout_data['ro']  # Acceder a resultados
```

## Análisis de los Programas de la Práctica

### S01P01.py: Estado Determinista
```python
X(0)        # |00⟩ → |10⟩
CNOT(0,1)   # |10⟩ → |11⟩
```
**Resultado**: Siempre [1,1] (determinista, no aleatorio)

### S01P02.py: Primer Estado de Bell |Φ⁺⟩
```python
H(0)        # Crear superposición
CNOT(0,1)   # Crear entrelazamiento
```
**Resultado**: 50% [0,0] y 50% [1,1] (aleatorio pero correlacionado)

### S01P03.py: Estado de Bell con Fase
```python
X(0)        # |00⟩ → |10⟩
H(0)        # |10⟩ → superposición con fase negativa
CNOT(0,1)   # Crear entrelazamiento
```
**Resultado**: Distribución ligeramente diferente debido a la fase negativa

### S01P05.py: Estado de Bell |Ψ⁺⟩
```python
H(0)        # Crear superposición en qubit 0
X(1)        # Voltear qubit 1 a |1⟩
Z(0)        # Ajuste de fase en qubit 0
Z(1)        # Ajuste de fase en qubit 1
CNOT(0,1)   # Crear entrelazamiento final
```
**Resultado**: 50% [0,1] y 50% [1,0] (patrón complementario al primer estado de Bell)

## Conceptos Clave para Recordar

**Superposición**: Un qubit puede estar en múltiples estados simultáneamente hasta que se mide.

**Entrelazamiento**: Dos qubits pueden estar tan correlacionados que medir uno instantáneamente determina el estado del otro.

**Fases Cuánticas**: Propiedades "invisibles" de los qubits que no afectan mediciones individuales pero sí afectan interacciones entre qubits.

**Colapso Cuántico**: El acto de medir fuerza a un sistema cuántico a "elegir" un estado definitivo, destruyendo la superposición.

**Estados de Bell**: Los cuatro estados de máximo entrelazamiento posible, representando las correlaciones más fuertes que puede tener un sistema de dos qubits.