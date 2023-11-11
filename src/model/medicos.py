class Medico:
    def __init__(self, 
                 CRM:str=None,
                 nome:str=None,
                 valor_consulta:float=None
                 ):
        self.set_CRM(CRM)
        self.set_nome(nome)
        self.set_valor_consulta(valor_consulta)

    def set_CRM(self, CRM:str):
        self.CRM = CRM

    def set_nome(self, nome:str):
        self.nome = nome

    def set_valor_consulta(self, valor_consulta:float):
        self.valor_consulta = valor_consulta

    def get_CRM(self) -> str:
        return self.CRM

    def get_nome(self) -> str:
        return self.nome
    
    def get_valor_consulta(self) -> float:
        return self.valor_consulta

    def to_string(self) -> str:
        return f"CRM: {self.get_CRM()} | Nome: {self.get_nome()} | Valor Consulta: {self.get_valor_consulta()}"