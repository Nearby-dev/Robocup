
import cv2
import numpy as np
from random import randint
import time

#Definindo o vídeo
video = cv2.VideoCapture(0)

#Kernel para dilatação
kernel = np.ones((10, 10), np.uint8) #"Parâmetros"


#Lendo valores do vídeo e tratamento HSV
ret, frame = video.read() #Lê o vídeo
hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Transforma o BGR em HSV



#================================================================
#=============== SELEÇÃO DA ÁREA PARA CALIBRAR ==================
#================================================================

#Seleção de ROI (Region of interest)
selection = cv2.selectROI('selection', frame) #Seleção
print(selection) #Printa coordenadas


#Salvamento das coordenadas do ROI
selection = list(selection) #Salva coordenadas em uma lista
x, y, w, h = selection[1], selection[0], selection[3], selection[2] #Separa os valores
print(x, y, w, h) #Printa as coordenadas


#Gera um vídeo apenas com a imagem do ROI
cropped = hsvImage[x:x+w, y:y+h] #Corta o vídeo
cv2.imshow("cropped", cropped) #Mostra o vídeo cortado
cv2.waitKey(0) #Espera o INPUT de alguma tecla
cv2.destroyWindow("cropped") #Fecha a janela com o vídeo



#================================================================
#======== CALIBRAÇÃO DOS VALORES HUE, SATURATION, VALUE =========
#================================================================

#Dando valores iniciais para HSV
(hue, sat, val) = hsvImage[round(w/2),round(h/2)] #Lê valores HSV do pixel especificado
hue_min, hue_max, sat_min, sat_max, val_min, val_max = hue,hue,sat,sat,val,val #Valores de corte iniciais

#------ Verificação de cada pixel da imagem -------

#Verificação das linhas X
for a in range(round(w)): #Para cada pixel na largura da imagem:

    #Verificação das colunas Y
    for b in range(round(h)): #Para cada pixel na altura da imagem:

        print("X:", a+x, "Y:", b+y) #Printa que pixel está sendo analisado no momento

        #Definição dos valores de corte ======================================
        (hue, sat, val) = cropped[(a), (b)] #Pega os valores HSV do pixel atual

        #= HUE ========================
        if hue < hue_min: #Se Hue atual for menor que o menor Hue já lido
            hue_min = hue #Hue mínimo se torna o Hue atual
            #print("Hue min: ", hue_min)

        if hue > hue_max: #Se Hue atual for maior que o maior Hue já lido
            hue_max = hue #Hue máximo se torna o Hue atual
            #print("Hue max: ", hue_max)

        #= SATURATION =================
        if sat < sat_min:
            sat_min = sat
            #print("Sat min: ", sat_min)

        if sat > sat_max:
            sat_max = sat
            #print("Sat max: ", sat_max)

        #= VALUE ========================
        if val < val_min:
            val_min = val
            #print("Val max: ", val_max)
            
        if val > val_max:
            val_max = val
            #print("Val max: ", val_max)


#Só para limpeza, transforma todos os valores em integrals
hue_min, hue_max = int(hue_min), int(hue_max)
sat_min, sat_max = int(sat_min), int(sat_max)
val_min, val_max = int(val_min), int(val_max)
print(hue_min, hue_max, sat_min, sat_max, val_min, val_max) #Printa os valores de corte


#================================================================
#========= IDENTIFICAÇÃO DE COR COM OS VALORES DE CORTE =========
#================================================================
while True:
    #GERAÇÃO DA MÁSCARA =========================
    ret, frame = video.read() #Lê o vídeo
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Converte de BGR para HSV
    lowerColor = np.array([hue_min, sat_min, val_min]) #Salva os valores de corte mínimos em uma variável
    upperColor = np.array([hue_max, sat_max, val_max]) #Salva os valores de corte máximos em uma variável
    mask = cv2.inRange(hsvImage, lowerColor, upperColor) #Gera a máscara com os valores de corte
    maskedFrame = cv2.bitwise_and(frame, frame, mask = mask) #Mistura a máscara com o vídeo


    #GERAÇÃO DO QUADRADO =======================
    #Acha os contornos da máscara
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if contours: #Se tiver contornos
        maxArea = cv2.contourArea(contours[0]) #Define onde tem a maior área de contorno
        contourMaxAreaId = 0 #Cria a variável que dira o ID dos contornos lidos
        i = 0 #Para definir o ID

        for cnt in contours: #Para cada contorno
            if maxArea < cv2.contourArea(cnt): #Se a área analisada for a maior que área máxima
                maxArea = cv2.contourArea(cnt) #Área máxima se torna a área analisada
                contourMaxAreaId = i #Define o ID da area máxima
            i += 1 #Aumenta 1 no ID

        cntMaxArea = contours[contourMaxAreaId] #Contorno de maior área é igual ao ID da maior área

        x, y, w, h = cv2.boundingRect(cntMaxArea) #Salva os coordenadas da maior área

        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,0,255),2) #Gera um retângulo com as coordenadas
    
    
    #MOSTRANDO VÍDEOS =======================
    cv2.imshow("webcam", frame) #Mostra o vídeo
    cv2.imshow("mask", mask) #Mostra a máscara
    cv2.imshow("masked frame", maskedFrame) #Mostra o vídeo com máscara
    
    if cv2.waitKey(1) & 0xff == ord("q"): #Se a tecla "Q" for apertada
        break #Quebra o "While True"

video.release() #Para de analisar o vídeo
cv2.destroyAllWindows #Fecha todas as janelas