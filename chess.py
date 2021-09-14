def Find(poz,zoznam):
    #Zistí, či je na pozícii figurka
    for figurka in zoznam:
        if poz==[figurka.x,figurka.y]:
            return True
    return False
def Pozicia(poz,zoznam):
    #Nájde pozíciu figurky v liste podľa jej pozície
    for i in range(len(zoznam)):
        if poz==[zoznam[i].x,zoznam[i].y]:
            return i
def Nasachovnici(poz):
    #Zistí či je daná súradnica na šachovnici
    if 1<=poz[0]<=8 and 1<=poz[1]<=8:
        return True
    else:
        return False

class Hra:
    #Pre globálne premenné, môžme sem ešte doplniť premenné pre ťah, kto je na rade...
    def __init__(self):
        self.enpassantB=0
        self.enpassantC=0
        self.tah=1
        self.pravidlo_50=0
        self.na_tahu=True
        self.koniec=False
    def mat(self):
        koniec_tahov = True
        if hra.na_tahu == True:
            for i in range(len(Figurky)):
                if Figurky[i].farba == 'C':
                    zoznam = Figurky[i].mozny_pohyb()
                    for pozicia in zoznam:
                        if not Figurky[i].sach(pozicia):
                            koniec_tahov = False
                            break
        else:
            for i in range(len(Figurky)):
                if Figurky[i].farba == 'B':
                    zoznam = Figurky[i].mozny_pohyb()
                    for pozicia in zoznam:
                        if not Figurky[i].sach(pozicia):
                            koniec_tahov = False
                            break
        if koniec_tahov and Figurky[1].ohrozenie:
            print('Biely vyhral - sach mat')
            self.koniec=True
        elif koniec_tahov and Figurky[0].ohrozenie:
            print('Cierny vyhral - sach mat')
            self.koniec=True
        elif koniec_tahov:
            print('Pat')
            self.koniec=True
class Figura:
    def  __init__(self, x, y, farba):
        self.x = x
        self.y = y
        self.farba = farba

    def __repr__(self):
        return '{} {} {} {}'.format(self.farba, self.__class__.__name__, chr(self.x+64), self.y)

    def __del__(self):
        hra.pravidlo_50=-1

    def posun(self, ax, ay):
        if Nasachovnici([self.x + ax, self.y + ay]):
            if  Find([self.x + ax, self.y + ay], Figurky):
                if Figurky[Pozicia([self.x + ax, self.y + ay], Figurky)].farba == self.farba:
                    return ['', 'stop']
                else:
                    return [[self.x + ax, self.y + ay], 'stop']
            else:
                return [[self.x + ax, self.y + ay], '']
        else:
            return ['', 'stop']

    def sach(self,kam,enpassant=0):
        #Zistí či bude po ťahu hráč v šachu
        vyhod=None
        x,y=self.x,self.y
        zoznam=[]
        if Find(kam,Figurky):
            vyhod=Pozicia(kam,Figurky)
        if enpassant!=0:
            a=hra.pravidlo_50
            Docasne=Figurky[Pozicia([kam[0],kam[1]+enpassant],Figurky)]
            del Figurky[Pozicia([kam[0],kam[1]+enpassant],Figurky)]
        self.x, self.y = kam[0], kam[1]
        for i in range(len(Figurky)):
            if i==vyhod:
                continue
            if Figurky[i].farba!=self.farba:
                zoznam.extend(Figurky[i].mozny_pohyb())
        if self.farba=='B':
            if [Figurky[0].x,Figurky[0].y] in zoznam:
                self.x,self.y=x,y
                return True
        if self.farba=='C':
            if [Figurky[1].x,Figurky[1].y] in zoznam:
                self.x,self.y=x,y
                return True
        self.x,self.y=x,y
        if enpassant!=0:
            Figurky.append(Docasne)
            hra.pravidlo_50=a
        return False

    def v_sachu(self):
        zoznam = []
        if self.farba == 'B':
            for i in range(len(Figurky)):
                if Figurky[i].farba == 'B':
                    zoznam = Figurky[i].mozny_pohyb()
                    if [Figurky[1].x, Figurky[1].y] in zoznam:
                        Figurky[1].ohrozenie = True
                        print('Cierny kral je v ohrozeni')
        elif self.farba == 'C':
            for i in range(len(Figurky)):
                if Figurky[i].farba == 'C':
                    zoznam = Figurky[i].mozny_pohyb()
                    if [Figurky[0].x, Figurky[0].y] in zoznam:
                        Figurky[0].ohrozenie = True
                        print('Biely kral je v ohrozeni')

    def pohyb_uspesny(self):
        #Neskôr tu bude aj kód na grafický posun
        self.v_sachu()
        if self.farba == 'B':
            Figurky[0].ohrozenie = False
        elif self.farba == 'C':
            Figurky[1].ohrozenie = False
        if self.__class__.__name__!='Pesiak':
            hra.enpassantB,hra.enpassantC=0,0
            hra.pravidlo_50+=1
        else:
            hra.pravidlo_50=0
        hra.mat()
        hra.na_tahu=not hra.na_tahu
        if hra.na_tahu:
            hra.tah+=1

class Jazdec(Figura):
    def mozny_pohyb(self):
        a,b=1,2
        zoznam=[]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    kam=[self.x+a,self.y+b]
                    if Nasachovnici(kam):
                        if not Find(kam,Figurky) or Figurky[Pozicia(kam,Figurky)].farba!=self.farba:
                            zoznam.append(kam)
                    a=-a
                b=-b
            a,b=b,a
        return zoznam
    def pohyb(self,kam):
        if kam in self.mozny_pohyb() and not self.sach(kam):
            if Find(kam,Figurky):
                del Figurky[Pozicia(kam,Figurky)]
            self.x=kam[0]
            self.y=kam[1]
            self.pohyb_uspesny()
            
class Pesiak(Figura):
    def mozny_pohyb(self):
        zoznam=[]
        if self.farba=='B':
            a=1 #smer
            z=2 #zaciatočná pozícia
            e=5 #pozícia na enpassant
            en=hra.enpassantC
        else:
            a=-1
            z=7
            e=4
            en=hra.enpassantB
        if not Find([self.x,self.y+a],Figurky):
            zoznam.append([self.x,self.y+a])
        if Find([self.x+1,self.y+a],Figurky):
            if Figurky[Pozicia([self.x+1,self.y+a],Figurky)].farba!=self.farba:
                zoznam.append([self.x+1,self.y+a])
        elif self.y==e and en==self.x+1:
            zoznam.append([self.x+1,self.y+a])
        if Find([self.x-1,self.y+a],Figurky):
            if Figurky[Pozicia([self.x-1,self.y+a],Figurky)].farba!=self.farba:
                zoznam.append([self.x-1,self.y+a])
        elif self.y==e and en==self.x-1:
            zoznam.append([self.x-1,self.y+a])
        if self.y==z and not Find([self.x,self.y+2*a],Figurky) and not Find([self.x,self.y+a],Figurky):
            zoznam.append([self.x,self.y+2*a])   
        return zoznam

    def pohyb(self,kam):
        if self.farba=='B':
            e=-1 #pre enpassant
            p=8 #pozícia na premenu
        else:
            e=1
            p=1
        if not (kam[0]!=self.x and not Find(kam,Figurky)):
            e=0
        if kam in self.mozny_pohyb() and not self.sach(kam,e):
            if Find(kam,Figurky):
                del Figurky[Pozicia(kam,Figurky)]
            if e!=0:
                del Figurky[Pozicia([kam[0],kam[1]+e],Figurky)]
            hra.enpassantB,hra.enpassantC=0,0
            if abs(kam[1]-self.y)==2:
                if self.farba=='B':
                    hra.enpassantB=self.x
                else:
                    hra.enpassantC=self.x
            self.x=kam[0]
            self.y=kam[1]
            self.pohyb_uspesny()
        if self.y==p:
                while True:
                    zmena=input('Zmeň na "dama", "veza", "strelec", "jazdec": ')
                    if zmena=='dama':
                        Figurky.append(Dama(self.x,p,'B'))
                        break
                    if zmena=='veza':
                        Figurky.append(Veza(self.x,p,'B'))
                        break
                    if zmena=='strelec':
                        Figurky.append(Strelec(self.x,p,'B'))
                        break
                    if zmena=='jazdec':
                        Figurky.append(Jazdec(self.x,p,'B'))
                        break
                del Figurky[Pozicia([self.x,p],Figurky)]

class Kral(Figura):
    def __init__(self, x, y, farba):
        Figura.__init__(self, x, y, farba)
        self.malarosada = True
        self.velkarosada = True
        self.ohrozenie = False
    def mozny_pohyb(self):
        smery =[ [self.x+1,self.y], [self.x+1,self.y+1], [self.x,self.y+1], [self.x-1,self.y+1] ]
        smery+=[ [self.x-1,self.y], [self.x-1,self.y-1], [self.x,self.y-1], [self.x+1,self.y-1] ]
        zoznam=[]
        for kam in smery:
            if Nasachovnici(kam):
                if not Find(kam,Figurky) or Figurky[Pozicia(kam,Figurky)].farba!=self.farba:
                        zoznam.append(kam)
        return zoznam
    def Rosada(self, kam):
        zoznam = []
        for i in range(len(Figurky)):
            if Figurky[i].farba!=self.farba:
                zoznam.extend(Figurky[i].mozny_pohyb())
        if self.farba == 'B':
            if kam == [3, 1] and self.velkarosada == True:
                if (Find([2,1], Figurky) or Find([3,1],Figurky) or Find([4,1],Figurky)) == False:
                    if not ([3,1] in zoznam or [4,1] in zoznam):
                        Figurky[Pozicia([1, 1], Figurky)].x = 4
                        self.x = kam[0]
                        return True
            if kam == [7, 1] and self.malarosada == True:
                if (Find([7, 1], Figurky) or Find([6, 1], Figurky)) == False:
                    if not ([7, 1] in zoznam or [6, 1] in zoznam):
                        self.x = 7
                        Figurky[Pozicia([8, 1], Figurky)].x = 6
                        return True
        if self.farba == 'C':
            if kam == [3, 8] and self.velkarosada == True:
                if  (Find([2, 8], Figurky) or Find([3, 8], Figurky) or Find([4, 8], Figurky))== False:
                    if not ( [3, 8] in zoznam or [4, 8] in zoznam):
                        self.x = 3
                        Figurky[Pozicia([1, 8], Figurky)].x = 4
                        return True
            if kam == [7, 8] and self.malarosada == True:
                if (Find([7, 8], Figurky) and not Find([6, 8], Figurky)) == False:
                    if not ([7, 8] in zoznam or [6, 8] in zoznam):
                        self.x = 7
                        Figurky[Pozicia([8, 8], Figurky)].x = 6
                        return True
    def pohyb(self,kam):
        if kam in self.mozny_pohyb() and not self.sach(kam):
            if Find(kam,Figurky):
                del Figurky[Pozicia(kam,Figurky)]
            self.x=kam[0]
            self.y=kam[1]
            self.pohyb_uspesny()
            self.malarosada, self.velkarosada = False,False
        elif not self.sach([self.x,self.y]):
            if self.Rosada(kam):
                self.pohyb_uspesny()
                self.velkarosada, self.malarosada = False,False

class Veza(Figura):
    def mozny_pohyb(self):
        zoznam = []
        for zmena in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            a = 1
            while True:
                b = self.posun(zmena[0] * a, zmena[1] * a)
                if b == ['', 'stop']:
                    break
                elif b[1] == 'stop':
                    zoznam.append(b[0])
                    break
                else:
                    zoznam.append(b[0])
                a += 1
        return zoznam
    def pohyb(self,kam):
        if kam in self.mozny_pohyb() and not self.sach(kam):
            if Find(kam,Figurky):
                del Figurky[Pozicia(kam,Figurky)]
            if [self.x, self.y] == [1,1] and self.farba == 'B':
                Figurky[0].velkarosada = False
            elif [self.x, self.y] == [8,1] and self.farba == 'B':
                Figurky[0].malarosada = False
            if [self.x, self.y] == [1, 8] and self.farba == 'C':
                Figurky[1].velkarosada = False
            elif [self.x, self.y] == [8,8] and self.farba == 'C':
                Figurky[1].malarosada = False
            self.x=kam[0]
            self.y=kam[1]
            self.pohyb_uspesny()

class Dama(Figura):
    def mozny_pohyb(self):
        zoznam = []
        for zmena in [[1,0], [-1,0], [0,1], [0,-1], [1,1], [1,-1], [-1,1], [-1,-1]]:
            a = 1
            while True:
                b = self.posun(zmena[0] * a, zmena[1] * a)
                if b == ['', 'stop']:
                    break
                elif b[1] == 'stop':
                    zoznam.append(b[0])
                    break
                else:
                    zoznam.append(b[0])
                a += 1
        return zoznam
    def pohyb(self,kam):
        if kam in self.mozny_pohyb() and not self.sach(kam):
            if Find(kam,Figurky):
                del Figurky[Pozicia(kam,Figurky)]
            self.x=kam[0]
            self.y=kam[1]
            self.pohyb_uspesny()

class Strelec(Figura):
    def mozny_pohyb(self):
        zoznam = []
        for zmena in [[1,1], [1,-1], [-1,1], [-1,-1]]:
            a = 1
            while True:
                b = self.posun(zmena[0] * a, zmena[1] * a)
                if b == ['', 'stop']:
                    break
                elif b[1] == 'stop':
                    zoznam.append(b[0])
                    break
                else:
                    zoznam.append(b[0])
                a += 1
        return zoznam
    def pohyb(self,kam):
        if kam in self.mozny_pohyb() and not self.sach(kam):
            if Find(kam,Figurky):
                del Figurky[Pozicia(kam,Figurky)]
            self.x=kam[0]
            self.y=kam[1]
            self.pohyb_uspesny()

hra=Hra()
Figurky=[Kral(7,6,'B'), Kral(2,8,'C'), Veza(1,1,'B'), Veza(3,2, 'B')]
print(Figurky)
while not hra.koniec:
    #tah = input('Zadaj ťah, 4 čísla vo formáte "a,b,c,d" - a,b-z miesta, c,d-kam\nalebo vo formáte "A,1,B,2" - A,1-z miesta, B,2-kam: ').split(',')
    tah = input().split(',')
    if tah==['vzdavam sa']:
        if hra.na_tahu:
            print('Čierny vyhral - biely sa vzdal.')
        else:
            print('Biely vyhral - čierny sa vzdal.')
        hra.koniec=True
    elif tah==['remiza'] and hra.pravidlo_50>=100:
        print('Remíza')
        hra.koniec=True
    else:
        if tah[0] not in '123456879':
            tah[0] = ord(tah[0]) - 64
            tah[2] = ord(tah[2]) - 64
        if Nasachovnici([int(tah[2]), int(tah[3])]) and Find([int(tah[0]), int(tah[1])], Figurky):
            f=Figurky[Pozicia([int(tah[0]), int(tah[1])], Figurky)]
            if hra.na_tahu and f.farba=='B' or not hra.na_tahu and f.farba=='C':
                    f.pohyb([int(tah[2]), int(tah[3])])
        else:
            print('Súradnica {}{} nie je na šachovnici alebo na súradnici {}{} nie je žiadna figúrka!'.format(chr(int(tah[2])+64), tah[3], chr(int(tah[0])+64), tah[1]))
    if len(Figurky)==2:
        print('Remíza')
        hra.koniec=True
    print(Figurky)
    #print(Figurky[0].ohrozenie, Figurky[1].ohrozenie)
    #print('Tah:',hra.tah, ', Pravidlo 50:', hra.pravidlo_50, ', Biely na tahu:',hra.na_tahu)
