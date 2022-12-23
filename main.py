from website import create_app

app = create_app()

# only run if this file is run not if it's imported
if __name__ == '__main__':
    app.run(debug=True)