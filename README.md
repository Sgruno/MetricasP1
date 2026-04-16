# TableroKanban
Esta es una app web que permite tener un tablero Kanban para las tareas de los DEVELOPERS, y utilizar métricas para ser especifico, las métricas:  cycle time, lead time y code churn 


Manual de Instalación y Ejecución
Proyecto: Dashboard de Métricas de Software (GQM)
Documentación para: Implementadores / QA / Stakeholders

1. Prerrequisitos
Antes de comenzar, asegúrate de tener instalado lo siguiente:
*Python 3.10 o superior: Es el lenguaje base del servidor.
  Descarga: [python.org](https://www.python.org/downloads/?hl=ES)
*Git: Para clonar el repositorio.
  Descarga: [git-scm.com](https://git-scm.com/install/)
*Editor de código (Opcional):
   Se recomienda VS Code para visualizar el código.
   Descarga: https://code.visualstudio.com/Downloadhttps://code.visualstudio.com/Download
*MongoDB Community Server:
     Descarga: [la página oficial.](https://www.mongodb.com/products/platform/atlas-database)https://www.mongodb.com/products/platform/atlas-database
3. Tecnologías y DependenciasEl proyecto utiliza las siguientes tecnologías clave:ComponenteTecnologíaFunciónBackendPython / FlaskProcesamiento de datos y lógica de métricas.FrontendHTML5 / CSS3 / Jinja2Interfaz de usuario y diseño.GráficosChart.jsRenderizado de las gráficas escalonadas.Data FlowJSON / JavaScriptComunicación entre el servidor y el cliente.

4. Guía de Instalación
Sigue estos pasos en orden para configurar tu entorno:
  Paso 1: Obtener el código
  Abre una terminal (CMD en Windows o Terminal en macOS/Linux) y clona el proyecto:
  git clone https://github.com/Sgruno/MetricasP1.git
  cd MetricasP1
  Paso 2: Crear un entorno virtual (Aislamiento)
  Es una buena práctica para que las librerías del proyecto no choquen con otras que tengas en tu PC.

  Windows:

  Bash
  python -m venv venv
  .\venv\Scripts\activate
  
  macOS / Linux:

  Bash
  python3 -m venv venv
  source venv/bin/activate

  Paso 3: Instalación de Flask y pymongo
  Instala el framework web necesario para correr el servidor:
  pip install flask
  pip install pymongo

4. Cómo Correr el Programa
Una vez que el entorno está configurado, la ejecución es muy sencilla:
  *Asegúrate de estar en la carpeta raíz del proyecto en tu terminal.
  *Verifica que el entorno virtual esté activo (deberías ver (venv) al inicio de tu línea de comando).

Ejecuta el servidor:
Bash(terminal)
python app.py

Acceso Web:
El terminal te dirá que el servidor está en el puerto 5000. Abre tu navegador y escribe:
http://127.0.0.1:5000
