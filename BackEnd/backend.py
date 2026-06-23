"""Local development entry point for the portfolio CMS."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
