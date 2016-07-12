import os
os.chdir("C:\\Program Files (x86)\\swipl\\bin")
from pyswip import *
from Tkinter import *
import Image
from PIL import ImageTk
master = Tk()
master.minsize(500, 500)
prolog = Prolog()
prolog.consult("C:/sistema_solar.pl")

w = Label(master, text="3er Parcial")
w.pack()

#cuando se selecciona una luna
def select(event):
    lunasFrames = Toplevel()
    contador = 0
    lunaList = Listbox(lunasFrames)
    e = event.widget
    index = int(e.curselection()[0])
    valor = e.get(index)
    print(valor)
    for luna in prolog.query("satelites(Planeta,Luna)"):
        if valor == luna["Planeta"]:
            if luna["Luna"] == []:
                lunaList.insert(contador,"No tiene luna(s)")
            else:
                for moon in luna["Luna"]:
                    lunaList.insert(contador,moon)
                    contador += 1
    lunaList.pack()

    print 'You selected item %d: "%s"' % (index, valor)

def lunasPlanetas():
    child1 = Toplevel()
    Lb1 = Listbox(child1, selectmode=SINGLE)

    i=1
    for luna in prolog.query("satelites(Planeta,Luna)"):
        Lb1.insert(i, luna["Planeta"])
        i += 1

    Lb1.bind('<<ListboxSelect>>',select)

    Lb1.pack()
def selectorPlanetas():
    child1 = Toplevel()
    Lb1 = Listbox(child1, selectmode=SINGLE)

    i=1
    for luna in prolog.query("satelites(Planeta,Luna)"):
        Lb1.insert(i, luna["Planeta"])
        i += 1

    Lb1.bind('<<ListboxSelect>>',select2)

    Lb1.pack()

def llamada(masas,diccionario):
    print masas.split()
    masaFrame2 = Toplevel()
    listamasa = Listbox(masaFrame2)
    k = 0  # contador para listamasa
    for planeta in masas.split():
        if planeta in diccionario:
            listamasa.insert(k, planeta + ": " + str(diccionario[planeta]))
            k += 1
        else:
            listamasa.insert(k, planeta + " no es valido")
            k += 1
    listamasa.pack()

def dibujar(listaPlaneta):
    dibujos = Toplevel()
    dibujos.minsize(500, 500)
    listPlan = listaPlaneta.split()
    d = Canvas(dibujos, width=1000, height=700, scrollregion=(0, 0, 2500, 0))
    hbar=Scrollbar(dibujos, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command = d.xview)
    k = 50

    def _create_circle(dibujos, x, y, r, **kwargs):
        return d.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    Canvas.create_circle = _create_circle
    posab = 0
    for var in prolog.query("planeta(Planeta,Clasificacion,Masa,Posicion)"):
        for plan in listPlan:
            if var["Planeta"] == plan:
                if var["Planeta"] == "jupiter":
                    var["Masa"] = 21
                elif var["Planeta"] == "saturno":
                    var["Masa"] = 19

                posab = posab + var["Posicion"]*k
                y =180
                d.create_circle(posab, 225,var["Masa"]*10, fill="blue", outline="#DDD", width=3)
                posab = posab + var["Masa"]*7
                #oval = d.create_oval(var["Posicion"]*k,var["Posicion"]+10,var["Masa"]*10,var["Masa"]+10,fill = "blue")
                #labels = Label(dibujos, text=var["Planeta"])
                k+100
    d.config(width=1000,height=700)
    d.config(xscrollcommand=hbar.set)
    d.pack(side=LEFT,expand=True,fill=BOTH)
    #d.pack()
    #labels.pack(side = TOP)

def masaPlanetas():
    masaFrame = Toplevel()
    masaFrame.minsize(400,400)
    lista = Listbox(masaFrame)
    diccionario = {}

    i = 1
    for luna in prolog.query("planeta(Planeta,Clasificacion,Masa,Posicion)"):
        lista.insert(i,str(luna["Posicion"])+". "+ luna["Planeta"])
        diccionario[luna["Planeta"]] = [luna["Masa"]]
        i += 1
    lista.pack()

    labels = Label(masaFrame,text="Numero(s) de Planeta(s):")
    labels.pack()
    labels.place(relx=.05,rely=.8)
    listaPlaneta = Entry(masaFrame,bd=15)
    listaPlaneta.pack(side=BOTTOM)
    listaPlaneta.place(relx=.5, rely=.82)

    botonMasa = Button(masaFrame, text="Masa", command = lambda: llamada(listaPlaneta.get(),diccionario))
    botonMasa.pack()
    botonMasa.place(relx=.06, rely=.87)
    botonTamano = Button(masaFrame, text="Tamano",command = lambda: dibujar(listaPlaneta.get()))
    botonTamano.pack()
    botonTamano.place(relx=.2, rely=.87)

#ventana de seleccion de planta para visualizar su rotacion y traslacion
def select2(event):

    #creando la ventana
    Movimientos = Toplevel()
    Movimientos.minsize(500, 500)

    #creando el canvas
    d = Canvas(Movimientos, width=1000, height=700, scrollregion=(0, 0, 2500, 0))

    #obteniendo el planeta seleccionado en la ventana anterior
    e = event.widget
    index = int(e.curselection()[0])
    valor = e.get(index)

    #definiendo scrollbars
    hbar=Scrollbar(Movimientos, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command = d.xview)
    vbar=Scrollbar(Movimientos,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=d.yview)

    k = 50

    def _create_circle(dibujos, x, y, r, **kwargs):
        return d.create_oval(x - r, y - r, x + r, y + r, **kwargs)
    Canvas.create_circle = _create_circle

    #posicion y radio del planeta
    sunx =500
    suny = 350
    sunr = 150

    #sol
    d.create_circle(sunx,suny,sunr, fill="yellow",outline="#DDD", width=3)

    for var in prolog.query("planeta(Planeta,Clasificacion,Masa,Posicion)"):
        if var["Planeta"] == valor:
            if var["Planeta"] == "jupiter":
                var["Masa"] = 13
                photo = Image.open("C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\jupiter.png")

            elif var["Planeta"] == "saturno":
                var["Masa"] = 12
                photo = Image.open("C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\saturno.png")

            elif var["Planeta"] == "neptuno":
                var["Masa"] = 9
                photo = Image.open("C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\neptuno.png")

            elif var["Planeta"] == "urano" :
                var["Masa"] = 8.5
                photo = Image.open("C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\urano.png")

            elif var["Planeta"] == "tierra" :
                var["Masa"] = 4
                photo = Image.open("C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\earth.png")

            elif var["Planeta"] == "venus" :
                var["Masa"] = 3
                photo = Image.open("C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\venus.png")

            elif var["Planeta"] == "marte" :
                var["Masa"] = 2
                photo = Image.open("C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\marte.png")

            elif var["Planeta"] == "mercurio":
                var["Masa"] = 1
                photo = Image.open("C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\mercurio.png")

            #posicion y radio del planeta
            planx = 2*sunx
            plany = suny
            planr = var["Masa"]*10
            #creacion del planetapil
            #img = PhotoImage(file="C:\\Users\\Jesus\\Desktop\\3erParcial_Logica-master\\earth.gif")
            #d.create_circle(planx, plany,planr, fill="blue", outline="#DDD", width=3)
            k+100

    #configuracion del canvas para incluir el scrollbar
    d.config(width=1000, height=700)
    d.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    d.pack(side=LEFT, expand=True, fill=BOTH)
    image = ImageTk.PhotoImage(photo)
    imagesprite = d.create_image(planx,plany,image=image)
    d.create_image(planx,plany,image = image)


b1 = Button(master,text="Lunas de Planetas",command = lunasPlanetas)
b2 = Button(master,text="Masa de Planetas",command = masaPlanetas)
b3 = Button(master, text="Tiempo respecto al Sol",command = selectorPlanetas)


b3.pack()
b2.pack()
b1.pack()

b3.place(relx=.35, rely=.53)
b2.place(relx=.39,rely=.46)
b1.place(relx=.39,rely=.39)




mainloop()