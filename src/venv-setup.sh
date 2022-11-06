#!/usr/bin/env bash
echo "Borrando antiguo venv"
rm -R ~/venv-cc
echo "Creando venv en la home"
python3 -m venv ~/venv-cc
source ~/venv-cc/bin/activate
echo "Instalando wheel"
pip3 install wheel
echo "Instalando librerías"
pip install vendor/*.whl
echo "Instalando requirements"
pip install -r requirements.txt