from app import create_app

# Entry point for local development
app = create_app()

if __name__ == "__main__":
    # Debug can be toggled via ENV or config
    app.run(host="127.0.0.1", port=5000, debug=True)