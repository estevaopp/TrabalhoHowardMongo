import pandas as pd
from model.medicos import Medico
from conexion.mongo_queries import MongoQueries

class Controller_Medico:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_medico(self) -> Medico:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo CRM
        crm = input("CRM (Novo): ")

        if self.verifica_existencia_medico(crm):
            # Solicita ao usuario a nova razão social
            valor_consulta = float(input("Razão Social (Novo): "))
            # Solicita ao usuario o novo nome fantasia
            nome = input("Nome Fantasia (Novo): ")
            # Insere e persiste o novo medico
            self.mongo.db["medicos"].insert_one({"crm": crm, "valor_consulta": valor_consulta, "nome": nome})
            # Recupera os dados do novo medico criado transformando em um DataFrame
            df_medico = self.recupera_medico(crm)
            # Cria um novo objeto medico
            novo_medico = Medico(df_medico.crm.values[0], df_medico.valor_consulta.values[0], df_medico.nome.values[0])
            # Exibe os atributos do novo medico
            print(novo_medico.to_string())
            self.mongo.close()
            # Retorna o objeto novo_medico para utilização posterior, caso necessário
            return novo_medico
        else:
            self.mongo.close()
            print(f"O CRM {crm} já está cadastrado.")
            return None

    def atualizar_medico(self) -> Medico:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do medico a ser alterado
        crm = int(input("CRM do medico que deseja atualizar: "))

        # Verifica se o medico existe na base de dados
        if not self.verifica_existencia_medico(crm):
            # Solicita ao usuario a nova razão social
            valor_consulta = float(input("Razão Social (Novo): "))
            # Solicita ao usuario o novo nome fantasia
            nome = input("Nome Fantasia (Novo): ")            
            # Atualiza o nome do medico existente
            self.mongo.db["medicos"].update_one({"crm":f"{crm}"},{"$set": {"valor_consulta":valor_consulta, "nome":nome}})
            # Recupera os dados do novo medico criado transformando em um DataFrame
            df_medico = self.recupera_medico(crm)
            # Cria um novo objeto medico
            medico_atualizado = Medico(df_medico.crm.values[0], df_medico.valor_consulta.values[0], df_medico.nome.values[0])
            # Exibe os atributos do novo medico
            print(medico_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto medico_atualizado para utilização posterior, caso necessário
            return medico_atualizado
        else:
            self.mongo.close()
            print(f"O CRM {crm} não existe.")
            return None

    def excluir_medico(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o CPF do medico a ser alterado
        crm = int(input("CRM do medico que irá excluir: "))        

        # Verifica se o medico existe na base de dados
        if not self.verifica_existencia_medico(crm):            
            # Recupera os dados do novo medico criado transformando em um DataFrame
            df_medico = self.recupera_medico(crm)
            # Revome o medico da tabela
            self.mongo.db["medicos"].delete_one({"crm":f"{crm}"})
            # Cria um novo objeto medico para informar que foi removido
            medico_excluido = Medico(df_medico.crm.values[0], df_medico.valor_consulta.values[0], df_medico.nome.values[0])
            self.mongo.close()
            # Exibe os atributos do medico excluído
            print("medico Removido com Sucesso!")
            print(medico_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O CRM {crm} não existe.")

    def verifica_existencia_medico(self, crm:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo medico criado transformando em um DataFrame
        df_medico = pd.DataFrame(self.mongo.db["medicos"].find({"crm":f"{crm}"}, {"crm": 1, "valor_consulta": 1, "nome": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_medico.empty

    def recupera_medico(self, crm:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo medico criado transformando em um DataFrame
        df_medico = pd.DataFrame(list(self.mongo.db["medicos"].find({"crm":f"{crm}"}, {"crm": 1, "valor_consulta": 1, "nome": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_medico