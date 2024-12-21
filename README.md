# Proyecto de Transformación de CSV

Este README describe los pasos necesarios para ejecutar un script de Python que transforma un archivo CSV con datos detallados (evento a evento) en otro CSV más resumido. Se explica la creación de un entorno virtual, la instalación de dependencias y la ejecución del script.

---

### Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Creación y Activación del Entorno Virtual](#creación-y-activación-del-entorno-virtual)
4. [Instalación de Dependencias](#instalación-de-dependencias)
5. [Ejecución del Script](#ejecución-del-script)
6. [¿Qué Hace el Script?](#qué-hace-el-script)
7. [Notas Finales](#notas-finales)

---

### Requisitos

- **Python 3.8** o superior (recomendado).
- **Pip** instalado (suele venir con la instalación de Python).
- Librería **pandas** (se instalará automáticamente con `pip install -r requirements.txt`).

---

### Estructura del Proyecto

- **`transformar.py`**  
  Contiene el código fuente del script que procesa los datos (no es necesario conocerlo en detalle para usarlo).
- **`requirements.txt`**  
  Lista de dependencias que se instalarán (principalmente `pandas`).

- **`README.md`**  
  El archivo que estás leyendo, con todas las instrucciones.

---

### Creación y Activación del Entorno Virtual

Para asegurarte de que no haya conflictos con otras librerías en tu sistema, es muy recomendable crear un entorno virtual. Realiza los siguientes pasos:

1. **Crear el entorno virtual** (dentro de la carpeta del proyecto):

   ```bash
   python -m venv .venv
   ```

   Esto generará una carpeta llamada `.venv` que contendrá el entorno virtual.

2. **Activar el entorno virtual:**

- En Windows:
  ```bash
   .venv\Scripts\activate
  ```
- En Linux/Mac:
  ```bash
   source .venv/bin/activate
  ```
  Luego de la activación, verás que tu consola muestra algo como `(.venv)` al inicio, indicando que estás dentro del entorno virtual.

---

### Instalación de Dependencias

Asegúrate de seguir en el entorno virtual (paso anterior). Luego instala las dependencias listadas en el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Esto descargará e instalará la versión de `pandas` especificada (u otras dependencias si existieran).

---

### Ejecución del Script

El script `transformar.py` se ejecuta desde la terminal o línea de comandos y requiere dos argumentos obligatorios:

1. **Archivo de entrada** (ruta y nombre del CSV detallado que se desea transformar).
2. **Archivo de salida** (ruta y nombre del CSV resultante en formato resumido).

Un ejemplo de ejecución sería:

```bash
python transformar.py data/archivo_entrada.csv data/archivo_salida.csv
```

Donde:

- `data/archivo_entrada.csv` es el CSV detallado que el script debe leer.
- `data/archivo_salida.csv` es el CSV nuevo que se generará con los datos agrupados y resumidos.

---

### ¿Qué Hace el Script?

En términos generales, el proceso que sigue el script es el siguiente:

1. **Lee** el archivo CSV de entrada usando `pandas`.
2. **Agrupa** la información por ciertas columnas clave (por ejemplo, Jugador, Rival, DNI, etc.) para sumar o consolidar la información de un mismo partido.
3. **Suma** métricas numéricas (pases, duelos 1v1, faltas, etc.) o crea nuevas columnas (p.ej. `PERDIDAS`) si es necesario.
4. **Calcula** valores “por 90 minutos” para poder comparar rendimientos de jugadores independiente de los minutos que hayan jugado.
5. **Genera** y **guarda** el archivo CSV de salida, ordenando las columnas según un formato deseado.

No es imprescindible conocer los detalles del código para su ejecución, pero si se requiere ajustar columnas o cambiar el criterio de agrupación, se puede editar el contenido de `transformar.py` (sección donde se definen columnas a agrupar, columnas a sumar y columnas a calcular por 90 minutos).

---

### Notas Finales

- Para **desactivar** el entorno virtual, puedes usar `deactivate` en la misma terminal.
- Si necesitas volver a ejecutar el script, recuerda activar el entorno virtual de nuevo si ya lo habías cerrado.
- Verifica que `archivo_salida.csv` no esté abierto en ningún editor (como Excel) antes de generar la salida, para evitar errores de escritura.
