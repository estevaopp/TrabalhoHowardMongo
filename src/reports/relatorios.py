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

    def get_relatorio_medicos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["medicos"].find({}, 
                                                     {"crm": 1, 
                                                      "valor_consulta": 1, 
                                                      "nome": 1, 
                                                      "_id": 0
                                                     }).sort("nome", ASCENDING)
        df_medico = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_medico)        
        input("Pressione Enter para Sair do Relatório de Medicos")

    def get_relatorio_agendamentos(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["agendamentos"].aggregate([
                                                    {
                                                        '$lookup': {
                                                            'from': 'medicos', 
                                                            'localField': 'crm', 
                                                            'foreignField': 'crm', 
                                                            'as': 'medico'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$medico'
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_agendamento': 1, 
                                                            'data_agendamento': 1, 
                                                            'empresa': '$medico.nome', 
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
                                                            'codigo_agendamento': 1, 
                                                            'data_agendamento': 1, 
                                                            'empresa': 1, 
                                                            'paciente': '$paciente.nome', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$lookup': {
                                                            'from': 'itens_agendamento', 
                                                            'localField': 'codigo_agendamento', 
                                                            'foreignField': 'codigo_agendamento', 
                                                            'as': 'item'
                                                        }
                                                    }, {
                                                        '$unwind': {
                                                            'path': '$item', 'preserveNullAndEmptyArrays': True
                                                        }
                                                    }, {
                                                        '$project': {
                                                            'codigo_agendamento': 1, 
                                                            'data_agendamento': 1, 
                                                            'empresa': 1, 
                                                            'paciente': 1, 
                                                            'item_agendamento': '$item.codigo_item_agendamento', 
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
                                                            'codigo_agendamento': 1, 
                                                            'data_agendamento': 1, 
                                                            'empresa': 1, 
                                                            'paciente': 1, 
                                                            'item_agendamento': 1, 
                                                            'quantidade': 1, 
                                                            'valor_unitario': 1, 
                                                            'valor_total': 1, 
                                                            'produto': '$produto.descricao_produto', 
                                                            '_id': 0
                                                        }
                                                    }, {
                                                        '$sort': {
                                                            'paciente': 1,
                                                            'item_agendamento': 1
                                                        }
                                                    }
                                                ])
        df_agendamento = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        print(df_agendamento[["codigo_agendamento", "data_agendamento", "paciente", "empresa", "item_agendamento", "produto", "quantidade", "valor_unitario", "valor_total"]])
        input("Pressione Enter para Sair do Relatório de Agendamento")
    
    