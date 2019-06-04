import json
import requests
import tkinter
import os
import cv2
import pytesseract
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image


# Funcões       
def request_api(placa):

    req = requests.get("https://monitoramento-embarcado.herokuapp.com/monitoramento/" + placa)
    #req = requests.get("http://172.17.32.31:8080/monitoramento/veiculo/" + placa)
    
    infos = req.json()

    status = StringVar(value=infos['data']['status'])

    input_statusveic["textvariable"] = status



def open_img():
    filename = filedialog.askopenfilename(title='open')
    img = cv2.imread(filename)
    imgaux = cv2.resize(img, None, fx = 0.2, fy = 0.2)
    #cv2.imshow("Imagem",img)
    

    #Converte Escala de Cinza
    imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgCinzaaux = cv2.resize(imgCinza, None, fx = 0.2, fy = 0.2)
    #cv2.imshow("Carro Cinza", imgCinzaaux)

    #Função de Processamento
    processamento(imgCinza,img)


def processamento(imagemCinza, imagemOriginal):
    threshold = 120
    valorRec = 4
    urlTesseract = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


    _, imgBin = cv2.threshold(imagemCinza, 112, 255, cv2.THRESH_BINARY)
    imgBinaux = cv2.resize(imgBin, None, fx = 0.2, fy = 0.2)
    _, imgBin1 = cv2.threshold(imagemOriginal, 100, 255, cv2.THRESH_BINARY)
    desfoque = cv2.GaussianBlur(imgBin, (5, 5), 0)

    #Detectar Contornos
    contornos, hier = cv2.findContours(imgBin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for c in contornos:
        perimetro = cv2.arcLength(c, True)

        if perimetro > threshold:

            aprox = cv2.approxPolyDP(c, 0.02 * perimetro, True)

            if len(aprox) == valorRec:
                (x, y, alt, lar) = cv2.boundingRect(c)
                cv2.rectangle(imagemOriginal, (x, y), (x + alt, y + lar), (0, 255, 0), 2)
                aux = imagemOriginal[y:y + lar, x:x + alt]
                cv2.imwrite("PlacaFinal.jpg", aux)
                #cv2.imshow("Placa do Carro", aux)

    imgaux2 = cv2.resize(imagemOriginal, None, fx = 0.2, fy = 0.2)

    #Aumenta a imagem
    imagemAumentada = cv2.resize(aux, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    #conversão da imagem aumentada para escala de cinza
    imagemAumentada = cv2.cvtColor(imagemAumentada, cv2.COLOR_BGR2GRAY)

    #Binariza imagem
    ret, imagemAumentada = cv2.threshold(imagemAumentada, 105, 255, cv2.THRESH_BINARY)
   # ret, imagemAumentada = cv2.threshold(imagemAumentada, 120, 255, cv2.THRESH_BINARY)


    #Aplicação do filtro gaussiano, com kernel de 5 x 5
    imagemAumentada = cv2.GaussianBlur(imagemAumentada, (5, 5), 0)

    #Criando imagem aumentada do recorte da placa
    cv2.imwrite('novaimg.jpg', imagemAumentada)

    #Recuperação da imagem escrita, pelo atributo Image do PIL, pois o tesseract abre apenas arquivos dessa maneira
    imagem = Image.open('novaimg.jpg')

    #Seto o cmd do tesseract com o caminho de onde o mesmo está localizado
    pytesseract.pytesseract.tesseract_cmd = urlTesseract

    #Recupero a placa e faço a leitura da string da mesma e a printo
    saida = pytesseract.image_to_string(imagem)
    print(saida)
    placaReplace = saida.replace(":","-")
   # placaReplace = saida
    placa = StringVar(value=placaReplace)

    #Requisição API
    request_api(placaReplace)

    #Coloca informação no input 
    input_placa["textvariable"] = placa




def inicia_interface():
    global input_placa
    global input_statusveic
    global lbl_statusMode
    global lbl_espacoImg
    
    # Teste conexão
    #status_conect()

    wd = tkinter.Tk()
    wd.title("Sistema de Processamento Veicular")
    wd.geometry("900x500")

    lbl_nomeImg = tkinter.Label(wd, text="Imagem", font=(16))
    lbl_nomeImg.grid(row=0, column=0, sticky=W, padx=5, pady=3)

    lbl_espacoImg = tkinter.Label(wd, bg="white", height=25, width=65)
    lbl_espacoImg.grid(row=1, column=0, padx=10,pady=10, columnspan=2, rowspan=4)

    lbl_statusServ = tkinter.Label(wd, text="Status do Serviço: ",  font=16)
    lbl_statusServ.grid(row=1, column=3, padx=10, sticky=NW)

    lbl_statusMode = tkinter.Label(wd, font=14)
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

    btn_imagem = tkinter.Button(wd, text="Imagem", command=open_img)
    btn_imagem.grid(row=6, column=0, sticky=E)

    btn_Processar = tkinter.Button(wd, text="Processar", command=request_api)
    btn_Processar.grid(row=6, column=1, sticky=W)

    wd.mainloop()

    

# Função Principal
inicia_interface()
