from flask import Flask, render_template, url_for, request, redirect, jsonify
from src.controller.controller import Controller

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<string:page_name>")
def works(page_name):
    return render_template(f"{page_name}.html")

@app.route("/buscar")
def buscar():
    cidade = request.args.get('cidade')
    passagens, nome_real_cidade, avaliacoes = Controller.obter_informacoes(cidade)
    
    return render_template("result.html", 
                         nome_real_cidade=nome_real_cidade,
                         passagens=passagens,
                         avaliacoes=avaliacoes)
    
# Uso: /api/passes?cidade=NOME_DA_CIDADE
@app.route("/api/passes")
def api_passes():
    cidade = request.args.get('cidade')
    if not cidade:
        return jsonify({"error": "O parâmetro 'cidade' é obrigatório."}), 400
    
    passagens, nome_real_cidade, avaliacoes = Controller.obter_informacoes(cidade)
    if not passagens:
        return jsonify({"error": "Cidade não encontrada."}), 404
    
    for i, p in enumerate(passagens):
        p['visibility_score'] = avaliacoes[i]

    response_data = {
        "query_city": cidade,
        "resolved_location": nome_real_cidade,
        "passes": passagens
    }
    
    return jsonify(response_data)
        
if __name__ == "__main__":
    app.run(debug=True)
    

