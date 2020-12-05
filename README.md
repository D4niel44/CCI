# CCI (Cloud Cover Index)
Proyecto 2 Modelado y Programación 2021-1

# Integrantes del Equipo
Jonás García Chavelas

Daniel Linares Gil

# Instalación y Ejecución

## Requerimientos
Para Ejecutar el programa es necesario Python 3.6+. Una vez instalado python
ejecutar 
`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

para instalar las dependencias.
## Ejecutar
Para ejecutar el programa ecribir el comando

`python3 -m cloudcoverindex [path to photos] [optional arguments]`

## Correr  Pruebas
Para correr las pruebas unitarias del programa ejecutar

`pytest`

## Generar documentación
Para generar la documentación es necesario ejecutar los siguientes comandos.

`cd docs && make html`

La documentación se generará en el directorio `docs/build/[html|latex]`

## Resources
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [PythonDoc](https://docs.python.org/3.8/)
- [SphinxDoc](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/build-the-docs.html#generating-documentation-from-docstrings)
