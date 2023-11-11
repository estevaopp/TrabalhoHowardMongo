from utils import config

class SplashScreen:

    def __init__(self):
        # Nome(s) do(s) criador(es)
        self.created_by = "Estêvão Paulo Pereira, Dyana Luiz Oliveira, João Guilherme Pigatto da Silva, José Henrique Bessi Wolkers, Matheus Barros Barreto e Karolini Prando de Mattos"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_documents_count(self, collection_name):
        # Retorna o total de registros computado pela query
        df = config.query_count(collection_name=collection_name)
        return df[f"total_{collection_name}"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE VENDAS                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - PACIENTES:         {str(self.get_documents_count(collection_name="pacientes")).rjust(5)}
        #      2 - MEDICOS:     {str(self.get_documents_count(collection_name="medicos")).rjust(5)}
        #      3 - AGENDAMENTOS:          {str(self.get_documents_count(collection_name="agendamentos")).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """