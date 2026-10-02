from ..services.errors import DomainError


def register_controllers(app):
    from .event_controller import bp as event_bp
    from .health_controller import bp as health_bp
    from .membership_controller import bp as membership_bp
    from .reservation_controller import bp as reservation_bp
    from .restaurant_controller import bp as restaurant_bp
    from .split_controller import bp as split_bp

    for bp in (health_bp, restaurant_bp, reservation_bp, membership_bp, event_bp, split_bp):
        app.register_blueprint(bp)

    @app.errorhandler(DomainError)
    def handle_domain_error(err):
        return {"error": err.message}, err.status
