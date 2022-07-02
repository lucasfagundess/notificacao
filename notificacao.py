from asyncore import loop
from email import message
from email.message import Message
from genericpath import isfile
from sqlite3 import Date
from tkinter import messagebox as mb
from traceback import print_tb
from turtle import title
from requests import options
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

def message_box(titulo,mensagem):
    return mb.askquestion(title=titulo,message=mensagem)
    

lista_notify = []
while(True):
    #Limpar a lista no inicio do dia
    if datetime.now().strftime('%H:%M') == '00:00':
        lista_notify = []
    #Abrir arquivo de agendamento
    f = open(path + file, 'r', encoding="utf-8")
    for line in f:
        agendamento = line.split(';')
        #Criar lista de horários, quando há mais que um
        horarios_agendamento = agendamento[3].replace('\n','').split(',')
        #Pular cabeçalho
        if str(agendamento[0]) == 'tipo': 
                continue
        #Se data e horario do agendamento forem iguais ao dia atual e hora atual:
        for horario_agendamento in horarios_agendamento:
            if horario_agendamento == 'hh':
                horario_agendamento = 'HH'
            if (agendamento[2] == 'diario' and horario_agendamento == datetime.now().strftime('%H:%M')) or (agendamento[2] == date.today().strftime('%d/%m/%Y') and horario_agendamento == datetime.now().strftime('%H:%M') or (horario_agendamento == 'HH' and datetime.now().strftime('%M') == '00')):
                #Verificar lista de agendamento: Se notificação do agendamento já tiver sido lançada, ignorar na próxima volta do loop
                if agendamento[1]+"-"+agendamento[2]+"-"+horario_agendamento in lista_notify:
                    break
                #Adicionar agendamento em uma lista
                lista_notify.append(agendamento[1]+"-"+agendamento[2]+"-"+horario_agendamento)
                #Notificar no rodapé
                toaster.show_toast(
                    agendamento[0],
                    agendamento[1],
                    threaded=True,
                    icon_path=None,
                    duration=30)
                time.sleep(1)
                #Notificar por message box
                ctypes.windll.user32.MessageBoxW(0, (str(agendamento[1])), agendamento[0], 1)
                #Ações extras
                if 'CLOCKIFY' in str(agendamento[1]).upper():
                    #Perguntar se já lançou as horas no clockify
                    res = message_box('CLOCKIFY','Já lançous suas horas no clockifY hoje?')
                    if res == 'no':
                        webbrowser.open("https://app.clockify.me/timesheet")
    time.sleep(5)   