from flask import render_template, Blueprint
import traceback
import sqlite3

# Blueprint for registering error handlers across the app
error_bp = Blueprint('error_handlers', __name__)


# Handles database operational errors to provide a user-friendly error page
# and log details for debugging
@error_bp.app_errorhandler(sqlite3.OperationalError)
def handle_operational_error(e):
    """
    Handles sqlite3.OperationalError exceptions.

    Inputs:
        e: The exception instance raised by sqlite3 operations.

    Processing:
        Logs the error and stack trace for diagnostics.

    Outputs:
        Renders a themed error page with a user-friendly message
        and returns HTTP 500.
    """
    from flask import current_app
    current_app.logger.error(
        f"OperationalError: {e}\n{traceback.format_exc()}")
    # Pass a friendly message to the template for SQL errors
    message = "A database error occurred. Please try again later"
    return render_template("pages/error.html", message=message), 500


# Catches any unhandled exceptions to prevent exposing internal errors to users
# and logs for troubleshooting
@error_bp.errorhandler(Exception)
def handle_exception(e):
    """
    Handles all uncaught exceptions.

    Inputs:
        e: The exception instance.

    Processing:
        Logs the error and stack trace for diagnostics.

    Outputs:
        Renders a themed error page with a user-friendly message
        and returns HTTP 500.
    """
    from flask import current_app
    current_app.logger.error(
        f"Unhandled Exception: {e}\n{traceback.format_exc()}"
    )
    # Pass a friendly message to the template for internal errors
    message = "An unexpected error occurred. Please try again later."
    return render_template("pages/error.html", message=message), 500


# Custom handler for 404 errors to show a friendly not-found page
@error_bp.app_errorhandler(404)
def page_not_found(e):
    """
    Handles 404 Not Found errors.

    Inputs:
        e: The exception instance (typically unused).

    Processing:
        None.

    Outputs:
        Renders a custom 404 page and returns HTTP 404.
    """
    return render_template('pages/404.html'), 404
