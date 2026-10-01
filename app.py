from flask import Flask, jsonify, request

app = Flask(__name__)

# Numero de documentos del checklist por perfil
# La cantidad ha sido definida arbitrariamente para los casos de prueba
REQUERIDOS_ADMINISTRATIVO = 5
REQUERIDOS_MEDICO = 7
app.json.sort_keys = False 

@app.route("/expediente/<nombreEmpleado>/<perfil>/<int(signed=true):documentosSubidos>/<nombreDocumento>")
def evaluarExpediente(nombreEmpleado, perfil, documentosSubidos, nombreDocumento):

    perfil = perfil.lower()

    # 1. Determinar los documentos requeridos segun el perfil
    if perfil == "administrativo":
        documentosRequeridos = REQUERIDOS_ADMINISTRATIVO

    elif perfil == "medico":
        documentosRequeridos = REQUERIDOS_MEDICO

    else:
        return jsonify({
            "empleado": nombreEmpleado,
            "perfil": perfil,
            "estado": "error: perfil no reconocido",
            "perfilesValidos": "administrativo, medico"
        }), 400
    documentosAntes = documentosSubidos
    if documentosSubidos < 0 or documentosSubidos > documentosRequeridos:
        return jsonify({
            "error": "La cantidad de documentos ingresada no es valida"
        }),400
    # 2. Verificar si el documento ya existia
    yaExistia = request.args.get("existente", "false").lower()

    if yaExistia not in ["true", "false"]:
        return jsonify({
            "error": "El parametro existente debe ser true o false"
        }), 400
    if yaExistia == "true":
        accion = "nueva version"
        mensaje = "El documento ya existia. Se conserva su historial."

    elif documentosSubidos < documentosRequeridos:
        accion = "documento nuevo"
        documentosSubidos += 1
        mensaje = "El documento se agrego al expediente."

    else:
        return jsonify({
            "empleado": nombreEmpleado,
            "documento": nombreDocumento,
            "error": "No se pueden agregar mas documentos: el checklist ya esta completo."
        }), 400

    # 3. Evaluar el estado actualizado del expediente
    if documentosSubidos == 0:
        estado = "sin iniciar"

    elif documentosSubidos < documentosRequeridos:
        estado = "incompleto"

    elif documentosSubidos == documentosRequeridos:
        estado = "completo"

    else:
        estado = "error: documentos exceden el checklist"

    # 4. Calcular documentos pendientes
    pendientes = documentosRequeridos - documentosSubidos

    return jsonify({
        "empleado": nombreEmpleado,
        "perfil": perfil,
        "documento": nombreDocumento,
        "documentos antes de actualizar": documentosAntes,
        "accion": accion,
        "mensaje": mensaje,
        "documentosRequeridos": documentosRequeridos,
        "documentos despues de actualizar": documentosSubidos,
        "documentosPendientes": pendientes,
        "estado": estado
    })


if __name__ == "__main__":
    app.run(debug=True)
