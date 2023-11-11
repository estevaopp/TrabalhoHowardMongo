from datetime import date
from model.pacientes import Paciente
from model.medicos import Medico

class Agendamento:
    def __init__(self, 
                 codigo_agendamento:int=None,
                 data_agendamento:date=None,
                 paciente:Paciente= None,
                 medico:Medico=None
                 ):
        self.set_codigo_agendamento(codigo_agendamento)
        self.set_data_agendamento(data_agendamento)
        self.set_paciente(paciente)
        self.set_medico(medico)


    def set_codigo_agendamento(self, codigo_agendamento:int):
        self.codigo_agendamento = codigo_agendamento

    def set_data_agendamento(self, data_agendamento:date):
        self.data_agendamento = data_agendamento

    def set_paciente(self, paciente:Paciente):
        self.paciente = paciente

    def set_medico(self, medico:Medico):
        self.medico = medico

    def get_codigo_agendamento(self) -> int:
        return self.codigo_agendamento

    def get_data_agendamento(self) -> date:
        return self.data_agendamento

    def get_paciente(self) -> Paciente:
        return self.paciente

    def get_medico(self) -> Medico:
        return self.medico

    def to_string(self) -> str:
        return f"Agendameto: {self.get_codigo_agendamento()} | Data: {self.get_data_agendamento()} | Paciente: {self.get_paciente().get_nome()} | Medico: {self.get_medico().get_nome()}"