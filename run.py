from flask import Flask, json, render_template, make_response, request, jsonify

app = Flask(__name__)

app.url_map.strict_slashes = False

app.config['JSON_SORT_KEYS'] = False

class cliente:

    def __init__(self, id, nome, email, data_cadastro):
        self._id = id
        self._nome = nome
        self._email = email
        self._data_cadastro = data_cadastro

class produto:

    def __init__(self, id, nome, categoria, data_cadastro):
        self._id = id
        self._nome = nome
        self._categoria = categoria
        self._data_cadastro = data_cadastro

lista_clientes = [cliente(1,"a","a@a","14/05/2021"), cliente(2,"b","b@b","14/05/2021"), cliente(3,"c","c@c","14/05/2021")]
lista_produtos = [produto(1,"a","higiene","14/05/2021"), produto(2,"b","limpeza","14/05/2021"), produto(3,"c","alimento","14/05/2021")]

@app.route("/")
def home():
    return "<h1 style='color:red'>Home!</h1>"


@app.route("/v1/cliente/", methods=["GET","POST"])
def cadastra_cliente():
    
    # o envio dos dados do cliente deve ser feito por json no corpo da requisição
    data = request.get_json()
    dic = { i._id:(i._nome, i._email, i._data_cadastro) for i in lista_clientes}

    if request.method == "POST":
        cli = cliente(data["id"], data["nome"], data["email"], data["data_cadastro"])

        for c in lista_clientes:
            if c._id == cli._id:
                print("\nO cliente que tentou cadastrar já existe.\n")
                return make_response("O cadastro falhou, pois o cliente que tentou cadastrar já existe.",409) 
        
        lista_clientes.append(cli)
        print("\nCliente cadastrado com sucesso:",data,"\n")

        return make_response(jsonify({ "id" : cli._id, "nome": cli._nome, "e-mail" : cli._email, "data de cadastro" : cli._data_cadastro}),201)

    # GET - visualiza a lista de clientes completa na página html
    return render_template("views.html", lista=dic),200

@app.route("/v1/produto/", methods=["GET","POST"])
def cadastra_produto():
    
    # o envio dos dados do produto deve ser feito por json no corpo da requisição
    data = request.get_json()
    dic =  {i._id:(i._nome, i._categoria, i._data_cadastro) for i in lista_produtos}

    if request.method == "POST":
        prod = produto(data["id"], data["nome"], data["categoria"], data["data_cadastro"])

        for p in lista_produtos:
            if p._id == prod._id:
                print("\nO produto que tentou cadastrar já existe.\n")
                return make_response("O cadastro falhou, pois o produto que tentou cadastrar já existe.", 409)

        lista_produtos.append(prod)
        print("\nProduto cadastrado com sucesso:",data,"\n")

        return make_response(jsonify({ "id" : prod._id, "nome": prod._nome, "categoria" : prod._categoria, "data de cadastro" : prod._data_cadastro}),201)

    # GET - visualiza a lista de produtos completa na página html
    return render_template("views.html", lista=dic),200

@app.route("/v1/cliente/<id>/")
def busca_cliente_id(id):

    print("\nId enviado: ",id,"\n")

    for cli in lista_clientes:
        if int(id) == cli._id:
            return make_response(f"Cliente de id {id}: \nNome: {cli._nome} \nE-mail: {cli._email} \nData de cadastro: {cli._data_cadastro}",200)
            
            # resposta na página html
            # return render_template("view_busca.html", id=id),200
    return make_response(f"Cliente com id {id} não encontrado", 400)

    # resposta na página html
    # return render_template("view_busca.html", id=-1, tipo="cliente"),400

@app.route("/v1/produto/<id>/")
def busca_produto_id(id):

    print("\nId enviado: ",id,"\n")
    
    for prod in lista_produtos:
        if int(id) == prod._id:
            return make_response(jsonify({"id" : id}),200)
            
            # resposta na página html
            # return render_template("view_busca.html", id=id),200
    
    return make_response(jsonify("Id não encontrado",{"id": id}), 400)
    
    # resposta na página html
    # return render_template("view_busca.html", id=-1, tipo="produto"),400

if __name__ == "__main__":
    app.run()
