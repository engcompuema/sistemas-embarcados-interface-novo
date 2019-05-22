import json
import requests
import tkinter
from tkinter import *


# Funcões
def request_api():
    req = requests.get("https://monitoramento-embarcado.herokuapp.com/monitoramento/HPR-1130")
    infos = req.json()
    placa = StringVar(value=infos['data']['placa'])
    status = StringVar(value=infos['data']['status'])

    input_placa["textvariable"] = placa
    input_statusveic["textvariable"] = status

def inicia_interface():
    global input_placa
    global input_statusveic

    wd = tkinter.Tk()
    wd.title("Sistema de Processamento Veicular")
    wd.geometry("900x500")

    lbl_nomeImg = tkinter.Label(wd, text="Imagem", font=(16))
    lbl_nomeImg.grid(row=0, column=0, sticky=W, padx=5, pady=3)

    lbl_espacoImg = tkinter.Label(wd, bg="white", height=25, width=65)
    lbl_espacoImg.grid(row=1, column=0, padx=10, pady=10, columnspan=2, rowspan=4)

    lbl_statusServ = tkinter.Label(wd, text="Status do Serviço: ",  font=16)
    lbl_statusServ.grid(row=1, column=3, padx=10, sticky=NW)

    lbl_statusMode = tkinter.Label(wd, font=14, text="ON", fg="green")
    lbl_statusMode.grid(row=1, column=4, sticky=NW)

    lbl_placa = tkinter.Label(wd, text="Placa: ",  font=16)
    lbl_placa.grid(row=2, column=3, padx=10, sticky=NW)

    input_placa = tkinter.Entry(wd, state=DISABLED)
    input_placa.grid(row=2, column=4, sticky=NW)

    lbl_prop = tkinter.Label(wd, text="Proprietário: ",  font=16)
    lbl_prop.grid(row=4, column=3, padx=10, sticky=NW)

    nome = StringVar(value="fulaninho")

    input_prop = tkinter.Entry(wd, state=DISABLED, width=40, textvariable=nome)
    input_prop.grid(row=4, column=4, sticky=NW)

    lbl_statusveic = tkinter.Label(wd, text="Status do Veiculo: ",  font=16)
    lbl_statusveic.grid(row=3, column=3, padx=10, pady=3, sticky=NW)

    input_statusveic = tkinter.Entry(wd, state=DISABLED)
    input_statusveic.grid(row=3, column=4, sticky=NW)

    btn_imagem = tkinter.Button(wd, text="Imagem")
    btn_imagem.grid(row=6, column=0, sticky=E)

    btn_Processar = tkinter.Button(wd, text="Processar", command=request_api)
    btn_Processar.grid(row=6, column=1, sticky=W)

    wd.mainloop()

inicia_interface()
