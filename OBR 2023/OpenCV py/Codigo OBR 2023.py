#Importação de bibliotecas
import cv2
import numpy as np
import math
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

#Definição do input do vídeo
video = cv2.VideoCapture(0)
width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

error = 0
pixelG = 0
pixelB = 0
wC = 0
comando = ""


#Função enviar dados
def sendData(erro):
    print("Enviando o número")
    data = str(erro) + '\n' #data recebe o valor do numero em str
    ser.write(data.encode('utf-8')) #a raspberry envia o dado para a arduino
 

while True:
    ret, frame = video.read()
    ret, frameG = video.read()

    #Criação da máscara para linha preta
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lowerColor = np.array([0, 0, 0])
    upperColor = np.array([255, 255, 60])
    mask = cv2.inRange(hsvImage, lowerColor, upperColor)
    cropped = mask[0:150, 0:640]

    #Criação da máscara para marcação verde
    ImageGreen = cv2.cvtColor(frameG, cv2.COLOR_BGR2HSV)
    lowerGreen = np.array([35, 56, 97])
    upperGreen = np.array([83, 255, 255])
    maskG = cv2.inRange(ImageGreen, lowerGreen, upperGreen)

    #Criação da máscara para marcação azul
    ImageBlue = cv2.cvtColor(frameG, cv2.COLOR_BGR2HSV)
    lowerBlue = np.array([83, 55, 0])
    upperBlue = np.array([121, 255, 255])
    maskB = cv2.inRange(ImageBlue, lowerBlue, upperBlue)

    #Gera os contornos
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contoursC, hierarchy = cv2.findContours(cropped, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contoursG, hierarchy = cv2.findContours(maskG, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contoursB, hierarchy = cv2.findContours(maskB, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #Analisa os contornos preto
    if contours:
        #Calcula o contorno da linha preta
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] !=0 :
            #Cria os pontos da linha preta
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #Calcula o erro
            erro = cx-319
            
            #Desenha os valores da linha preta na tela
            cv2.line(frame, (320,cy),(cx,cy), (255,0,0), 2)
            cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
            cv2.circle(frame, (320,cy), 5, (0,255,0), -1)
            cv2.line(frame, (320,0),(320,360), (0,0,255), 1)
            #cv2.putText(frame, "Erro: ",(40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,190,0), 2)
            cv2.putText(frame, str(comando),(40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,190,0), 2)
            cv2.drawContours(frame, c, -1, (0,255,0), 1)

    #Analisa os contornos preto de cima
    if contoursC:
        maxAreaC = cv2.contourArea(contoursC[0])
        contourMaxAreaIdC = 0
        iC = 0
        #Pra cada contorno de cima
        for cntC in contoursC:
            if maxAreaC < cv2.contourArea(cntC):
                maxAreaC = cv2.contourArea(cntC)
                contourMaxAreaIdC = iC
                
            iC += 1
        #Gera o quadrado preto de cima
        cntMaxAreaC = contoursC[contourMaxAreaIdC]
        xC, yC, wC, hC = cv2.boundingRect(cntMaxAreaC)
        cv2.rectangle(frame, (xC,yC), (xC+wC,yC+hC),(255,0,255),3)


    #Cálculo do verde
    if contoursG:
        maxAreaG = cv2.contourArea(contoursG[0])
        contourMaxAreaIdG = 0
        iG = 0

        #Analisa os contornos do verde
        for cntG in contoursG:
            if maxAreaG < cv2.contourArea(cntG):
                maxAreaG = cv2.contourArea(cntG)
                contourMaxAreaIdG = iG
            iG += 1

        #Gera o quadrado do verde
        cntMaxAreaG = contoursG[contourMaxAreaIdG]
        xG, yG, wG, hG = cv2.boundingRect(cntMaxAreaG)

        cv2.rectangle(frame, (xG,yG), (xG+wG,yG+hG),(0,255,0),2)

        #Calcula a quantidade de pixels verdes na tela
        pixelG = np.sum (maskG == 255)

    #Cálculo do blue
    if contoursB:
        maxAreaB = cv2.contourArea(contoursB[0])
        contourMaxAreaIdB = 0
        iB = 0

        #Analisa os contornos do azul
        for cntB in contoursB:
            if maxAreaB < cv2.contourArea(cntB):
                maxAreaB = cv2.contourArea(cntB)
                contourMaxAreaIdB = iB
            iB += 1

        #Gera o quadrado do azul
        cntMaxAreaB = contoursB[contourMaxAreaIdB]
        xB, yB, wB, hB = cv2.boundingRect(cntMaxAreaB)

        #Calcula a quantidade de pixels verdes na tela
        pixelB = np.sum (maskB == 255)
        


    if pixelB > 2000:
            cv2.rectangle(frame, (xB,yB), (xB+wB,yB+hB),(255,0,0),2)
            comando = "kit de resgate"
            sendData(1026)
            print(comando)
    else:
        comando = erro
        print("Erro: ", comando)
        sendData(erro)

    if pixelG > 10000 and wC > 350 and yG > yC:
        if pixelG < 109999:
            #Se o meio do verde estiver para a direita da linha
            if round(xG + (wG / 2)) > cx:
                comando = "verde direta"
                sendData(1023)
                print(comando)

            #Se não, é esquerda
            else:
                comando = "verde esquerda"
                sendData(1024)
                print(comando)
        else:
            comando = "meia volta"
            sendData(1025)
            print(comando)

    else:
        comando = erro
        print("Erro: ", comando)
        sendData(erro)

    


    #cv2.imshow("black line mask", mask)
    #cv2.imshow("cropped mask", cropped)
    #cv2.imshow("green mask", maskG)
    cv2.imshow("mascara", frame)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

video.release()
cv2.destroyAllWindows
