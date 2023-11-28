from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/episodes')
def pretend_endpoint():
    data = {"doug": "rules"}
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
