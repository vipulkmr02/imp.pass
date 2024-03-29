from flask import Flask, render_template

app = Flask("IMP.PASS server")


@app.route('/', methods=['GET'])
def return_index():
    return render_template('index.html')

