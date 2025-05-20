from flask import Flask, request, render_template

# 1) Instanciar Flask
app = Flask(__name__)

# 2) Definir ruta /home
@app.route("/home")
def main():
    # Renderiza la plantilla e inyecta la IP del cliente
    return render_template("index.html", client_ip=request.remote_addr)

# 3) Ejecutar en 0.0.0.0:3000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, threaded=False)
