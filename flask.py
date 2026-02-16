from flask import Flask

app = Flask(__name__)

# adds the route "/" to the application
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__== "__main__":
    app.run(debug=True)

# to run the flas app, use the command
# falsk run
# python flask.py
