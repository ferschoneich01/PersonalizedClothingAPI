from flask import Blueprint, jsonify, request
from sqlalchemy.sql import text
from database import db

try:
    from rivescript import RiveScript
    RIVESCRIPT_AVAILABLE = True
except ImportError:
    RIVESCRIPT_AVAILABLE = False

main = Blueprint('messages_blueprint', __name__)


@main.route("/webhook", methods=["POST", "GET"])
def webhook_whatsapp():
    # Verificación del webhook (GET)
    if request.method == "GET":
        if request.args.get('hub.verify_token') == "hola":
            return request.args.get('hub.challenge')
        else:
            return "Error de autentificacion.", 403

    # Procesamiento del mensaje (POST)
    try:
        data = request.get_json()

        telefono_cliente = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        mensaje          = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        id_wa            = data['entry'][0]['changes'][0]['value']['messages'][0]['id']
        timestamp        = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']

        # Obtener respuesta del bot
        if RIVESCRIPT_AVAILABLE:
            bot = RiveScript()
            bot.load_file('res.rive')
            bot.sort_replies()
            respuesta = bot.reply("localuser", mensaje)
            respuesta = respuesta.replace("\\n", "\n").replace("\\", "")
        else:
            respuesta = "Hola, recibimos tu mensaje. En breve te atendemos."

        # Verificar si el mensaje ya fue procesado (evitar duplicados)
        cantidad = db.execute(
            text("SELECT sp_get_whatsapp_msg_count(:id_wa)"),
            {"id_wa": id_wa}
        ).scalar()

        if cantidad == 0:
            db.execute(
                text("CALL sp_insert_whatsapp_msg(:recibido, :enviado, :id_wa, :timestamp, :telefono)"),
                {
                    "recibido":  mensaje,
                    "enviado":   respuesta,
                    "id_wa":     id_wa,
                    "timestamp": str(timestamp),
                    "telefono":  str(telefono_cliente),
                }
            )
            db.commit()

        return jsonify({"status": "success"}), 200

    except Exception as ex:
        db.rollback()
        return jsonify({"status": "error", "message": str(ex)}), 500