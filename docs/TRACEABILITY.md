# Trazabilidad — BankPulse (Sprint 1)

La matriz completa está en el Documento de diseño (PDF). Resumen vigente:

| Historia | Controlador | Servicio | Prueba | PR | Estado |
|----------|-------------|----------|--------|----|--------|
| HU-BP-01 | RestaurantController | reservation_service.search_restaurants | test_restaurants_filtered_by_capacity | PR-BP-01 | Implementada en esqueleto |
| HU-BP-02 | ReservationController | reservation_service.create_reservation | test_reservation_created_and_capacity_consumed | PR-BP-02 | Implementada en esqueleto |
| HU-BP-04 | MembershipController | (consulta directa al modelo) | test_membership_found_and_missing | PR-BP-03 | Implementada en esqueleto |
| HU-BP-07 | EventController | event_service.list_events | test_events_eligibility_by_tier | PR-BP-04 | Implementada en esqueleto |
| HU-BP-10 | SplitController | split_service.create_split | test_split_equal_distributes_remainder, test_split_custom_must_sum_to_total | PR-BP-05 | Implementada en esqueleto |

Actualice las columnas "PR" con el enlace real al fusionar cada Pull Request.
