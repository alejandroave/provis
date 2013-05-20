import random
import cv
import time
from PIL import Image, ImageDraw,ImageFont

#cv.NamedWindow("Deteccion", 0)

arra = []
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

def cambio(imagen):
    imagen=cv.LoadImage(imagen,cv.CV_LOAD_IMAGE_COLOR)
    xx,yy = cv.GetSize(imagen)
        
    for i in range(xx):
        for y in range(yy):
            if cv.Get2D(imagen, y,i) == (0.0,0.0,0.0,0.0):
                cv.Set2D(imagen, y,i, (255.0,255.0,255.0,255.0))
            else:
                cv.Set2D(imagen, y,i, (0.0,0.0,0.0,0.0))
            if y < yy/3:
                cv.Set2D(imagen, y,i, (0.0,0.0,0.0,0.0))        
    cv.SaveImage("ngrey.jpg",imagen)



#def che():
    
def de(puntos,anch,alt):
    global arra
    nuevo = []
    for i in range(len(puntos)):
        cont = 0
        z = 'static'
        p = 'static'
        for l in range(-5,5):
            for k in range(-5,5):
                px,py = puntos[i]
                pxx = px + l
                pyy = py + k
                for j in range(len(arra)):
                    x,y = arra[j]
                    if (pxx,pyy) == (x,y) and cont == 0:
                        cont = 1
                        nx,ny = x,y
                        lug = j
                        if px > nx:
                            z = 'derecha'
                        if px < nx:
                            z = 'izquierda'
        if cont == 0:
            arra.append((px,py))
            nuevo.append((px,py,z))
        else:
            arra[j] = ((nx,ny))
            nuevo.append((nx,ny,z))
    return nuevo
    
def main():
    capture = cv.CreateCameraCapture(1)
    global arra
    font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 3) #Creates a font
    #fuente = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-C.ttf',20)
    while True:
        img = cv.QueryFrame(capture)
        #draw = ImageDraw.Draw(img)
        anch,alt = cv.GetSize(img)
        k = cv.WaitKey(10);
        cv.SaveImage("test.jpg",img)
        cv.Smooth(img,img,cv.CV_GAUSSIAN,9,9) ##menos ruido
        cv.SaveImage("sruido.jpg",img)
        grey=    cv.CreateImage(cv.GetSize(img),8,1)
        bn =  cv.CreateImage(cv.GetSize(img), 8, 1);
        cv.CvtColor(img,grey,cv.CV_BGR2GRAY)  ###escala de grises        
        cv.ConvertImage(img, bn, 0);
        threshold=40
        colour=255
        cv.Threshold(grey,grey, threshold,colour,cv.CV_THRESH_BINARY) ##binarizacion
        cv.Canny( grey, bn, 1, 1, 3)
        cv.SaveImage("cont.jpg",bn)
        cv.SaveImage("grey.jpg",grey)
        cambio("grey.jpg")
        imgg = cv.LoadImage('ngrey.jpg',cv.CV_LOAD_IMAGE_GRAYSCALE)
        storage = cv.CreateMemStorage(0)
        contours = cv.FindContours(imgg,storage,cv.CV_RETR_TREE,cv.CV_CHAIN_APPROX_SIMPLE,(0,0))
        puntos = []
        while contours:
            nx,ny =contours[0]
            mx,my =contours[0]
            ancho,altura = cv.GetSize(img)
            for i in range(len(contours)):
                xx,yy = contours[i]
                if xx > mx:
                    mx = xx
                if xx < nx:
                    nx = xx
                if yy > my:
                    my = yy
                if yy < ny:
                    ny = yy        
            a,b,c,d = random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255)
            if len(contours) >= 50:
                cv.Rectangle(img,(nx,ny),(mx,my),cv.RGB(0,255,0),1,8,0) 
                #are = abs(mx-nx)*abs(my-ny)
                puntos.append((abs(mx+nx)/2,abs(my+ny)/2))
                #are = abs(mx-nx)*abs(my-ny)
            contours = contours.h_next() # go to next contour
        nuevo = de(puntos,anch,alt)
        
        for i in range(len(nuevo)):
            x,y,z = nuevo[i]
            cv.PutText(img,""+z+"", (x,y),font, 255)        
        cv.ShowImage('img',img)
        if k == 'f':
            break
main()
