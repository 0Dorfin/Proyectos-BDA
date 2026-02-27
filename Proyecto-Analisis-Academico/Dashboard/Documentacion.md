# Construcción del Dashboard de Análisis Académico

**Objetivo:** Diseñar, modelar y construir un Dashboard en Power BI que permita evaluar de forma visual el rendimiento académico del alumnado.

### 6.1. Construcción del Dashboard de Analisis Académico

## Páginas del Dashboard

### 1. General

**Filtros aplicables**: Año

**Métricas (KPIs)**:
- **Nota media junto a la nota máxima**
- **Porcentaje de alumnos aprobados junto a la distribución de hombres y mujeres**
- **Alumnos con todo aprobado junto a los que son de mañana o tarde**
- **Total de alumnos evaluados junto a la distribución de hombres y mujeres**

**Gráficos**:
- **Combinado (Líneas y Columnas)**: Nota media y total de alumnos por curso.
- **Columnas agrupadas**: Evolución histórica de la nota media por familia profesional.
- **Histograma / Cascada**: Distribución general de las notas.

---

### 2. Familia

**Filtros aplicables**: Año, Familia, Curso, Grado, Turno, Sexo y Evaluación.

**Métricas (KPIs)**:
- **Nota media**
- **Porcentaje de alumnos aprobados**
- **Porcentaje de alumnos con todo aprobado**
- **Total de alumnos evaluados (o tasa de abandono)**

**Gráficos**:
- **Líneas**: Evolución de la nota media (comparativa: familia seleccionada vs. media global del centro).
- **Combinado (Líneas y Columnas)**: Rendimiento por curso (nota media y % de aprobados).
- **Columnas agrupadas**: Nota media desglosada por curso y sexo.
- **Barras horizontales**: Módulos críticos (tasa de suspensos por cada módulo de la familia).

---

### 3. Módulos

**Filtros aplicables**: Año, Familia, Curso, Grado, Módulo, Turno, Sexo y Evaluación.

**Métricas (KPIs)**:
- **Nota media**
- **Número de alumnos evaluados**
- **Porcentaje de aprobados**
- **Tasa de suspensos**

**Gráficos**:
- **Dispersión**: Priorización de módulos (tasa de suspensos vs. nota media, tamaño por número de evaluados).
- **Histograma**: Distribución del número de alumons evaluados por rango de notas.
- **Líneas**: Evolución histórica de la nota media por año.
- **Columnas agrupadas**: Nota media comparada por turno y sexo.

---

### 4. Perfil del Alumnado

**Filtros aplicables**: Año, Familia, Curso, Grado, Turno, Sexo y Evaluación.

**Métricas (KPIs)**:
- **Total de alumnos**
- **Porcentaje de mujeres**
- **Tasa de abandono**
- **Edad media**

**Gráficos**:
- **Barras horizontales**: Distribución del volumen de alumnado por familia profesional.
- **Pirámide poblacional**: Distribución por rangos de edad y sexo.
- **Donut**: Proporción total de alumnos por sexo.
- **Barras horizontales**: Volumen de alumnos según su estado de matrícula.

---

### 3. Columnas creadas para cada Tabla

### Tabla de Hechos (`Fact_Calificaciones`)

- Rango Notas

### Tabla de Dimensión (`Dim_Alumnos`)

- Edad
- Estado Matrícula texto
- Rango Edad

---

### 2. Medidas creadas para cada Tabla

### Tabla de Hechos (`Fact_Calificaciones`)

- % Aprobados Hombres
- % Aprobados Mujeres
- % Alumnos Todo Aprobado  
- % aprobados  
- Alumnos Aprobados  
- Alumnos Evaluados  
- Alumnos Todo Aprobado  
- Tasa Suspenso Módulo
- Nº Evaluados  
- Nota Maxima  
- Nota media    
- Promedio Calificaciones  
- Rango Notas  
- Tasa Suspensos  
- Total Aprobados  
- Total Estudiantes  
- Total Notas

---

### Tabla de Dimensión (`Dim_Alumnos`)

- % Abandono  
- % Mujeres  
- Alumnas  
- Alumnos  
- Edad  
- Edad Media  
- Hombres  
- Mañana  
- Mujeres  
- Tarde  
- Total Alumnos  
---

### Tabla de Dimensión (`Dim_Modulos`)

- Nota Media Centro
