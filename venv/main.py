from flask import Flask, request, jsonify, make_response
from dataBase import myDb

app = Flask(__name__)
app.config['JSON_SORT_KEY']=False


#cria um usuário
@app.route("/users/create", methods=['POST'])
def createUser():
    user = request.json
    sql = f"INSERT INTO users (nome, email, cpf, telefone) VALUES ('{user['nome']}', '{user['email']}', '{user['cpf']}', '{user['telefone']}')"
    myCursor = myDb.cursor()
    myCursor.execute(sql)
    myDb.commit()

    return make_response(
        jsonify(
            message='user has been created',
            data=user
        )
    )

#retorna todos os usuários cadastrados
@app.route("/", methods=['GET'])
def getUsers():
    user = request.json
    userList = list()
    table = 'users'
    sql = f'SELECT * FROM {table}'

    myCursor = myDb.cursor()
    myCursor.execute(sql)
    usersData = myCursor.fetchall()

    for user in usersData:
        userList.append(
            {
                "id": user[0],
                "nome": user[1],
                "email": user[2],
                "cpf": user[3],
                "telefone": user[4]
            }
        )
    
    if len(userList) == 0:
        return make_response(
            jsonify(
                message='the user list is empty',
                data=userList
            )
        )
    
    else:
        return make_response(
            jsonify(
                message='users list',
                data=userList
            )
        )

#altera um usuário através do id

@app.route("/users/update/<int:id>", methods=['PUT'])
def updateUser(id):
    newUser = request.json
    sql = f"UPDATE users SET nome = '{newUser['nome']}', cpf = '{newUser['cpf']}', email = '{newUser['email']}', telefone = '{newUser['telefone']}' WHERE id = {id}"
    myCursor = myDb.cursor()
    myCursor.execute(sql)
    myDb.commit()

    return make_response(
        jsonify(
            message='user has been updated',
            dada=newUser
        )
    )

#deleta um usuário através do id
@app.route("/users/delete/<int:id>", methods=['DELETE'])
def deleteUser(id):
    user = request.json
    sql = f'DELETE FROM users WHERE id = {id}'
    myCursor = myDb.cursor()
    myCursor.execute(sql)
    myDb.commit()

    return make_response(
        jsonify(
            message='user has been deleted',
            dada=user
        )
    )

if '__main__' == __name__:
    app.run(debug=True)