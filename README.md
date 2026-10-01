# Tarea2-flask-expedientes
Tarea 2: Programa en Flask con una ruta que evalúa el estado de un expediente digital (sin iniciar, incompleto, completo) según el checklist de documentos del perfil del empleado, usando if/elif/else.

# Levantamiento de requerimientos

**Reto: Expedientes digitales: modernizando el ingreso de personal en RRHH.**

### 1. Estados posibles

La ficha del Hospital establece dos estados visuales para los expedientes: *incompleto* (cuando existen documentos pendientes) y *completo* (cuando se han registrado todos los documentos requeridos). Para la lógica de decisión, separamos *sin iniciar* (0 documentos) como un caso particular de expediente incompleto, ya que representa a un empleado que todavía no tiene documentos registrados.

Por lo tanto, se consideran tres estados:

* **Sin iniciar:** el expediente no tiene documentos registrados.
* **Incompleto:** el expediente contiene algunos documentos, pero todavía faltan documentos requeridos.
* **Completo:** el expediente contiene todos los documentos establecidos en el checklist de su perfil.

### 2. Qué define cada estado

El estado se determina comparando el número de documentos distintos registrados con la cantidad de documentos requeridos según el perfil del empleado.

| **Condición**                                                   | **Estado**  |
| --------------------------------------------------------------- | ----------- |
| 0 documentos registrados                                        | sin iniciar |
| Más de 0 documentos, pero menos de los requeridos por el perfil | incompleto  |
| Exactamente los documentos requeridos                           | completo    |

La ficha establece que el checklist debe ser configurable según el perfil o puesto del empleado. Para esta implementación se utilizan dos perfiles de prueba: administrativo, con 5 documentos requeridos, y médico, con 7.

### 3. Reglas de la ficha que no estaban en el ejemplo genérico

* **Checklist configurable por perfil:** la cantidad de documentos requeridos depende del puesto del empleado. Por ello, la ruta recibe el perfil y el programa asigna la cantidad correspondiente mediante una estructura `if/elif/else`.
* **Manejo de versiones:** la ficha establece que los documentos que se renuevan periódicamente deben conservar sus versiones anteriores sin perder el historial. Por esta razón, el programa distingue entre documentos nuevos y documentos existentes. Si el documento ya existe, se registra la acción como una nueva versión y no aumenta la cantidad de documentos del checklist. Si es nuevo, se agrega al expediente y aumenta la cantidad de documentos registrados.
* **Actualización del estado:** después de determinar si se agregó un documento nuevo o se registró una nueva versión, el programa vuelve a evaluar el estado del expediente y calcula cuántos documentos quedan pendientes.

Como todavía no se utilizan bases de datos ni archivos, el manejo de versiones se simula mediante parámetros recibidos en la URL. El almacenamiento real del historial se implementará en una etapa posterior del proyecto.

