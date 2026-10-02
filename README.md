# BankPulse

Aplicación de pagos premium (dominio financiero) del proyecto integrador. Este repositorio contiene el **esqueleto ejecutable del Sprint 1** (SPR-BP-01): arquitectura MVC, base de datos PostgreSQL y entorno Docker.

## 1. Propósito y alcance

BankPulse convierte los beneficios premium de un banco en experiencias que se reservan, acreditan y pagan desde la app. Épicas del producto:

1. Gestión de Reservas Gastronómicas Exclusivas
2. Gestión de Membresías y Credenciales Offline
3. Gestión de Preventas y Eventos Premium
4. División de Gastos y Pagos Grupales

**Incluido en el Sprint 1 (esqueleto):** HU-BP-01, HU-BP-02, HU-BP-04, HU-BP-07, HU-BP-10.
**Fuera de alcance:** pasarela de pagos real, autenticación real (se usan clientes semilla), credencial QR offline (HU-BP-05/06), lista de espera y recordatorios.

## 2. Stack y versiones

| Componente | Versión |
|------------|---------|
| Python | 3.12 |
| Flask / Flask-SQLAlchemy / SQLAlchemy | 3.1 / 3.1 / 2.0 |
| PostgreSQL | 16 (alpine) |
| Gunicorn | 23 |
| Docker Engine / Compose | 24+ / v2 |

## 3. Requisitos previos

- Git y Docker con Docker Compose v2 (Docker Desktop o GitHub Codespaces).
- Puerto libre `8000` (configurable con `APP_PORT`).

## 4. Configuración de variables

```bash
cp .env.example .env      # Windows PowerShell: Copy-Item .env.example .env
```

Edite `.env` si desea otros valores. **No suba `.env` al repositorio.**

| Variable | Descripción | Valor de ejemplo |
|----------|-------------|------------------|
| POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB | Credenciales y nombre de la BD | bankpulse / change_me_locally / bankpulse |
| SECRET_KEY | Clave de Flask | change_me_locally |
| APP_PORT | Puerto publicado en el host | 8000 |
| SEED_DATA | Carga datos semilla ficticios | true |
| DB_CONNECT_RETRIES / DB_CONNECT_DELAY | Reintentos y espera (s) hasta que la BD responda | 15 / 2 |

## 5. Comandos

```bash
docker compose up --build -d     # construir e iniciar
docker compose ps                # estado de los servicios (db y app en healthy)
docker compose logs -f app       # logs de la aplicación
docker compose down              # detener (conserva datos)
docker compose down -v           # detener y borrar el volumen de la BD
```

| Servicio | Puerto host | Notas |
|----------|-------------|-------|
| app (SVC-BP-01) | 8000 | API y vista HTML en http://localhost:8000 |
| db (SVC-BP-02) | no publicado | PostgreSQL accesible solo dentro de la red de Compose; datos en el volumen `bankpulse_pgdata` |

## 6. Endpoint de salud y operación demostrable

```bash
curl http://localhost:8000/health
# {"db":"up","service":"bankpulse","status":"ok"}

# HU-BP-01: restaurantes con cupo para 4 personas
curl "http://localhost:8000/api/restaurants?date=2026-11-10&guests=4"

# HU-BP-02: reservar mesa (garantía simulada)
curl -X POST http://localhost:8000/api/reservations \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"restaurant_id":1,"date":"2026-11-10","guests":4}'

# HU-BP-04: membresía
curl http://localhost:8000/api/customers/1/membership

# HU-BP-07: eventos y elegibilidad
curl "http://localhost:8000/api/events?customer_id=2&on=2026-10-05"

# HU-BP-10: dividir un gasto en partes iguales
curl -X POST http://localhost:8000/api/splits -H "Content-Type: application/json" \
  -d '{"owner_id":1,"description":"Cena","total_cents":10000,"mode":"equal","members":[{"name":"A"},{"name":"B"},{"name":"C"}]}'
```

Los montos se manejan en centavos (`*_cents`). Los clientes semilla son 1 (platinum), 2 (gold) y 3 (classic).

## 7. Pruebas

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q          # usa SQLite en memoria; no requiere Docker
```

## 8. Estructura de carpetas

```
bankpulse/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore / .dockerignore
├── requirements.txt
├── wsgi.py                      # punto de entrada de Gunicorn
├── .github/
│   └── pull_request_template.md
├── app/
│   ├── __init__.py              # create_app (Application Factory) + espera de la BD
│   ├── config.py
│   ├── extensions.py
│   ├── seed.py                  # datos semilla ficticios
│   ├── models/                  # MODELO: customer, restaurant, event, split
│   ├── views/                   # VISTA: templates/home.html, presenters.py
│   ├── controllers/             # CONTROLADOR: un Blueprint por recurso
│   └── services/                # Reglas de negocio y errores de dominio
├── tests/
│   ├── conftest.py
│   └── test_api.py
└── docs/
    ├── ARCHITECTURE.md
    ├── BRANCHING.md             # GitHub Flow y plan de PRs
    ├── TRACEABILITY.md
    └── evidence/                # capturas (docker compose ps, /health, PRs)
```

## 9. Arquitectura y flujo de trabajo

- Arquitectura MVC: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Estrategia de ramas (GitHub Flow): [docs/BRANCHING.md](docs/BRANCHING.md)
- Trazabilidad HU → MVC → PR → servicio → prueba: [docs/TRACEABILITY.md](docs/TRACEABILITY.md)

## 10. Solución de problemas frecuentes

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| `variable is not set` al ejecutar compose | Falta el archivo `.env` | `cp .env.example .env` |
| `port is already allocated` | Puerto 8000 ocupado | Cambie `APP_PORT` en `.env` y repita `docker compose up -d` |
| La app reinicia o no conecta a la BD | La BD aún arranca | Es normal unos segundos; revise `docker compose logs app` (reintentos automáticos) |
| Cambié las credenciales y falla el login a PostgreSQL | El volumen conserva las credenciales anteriores | `docker compose down -v` y vuelva a levantar |
| En Codespaces no abre localhost:8000 | Puerto no reenviado | Use la pestaña *Ports* y abra el puerto 8000 |
