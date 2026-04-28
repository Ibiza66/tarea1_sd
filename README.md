# Tarea 1 - Sistemas Distribuidos

## Descripción

Este proyecto implementa una arquitectura distribuida basada en microservicios para responder consultas, almacenar resultados en caché y generar tráfico automático para evaluar el comportamiento del sistema.

La solución está compuesta por tres servicios principales:

- **response-generator**: procesa las consultas solicitadas.
- **cache-service**: almacena respuestas en caché y entrega métricas de rendimiento.
- **traffic-generator**: genera tráfico automático sobre el sistema y produce gráficos de resultados.

---

## Arquitectura del sistema

El sistema se compone de los siguientes servicios:

### 1. Response Generator
Servicio encargado de procesar consultas sobre zonas y devolver resultados.

- Puerto: `8001`
- Endpoint de salud: `GET /health`
- Endpoint principal: `POST /query`

### 2. Cache Service
Servicio intermedio que consulta al `response-generator`, guarda resultados en caché y expone métricas.

- Puerto: `8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Métricas: `http://127.0.0.1:8000/metrics`
- Gráfico en vivo (v2): `http://127.0.0.1:8000/plot`

### 3. Traffic Generator
Servicio que envía 100 solicitudes automáticas al sistema para evaluar el comportamiento de la caché.

- Genera tráfico de prueba
- Guarda un gráfico llamado `metrics.png`

---

## Estructura del proyecto

```text
tarea1_sd/
│
├── data/
├── response_generator/
│
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