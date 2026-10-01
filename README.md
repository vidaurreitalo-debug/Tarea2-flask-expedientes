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

### 4. Caso por defecto

* Si el perfil no existe en las plantillas de RRHH, el sistema responde error: perfil no reconocido y muestra los perfiles válidos.
* Si se intenta agregar un documento nuevo cuando el checklist ya está completo, el sistema responde con un error indicando que no se pueden agregar más documentos.  Además, si se intenta agregar una cantidad de documentos negativa o una cantidad mayor a la requerida el sistema indica que se necesita un número válido                                                                                                                                                         
* Si el parámetro que indica si el documento ya existía no es true o false, el sistema devuelve un error de entrada.
* Si el documento ya existía, se permite registrar una nueva versión incluso cuando el expediente está completo, ya que una renovación no representa un documento adicional.
* Si los datos son válidos y la cantidad de documentos registrados coincide con la requerida, el expediente se clasifica como completo.

---

## Cómo ejecutarlo

```bash
pip install flask
python app.py
```

**Ruta:**

```text
/expediente/<nombreEmpleado>/<perfil>/<documentosSubidos>/<nombreDocumento>?existente=<true|false>
```

El parámetro `existente` se recibe mediante query string. Su valor determina si el documento se registra como nuevo o como una versión de uno que ya se encontraba en el expediente.

## Cómo funciona
**Funcionamiento paso a paso:**
1. Recepción de Datos (Ruta):
A través de la URL /expediente/..., la API recibe cuatro parámetros principales: el nombre del empleado, su perfil, la cantidad de documentos que ya ha subido y el nombre del documento actual.

2. Validación del Perfil:
Asigna una cantidad obligatoria de documentos a entregar según el rol:

* Administrativo: 5 documentos.
* Médico: 7 documentos.
(Si se ingresa un perfil distinto o una cantidad de documentos ilógica, devuelve un error 400).

3. Lógica de Actualización:
Lee un parámetro de consulta (?existente=true/false) para decidir qué acción tomar:

* Si el documento ya existía (true): Lo registra como una "nueva versión" y conserva el mismo número de documentos subidos.
* Si es un documento nuevo (false): Suma 1 a la cantidad de documentos subidos, siempre y cuando no se haya superado el límite del perfil.

4. Evaluación del Estado:
Con base en el nuevo total de documentos, clasifica el expediente en:

* Sin iniciar: 0 documentos.
* Incompleto: Menos de los requeridos.
* Completo: Exactamente la cantidad requerida.

5. Respuesta:
Finaliza devolviendo un objeto JSON con un reporte detallado que incluye: datos del empleado, acción realizada (nuevo o versión), documentos previos/actuales, documentos pendientes y el estado final del expediente.

## Pruebas

| *URL*                                                                            | *Acción*                                              | *Estado obtenido*                        |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------ |
| http://127.0.0.1:5000/expediente/Ana/administrativo/0/DUI?existente=false        | Agregar documento nuevo                                 | incompleto (4 pendientes)                  |
| http://127.0.0.1:5000/expediente/Luis/medico/4/Carnet?existente=true             | Registrar nueva versión                                 | incompleto (3 pendientes)                  |
| http://127.0.0.1:5000/expediente/Sofia/administrativo/4/Contrato?existente=false | Agregar documento nuevo                                 | completo                                   |
| http://127.0.0.1:5000/expediente/Pedro/medico/7/Carnet?existente=false           | Intentar agregar documento nuevo con checklist completo | error: no se pueden agregar más documentos |
| http://127.0.0.1:5000/expediente/Eva/enfermero/3/DUI?existente=false             | Ingresar perfil no reconocido                           | error: perfil no reconocido                |

*Nota:* Cada prueba se ejecuta de manera independiente, ya que todavía no existe persistencia de datos entre solicitudes. Los resultados permiten verificar la lógica de decisión y el comportamiento esperado de cada condición.

Las capturas de pantalla de cada prueba se incluyen en la entrega.
