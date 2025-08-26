from flask import Flask, render_template, Blueprint
import logging
import traceback
import sqlite3

error_bp = Blueprint('error_handlers', __name__)

# Handler for sqlite3 OperationalError
@error_bp.app_errorhandler(sqlite3.OperationalError)
def handle_operational_error(e):
    from flask import current_app
    current_app.logger.error(f"OperationalError: {e}\n{traceback.format_exc()}")
    return render_template("error.html", error=e), 500

# Global error handler for any unhandled exception
@error_bp.errorhandler(Exception)
def handle_exception(e):
    from flask import current_app
    current_app.logger.error(f"Unhandled Exception: {e}\n{traceback.format_exc()}")
    return render_template("error.html", error=e), 500

@error_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
