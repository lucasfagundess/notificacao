from asyncore import loop
from genericpath import isfile
from sqlite3 import Date
from win10toast import ToastNotifier
from datetime import date, datetime
import webbrowser
import ctypes
import time 
import os

#Definir a pasta do processo
path = 'C:/Users/'+ os.getlogin() + '/Notificacao/'
#Definir o nome do arquivo de agendamento
file = 'agendamento.txt'
#Criar diretório e arquivo de agendamento, caso não existam
isExist = os.path.exists(path) 
if isExist == False:
    os.makedirs(path)
    cabecalho = 'tipo;descricao;data;horario'
    agendamento = open(path + file, "w+")
    agendamento.write(cabecalho)
    agendamento.close

#Iniciar notificador
toaster = ToastNotifier()

lista_notify = []
while(True):
    #Abrir arquivo de agendamento
    f = open(path + file, 'r')
    for line in f:
        agendamento = line.split(';')
        #Pular cabeçalho
        if str(agendamento[0]) == 'tipo': 
                continue
        #Se data e horario do agendamento forem iguais ao dia atual e hora atual:
        if (agendamento[2] == 'diario' and agendamento[3] == datetime.now().strftime('%H:%M')) or (agendamento[2] == date.today().strftime('%d/%m/%Y') and agendamento[3] == datetime.now().strftime('%H:%M')):
            #Verificar lista de agendamento: Se notificação do agendamento já tiver sido lançada, ignorar na próxima volta do loop
            if str(agendamento[1]) in lista_notify:
                break
            #Adicionar agendamento em uma lista
            lista_notify.append(agendamento[1])
            #Notificar no rodapé
            toaster.show_toast(
                agendamento[0],
                agendamento[1],
                threaded=True,
                icon_path=None,
                duration=30)
            time.sleep(1)
            #Notificar por message box
            ctypes.windll.user32.MessageBoxW(0, (str(agendamento[1])), 'Notificação', 1)
            #Ações extras
            if 'CLOCKIFY' in str(agendamento[1]).upper():
                webbrowser.open("https://app.clockify.me/timesheet")
        else: 
            #Limpar lista
            lista_notify = []
    time.sleep(5)