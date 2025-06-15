
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Caminho para o arquivo de recordes
SCORES_FILE = "recordes.txt"

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Página do jogo
@app.route("/game")
def game():
    return render_template("game.html")

# Servir arquivos estáticos (imagens, sons)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Função para carregar os recordes
def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Função para salvar os recordes
def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f)

# Rota para adicionar um novo score
@app.route("/score", methods=["POST"])
def add_score():
    data = request.get_json()
    if not all(k in data for k in ("name", "stage", "time")):
        return jsonify({"error": "Invalid data"}), 400

    scores = load_scores()
    scores.append(data)
    scores = sorted(scores, key=lambda x: (-x["stage"], x["time"]))[:5]
    save_scores(scores)
    return jsonify({"message": "Score added"}), 200

# Rota para obter os scores
@app.route("/score", methods=["GET"])
def get_scores():
    scores = load_scores()
    return jsonify(scores)

if __name__ == "__main__":
    app.run(debug=True)
