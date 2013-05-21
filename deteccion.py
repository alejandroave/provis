import random 
import cv ##libreria opencv para el tratamiento de las imagenes
import time ##libreria time para medir el rendimiento
from PIL import Image, ImageDraw,ImageFont ## librerias para tratamiento de imagenes

#cv.NamedWindow("Deteccion", 0)
#f=open("sim.txt","w")
arra = [] ## guardamos las coordenadas de los objetos

'''
def detec(imagen1,imagen2):
    ancho,altura,pixels,im = cargar(imagen1)
    ancho1,altura1,pixels1,im1 = cargar(imagen2)
    imagen=cv.LoadImage(imagen2,cv.CV_LOAD_IMAGE_COLOR)
    visitados = []
    for i in range(altura):
        visitados.append([])
        for j in range(ancho):
            visitados[i].append(0)
    i = 0
    j = 0

    while i < altura:
        while j < ancho:
            cont = 0
            fcont = 0
            for a in range(2):
                for b in range(2):
                     if i+a > 0 and j+b > 0 and i+a < altura and j+b < ancho:     
                         if pixels[j+b,i+a] == 0:  
                             cont += 1
                         fcont += 1
            if (cont*100/fcont) > 50:
                for a in range(2):
                    for b in range(2):
                        if i+a > 0 and j+b > 0 and i+a < altura and j+b < ancho:
                            visitados[i+a][j+b] = 1                                       
                            value = (150,150,150)
                            cv.Set2D(imagen, i+a,j+b, value)
                            #visitados[i+a][j+b] = 1
            j+=2
        i += 2
        j = 0                    
    #im1.save(imagen2)            
    return imagen,visitados
'''
'''
def lin(imagen,imagen2):
    imagen=cv.LoadImage(imagen,cv.CV_LOAD_IMAGE_COLOR)
    imagen2=cv.LoadImage(imagen2,cv.CV_LOAD_IMAGE_COLOR)
    x,y = cv.GetSize(imagen)
    pvisitados = []
    img = cv.CreateImage((x,y),cv.IPL_DEPTH_8U,3)  
    for i in range(x):
        men = 0
        for j in range(y):
            if cv.Get2D(imagen, j,i)[0] == 255:
                men = j
        if men != 0:
            cv.Set2D(imagen, men,i, (0,255,0))
            men = men - 1
            while men > 0:
                if cv.Get2D(imagen, men,i)[0] == 255:
                    men = 0
                cv.Set2D(imagen, men,i, (0,255,0))
                men = men-1
    cont = 0
    prueba = []
    con = 0
    contour = cv.FindContours(imagen2, imagen2, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)

    return imagen2
'''        

'''    
def chekar(visitados,ancho,altura):
    for y in range(altura):
        for x in range(ancho):
            if visitados[x][y] == 0:
                return x,y
            return 0,0
'''
'''
def cargar(imagen):
    im = Image.open(imagen)
    ancho, altura = im.size
    pixels = im.load()
    return ancho,altura,pixels,im
'''

## funcions que nos invierte blanco a negro y viciversa
def cambio(imagen):
    imagen=cv.LoadImage(imagen,cv.CV_LOAD_IMAGE_COLOR) ##cargamos imagen
    xx,yy = cv.GetSize(imagen) ##sacamos el tam
        
    for i in range(xx):
        for y in range(yy):
            if cv.Get2D(imagen, y,i) == (0.0,0.0,0.0,0.0):
                cv.Set2D(imagen, y,i, (255.0,255.0,255.0,255.0))
            else:
                cv.Set2D(imagen, y,i, (0.0,0.0,0.0,0.0))
            if y < yy/3: ## solo tomamos 3/4 de la imagen para verificacion
                cv.Set2D(imagen, y,i, (0.0,0.0,0.0,0.0))        
    cv.SaveImage("ngrey.jpg",imagen) ##guardamos la imagen



#def che():
    
##funcion para verificar los objetos
def de(puntos,anch,alt):
    global arra
    nuevo = []
    for i in range(len(puntos)): ##leemos los puntos resividos
        cont = 0
        z = 'static'
        p = 'static'
        for l in range(-5,5):
            for k in range(-5,5): ##verificamos si estan o no 
                px,py = puntos[i] ##en una area parecida para
                pxx = px + l      ##verificar si pertenecen al mismo 
                pyy = py + k      ##objeto
                for j in range(len(arra)):
                    x,y = arra[j]
                    if (pxx,pyy) == (x,y) and cont == 0: ## si es asi 
                        cont = 1                         ##buscamos el cambio de direccion
                        nx,ny = x,y
                        lug = j
                        if px > nx:
                            z = 'derecha'
                        if px < nx:
                            z = 'izquierda'
        if cont == 0:                 ##si no se encontro quiere decir que es nueva
            arra.append((px,py))      ##y la agregamos
            nuevo.append((px,py,z))
        else:                         ##si se encontro solo modificamos 
            arra[j] = ((nx,ny))
            nuevo.append((nx,ny,z))
    return nuevo                      ##enviamoslas cordenadas para dibujar  
    

def main():
    captura = cv.CreateCameraCapture(1) ##guardamos la imagen de la camara web usb
    global arra ##cargamos el arreglo de los objetos
    font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 3) #creamos el fondo para las letras
    proses  = 0
    sumaa = 0
    while True:
        img = cv.QueryFrame(captura)
        #cv.Resize(img,img,cv.CV_INTER_CUBIC)
        #tiempoi = time.time()
        #draw = ImageDraw.Draw(img)
        anch,alt = cv.GetSize(img) ##obtenemos las dimensiones
        k = cv.WaitKey(10);        ##esperemos para cualquier incombeniente
        #cv.SaveImage("test.jpg",img)
        cv.Smooth(img,img,cv.CV_GAUSSIAN,9,9) ##aplicamos filtro para reducir el ruido
        #cv.SaveImage("sruido.jpg",img)
        grey=    cv.CreateImage(cv.GetSize(img),8,1) ##creamos una imagen en blanco
        bn =  cv.CreateImage(cv.GetSize(img), 8, 1); ##creamos imagen en blanco
        cv.CvtColor(img,grey,cv.CV_BGR2GRAY)  ###pasamos la imagen a escala de grises y la guardamos en la imagen ne blanco
        #cv.SaveImage("gris.jpg",grey)
        cv.ConvertImage(img, bn, 0); ##convertimos la imagen a blancos
        threshold=40 ##umbral 1 para binarizacion
        colour=255   ## umbral 2 para binarizacion 
        cv.Threshold(grey,grey, threshold,colour,cv.CV_THRESH_BINARY) ##aplicamos binarizacion
        cv.Canny( grey, bn, 1, 1, 3) ##preparamos para obtener contornos, esto nos muestra la imagen con los contornos
        #cv.SaveImage("cont.jpg",bn)
        cv.SaveImage("grey.jpg",grey) ##guardamos la imagen
        cambio("grey.jpg")            ##invertimos la imagen y discretisamos
        imgg = cv.LoadImage('ngrey.jpg',cv.CV_LOAD_IMAGE_GRAYSCALE) ##cargamos nuevamente la imagen
        storage = cv.CreateMemStorage(0)  ##para guardar los puntos y no saturar la memoria
        contours = cv.FindContours(imgg,storage,cv.CV_RETR_TREE,cv.CV_CHAIN_APPROX_SIMPLE,(0,0)) ##obtener los puntos de los contornos
        puntos = [] ##para guardar los diferente centros de los objetos y verificarlas posteriormente
        while contours: ##leemos los contornos
            nx,ny =contours[0] ##para verificar donde se encuentra los centros de la figura u bojeto
            mx,my =contours[0] ##
            ancho,altura = cv.GetSize(img) ##obtenemos el tama de la imagen
            for i in range(len(contours)):  ##verificamos las esquinas
                xx,yy = contours[i]
                if xx > mx:
                    mx = xx
                if xx < nx:
                    nx = xx
                if yy > my:
                    my = yy
                if yy < ny:
                    ny = yy        
            a,b,c,d = random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255) ##para el color
            if len(contours) >= 50: ##si son mas de 50 puntos es tomada como figura
                cv.Rectangle(img,(nx,ny),(mx,my),cv.RGB(0,255,0),1,8,0) ##pintamos el rectangulo con las esquinas
                #are = abs(mx-nx)*abs(my-ny)
                puntos.append((abs(mx+nx)/2,abs(my+ny)/2)) ##agregamos los centros
                #are = abs(mx-nx)*abs(my-ny)
            contours = contours.h_next() #pasamos con los siguientes puntos unidos
        nuevo = de(puntos,anch,alt) ##verificamos los objetos y obtenemos los centros de los mismos
        
        for i in range(len(nuevo)): ## pintamos la direccin de los mismos
            x,y,z = nuevo[i]
            cv.PutText(img,""+z+"", (x,y),font, 255)        
        tiempof = time.time() ##verificar rendimiento
        cv.ShowImage('img',img)
        #cv.SaveImage("final.jpg",img)
        #tiempoa = tiempof - tiempoi
        #proses += 1
        #sumaa  =  sumaa + tiempoa
        #print float(sumaa)/float(proses)
        #f.write(""+str(proses)+" "+str(tiempoa)+"\n")
        ##verificar rendimientp
        if k == 'f': ##si se preciona f se sale
            break
main()
