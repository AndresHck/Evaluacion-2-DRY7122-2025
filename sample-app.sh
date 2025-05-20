#!/bin/bash
set -e

# 1. Definir variables
APP_DIR="/home/devasc/labs/devnet-src/sample-app"
TEMP="./tempdir"

# 2. Limpiar y crear estructura temporal
rm -rf "$TEMP"
mkdir -p "$TEMP/templates" "$TEMP/static"

# 3. Copiar la app y recursos
cp "$APP_DIR/sample_app.py"    "$TEMP/"
cp -r "$APP_DIR/templates/"*   "$TEMP/templates/"
cp -r "$APP_DIR/static/"*      "$TEMP/static/"

# 4. Crear requirements.txt
echo "flask" > "$TEMP/requirements.txt"

# 5. Generar Dockerfile
cat > "$TEMP/Dockerfile" <<EOF
FROM python:3.11-slim

WORKDIR /home/myapp
COPY requirements.txt ./
RUN pip install --no-cache-dir -q -r requirements.txt

COPY sample_app.py ./
COPY templates/    ./templates/
COPY static/       ./static/

EXPOSE 3000
CMD ["python3", "sample_app.py"]
EOF

# 6. Construir imagen Docker
cd "$TEMP"
docker build -t sampleapp:latest .

# 7. Ejecutar contenedor (elimina previos si existen)
docker rm -f samplerunning 2>/dev/null || true
docker run -d -p 3000:3000 --name samplerunning sampleapp:latest

# 8. Mostrar estado
echo
docker ps -a --filter "name=samplerunning"
echo
echo "→ La app está accesible en http://10.0.2.15:3000/home"

