import pandas as pd
from model.pacientes import Paciente
from conexion.mongo_queries import MongoQueries

class Controller_Paciente:
    def __init__(self):
        self.mongo = MongoQueries()
        
    def inserir_paciente(self) -> Paciente:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_paciente(cpf):
            # Solicita ao usuario o novo nome
            nome = input("Nome (Novo): ")

            telefone = input("Telefone (Novo): ")
            # Insere e persiste o novo paciente
            self.mongo.db["pacientes"].insert_one({"cpf": cpf, "nome": nome, "telefone":telefone})
            # Recupera os dados do novo paciente criado transformando em um DataFrame
            df_paciente = self.recupera_paciente(cpf)
            # Cria um novo objeto Paciente
            novo_paciente = Paciente(df_paciente.cpf.values[0], df_paciente.nome.values[0], df_paciente.telefone.values[0])
            # Exibe os atributos do novo paciente
            print(novo_paciente.to_string())
            self.mongo.close()
            # Retorna o objeto novo_paciente para utilização posterior, caso necessário
            return novo_paciente
        else:
            self.mongo.close()
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_paciente(self) -> Paciente:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do paciente a ser alterado
        cpf = input("CPF do paciente que deseja alterar o nome: ")

        # Verifica se o paciente existe na base de dados
        if not self.verifica_existencia_paciente(cpf):
            # Solicita a nova descrição do paciente
            novo_nome = input("Nome (Novo): ")
            novo_telefone = input("Telefone (Novo): ")
            # Atualiza o nome do paciente existente
            self.mongo.db["pacientes"].update_one({"cpf": f"{cpf}"}, {"$set": {"nome": novo_nome}, "$set": {"telefone": novo_telefone}})
            # Recupera os dados do novo paciente criado transformando em um DataFrame
            df_paciente = self.recupera_paciente(cpf)
            # Cria um novo objeto paciente
            paciente_atualizado = Paciente(df_paciente.cpf.values[0], df_paciente.nome.values[0], df_paciente.telefone.values[0])
            # Exibe os atributos do novo paciente
            print(paciente_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto paciente_atualizado para utilização posterior, caso necessário
            return paciente_atualizado
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_paciente(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o CPF do Paciente a ser alterado
        cpf = input("CPF do Paciente que irá excluir: ")

        # Verifica se o paciente existe na base de dados
        if not self.verifica_existencia_paciente(cpf):            
            # Recupera os dados do novo paciente criado transformando em um DataFrame
            df_paciente = self.recupera_paciente(cpf)
            # Revome o paciente da tabela
            self.mongo.db["pacientes"].delete_one({"cpf":f"{cpf}"})
            # Cria um novo objeto Paciente para informar que foi removido
            paciente_excluido = Paciente(df_paciente.cpf.values[0], df_paciente.nome.values[0], df_paciente.telefone.values[0])
            self.mongo.close()
            # Exibe os atributos do paciente excluído
            print("Paciente Removido com Sucesso!")
            print(paciente_excluido.to_string())
        else:
            self.mongo.close()
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_paciente(self, cpf:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo paciente criado transformando em um DataFrame
        df_paciente = pd.DataFrame(self.mongo.db["pacientes"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_paciente.empty

    def recupera_paciente(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo paciente criado transformando em um DataFrame
        df_paciente = pd.DataFrame(list(self.mongo.db["pacientes"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "telefone": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_paciente