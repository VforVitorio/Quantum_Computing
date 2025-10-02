# Práctica: Las Puertas de Pauli

## Configuración Inicial

```bash
# Ejecutar en dos terminales antes de ejecutar el programa:
quilc -P -S
qvm -S

# Version pyquil: pyquil==3.2.1
```

---

## 📋 FASE 1: CONFIGURACIÓN DEL ENTORNO

**Objetivo** : Adaptar el código base de la práctica anterior para trabajar con las puertas de Pauli

### Tareas:

#### 1. Configurar el entorno

- Ejecutar en terminales: `quilc -P -S` y `qvm -S`
- Importar librerías necesarias para esta práctica
- Verificar versión pyquil==3.2.1

#### 2. Adaptar el código base

- Partir del código de la práctica 1 (que usa puerta I)
- Modificar imports para incluir puertas X, Y, Z
- Preparar estructura base para usar WavefunctionSimulator
- Crear función base que permita cambiar el estado inicial

#### 3. Preparar funciones auxiliares

- Función para imprimir función de onda de forma clara
- Función para crear estado |1⟩ inicial (usando puerta X sobre |0⟩)
- Función template para el flujo: estado inicial → wavesimulator → puerta → wavesimulator

---

## 📋 FASE 2: IMPLEMENTACIÓN DE LAS 6 PUERTAS BÁSICAS

**Objetivo** : Crear los 6 programas según el documento

### Los 6 programas son:

1. **Programa X con |0⟩**
2. **Programa X con |1⟩**
3. **Programa Z con |0⟩**
4. **Programa Z con |1⟩**
5. **Programa Y con |0⟩**
6. **Programa Y con |1⟩**

### Flujo para cada programa (basado en el código de la práctica 1):

1. `prog = Program()` → definir programa con estado inicial
2. `result = qvm.wavefunction(prog)` → **ANTES** de la puerta
3. `prog.inst(PUERTA(0))` → añadir puerta
4. `result = qvm.wavefunction(prog)` → **DESPUÉS** de la puerta
5. Comparar resultados

### Estructura de cada programa:

```python
# Definición del programa con estado inicial
prog = Program()
# [Preparar estado inicial si es |1⟩]

# Ejecución ANTES de aplicar la puerta
qvm = WavefunctionSimulator()
result_before = qvm.wavefunction(prog)
print(f"Estado ANTES de aplicar puerta: {result_before}")

# Aplicar la puerta usando inst()
prog.inst(PUERTA(0))

# Ejecución DESPUÉS de aplicar la puerta
result_after = qvm.wavefunction(prog)
print(f"Estado DESPUÉS de aplicar puerta: {result_after}")
```

---

## 📋 FASE 3: ANÁLISIS DE RESULTADOS

**Objetivo** : Comparar y analizar los efectos de cada puerta

### Tareas:

- Comparar funciones de onda antes/después para cada puerta
- Verificar comportamientos teóricos esperados
- Documentar observaciones

### Tabla de resultados esperados:

| Puerta | Estado Inicial | Estado Final | Observación |
| ------ | -------------- | ------------ | ----------- |
| X      |                | 0⟩           |             |
| X      |                | 1⟩           |             |
| Z      |                | 0⟩           |             |
| Z      |                | 1⟩           | -           |
| Y      |                | 0⟩           | i           |
| Y      |                | 1⟩           | -i          |

---

## 📋 FASE 4: CONSTRUCCIÓN MANUAL DE PUERTA Y

**Objetivo** : Demostrar cómo construir Y usando combinaciones y el número imaginario `1j`

### Pregunta del ejercicio:

_"La puerta Y se puede construir de forma particular con combinación de resultados de ejecución del simulador sobre diferentes puertas, particularmente de sus amplitudes, además del número imaginario en Python (1j). ¿Cómo se haría?"_

### Los 2 programas finales:

1. **Construcción manual Y|0⟩** → debe dar como resultado `i|1⟩`
2. **Construcción manual Y|1⟩** → debe dar como resultado `-i|0⟩`

### Matrices de referencia:

```
Y|0⟩ = (0  -i) (1) = (0)  = i|1⟩
       (i   0) (0)   (-i)

Y|1⟩ = (0  -i) (0) = (-i) = -i|0⟩
       (i   0) (1)   (0)
```

---

## Resumen de Programas

| Fase | Programas | Descripción                                 |
| ---- | --------- | ------------------------------------------- |
| 1    | 0         | Solo configuración del entorno              |
| 2    | 6         | X(2) + Z(2) + Y(2) con estados              |
| 3    | 0         | Solo análisis de resultados                 |
| 4    | 2         | Construcción manual de Y para ambos estados |

**Total: 8 programas**
