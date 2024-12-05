from flask import Flask, render_template

app = Flask("sccproject")

@app.route("/")
def hello_world():
     return render_template('index.html', person1="Aouni", person2="Peter")


if __name__ == "__main__":
    app.run(debug=True)