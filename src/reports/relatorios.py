from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_pacientes(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["pacientes"].find({}, 
                                                 {"cpf": 1, 
                                                  "nome": 1, 
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        df_paciente = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_paciente)
        input("Pressione Enter para Sair do Relatório de Pacientes")

    def get_relatorio_fornecedores(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["fornecedores"].find({}, 
                                                     {"cnpj": 1, 
                                                      "razao_social": 1, 
                                                      "nome_fantasia": 1, 
                                                      "_id": 0
                                                     }).sort("nome_fantasia", ASCENDING)
        df_fornecedor = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_fornecedor)        
        input("Pressione Enter para Sair do Relatório de Fornecedores")

    def get_relatorio_pedidos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["pedidos"].aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'fornecedores', 
                                                            'localField': 'cnpj', 
                                                            'foreignField': 'cnpj', 
                                                            'as': 'fornecedor'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$fornecedor'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1, 
                                                            'data_pedido': 1, 
                                                            'empresa': '$fornecedor.nome_fantasia', 
                                                            'cpf': 1, 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'pacientes', 
                                                            'localField': 'cpf', 
                                                            'foreignField': 'cpf', 
                                                            'as': 'paciente'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$paciente'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1, 
                                                            'data_pedido': 1, 
                                                            'empresa': 1, 
                                                            'paciente': '$paciente.nome', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'itens_pedido', 
                                                            'localField': 'codigo_pedido', 
                                                            'foreignField': 'codigo_pedido', 
                                                            'as': 'item'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$item', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1, 
                                                            'data_pedido': 1, 
                                                            'empresa': 1, 
                                                            'paciente': 1, 
                                                            'item_pedido': '$item.codigo_item_pedido', 
                                                            'quantidade': '$item.quantidade', 
                                                            'valor_unitario': '$item.valor_unitario', 
                                                            'valor_total': {
                                                                '$multiply': [
                                                                    '$item.quantidade', '$item.valor_unitario'
                                                                ]
                                                            }, 
                                                            'codigo_produto': '$item.codigo_produto', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'produtos', 
                                                            'localField': 'codigo_produto', 
                                                            'foreignField': 'codigo_produto', 
                                                            'as': 'produto'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$produto', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_pedido': 1, 
                                                            'data_pedido': 1, 
                                                            'empresa': 1, 
                                                            'paciente': 1, 
                                                            'item_pedido': 1, 
                                                            'quantidade': 1, 
                                                            'valor_unitario': 1, 
                                                            'valor_total': 1, 
                                                            'produto': '$produto.descricao_produto', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'paciente': 1,
                                                            'item_pedido': 1
                                                        }
                                                    }
                                                ])
        df_pedido = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        print(df_pedido[["codigo_pedido", "data_pedido", "paciente", "empresa", "item_pedido", "produto", "quantidade", "valor_unitario", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Pedidos")
    
    