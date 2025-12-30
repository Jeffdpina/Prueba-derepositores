## ESTA APP SIRVE PARA DEMO USO DE TERRAFORM Y FLASK
from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient
import os, uuid


## inicializar Flask
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

AZURE_CONNECTION_STRING= ()

CONTAINER_NAME=""


# Cliente blob storage
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# container
container = blob_service_client.get_container_client(CONTAINER_NAME)

try:
    container.get_container_properties()
except Exception:
    container.create_container()


## rutas para formulario
@app.route("/")
def index():
    return render_template("upload.html")

## ruta para subir archivo por medio de POST
@app.route("/upload", methods=["POST"])
def upload():
    archivo = request.files.get("archivo")
    if not archivo or archivo.filename == "":
        return render_template("upload.html", mensaje="elegir un archivo para continuar")
    
    nombre_original = archivo.filename
    extension = os.path.splitext(nombre_original)[1]

    

    nombre_blob = f"{uuid.uuid4().hex}{extension}"

    container.upload_blob(name=nombre_blob, data=archivo.stream, overwrite=True)

    # subir archivo al contenedor
    url_blob = f"{container.url}/{nombre_blob}"

    return render_template(
        "upload.html",
        mensaje = "Archivo subido con exito",
        blob_url = url_blob,
        nombre_archivo = nombre_original
    )

## arrancamos el server flask
if __name__ == "__main__":
    app.run(debug=True, port=5050)