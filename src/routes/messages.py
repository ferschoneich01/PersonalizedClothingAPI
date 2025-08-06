from flask import Blueprint,jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
import os
from rivescript import RiveScript

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

main = Blueprint('messages_blueprint', __name__)

#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@main.route("/webhook", methods=["POST", "GET"])
def webhook_whatsapp():
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "hola":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
            return "Error de autentificacion."
        
    else:
        #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
        data=request.get_json()
        #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
        telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        #EXTRAEMOS EL TELEFONO DEL CLIENTE
        mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        #EXTRAEMOS EL ID DE WHATSAPP DEL ARRAY
        idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
        #EXTRAEMOS EL TIEMPO DE WHATSAPP DEL ARRAY
        timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
        #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
          
        #INICIALIZAMOS RIVESCRIPT Y CARGAMOS LA CONVERSACION
        bot = RiveScript()
        bot.load_file('res.rive')
        bot.sort_replies()
        #OBTENEMOS LA RESPUESTA
        respuesta= bot.reply("localuser",mensaje)
        respuesta=respuesta.replace("\\n","\\\n")
        respuesta=respuesta.replace("\\","")
        #CONECTAMOS A LA BASE DE DATOS
        
        query=db.execute(text("SELECT count(id) AS cantidad FROM MsgWhatsapp WHERE id_wa='" + idWA + "';"))

        
        cantidad = query.fetchone()
        cantidad=str(cantidad)
        cantidad=int(cantidad)
        if cantidad==0 :
            sql = ("INSERT INTO MsgWhatsapp"+ 
            "(mensaje_recibido,mensaje_enviado,id_wa      ,timestamp_wa   ,telefono_wa) VALUES "+
            "('"+mensaje+"'   ,'"+respuesta+"','"+idWA+"' ,'"+timestamp+"','"+telefonoCliente+"');")
            db.execute(sql)
            db.commit()

        #RETORNAMOS EL STATUS EN UN JSON
        return jsonify({"status": "success"}, 200)