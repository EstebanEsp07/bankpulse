# Arquitectura MVC — BankPulse

```
Cliente (navegador / app móvil)
        │  1. Solicitud HTTP            ▲ 6. Respuesta (HTML o JSON)
        ▼                               │
VISTA        views/templates/home.html · views/presenters.py
        │                               ▲
CONTROLADOR  controllers/*_controller.py (Blueprints Flask)
        │                               ▲
SERVICIOS    services/*_service.py (reglas de negocio)
        │                               ▲
MODELO       models/*.py (SQLAlchemy) ──► PostgreSQL 16 (volumen bankpulse_pgdata)
```

| Capa | Elementos | Responsabilidad |
|------|-----------|-----------------|
| Modelo | Customer, Membership, Restaurant, Reservation, Event, ExpenseSplit, SplitShare | Entidades y persistencia |
| Vista | home.html, presenters (restaurant_view, reservation_view, membership_view, event_view, split_view) | Representación de la respuesta |
| Controlador | HealthController, RestaurantController, ReservationController, MembershipController, EventController, SplitController | Recibir la petición, validar entrada, invocar servicios y elegir la vista |
| Servicios | reservation_service, event_service, split_service | Reglas de negocio (cupo, elegibilidad, reparto) |

Patrones: Application Factory, Blueprint por controlador, capa de servicios, presentadores.
El diagrama completo y la justificación están en el Documento de diseño (PDF).
