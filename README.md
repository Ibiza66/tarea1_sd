# Tarea 1 - Sistemas Distribuidos

## Descripción

Este proyecto implementa una arquitectura distribuida basada en microservicios para procesar consultas, utilizar caché y generar tráfico de prueba.

La solución está compuesta por tres servicios:

- **response-generator**: procesa consultas y entrega resultados.
- **cache-service**: recibe solicitudes, consulta al generador de respuestas y almacena resultados en caché.
- **traffic-generator**: automatiza múltiples solicitudes al sistema para medir su comportamiento.

## Arquitectura

El sistema se compone de los siguientes servicios:

1. **response-generator**
   - Procesa consultas del tipo `Q1`, `Q4` y `Q5`.
   - Se ejecuta en el puerto **8001**.

2. **cache-service**
   - Expone un endpoint único `POST /query`.
   - Reenvía consultas al `response-generator` cuando no están en caché.
   - Almacena respuestas para reutilizarlas.
   - Se ejecuta en el puerto **8000**.

3. **traffic-generator**
   - Genera tráfico automático contra el sistema.
   - Envía 100 solicitudes de prueba.
   - Consulta métricas al finalizar y genera un gráfico `metrics.png`.

## Estructura del proyecto

```text
tarea1_sd/
│
├── data/
├── response_generator/
├── cache_service/
│   ├── app/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── requirements.txt
│
├── Generador_Trafico/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── Dockerfile
├── docker-compose.yml
└── README.md