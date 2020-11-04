import threading
import sqlite3 as lite
import os, shutil, sys, time
import  platform as platte

from PIL import ImageTk, Image
import tkinter ,tkinter.scrolledtext
from tkinter import messagebox, PhotoImage, Canvas
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
# Klassen, Objekte ...  #--------------------------------------------------------------#    
class FredFillSQL(threading.Thread):
    def __init__(self,datenbankname,maxfiles):
        threading.Thread.__init__(self)
        self.datenbankname=datenbankname
        self.maxfiles=maxfiles
        self.swaiting=0.1
        self.NeuAnlage=False
    def run(self):
        global NeuAnlage
        FredId=threading.get_ident()
        print("Start Fred1:",FredId)
        datenbankname = self.datenbankname
        maxFiles=self.maxfiles
        print(NeuAnlage)
        #NeuAnlage=self.NeuAnlage
        con = None
        con = lite.connect(datenbankname)
        cur = con.cursor()

        if NeuAnlage==True:
            cur.execute("DROP TABLE IF EXISTS DATEINAMEN;")
            cur.execute("CREATE TABLE DATEINAMEN(Id INTEGER PRIMARY KEY, Dateiname TEXT, PfadAbsolut TEXT, BildWert TEXT,Bild BLOB NOT NULL );")#,Bild50 BLOB NOT NULL
            print("Neuanlage")
        bef="SELECT * FROM DATEINAMEN"
        b=Bilder()
        ian=0
        bilddateiname = ['jpg','jpeg','nef','JPG']
        for root, dirs, files in os.walk(DATVerzeichnis, topdown=True):
            try:
                root=root
                dirs=dirs
                for name in files:
                    pfad = os.path.abspath(name) # Absoluten Pfad der Datei ermitteln und in Datenbank schreiben
                    pfad=root
                    typ = name.split(".")[-1]
                    if typ in bilddateiname:
                        if ian< maxFiles:
                        # Bildgröße in Pixeln ermitteln, damit nachher die Ecken abgefragt werden können
                            s=root[-1:]
                            dx=ADD_path_file(root,name)
                            BildWert=b.BildWert(dx,500)
                            BildWert="1234"
                            Bild50= "1234"
                            ian+=1
                            if (ian%20)==0:
                                time.sleep(self.swaiting)
                                if self.swaiting < 0.5:
                                    self.swaiting+=0.1
                            #print(ian," Bilder eingelesen")
                            if NeuAnlage:
                                cur.execute("INSERT INTO DATEINAMEN (Dateiname, PfadAbsolut, BildWert,Bild) VALUES (?, ?, ?,  ?)",(name,pfad,BildWert,Bild50))
                                con.commit()
                            else:
                                bef="SELECT * FROM DATEINAMEN WHERE ID ="+str(ian)
                                check=cur.execute(bef).fetchone()
                                if check is None:
                                    #print(str(ian)+" neu")
                                    cur.execute("INSERT INTO DATEINAMEN (Dateiname, PfadAbsolut, BildWert,Bild) VALUES (?, ?, ?,  ?)",(name,pfad,BildWert,Bild50))
                                    con.commit()
                        else:
                            break
            except:
                x=1
                #SHOW_MESS("1 Datei konnte nicht eingelesen werden : "+ name,gstrLogBuchName)
                #SHOW_MESS("2 Datei im Pfad : "+ root ,gstrLogBuchName)
        con.close()
        print(ian," Bilder eingelesen")
        print("Stopp Fred1:",FredId)
        t2.start()   
        return ian
class FredWerteNachtragen(threading.Thread):
    def __init__(self,datenbankname):
        threading.Thread.__init__(self)
        self.datenbankname=datenbankname
        self.swaiting=0.1
    def run(self):
        FredId=threading.get_ident()
        print("Start Fred2:",FredId)
        ian=0
        b=Bilder()
        datenbankname = self.datenbankname
        con = None
        con = lite.connect(datenbankname)
        cur = con.cursor()
        cur.execute("SELECT * FROM DATEINAMEN")
        zeilen = cur.fetchall()
        for zeile in zeilen:
            s=zeile[2][-1:]
            dx=ADD_path_file(zeile[2],zeile[1])
            Id=zeile[0]
            if zeile[3]=="1234":
                BildWert=b.BildWert(dx,500)
                bef="UPDATE DATEINAMEN SET BildWert = '"+ BildWert +"' WHERE Id ="+str(Id)
                print("Fred2 {} Update: {}".format(FredId,Id))
                cur.execute(bef)
                con.commit()
            ian+=1
            if (ian%20)==0:
                #print(ian," Werte nachgetragen")
                time.sleep(self.swaiting)
                if self.swaiting < 0.5:
                   self.swaiting+=0.1
                #print("Run: ",FredId)
        con.close()
        print("Stopp Fred2:",FredId)
        return ian
class Dias(threading.Thread):
    def __init__(self,nr):
        threading.Thread.__init__(self)
        self.nr=nr
    def run(self):
        global Liste100
        global imageTHRE
        global xxl
        global twait
        print(self.nr)
        FredId=threading.get_ident()
        print("Start Fred3:",FredId)
        nr=self.nr
        while(True):
            bild,im=Liste100[nr]
            xxl.ChangeBild(fr3,500,bild,im)
            time.sleep(twait)
            nr+=1
            if nr==len(Liste100)-1:
                nr=0

class Glos:
    def __init__(self):
        self.first=0
        self.last=9
        self.pointer=4
    def setfirst(self,w):
        self.first=w
    def setlast(self,w):
        self.last=w
    def setpointer(self,w):
        self.pointer=w
        
    def Pointerplus1(self):
        self.pointer+=1
        if self.pointer > self.last:
            self.pointer=self.last
        i=self.pointer
        print("+",i)
        return i
    def Pointerminus1(self):
        self.pointer-=1
        if self.pointer<1:
            self.pointer=1
        i=self.pointer
        print("-",i)
        return i
    def getpointer(self):
        i=self.pointer
        print("get",i)
        return i    
class Bilder:
    BildAktuell=1
    s=""
    def __init__(self):
        self.BildAktuell=1
        self.s=""
    def BildWertRGB(self,rgb_im,x,y):       # Funktion zur Abfrage der Pixelfarben
        self.s=""
        mx1=int(x/2)
        my1=int(y/2)
        my2=int(y/4)
        r1, g1 , b1 =rgb_im.getpixel((0,0))
        r2, g2 , b2 =rgb_im.getpixel((x, 0))
        r3, g3 , b3 =rgb_im.getpixel((0, y))
        r4, g4 , b4 =rgb_im.getpixel((x, y))
        r5, g5 , b5 =rgb_im.getpixel((mx1,my2))
        r6, g6 , b6 =rgb_im.getpixel((mx1,my1))
        r7, g7 , b7 =rgb_im.getpixel((mx1,my1+my2))

        # im Tupel verpacken
        rgb= r1,g1,b1,r2,g2,b2,r3,g3,b3,r4,g4,b4,r5,g5,b5,r6,g6,b6,r7,g7,b7
        ian=len(rgb)
        for j in range(ian):
            self.s+=str(rgb[j])+" "
        #print(self.s)
        return self.s
    def BildWert(self,bild,baseheight):
        im = Image.open(bild)
        width, height = im.size
        width1=width
        wpercent = baseheight/height
        width = int(width)-1
        height = int(height)-1
        try:
            rgb_im = im.convert('RGB')
            Wert=self.BildWertRGB(rgb_im,width,height)
        except:
            self.s=""
            for i in range(22):
                self.s+=str(0)+" "
            Wert=self.s  
            print(Wert)
        return Wert
class BildaufCanvas:
    def __init__(self,frame,baseheight,bildname,im,pointer):
        self.frame=frame
        self.baseheight=baseheight
        self.bildname=bildname
        self.pointer=pointer
        self.canvas=1
    def ShowBild(self,frame,baseheight,bildname,im,pointer):
        #im=Image.open(bildname).convert("L")
        width, height = im.size
        wpercent = baseheight/height                                                # Bildgroesse anpassen
        newwidth = width * wpercent
        newwidth = int(newwidth)
        newsize = (newwidth, baseheight)                                            # Groesse als tuple
        imnew = im.resize(newsize)
        self.canvas = Canvas(frame,  height=baseheight,width=baseheight,bg="black")    # Leinwand = Canvas definieren, auf der das Bild im Frame erscheint
        self.canvas.pack(padx=5,side="left")

        self.canvas.bind("<Enter>",lambda event: onenter(pointer))
        self.canvas.bind("<Leave>",lambda event: onleave(bildname))
        self.canvas.bind("<Double-Button-1>",lambda event: ondouble(pointer))

        self.canvas.image=ImageTk.PhotoImage(imnew)                                 # Bild mit neuen Maßen wird mit der Leinwand = Canvas verbunden
        bild=self.canvas.create_image( 0,0, image=self.canvas.image, anchor='nw')   # Bild wird angezeigt
    def ChangeBild(self,frame,baseheight,bildname,im):
        #im=Image.open(bildname)
        width, height = im.size
        wpercent = baseheight/height                                                # Bildgroesse anpassen
        newwidth = width * wpercent
        newwidth = int(newwidth)
        newsize = (newwidth, baseheight)                                            # Groesse als tuple
        imnew = im.resize(newsize)
        self.canvas.image=ImageTk.PhotoImage(imnew)                                 # Bild mit neuen Maßen wird mit der Leinwand = Canvas verbunden
        bild=self.canvas.create_image( 0,0, image=self.canvas.image, anchor='nw')   # Bild wird angezeigt
    def deleteBild(self):
        self.canvas.pack_forget()
#SQLITE3 function       #--------------------------------------------------------------#    
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
def DBNew(gstrDatenBankName):
    SHOW_MESS("Datei angelegt und  geöffnet ! nicht wirklich",gstrLogBuchName)
def DBAuswahl():
    filename = askopenfilename(initialdir=SQLVerzeichnis, 
                                filetypes = (("Datenbank", "*.db"),("All Files","*.*")),
                                title = "Datenbank auswählen.")
    if  filename: 
        try: 
            ergebnis=filename
            DBOpen(ergebnis)
            return ergebnis
        except: 
            SHOW_MESS("Fehler bei der Auswahl der Datenbank",gstrLogBuchName)
def DBOpen(datenbankname):
    datenbankname = datenbankname
    con = None
    con = lite.connect(datenbankname)
    cur = con.cursor()
    con.commit()
    con.close()    
    SHOW_MESS("Dateibank geöffnet",gstrLogBuchName)
    #SHOW_MESS("DatenBank geöffnet ("+datenbankname+")",gstrLogBuchName)
def DBNumber_of_Records(datenbankname):
    ian=0
    try:
        con = None
        con = lite.connect(datenbankname)
        cur = con.cursor()
        bef="SELECT * FROM DATEINAMEN ORDER BY Id DESC LIMIT 1"
        ian = cur.execute(bef).fetchone()
        ret=ian[0]
    except:
        ret=0
        SHOW_MESS("Dateibank geöffnet, aber leer",gstrLogBuchName)
    cur.close()    
    return ret    
def DBStrukturAnlegen(datenbankname):
    ian=0
    try:
        con = None
        con = lite.connect(datenbankname)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS DATEINAMEN;")
        cur.execute("CREATE TABLE DATEINAMEN(Id INTEGER PRIMARY KEY, Dateiname TEXT, PfadAbsolut TEXT, BildWert TEXT,Bild BLOB NOT NULL );")#,Bild50 BLOB NOT NULL
        print("Neuanlage")
        ret=ian
    except:
        ret=0
        SHOW_MESS("Dateibank geöffnet, aber leer",gstrLogBuchName)
    cur.close()    
    return ret        
def DBFuellen(datenbankname,DATVerzeichnis,maxFiles):
    datenbankname = datenbankname
    NeuAnlage=True
    t1.start()    
    time.sleep(10)
    GetBilder(gstrDatenBankName,1,50)    
def AbortFile(gstrLogBuchName):
    # nicht speichern insertBefehle löschen
    SHOW_ERR("Ende ohne speichern in 3 Sekunden",gstrLogBuchName)
    LogSave("000001",12,"Programm mit Abbruch beendet",gstrLogBuchName)
    HR.after(3*1000, HR.quit)
def SaveAndExit(gstrLogBuchName):
    # Daten speichern und Programm beenden
    try:
        LogSave("000001",12,"Programm mit Save beendet",gstrLogBuchName)
        SHOW_MESS("Daten gespeichert! In 3 Sekunden EXIT!",gstrLogBuchName)
        HR.after(3*1000, HR.quit)
    except:
        SHOW_ERR("Keine Daten eingelesen!",gstrLogBuchName)
# Anwendumgen           #--------------------------------------------------------------#
def showDaten():
    print(ext.get())
def RunDubletten(datenbankname,AnzeigeListe):
    ian=len(AnzeigeListe)
    for i in range(ian):
        AnzeigeListe.pop()
    print(AnzeigeListe)
    #datenbankname = datenbankname
    con = None
    con = lite.connect(datenbankname)
    cur = con.cursor()
    bef="SELECT * FROM DATEINAMEN"
    cur.execute(bef)
    zeilen = cur.fetchall()
    ian=len(zeilen)
    for Bild1 in range(ian):
        b1=zeilen[Bild1][3]
        for Bild2 in range(Bild1+1,ian):
            b2=zeilen[Bild2][3]
            if b1==b2:
                t=Bild1,Bild2
                AnzeigeListe.append(Bild1-1)
                AnzeigeListe.append(Bild2-1)
                print(AnzeigeListe)
    con.close()
    ian=len(AnzeigeListe)
    for i in range(int((10-ian)/2)):
        AnzeigeListe[:0]=[-1]
        print(AnzeigeListe)
    ian=10-len(AnzeigeListe)        
    for i in range(ian):
        AnzeigeListe.append(-1)
        print(AnzeigeListe)
    #ChangeBilder(AnzeigeListe)
    print(AnzeigeListe)
    ChangeBilder(AnzeigeListe)
    return AnzeigeListe
def RunJahr():
    print("Berechne Jahr")
def DiaShow(nr):
    # Alle Dateien anzeigen
    Regler.pack(expand=1,fill="x",side="left")
    if t3.is_alive():
        print("run")
    else:
        print("not run")
        t3.start()

#  Logbuch              #--------------------------------------------------------------#
def SHOW_MESS(strM,gstrLogBuchName):
    LogSave("000000","00", strM,gstrLogBuchName)
    FrameMessageZeile["text"]=strM
    FrameMessageZeile["bg"]="#FFFFFF"
def SHOW_ERR(strM,gstrLogBuchName):
    LogSave("999999",99,strM,gstrLogBuchName)
    FrameMessageZeile["text"]=strM
    FrameMessageZeile["bg"]="#FFF200"
def OpenLogBuch(gstrLogBuchName):
    try:
        gstrLogBuch= open(gstrLogBuchName,"a")
        gstrLogBuch.close()
        #SHOW_MESS("Logbuch geöffnet",gstrLogBuchName)
    except:
        print("Dateizugriff Logbuch nicht möglich")
        sys.exit(0)
def ShowLogBuch(gstrLogBuchName):
    def Ende(frLog,lbLog,buttonLog):
        lbLog.pack_forget()
        buttonLog.pack_forget()
        frLog.pack_forget()
    try:
        frLog=tkinter.Frame(HR)
        frLog.pack(expand=1)
        lbLog=tkinter.scrolledtext.ScrolledText(frLog,bg="#FFFFFF",width=100,height=10,wrap=tkinter.WORD)
        lbLog.pack(expand=1,fill="x",pady=0)    
        buttonLog=tkinter.Button(frLog,text="Anzeige Logbuch schliessen",width=30,height=1,bg="#FFFF00",command=lambda:Ende(frLog,lbLog,buttonLog))
        buttonLog.pack(side="right")

        gstrLogBuch= open(gstrLogBuchName,"r")
        strlog=gstrLogBuch.readline()
        while strlog:
            lbLog.insert("end",strlog)
            strlog=gstrLogBuch.readline()
        gstrLogBuch.close()
    except:
        print("Dateizugriff Logbuch nicht möglich")
        sys.exit(0)
def DeleteLogBuch(gstrLogBuchName):
    try:
        gstrLogBuch= open(gstrLogBuchName,"w")
        gstrLogBuch.close()
        ShowLogBuch(gstrLogBuchName)
    except:
        print("Dateizugriff Logbuch nicht möglich")
        sys.exit(0)
def LogSave(strCode,intID,strText,gstrLogBuchName):
    gstrLogBuch=open(gstrLogBuchName,"a")
    lt=time.localtime()
    strT=time.strftime("%d.%m.%Y %H:%M:%S",lt)+";"
    strC=("000000"+strCode)[-6:]+";"
    stri=("000000"+str(intID))[-6:]+";"
    strLogSatz = strT+strC+stri+strText+"\n"
    gstrLogBuch.write(strLogSatz)
    gstrLogBuch.close()
def on_closing():
    global globDatenVorhanden
    if globDatenVorhanden: 
        if messagebox.askokcancel("Quit", "Ohne Speichern das Programm verlassen?"):
            AbortFile(gstrLogBuchName)
    else:
        AbortFile(gstrLogBuchName)     
#Bilder                 #--------------------------------------------------------------#
def ImagePath(Dir):
    ImageDir=filedialog.askdirectory( initialdir=Dir)
    return ImageDir
def ADD_path_file(p,f):
    Version=platte.platform()
    s=p[-1:]
    ian=Version.count("Window")    
    if ian > 0:
        if s=="\\":
            name=p+f
        else:    
            name=p+"\\"+f            
    else:
        name=p+"/"+f
    return name    
def GetBilder(datenbankname,first,anzahl):
    global Liste100
    #Liste=[]
    datenbankname = datenbankname
    con = None
    con = lite.connect(datenbankname)
    cur = con.cursor()
    cur.execute("SELECT * FROM DATEINAMEN")
    zeilen = cur.fetchall()  #fetchmany ?
    bilddateiname = ['jpg','jpeg','nef','JPG']
    ian=0
    for zeile in zeilen:
        ian+=1
        if ian<anzahl:
            filename = zeile[1]
            typ = filename.split(".")[-1]
            if typ in bilddateiname:
                bildname=ADD_path_file(zeile[2],zeile[1])
                im=Image.open(bildname)  
                tu=bildname,im
                if ian < 10:
                    Liste100[ian-1]=tu
                else:
                    Liste100.append(tu)
    con.close()
    #print(Liste100)
    return 
# BildFunktionen        #--------------------------------------------------------------#
def AnzeigeListeRight(AnzeigeListe,anz):
    for i in range(anz): 
        ian=len(Liste100)
        i=AnzeigeListe[len(AnzeigeListe)-1]
        if i < ian+1:
            del AnzeigeListe[0]
            AnzeigeListe.append(i+1)
    return AnzeigeListe
def AnzeigeListeLeft(AnzeigeListe,anz):
    for i in range(anz):
        i=AnzeigeListe[0]
        if i>-4:
            del AnzeigeListe[len(AnzeigeListe)-1]
            AnzeigeListe[:0]=[i-1]
    #print("Left",i,AnzeigeListe)
def ShowBilder(AnzeigeListe):
    ian1=len(Liste100)
    mitte=4
    xxlPointer=AnzeigeListe[mitte]
    bild,im=Liste100[xxlPointer]
    xxl.ShowBild(fr3,500,bild,im,xxlPointer)
    ian2=len(AnzeigeListe)
    ian=min(ian1,ian2)
    for i in range(ian):
        s="b"+str(i)
        j=AnzeigeListe[i]
        bild,im=Liste100[j]
        xx[s].ShowBild(fr5,50,bild,im,i)
def ChangeBilder(AnzeigeListe):
    global imageTHRE
    ian1=len(AnzeigeListe)
    mitte=4
    xxlPointer=AnzeigeListe[mitte]
    bild,im=Liste100[xxlPointer]
    xxl.ChangeBild(fr3,500,bild,im)
    for i in range(ian):
        s="b"+str(i)
        j=AnzeigeListe[i]     
        if (j < 0) or (j>=len(Liste100)) :
            xx[s].ChangeBild(fr5,50,"",imageTHRE)
        else: 
            bild,im=Liste100[j]
            xx[s].ChangeBild(fr5,50,bild,im)
def Bild1Left(g,anz):
    #xxlPointer=AnzeigeListe[4]
    AnzeigeListeLeft(AnzeigeListe,anz)
    print(AnzeigeListe)
    ChangeBilder(AnzeigeListe)
def Bild1Right(g,anz):
    #xxlPointer=AnzeigeListe[4]
    AnzeigeListeRight(AnzeigeListe,anz)
    print(AnzeigeListe)
    ChangeBilder(AnzeigeListe)
    Liste100Nachladen()
def Liste100Nachladen():
    print("Starte Nachladen noch programmieren")
    time.sleep(0.1)
    #print("Ende Nachladen noch programmieren")
    return
# Bindings              #--------------------------------------------------------------#
def ondouble(x):
    diff=x-4
    if  diff > 0:
        Bild1Right(AnzeigeListe,diff)
    else:
        Bild1Left(AnzeigeListe,-diff)
    ChangeBilder(AnzeigeListe)
    print(x,diff)
def onenter(e):
    ian=len(Liste100)
    point=AnzeigeListe[e]
    if point>=ian:
        name="THRE"
    else:
        name,im=Liste100[point]
    NameBild.config(text=name)
def onleave(e):
    NameBild.config(text="")
def BildAnzahl(s):
    global twait
    print("Twait: ",s,twait)
    twait=int(s)
    
#--------------------------------------------------------------#   
# 
#  M A I N
#--------------------------------------------------------------#   

HR = tkinter.Tk()
HR.title("Übungsprogramm")

# auf schliessen des Hauptfensterns vorbereitet sein
HR.protocol("WM_DELETE_WINDOW", on_closing)
fr=tkinter.Frame(HR,height=20,width=600,bg="#FFFFFF",bd=10) 
fr.pack()

# Überschrift
fr00=tkinter.Frame(HR)

# Eine Zeile Abstand
fr01=tkinter.Message(HR,width=100,text="")
fr01.pack()

# 1.Zeile

fr1=tkinter.Frame(HR)
fr1.pack(expand=1)
#RadioButton
ext=tkinter.StringVar()
ext.set("jpg")
lb111=tkinter.Radiobutton(fr1,text="jpg",variable=ext,value="jpg",command=showDaten)
lb111.pack(expand=1,fill="x",pady=0,side="left")
lb112=tkinter.Radiobutton(fr1,text="mp4",variable=ext,value="mp4",command=showDaten)
lb112.pack(expand=1,fill="x",pady=0,side="left")
lb113=tkinter.Radiobutton(fr1,text="txt",variable=ext,value="txt",command=showDaten)
lb113.pack(expand=1,fill="x",pady=0,side="left")

# 2.Zeile

fr2=tkinter.Frame(HR)#, relief=RIDGE, borderwidth=12)
fr2.pack(fill="x",expand=1)

# 3.Zeile

fr3=tkinter.Frame(HR)
fr3.pack(fill="y",expand=1)

fr4=tkinter.Frame(HR)#, relief=RIDGE, borderwidth=12)
fr4.pack(fill="x",expand=1)
ButtLeft=tkinter.Button(fr4,text="<",width=10,height=1,command=lambda:Bild1Left(BildWerte,1))
ButtLeft.pack(side="left")
Regler=tkinter.Scale(fr4,from_=1.0,to=9.0,label="DiaShow Geschwindigkeit",resolution=1,orient="horizontal",showvalue=1,width=10,sliderlength=10,length=400,command=BildAnzahl)
Regler.pack_forget()
ButtRight=tkinter.Button(fr4,text=">",width=10,height=1,command=lambda:Bild1Right(BildWerte,1))
ButtRight.pack(side="right")

# 4.Zeile 
fr5=tkinter.Frame(HR)#, relief=RIDGE, borderwidth=12)
fr5.pack(fill="x",expand=1)

# Zeile für Ausgaben
# Mitteilungen unten
fr6=tkinter.Frame(HR)
fr6.pack()
NameBild=tkinter.Label(fr6,text="",relief="sunken")
NameBild.pack()

FrameMessageZeile=tkinter.Message(HR,width=600,text="2")
FrameMessageZeile.pack() #


#Menu
mBar=tkinter.Menu(HR)
mH1=tkinter.Menu(mBar)
mH2=tkinter.Menu(mBar)
mH3=tkinter.Menu(mBar)
mH4=tkinter.Menu(mBar)
mH5=tkinter.Menu(mBar)
mH6=tkinter.Menu(mBar)

mH1.add_command(label="Datenbank neu öffnen",command=DBAuswahl)
mH1.add_command(label="DatenBank neu füllen",command=lambda:DBFuellen(gstrDatenBankName,DATVerzeichnis,500))
mH1.add_command(label="DatenBank speichern",command=lambda:gstrLogBuchName(gstrLogBuchName))
mH1.add_command(label="DatenBank speichern als",command=lambda:DBNew(gstrDatenBankName))
mH1.add_command(label="Logbuch anzeigen",command=lambda:ShowLogBuch(gstrLogBuchName))
mH1.add_command(label="Logbuch löschen",command=lambda:DeleteLogBuch(gstrLogBuchName))

mH2.add_command(label="Daten anzeigen",command=lambda:(ShowBilder(AnzeigeListe)))
mH2.add_command(label="Diashow",command=lambda:DiaShow(0))

mH3.add_command(label="Doppelte Bilder",command=lambda:RunDubletten(gstrDatenBankName,AnzeigeListe))
mH3.add_command(label="Verbrauch letztes Jahr",command=RunJahr)

mH4.add_command(label="EXIT mit speichern",command=lambda:SaveAndExit(gstrLogBuchName))
mH4.add_command(label="EXIT ohne speichern",command=lambda:AbortFile(gstrLogBuchName))

mBar.add_cascade(label="Datei", menu=mH1)
mBar.add_cascade(label="Bearbeiten", menu=mH2)
mBar.add_cascade(label="Auswerten", menu=mH3)
mBar.add_cascade(label="EXIT", menu=mH4)
HR["menu"]=mBar

# Objekte und Vereinbarungen Start


NeuAnlage=False
wd = os.getcwd()
print("working directory is ", wd)

filePath = __file__
#print("This script file path is ", filePath)

absFilePath = os.path.abspath(__file__)
#print("This script absolute path is ", absFilePath)

path, filename = os.path.split(absFilePath)
print("Programm:{} / {}".format(path, filename))
SQLVerzeichnis=path 
#os.chdir("..") 

DATVerzeichnis=ImagePath(path)                          
Version=platte.platform()
print("OS-Version: "+Version)
print("SQLVerzeichnis: ",SQLVerzeichnis)
print("DATVerzeichnis: ",DATVerzeichnis)

gstrDatenBankName=ADD_path_file(SQLVerzeichnis,"Dateishow.db")
gstrLogBuchName=ADD_path_file(SQLVerzeichnis,"Dateishow.log")

THRE=ADD_path_file(path,"THRE.jpg")
THREim=Image.open(THRE)
tu=THRE,THREim

Liste100=[]
Liste100=[tu for i in range(0,9)]
BildWerte=Glos()
twait=1
xx={}
HR.iconbitmap() #SQLVerzeichnis+"icon.ico")
imageTHRE=Image.open(THRE)
OpenLogBuch(gstrLogBuchName)
LogSave("000001",12,"Programm gestartet",gstrLogBuchName)
DBOpen(gstrDatenBankName)
print("Datenbank: ",gstrDatenBankName)
ian=DBNumber_of_Records(gstrDatenBankName)
if ian==0:
    DBStrukturAnlegen(gstrDatenBankName)
t1=FredFillSQL(gstrDatenBankName,5000)
t2=FredWerteNachtragen(gstrDatenBankName)
t3=Dias(0)
# DB fuellen in Thread T1 
# Liste100 füllen in GetBilder
if ian<100:
   # Datenbank neu füllen 
    NeuAnlage=True
    t1.start()    
elif ian< 5000:
    # Datenbank weiter füllen
    NeuAnlage=False
    t1.start()
else:
    # Datenbank gefüllt BildWerte nachträglich in DB eintragen
    t2.start()
time.sleep(5)    
GetBilder(gstrDatenBankName,1,50)
AnzeigeListe=[i for i in range(0,9)]
xxl=BildaufCanvas(fr3,500,"",imageTHRE,1)
ra=("b0","b1","b2","b3","b4","b5","b6","b7","b8","b9")
for i in (ra):
    xx[i]=BildaufCanvas(fr5,50,"",imageTHRE,1)

ian=len(AnzeigeListe)
BildWerte.setpointer=(int(ian/2))
BildWerte.setfirst=(0)
BildWerte.setlast=(9)

xxlPointer=BildWerte.getpointer()
ShowBilder(AnzeigeListe)
HR.mainloop()
#done
