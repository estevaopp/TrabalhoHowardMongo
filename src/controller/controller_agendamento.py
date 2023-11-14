import pandas as pd
from bson import ObjectId

from reports.relatorios import Relatorio

from model.agendamentos import Agendamento
from model.pacientes import Paciente
from model.medicos import Medico

from controller.controller_paciente import Controller_Paciente
from controller.controller_medico import Controller_Medico

from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Agendamento:
    def __init__(self):
        self.ctrl_paciente = Controller_Paciente()
        self.ctrl_medico = Controller_Medico()
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
    def inserir_agendamento(self) -> Agendamento:
        # Cria uma nova conexão com o banco
        self.mongo.connect()
        
        # Lista os pacientes existentes para inserir no agendamento
        self.relatorio.get_relatorio_pacientes()
        cpf = str(input("Digite o número do CPF do Paciente: "))
        paciente = self.valida_paciente(cpf)
        if paciente == None:
            return None

        # Lista os medicos existentes para inserir no agendamento
        self.relatorio.get_relatorio_medicos()
        crm = str(input("Digite o número do CRM do Medico: "))
        medico = self.valida_medico(crm)
        if medico == None:
            return None

        data_hoje = datetime.today().strftime("%m-%d-%Y")
        proximo_agendamento = self.mongo.db["agendamentos"].aggregate([
                                                            {
                                                                '$group': {
                                                                    '_id': '$agendamentos', 
                                                                    'proximo_agendamento': {
                                                                        '$max': '$codigo_agendamento'
                                                                    }
                                                                }
                                                            }, {
                                                                '$project': {
                                                                    'proximo_agendamento': {
                                                                        '$sum': [
                                                                            '$proximo_agendamento', 1
                                                                        ]
                                                                    }, 
                                                                    '_id': 0
                                                                }
                                                            }
                                                        ])

        proximo_agendamento = int(list(proximo_agendamento)[0]['proximo_agendamento'])
        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo_agendamento=proximo_agendamento, data_agendamento=data_hoje, cpf=paciente.get_CPF(), crm=medico.get_CRM())
        # Insere e Recupera o código do novo agendamento
        id_agendamento = self.mongo.db["agendamentos"].insert_one(data)
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_agendamento = self.recupera_agendamento(id_agendamento.inserted_id)
        # Cria um novo objeto Produto
        novo_agendamento = Agendamento(df_agendamento.codigo_agendamento.values[0], df_agendamento.data_agendamento.values[0], paciente, medico)
        # Exibe os atributos do novo produto
        print(novo_agendamento.to_string())
        self.mongo.close()
        # Retorna o objeto novo_agendamento para utilização posterior, caso necessário
        return novo_agendamento

    def atualizar_agendamento(self) -> Agendamento:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_agendamento = int(input("Código do Agendamento que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_agendamento(codigo_agendamento):

            # Lista os pacientes existentes para inserir no agendamento
            self.relatorio.get_relatorio_pacientes()
            cpf = str(input("Digite o número do CPF do Paciente: "))
            paciente = self.valida_paciente(cpf)
            if paciente == None:
                return None

            # Lista os medicos existentes para inserir no agendamento
            self.relatorio.get_relatorio_medicos()
            crm = str(input("Digite o número do CRM do Medico: "))
            medico = self.valida_medico(crm)
            if medico == None:
                return None

            data_hoje = datetime.today().strftime("%m-%d-%Y")

            # Atualiza a descrição do produto existente
            self.mongo.db["agendamentos"].update_one({"codigo_agendamento": codigo_agendamento}, 
                                                {"$set": {"crm": f'{medico.get_CRM()}',
                                                          "cpf":  f'{paciente.get_CPF()}',
                                                          "data_agendamento": data_hoje
                                                          }
                                                })
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_agendamento = self.recupera_agendamento_codigo(codigo_agendamento)
            # Cria um novo objeto Produto
            agendamento_atualizado = Agendamento(df_agendamento.codigo_agendamento.values[0], df_agendamento.data_agendamento.values[0], paciente, medico)
            # Exibe os atributos do novo produto
            print(agendamento_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto agendamento_atualizado para utilização posterior, caso necessário
            return agendamento_atualizado
        else:
            self.mongo.close()
            print(f"O código {codigo_agendamento} não existe.")
            return None

    def excluir_agendamento(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_agendamento = int(input("Código do Agendamento que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_agendamento(codigo_agendamento):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_agendamento = self.recupera_agendamento_codigo(codigo_agendamento)
            paciente = self.valida_paciente(df_agendamento.cpf.values[0])
            medico = self.valida_medico(df_agendamento.crm.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o agendamento {codigo_agendamento} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso o agendamento possua itens, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir o agendamento {codigo_agendamento} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Revome o produto da tabela
                    self.mongo.db["itens_agendamento"].delete_one({"codigo_agendamento": codigo_agendamento})
                    print("Itens do agendamento removidos com sucesso!")
                    self.mongo.db["agendamentos"].delete_one({"codigo_agendamento": codigo_agendamento})
                    # Cria um novo objeto Produto para informar que foi removido
                    agendamento_excluido = Agendamento(df_agendamento.codigo_agendamento.values[0], df_agendamento.data_agendamento.values[0], paciente, medico)
                    self.mongo.close()
                    # Exibe os atributos do produto excluído
                    print("Agendamento Removido com Sucesso!")
                    print(agendamento_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O código {codigo_agendamento} não existe.")

    def verifica_existencia_agendamento(self, codigo:int=None, external: bool = False) -> bool:
        # Recupera os dados do novo agendamento criado transformando em um DataFrame
        df_agendamento = self.recupera_agendamento_codigo(codigo=codigo, external=external)
        return df_agendamento.empty

    def recupera_agendamento(self, _id:ObjectId=None) -> bool:
        # Recupera os dados do novo agendamento criado transformando em um DataFrame
        df_agendamento = pd.DataFrame(list(self.mongo.db["agendamentos"].find({"_id":_id}, {"codigo_agendamento": 1, "data_agendamento": 1, "cpf": 1, "crm": 1, "_id": 0})))
        return df_agendamento

    def recupera_agendamento_codigo(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo agendamento criado transformando em um DataFrame
        df_agendamento = pd.DataFrame(list(self.mongo.db["agendamentos"].find({"codigo_agendamento": codigo}, {"codigo_agendamento": 1, "data_agendamento": 1, "cpf": 1, "crm": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_agendamento

    def valida_paciente(self, cpf:str=None) -> Paciente:
        if self.ctrl_paciente.verifica_existencia_paciente(cpf=cpf, external=True):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo paciente criado transformando em um DataFrame
            df_paciente = self.ctrl_paciente.recupera_paciente(cpf=cpf, external=True)
            # Cria um novo objeto paciente
            paciente = Paciente(df_paciente.cpf.values[0], df_paciente.nome.values[0], df_paciente.telefone.values[0])
            return paciente

    def valida_medico(self, crm:str=None) -> Medico:
        if self.ctrl_medico.verifica_existencia_medico(crm, external=True):
            print(f"O CRM {crm} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo medico criado transformando em um DataFrame
            df_medico = self.ctrl_medico.recupera_medico(crm, external=True)
            # Cria um novo objeto medico
            medico = Medico(df_medico.crm.values[0], df_medico.valor_consulta.values[0], df_medico.nome.values[0])
            return medico