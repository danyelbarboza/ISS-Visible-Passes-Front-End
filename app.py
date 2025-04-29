from flask import Flask, render_template, url_for, request, redirect
from controler import RunTheProgram

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
    passagens, nome_real_cidade, avaliacoes = RunTheProgram.obter_informacoes(cidade)
    
    return render_template("result.html", nome_real_cidade=nome_real_cidade, passagens=passagens, avaliacoes=avaliacoes)
        
if __name__ == "__main__":
    app.run(debug=True)
    

