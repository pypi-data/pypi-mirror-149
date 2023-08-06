from flask import Blueprint, redirect, url_for

error_routes = Blueprint('error_routes', __name__)


@error_routes.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

    return(division_by_zero)


@error_routes.errorhandler(404)
def page_not_found(e):

    return redirect(url_for('home', info=None))
