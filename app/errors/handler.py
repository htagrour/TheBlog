from app.errors import bp

@bp.app_errorhandler(404)
def not_found_error(error):
    return "fuck off", 404

@bp.app_errorhandler(500)
def innternal_error(error):
    return "maxi x4elk", 500