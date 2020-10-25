from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
from tkinter import filedialog
import PIL
from PIL import ImageTk
from PIL import Image
import os
import requests
import numpy as np
import codecs, json
import scipy.linalg as la
import math
import scipy.sparse.linalg as sc
import webbrowser

PCcriteria = np.empty([5, 5])
first_run = True

#Alkalmazásablak létrehozása
root = Tk()

def ahp(PCM, PCcriteria, m, n):
    #Szempontokhoz tartozó súlyvektor kiszámítása
    #A legnagyobb sajátértékhez tartozó sajátvektor kiszámítása
    val, vec = sc.eigs(PCcriteria, k = 1, which = 'LM')
    #Értékek valós számmá alakítása
    eigcriteria = np.real(vec)
    #Értékek 1-re normalizálása
    w = eigcriteria / sum(eigcriteria)
    w = np.array(w).ravel()

    #Alternatívákhoz tartozó súlyvektorok kiszámítása
    S = []
    for i in range(n):
        val, vec = sc.eigs(PCM[i * m:i * m + m, 0:m], k = 1, which = 'LM')
        eigalter = np.real(vec)
        s = eigalter / sum(eigalter)
        s = np.array(s).ravel()
        S.append(s)
    S = np.transpose(S)

    #Végső súlyok kiszámítása
    v = S.dot(w.T)
    return v

def main(PCcriteria):

    #Eredmény ablak létrehozása
    resultWindow = Toplevel(root)
    resultWindow.title("Result")
    resultWindow.geometry("1000x600")
    resultWindow.iconbitmap("icons/result.ico")
    resultWindow.minsize(800, 600)
    title = Label(resultWindow, text="Az ön számára ajánlott készülékek", font=titleFont)
    title.place(relx=0.5, y=10, anchor=N)
    frameResult = ttk.Frame(resultWindow)
    frameResult.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    #Szükséges objektumok definiálása
    for j in range(3):
        exec(f'lbl{j} = Label(frameResult, width=22, bd=3, relief=RAISED, borderwidth=6, fg="white", bg="#DF1176", font=orderFont)')
        exec(f'lbl{j}.grid(row=0, column=j)')
        exec(f'global panel{j}')
        exec(f'panel{j} = Button(frameResult, bd=3, relief=RAISED, borderwidth=7, bg="#DF1176")')
        exec(f'panel{j}.grid(row=1, column=j)')
        exec(f'global name{j}')
        exec(f'name{j} = Label(frameResult, width=28, bd=3, relief=RAISED, borderwidth=4, bg="#DF1176", fg="white", font=attrFont)')
        exec(f'name{j}.grid(row = 2, column = {j})')
        exec(f'price{j} = Label(frameResult, width=28, bd=3, relief=RAISED, borderwidth=4, bg="#DF1176", fg="white", font=attrFont)')
        exec(f'price{j}.grid(row = 3, column = {j})')
        exec(f'camera{j} = Label(frameResult, width=28, bd=3, relief=RAISED, borderwidth=4, bg="#DF1176", fg="white", font=attrFont)')
        exec(f'camera{j}.grid(row = 4, column = {j})')
        exec(f'storage{j} = Label(frameResult, width=28, bd=3, relief=RAISED, borderwidth=4, bg="#DF1176", fg="white", font=attrFont)')
        exec(f'storage{j}.grid(row = 5, column = {j})')
        exec(f'battery{j} = Label(frameResult, width=28, bd=3, relief=RAISED, borderwidth=4, bg="#DF1176", fg="white", font=attrFont)')
        exec(f'battery{j}.grid(row = 6, column = {j})')
        exec(f'performance{j} = Label(frameResult, width=28, bd=3, relief=RAISED, borderwidth=4, bg="#DF1176", fg="white", font=attrFont)')
        exec(f'performance{j}.grid(row = 7, column = {j})')

    #AHP kalkulációhoz szükséges változók
    m = 41
    n = 5
    PCcriteria
    mobile_list = ["Huawei-P40-Lite", "Samsung-Galaxy-A71", "Apple-iPhone-11", "Apple-iPhone-SE", "Samsung-Galaxy-A21S", "Samsung-Galaxy-S10", "Samsung-Galaxy-A51", "Samsung-Galaxy-S20", "Xiaomi-Redmi-9", "Huawei-P30-Lite", "Xiaomi-Redmi-Note-9-Pro", "Xiaomi-Redmi-Note-8T", "Samsung-Galaxy-Note-20-Ultra", "Apple-iPhone-11-Pro-Max", "Apple-iPhone-11-Pro", "Samsung-Galaxy-S20-Ultra", "Samsung-Galaxy-A41", "Apple-iPhone-XR", "Samsung-Galaxy-A20e", "Huawei-P30-Pro", "Huawei-P40-Pro", "Xiaomi-Redmi-Note-9", "Xiaomi-Mi-Note-10", "Samsung-Galaxy-S20-Plus", "Xiaomi-Mi-Note-10-Lite", "Honor-20-Lite", "Samsung-Galaxy-Note-20", "Huawei-P30", "Samsung-Galaxy-Note-10-Lite", "Honor-20", "Honor-20-Pro", "Honor-8A", "OnePlus-7T", "LG-K40s", "TCL-10-PRO", "Sony-Xperia-5", "Huawei-Y6P", "TCL-10L", "Samsung-Galaxy-Z-Flip", "Alcatel-3X", "LG-V50-Thinq"]
    
    #Mátrix json-ből adatok kinyerése és átadása
    obj_text = codecs.open('pwc.json', 'r', encoding='utf-8').read()
    matrices = json.loads(obj_text)

    pwc_j = matrices['matrices'][0]
    pwc = np.array(pwc_j)
    pwc2_j = matrices['matrices'][1]
    pwc2 = np.array(pwc2_j)
    pwc3_j = matrices['matrices'][2]
    pwc3 = np.array(pwc3_j)
    pwc4_j = matrices['matrices'][3]
    pwc4 = np.array(pwc4_j)
    pwc5_j = matrices['matrices'][4]
    pwc5 = np.array(pwc5_j)

    all_pwc = np.vstack((pwc, pwc2, pwc3, pwc4, pwc5))

    scores = ahp(all_pwc, PCcriteria, m, n)
    listed = scores.tolist()
    n = 3
    res = sorted(scores)
    winners = res[-n:]

    #Kiszámolt győztesekhez tartozó információk lekérdezés és hozzáadása az objektumokhoz
    suggestions = [None] * 3
    j = 0
    with open('conf.json', 'r') as f:
        config = json.load(f)
    global tmp_link
    tmp_link = [None] * 3
    for i in winners:
        index = listed.index(i)
        suggestions[j] = mobile_list[index]
        exec(f'var_a{j} = StringVar()')
        exec(f'var_b{j} = StringVar()')
        exec(f'var_c{j} = StringVar()')
        exec(f'var_d{j} = StringVar()')
        exec(f'var_e{j} = StringVar()')
        exec(f'var_f{j} = StringVar()')
        order = j+1
        exec(f'lbl{j}.configure(text=order)')
        exec(f'name{j}.configure(textvariable=var_a{j})')
        exec(f'var_a{j}.set(suggestions[j].replace("-", " ", 10))')

        exec(f'price{j}.configure(textvariable=var_b{j})')
        exec(f"var_b{j}.set(str(list(config['devices'][index].items())[0][1]['price']) + ' Ft')")

        exec(f'camera{j}.configure(textvariable=var_c{j})')
        exec(f"var_c{j}.set(str(list(config['devices'][index].items())[0][1]['camera']) + ' MP')")

        exec(f'storage{j}.configure(textvariable=var_d{j})')
        exec(f"var_d{j}.set(str(list(config['devices'][index].items())[0][1]['storage']) + ' GB')")

        exec(f'battery{j}.configure(textvariable=var_e{j})')
        exec(f"var_e{j}.set(str(list(config['devices'][index].items())[0][1]['battery']) + ' mAh')")

        exec(f'performance{j}.configure(textvariable=var_f{j})')
        exec(f"var_f{j}.set(str(list(config['devices'][index].items())[0][1]['perf']) + ' pont')")

        tmp_img = "pictures/" + list(config['devices'][index].items())[0][1]['name'] + ".jpg"
        exec(f'img{j} = ImageTk.PhotoImage(Image.open(tmp_img))')
        exec(f'panel{j}.configure(image=img{j})')
        exec(f'panel{j}.image = img{j}')
        tmp_link[j] = ("https://www.gadgetsnow.com/mobile-phones/" + suggestions[j])
        j+=1
    for j in range(3):
        exec(f'panel{j}.configure(command=lambda: callback(tmp_link[{j}]), cursor="hand2")')
    first_run = False

def build():
    #Megadott értékek kinyerése a beviteli mezőkből, majd a main kód futtatása, mely kiszámolja az eredményeket
    v = [None] * 10
    j = 0
    for i in range(len(v)):
        exec(f'v[i] = float(E{i}.get())')
        j+=1
    k = 0
    l = 0
    for i in range(0,5):
        for j in range(0,5):
            if i == j:
                PCcriteria[i][j] = 1
            else:
                if j > i:
                    PCcriteria[i][j] = v[k]
                    k+=1
                elif j < i:
                    PCcriteria[i][j] = 1 / v[l]
                    l+=1
    main(PCcriteria)

def funcExit():
    #Kilépés az alkalmazásból
    mbox = messagebox.askquestion("Exit", "Are you sure you want to exit?")
    if mbox == "yes":
        root.destroy()

infoWindow = None
aboutWindow = None

def openInfoWindow():
    global infoWindow
    infoWindow = Toplevel(root)
    infoWindow.title("Info")
    infoWindow.geometry("600x300")
    infoWindow.iconbitmap("icons/info.ico")
    title = Message(infoWindow, text="Az alkalmazás az Analytic Hierarchy Process nevű többszempontú döntési modellen alapszik. A módszertan lényege, hogy a döntéshozó által megadott preferenciák alapján képes megmondani, hogy többféle alternatíva közül melyik lenne számára a legjobb. Önnek egész pontosan azt kell megadnia a beviteli mezőkben, hogy egyik szempont hányszor fontosabb az ön számára, mint a másik. Így például az első mezőben azt, hogy az ár mennyiszer fontosabb a kameránál. Ezeket a preferenciákat a program úgynevezett páros összehasonítás mátrix formájába rendezi, majd egy sor matematikai művelet elvégzése után képes megadni az egyes szempontok fontossági súlyát. A program az egyes szempontok szerinti alternatíva-összehasonlításokat előre betáplálva kapja meg, az ön által megadott összehasonlítások alapján pedig személyre szabott ajánlást képes adni az ön számára.")
    title.configure(width=500, justify="center", font=infoFont)
    title.place(relx=0.5, rely=0.5, anchor=CENTER)

def checkInfoWindow():
    if infoWindow == None or not infoWindow.winfo_exists():
        openInfoWindow()
    else:
        infoWindow.focus_force()

def openAboutWindow():
    global aboutWindow
    aboutWindow = Toplevel(root)
    aboutWindow.title("About")
    aboutWindow.geometry("600x300")
    aboutWindow.iconbitmap("icons/info.ico")
    title = Message(aboutWindow, text="Ez az alkalmazás egy alapszakos szakdolgozat keretében jött létre. Célja a többszempontú döntési modellek gyakorlati alkalmazási lehetőségeinek vizsgálata. A program a Magyar Telekom készülékkínálatát használja fel. Azt szeretném bizonyítani, hogy ez egy működöképes kiegészítés, alternatíva lehetne a vállalat ajánló rendszerének. Az alkalmazás ettől eltekintve is hasznos lehet olyanok számára, akik mobiltelefon vásárlás előtt állnak, de még nem tudják eldönteni, hogy milyen készüléket válasszanak. A preferenciák megadásával személyre szabott ajánlatot kapnak az érdeklődők.")
    title.configure(width=500, justify="center", font=infoFont)
    title.place(relx=0.5, rely=0.5, anchor=CENTER)

def checkAboutWindow():
    if aboutWindow == None or not aboutWindow.winfo_exists():
        openAboutWindow()
    else:
        aboutWindow.focus_force()

def callback(url):
    #Weboldal megnyitásához használatos
    webbrowser.open_new(url)

def newCalc():
    #Beviteli mezők kiürítése
    for j in range(10):
        exec(f'E{j}.delete(0, "end")')

def showTooltip(content, parent, relx, rely, width, bg, fg):
    global ttp_lbl
    ttp_lbl = Message(master=parent, text=content)
    ttp_lbl.place(relx=relx, rely=rely)
    ttp_lbl.configure(bg=bg, fg=fg, font=orderFont, justify="center", width=width, relief=RAISED, bd=3)

def hideTooltip():
    ttp_lbl.destroy()

def isFloat(input):
    #Megállapítja, hogy egy változó Float típusú-e
    try:
        float(input)
        return True
    except ValueError:
        return False

def canRun():
    try:
        build()
    except ValueError:
        showTooltip("Az összes mezőt kötelező kitölteni! Csak egész számok és ponttal elválasztott tizedestörtek elfogadottak!", root, 0.75, 0.4, 150, "red", "white")
        root.after(1500, hideTooltip)

def validate(input):
    #Beviteli mezők validáciújához használatos függvény. Csak szám értékeket fogad el.
    if input.isnumeric():
        return True
    elif input == "":
        return True
    elif isFloat(input):
        return True
    else:
        showTooltip("Csak egész számok és ponttal elválasztott tizedestörtek elfogadottak!", root, 0.75, 0.4, 150, "red", "white")
        root.after(2500, hideTooltip)
        return False

#Betűtítpusok definiálása
entryFont = Font(family="Arial", size=12, weight="bold")
labelFont = Font(family="Arial", size=10, weight="bold")
attrFont = Font(family="Arial", size=10, weight="bold")
btnFont = Font(family="Arial", size=10, weight="bold")
titleFont= Font(family="Arial", size=16, weight="bold")
orderFont = Font(family="Arial", size=12, weight="bold")
infoFont = Font(family="Times New Roman", size=12)
mainFont = Font(family="Courier", size=20, weight="bold")

#Menüszalag létrehozása
menubar = Menu(root)
root.config(menu=menubar)
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=file)
file.add_command(label="New", command=newCalc)
file.add_command(label="About", command=checkAboutWindow)
file.add_separator()
file.add_command(label="Exit", command=funcExit)
edit = Menu(menubar)
about = Menu(menubar)

#Frame csoportok létrehozása
frame1 = Frame(root, height=450) 
frame1.place(relx = 0.5, rely=0.57, anchor=CENTER)
frame1.configure(background	= "#DF1176", bd=3, relief=RAISED)

frame2 = ttk.Frame(root)
frame2.place(relx = 0.5, rely = 0.7, anchor=CENTER)

#Fő ablakhoz tartozó elemek meghatározása
#Cím
main_title = Message(root, text="Decision Support Application")
main_title.configure(width=300, font=mainFont, justify="center")#, bg="#DF1176", fg="white")
main_title.place(relx=0.5, y=20, anchor=N)

#Szeparáló vonal
separator = ttk.Separator(root, orient='horizontal')
separator.place(x=0, y=100, relwidth=1)

#Üdvözlő szöveg
title_lbl = Message(root, text="Kérem, hasonlítsa össze egymással az alábbi szempontokat! Csak egész számokat, illetve tizedesponttal elválasztott tizedestörteket használjon! Az első sor például így értelmezendő: a készülék ára hányszor fontosabb ön számára, mint a kamera minősége?")
title_lbl.configure(width=400, font=labelFont, justify="center")#, bg="#DF1176", fg="white")
title_lbl.place(relx=0.5, y=130, anchor=N)

#Gombok definiálása, konfigurálása
btn_calc = Button(frame1, text ="Indítás", command = canRun, font=btnFont, fg="#DF1176", bg="white", bd=3, cursor="hand2")
btn_calc.grid(row=12, column=3, pady=(10,5))

btn_info = Button(root, text ="Szeretnék többet tudni", command=checkInfoWindow, fg="white", font=btnFont, bg="#DF1176", bd=3, cursor="hand2")
btn_info.place(relx=0.95, y=10, anchor=NE, width=200)

btn_new = Button(root, text ="Új kalkuláció", command=newCalc, font=btnFont, fg="white", bg="#DF1176", bd=3, cursor="hand2")
btn_new.place(relx=0.95, y=50, anchor=NE, width=200)

#Beviteli mezőkhöz szövegek és ikonok
compare_list = ["Ár - Kamera", "Ár - Tárhely", "Ár - Akkumulátor", "Ár - Teljesítmény", "Kamera - Tárhely", "Kamera - Akkumulátor", "Kamera - Teljesítmény", "Tárhely - Akkumulátor", "Tárhely - Teljesítmény", "Akkumulátor - Teljesítmény"]
price_icon = PhotoImage(file = "icons/price_icon.png").subsample(25,25)
camera_icon = PhotoImage(file = "icons/camera_icon.png").subsample(25,25)
storage_icon = PhotoImage(file = "icons/storage_icon.png").subsample(25,25)
battery_icon = PhotoImage(file = "icons/battery_icon.png").subsample(25,25)
performance_icon = PhotoImage(file = "icons/performance_icon.png").subsample(25,25)

#Ikon információk
price_info = "A készülék ára"
camera_info = "A készülék kamerájának minősége"
storage_info = "A készülék belső tárhelyének mérete"
battery_info = "A készülék üzemideje"
performance_info = "A készülék gyorsasága, grafikus képességei"

#Beviteli mezők létrehozása, konfigurálása
reg = root.register(validate)
for k in range(10):
    exec(f'var{k} = StringVar()')
    exec(f'L{k} = Label(frame1, text = compare_list[k])')
    exec(f'L{k}.configure(font=labelFont, bg="#c3dbd0")')
    exec(f'L{k}.grid(row = k, column=1)')
    exec(f'tmp = L{k}["text"]')

    if tmp.startswith('Ár'):
        exec(f'img_lbl_a{k} = Label(frame1, image = price_icon)')
        exec(f'img_lbl_a{k}.bind("<Enter>", lambda e : showTooltip(price_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    elif tmp.startswith('Kamera'):
        exec(f'img_lbl_a{k} = Label(frame1, image = camera_icon)')
        exec(f'img_lbl_a{k}.bind("<Enter>", lambda e : showTooltip(camera_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    elif tmp.startswith('Tárhely'):
        exec(f'img_lbl_a{k} = Label(frame1, image = storage_icon)')
        exec(f'img_lbl_a{k}.bind("<Enter>", lambda e : showTooltip(storage_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    elif tmp.startswith('Akkumulátor'):
        exec(f'img_lbl_a{k} = Label(frame1, image = battery_icon)')
        exec(f'img_lbl_a{k}.bind("<Enter>", lambda e : showTooltip(battery_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    else:
        exec(f'img_lbl_a{k} = Label(frame1, image = performance_icon)')
        exec(f'img_lbl_a{k}.bind("<Enter>", lambda e : showTooltip(performance_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    exec(f'img_lbl_a{k}.grid(row = k, column = 0, padx=(20,0))')
    exec(f'img_lbl_a{k}.configure(bg="#c3dbd0")')
    exec(f'img_lbl_a{k}.bind("<Leave>", lambda e : hideTooltip())')

    if tmp.endswith('Ár'):
        exec(f'img_lbl_b{k} = Label(frame1, image = price_icon)')
        exec(f'img_lbl_b{k}.bind("<Enter>", lambda e : showTooltip(price_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    elif tmp.endswith('Kamera'):
        exec(f'img_lbl_b{k} = Label(frame1, image = camera_icon)')
        exec(f'img_lbl_b{k}.bind("<Enter>", lambda e : showTooltip(camera_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    elif tmp.endswith('Tárhely'):
        exec(f'img_lbl_b{k} = Label(frame1, image = storage_icon)')
        exec(f'img_lbl_b{k}.bind("<Enter>", lambda e : showTooltip(storage_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    elif tmp.endswith('Akkumulátor'):
        exec(f'img_lbl_b{k} = Label(frame1, image = battery_icon)')
        exec(f'img_lbl_b{k}.bind("<Enter>", lambda e : showTooltip(battery_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    else:
        exec(f'img_lbl_b{k} = Label(frame1, image = performance_icon)')
        exec(f'img_lbl_b{k}.bind("<Enter>", lambda e : showTooltip(performance_info, root, 0.38, 0.85, 110, "white", "#DF1176"))')
    exec(f'img_lbl_b{k}.grid(row = k, column = 2)')
    exec(f'img_lbl_b{k}.configure(bg="#c3dbd0")')
    exec(f'img_lbl_b{k}.bind("<Leave>", lambda e : hideTooltip())')
    
    exec(f'E{k} = Entry(frame1, bd=5, width=10, textvariable=var{k}, justify="center")')
    exec(f'E{k}.configure(font=entryFont)')
    exec(f'E{k}.grid(row = k, column=3, padx=20)')
    exec(f'E{k}.config(validate="key", validatecommand=(reg, "%P"))')
E0.grid(pady=(20,0))
L0.grid(pady=(20,0))
img_lbl_a0.grid(pady=(20,0))
img_lbl_b0.grid(pady=(20,0))

for child in frame1.winfo_children():
    child.configure(fg="white", background="#DF1176")

#Fő ablakon végzett utólagos konfigurációk
root.geometry("900x750")
root.minsize(700, 600)
root.title("AHP Application")
root.iconbitmap("icons/window_icon.ico")
root.mainloop() 