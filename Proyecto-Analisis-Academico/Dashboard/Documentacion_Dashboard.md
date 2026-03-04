# Construcción del Dashboard de Análisis de Cláusulas Abusivas

**Objetivo:** Diseñar y construir un Dashboard en Power BI que permita ver y comparar la presencia de cláusulas potencialmente abusivas en los términos de servicio de las principales plataformas de streaming.

## Páginas del Dashboard

### 1. General

**Filtros aplicables**: Periodo de años

**Métricas (KPIs)**

- **Total Cláusulas detectadas**: con comparativa con el periodo anterior.
- **Empresas Analizadas**: con total de archivos procesados.
- **Categoría Más Frecuente**: con recuento de detecciones.
- **Índice de Abusividad Promedio**: con comparativa con el periodo anterior.
- **Cláusulas Gravedad Alta**: con % sobre el total.
- **Cláusulas Gravedad Media**: con % sobre el total.

**Gráficos**
  
- **Donut**: Cláusulas por Categoría.
- **Tabla**: Ranking de Empresas.
  - Columnas: Empresa, Año, Cláusulas Abusivas, Categoría Predominante.
- **Líneas**: Evolución de Cláusulas Abusivas por Plataforma.

---

### 2. Análisis por Plataforma (Perfil de Abusividad)

**Filtros aplicables**: Periodo de años y Plataforma.

**Métricas (KPIs)**

- **Perfil General**
  - Total de cláusulas detectadas.
  - Índice de abusividad.
  - Categoría predominante.
- **Comparativa con el sector**
  - Diferencia contra el promedio del sector.
  - Ranking de abusividad.
  - Diferencia contra la tendencia del último año.

**Gráficos**

- **Líneas**: Evolución histórica contra el promedio.
- **Matriz / Barras Agrupadas**: Distribución de categorías por año
- **Tabla detallada con buscador**
  - Listado de cláusulas con:
    - Categoría
    - Gravedad
    - Año
    - Texto original

---

### 3. Rendimiento Pipeline (Logs)

**Métricas (KPIs)**

- **Pasos Ejecutados**: con tiempo total de ejecución.
- **Paso Más Lento**: con su duración.
- **Número de Fases**: con promedio de tiempo por paso.

**Gráficos**

- **Barras horizontales**: Duración por fase.
- **Barras horizontales**: Duración por paso específico.
- **Tabla de Logs con buscador**
  - Fase, paso, fecha inicio, fecha fin, tiempo de ejecución y tipo.

---

### 3. Columnas creadas para cada Tabla

### Tabla de Hechos: `fact_clausulas_detectadas`
- empresa_anio (para relacionarla don dim_empresas)
- Texto corto (para la tabla detallada)

### Tabla de Dimensión: `dim_empresas`
- empresa_anio
- Periodo
- orden_empresa

---

---

## 2. Medidas creadas para cada Tabla

### Tabla de Hechos `fact_clausulas_detectadas`

- **% Cláusulas por Categoría**
- **% del Total**
- **Categoría Más Frecuente**
- **Categoría_Top_Visual**
- **Cláusulas Cat Año**
- **Cláusulas Grav. Alta**
- **Cláusulas Grav. Media**
- **Cláusulas por Categoría**
- **Cláusulas por Categoría 2**
- **Detecciones_Cat_Top**
- **Indice Abusividad Prom 2**
- **Label Distribución**
- **Pct_Gravedad_Alta**
- **Pct_Gravedad_Media**
- **Perfil_Categoria_Top**
- **Perfil_Categoria_Top_Visual**
- **Perfil_Total_Clausulas**
- **Promedio del Sector**
- **Ranking de Abusividad**
- **Ref_Total_Clausulas_1**
- **Ref_Total_Clausulas**
- **Tendencia Último Año**
- **Total Cláusulas**
- **Total_Clausulas_Ant**
- **Variación_Clausulas_Pct**
- **Variación_Indice_Pct_2**

---

### Tabla de Dimensiones `dim_empresas`

- **Archivos_Procesados**
- **Categoría Predominante**
- **Empresas Analizadas**
- **Indice Abusividad Prom.**
- **Índice de Abusividad**
- **Indice_Abusividad_Ant**
- **Indice_Abusividad_Ant1**
- **Perfil_Indice_Abusividad**
- **Periodo_Anterior**
- **Plataforma**
- **Promedio Sector**
- **Subtitulo_Dashboard**
- **Título Perfil**
- **Total Cláusulas Detectadas**
- **Total_Clausulas_Ant1**
- **Variacion_Indice_Pct**

---

### Rendimiento Pipeline `tabla_log`

- **Duración**
- **Número de fases**
- **Paso más lento**
- **Pasos ejecutados**
- **Promedio por paso**
- **Tiempo de Ejecución**
