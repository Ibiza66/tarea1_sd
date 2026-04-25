## \# Tarea 1 - Sistemas Distribuidos

## 

## \## Descripción

## 

## Este proyecto implementa una arquitectura distribuida basada en microservicios para procesar consultas, utilizar caché y generar tráfico de prueba.

## 

## La solución está compuesta por tres servicios:

## 

## \- \*\*response-generator\*\*: procesa consultas y entrega resultados.

## \- \*\*cache-service\*\*: recibe solicitudes, consulta al generador de respuestas y almacena resultados en caché.

## \- \*\*traffic-generator\*\*: automatiza múltiples solicitudes al sistema para medir su comportamiento.

## 

## \---

## 

## \## Arquitectura

## 

## El sistema se compone de los siguientes servicios:

## 

## 1\. \*\*response-generator\*\*

## &#x20;  - Procesa consultas del tipo `Q1`, `Q4` y `Q5`.

## &#x20;  - Se ejecuta en el puerto \*\*8001\*\*.

## 

## 2\. \*\*cache-service\*\*

## &#x20;  - Expone un endpoint único `POST /query`.

## &#x20;  - Reenvía consultas al `response-generator` cuando no están en caché.

## &#x20;  - Almacena respuestas para reutilizarlas.

## &#x20;  - Se ejecuta en el puerto \*\*8000\*\*.

## 

## 3\. \*\*traffic-generator\*\*

## &#x20;  - Genera tráfico automático contra el sistema.

## &#x20;  - Envía 100 solicitudes de prueba.

## &#x20;  - Consulta métricas al finalizar y genera un gráfico `metrics.png`.

## 

## \---

## 

## \## Estructura del proyecto

## 

## ```text

## tarea1\_sd/

## │

## ├── data/

## ├── response\_generator/

## ├── cache\_service/

## │   ├── app/

## │   ├── docker-compose.yml

## │   ├── Dockerfile

## │   └── requirements.txt

## │

## ├── Generador\_Trafico/

## │   ├── app/

## │   ├── Dockerfile

## │   └── requirements.txt

## │

## ├── Dockerfile

## ├── docker-compose.yml

## └── README.md

