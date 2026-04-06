# Laboratory 2 --- Architectural Modeling with textX (PRO)

## 1. Introducción

Este proyecto implementa el paradigma de **Model-Driven Engineering
(MDE)** para generar automáticamente el esqueleto de un sistema basado
en una arquitectura definida mediante un DSL (Domain Specific Language).

El caso de estudio es el sistema **ERTMS (European Rail Traffic
Management System)**.

------------------------------------------------------------------------

## 2. Arquitectura del proyecto

El flujo MDE es:

1.  Definir DSL → `arch.tx`
2.  Crear modelo → `model.arch`
3.  Cargar metamodelo → `metamodel.py`
4.  Aplicar transformaciones → `transformations.py`
5.  Ejecutar generación → `generation.py`
6.  Generar sistema → `skeleton/`

------------------------------------------------------------------------

## 3. Estructura del proyecto

    .
    ├── arch.tx
    ├── metamodel.py
    ├── transformations.py
    ├── model.arch
    ├── generation.py
    ├── Dockerfile
    └── README.md

Salida generada:

    skeleton/
    ├── docker-compose.yml
    ├── servicios...

------------------------------------------------------------------------

## 4. Requisitos

-   Docker
-   Docker Compose

------------------------------------------------------------------------

## 5. Construcción del contenedor

``` bash
docker build -t lssa-lab2 .
```

------------------------------------------------------------------------

## 6. Ejecución del generador

``` bash
docker run --rm -v "$PWD:/app" lssa-lab2
```

Resultado esperado:

    skeleton/

------------------------------------------------------------------------

## 7. Levantar el sistema

``` bash
cd skeleton
docker-compose up --build
```

------------------------------------------------------------------------

## 8. Validación del sistema

### Dashboard

http://localhost:8003

### API Gateway

``` bash
curl http://localhost:8002/passengers/records
```

### Authority Service

``` bash
curl -X POST http://localhost:8002/authority \
  -H "Content-Type: application/json" \
  -d '{"train_id":"T-001","corridor":"CORRIDOR-A"}'
```

------------------------------------------------------------------------

## 9. Flujo completo

``` bash
docker build -t lssa-lab2 .
docker run --rm -v "$PWD:/app" lssa-lab2
cd skeleton
docker-compose up --build
```

------------------------------------------------------------------------

## 10. Entrega

Archivos requeridos:

-   arch.tx
-   metamodel.py
-   transformations.py
-   model.arch
-   generation.py
-   Dockerfile
-   skeleton/
-   report.pdf

Formato:

    lab2-team-X.zip

------------------------------------------------------------------------

## 11. Autor

Proyecto académico --- Large Scale Software Architecture


## 12

generar primero un environment de python para instalar textX

```Bash
pip install "textX[cli]"

pip install textX

textx check model.arch --grammar arch.tx 

textx generate arch.tx --target dot --overwrite ## genera un archivo dot a partir del meta modelo 

textx generate model.arch --grammar arch.tx --target dot --overwrite ## genera un archivo dot a partir del modelo y la gramática que es el meta modelo

textx generate model.arch --grammar arch.tx --target plantuml 
## no tiene lengueje

```

## 13 . Referencias

- textx --help
- docu https://textx.github.io/textX/visualization.html
- examples https://github.com/textX/textX/blob/master/examples


