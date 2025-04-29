from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = "segredo_simples"  # Pode ser mais seguro em produção

# Usuários: username -> (senha, tipo)
USUARIOS = {
    "adm": ("admin123", "admin"),
    "joao": ("estudante123", "estudante"),
}

CAMINHO_ARQUIVO = "comentarios.txt"

def ler_comentarios():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f.readlines() if linha.strip()]

def salvar_comentario(usuario, comentario):
    with open(CAMINHO_ARQUIVO, "a", encoding="utf-8") as f:
        f.write(f"{usuario}: {comentario}\n")

@app.route("/", methods=["GET", "POST"])
def index():
    if "usuario" not in session:
        return redirect(url_for("login"))

    tipo = session.get("tipo")
    usuario = session.get("usuario")

    if request.method == "POST" and tipo == "estudante":
        comentario = request.form.get("comentario")
        if comentario:
            salvar_comentario(usuario, comentario)
        return redirect(url_for("index"))

    comentarios = ler_comentarios() if tipo == "admin" else []
    return render_template("index.html", comentarios=comentarios, tipo=tipo, usuario=usuario)

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        if usuario in USUARIOS and USUARIOS[usuario][0] == senha:
            session["usuario"] = usuario
            session["tipo"] = USUARIOS[usuario][1]
            return redirect(url_for("index"))
        else:
            erro = "Usuário ou senha inválidos."
    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
