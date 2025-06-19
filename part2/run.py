"""
Entry point for running the HBnB Flask application.

This script imports the application factory, creates the app instance,
and starts the development server when executed as the main program.
"""

from hbnb.app import create_app

app = create_app()

if __name__ == '__main__':
    """
    Run the Flask development server.

    Enables debug mode for live reloading and detailed error pages.
    """
    app.run(debug=True)
