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
