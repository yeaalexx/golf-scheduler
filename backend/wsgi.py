from app import create_app

application = create_app()
app = application  # Flask looks for 'app' by default

if __name__ == '__main__':
    app.run(debug=True) 