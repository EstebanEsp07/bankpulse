# Estrategia de ramas — GitHub Flow

- `main`: siempre estable y desplegable. Protegida: solo se modifica mediante Pull Request aprobado.
- Ramas de trabajo (se crean desde `main`, vida corta, una por historia o tarea):
  - `feature/HU-BP-01-consultar-restaurantes`
  - `fix/HU-BP-02-validar-cupo`
  - `docs/readme-estructura`
  - `chore/docker-compose`
- Commits: mensajes en imperativo con prefijo (`feat:`, `fix:`, `docs:`, `test:`, `chore:`) y el ID de la historia. Ej.: `feat(HU-BP-01): filtrar restaurantes por cupo`.
- Pull Request: usa la plantilla de `.github/`, enlaza la(s) historia(s), requiere al menos 1 revisión de otro integrante y se fusiona con *Squash and merge*. La rama se elimina tras el merge.
- Justificación: equipo pequeño, entregas cortas (sprint de 2 semanas) y un único entorno; GitHub Flow reduce la complejidad frente a Gitflow.

## Plan de Pull Requests del Sprint 1
| PR | Rama | Historia |
|----|------|----------|
| PR-BP-01 | feature/HU-BP-01-consultar-restaurantes | HU-BP-01 |
| PR-BP-02 | feature/HU-BP-02-reservar-mesa | HU-BP-02 |
| PR-BP-03 | feature/HU-BP-04-ver-membresia | HU-BP-04 |
| PR-BP-04 | feature/HU-BP-07-eventos-preventa | HU-BP-07 |
| PR-BP-05 | feature/HU-BP-10-dividir-gasto | HU-BP-10 |
