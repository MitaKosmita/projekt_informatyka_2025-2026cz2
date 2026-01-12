import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QSlider
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor, qPremultiply
from PyQt5.QtCore import Qt, QPointF, QTimer,QRectF


class Zbiornik:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.szerokosc = 150.0
        self.wysokosc = 150.0
        self.poziom_zapelnienia = 0.0
        self.max_poziom = self.wysokosc
        self.napelnia_sie = False
        self.krok_napelniania =0.5
        self.struga_y = self.y +60 #struga zaczyna sie nad zbiornikiem
        self.struga_szerokosc = 10
        self.struga_wysokosc = 40
        self.struga_jest = False
        self.maksymalna_objetosc =  1000.0
        self.objetosc_teraz =0.0
        self.objetoscpx = (self.objetosc_teraz/self.maksymalna_objetosc)*self.wysokosc

    def draw(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()

        #punkty zbiornika
        LG = QPointF(self.x, self.y) #lewy gorny
        PG = QPointF(self.x + self.szerokosc, self.y) #prawy górny
        PD = QPointF(self.x + self.szerokosc, self.y + self.wysokosc) #prawy dolny
        LD = QPointF(self.x, self.y + self.wysokosc) #lewy dolny

        # PUNKTY WLEWU (górna część)
        WLG = QPointF(self.x + 40, self.y - 40) #lewy gorny wlew
        WPG = QPointF(self.x + self.szerokosc - 40, self.y - 40) #prawy górny wlew
        WLD = QPointF(self.x + 60, self.y) #lewy dolny wlew
        WPD = QPointF(self.x + self.szerokosc - 60, self.y) #prawy dolny wlew

        LGR = QPointF(self.x, self.y + 125)#lewy górny róg rury
        #rysowanie zbiornika
        path.moveTo(LGR)
        path.lineTo(LG)
        path.lineTo(WLD)
        path.lineTo(WLG)
        path.lineTo(WPG)
        path.lineTo(WPD)
        path.lineTo(PG)
        path.lineTo(PD)
        path.lineTo(LD)

        #rysowanie cieczy z maskowaniem (z zajec)
        if self.objetosc_teraz > 0:
            painter.save()
            painter.setClipPath(path) #maskowanie do kształtu zbiornika
            wysokosc_zapelnieniapx = self.wysokosc * (self.objetosc_teraz / self.maksymalna_objetosc) #przeliczenie na piksele
            rect_liquid = QRectF(
                self.x,
                self.y + self.wysokosc - wysokosc_zapelnieniapx,
                self.szerokosc,
                wysokosc_zapelnieniapx
            )
            painter.fillRect(rect_liquid, QColor(0, 120, 255, 180)) #niebieska ciecz z przezroczystością
            painter.restore()

        #rysowanie konturu zbiornika
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.darkGray, 4))
        painter.drawPath(path)

        #rysowanie strugi
        if self.struga_jest:
            struga_x = self.x + self.szerokosc / 2 - self.struga_szerokosc / 2 #gdzie zaczyna sie struga w x
            struga_y = self.y - 60 #gdzie zaczyna sie struga w y
            #gdzie jest poziom wody w pikselach
            poziom_wody_y = self.y + self.wysokosc - (self.wysokosc * (self.objetosc_teraz / self.maksymalna_objetosc))
            #wysokosc strugi to odleglosc od startu do wody
            aktualna_wysokosc_strugi = poziom_wody_y - struga_y
            #rysowanie strugi
            rect_struga = QRectF(struga_x, struga_y, self.struga_szerokosc, aktualna_wysokosc_strugi)
            painter.fillRect(rect_struga, QColor(0, 120, 255, 180))

    def dolej(self):
        if self.napelnia_sie: #tylko jeśli tryb napełniania jest włączony
            self.objetosc_teraz += self.krok_napelniania
            #ograniczamy do maksymalnej wysokości
            if self.objetosc_teraz > self.maksymalna_objetosc:
                self.objetosc_teraz = self.maksymalna_objetosc

        if self.objetosc_teraz >= self.maksymalna_objetosc:
            self.struga_jest = False

    def poziomPierwszegoZbiornika(self):#getter obencego poziomu cieczy
        return self.objetosc_teraz


class Piec:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.poziom_wegla = 0
        self.wysokosc = 500
        self.szerokosc = 250
        self.max_poziom_wegla = 50
        self.poziom_zapelnienia = 0
        self.czy_sie_napelnia = False
        self.otwiera_sie = False
        self.czy_jest_ogien = False
        self.licznik_czasu = 0
        self.doplyw_powietrza = 100


    def draw(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        #punkty pieca (do rozbudowania o rury )!!!
        LG = QPointF(self.x, self.y)
        PG = QPointF(self.x+self.szerokosc, self.y)
        PD = QPointF(self.x+self.szerokosc, self.y+ self.wysokosc)
        LD = QPointF(self.x, self.y+self.wysokosc)

        RHG= QPointF(self.x, self.y+425)#gora rury hoppera na wegiel
        RHD = QPointF(self.x, self.y+ 450)#dol rury hoppera na wegiel

        ZPG = QPointF(self.x,self.y+10)#zasuwa powietrza góra
        ZPD = QPointF(self.x, self.y+60)#zasówa powietrza dół

        #budowanie ksztaltu pieca
        path.moveTo(RHG)
        path.lineTo(ZPD)
        path.moveTo(ZPG)
        path.lineTo(LG)
        path.lineTo(PG)
        path.lineTo(PD)
        path.lineTo(LD)
        path.lineTo(RHD)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.darkGray, 4))
        painter.drawPath(path)

        #rysowanie zasuwy
        painter.setPen(QPen(Qt.black, 4))
        zakres_ruchu = ZPD.y() - ZPG.y()
        wysuniecie_teraz = zakres_ruchu *  self.doplyw_powietrza / 100
        painter.drawLine(int(ZPD.x()),int(ZPD.y()-wysuniecie_teraz),int(ZPG.x()),int(ZPG.y()))#musi byc int bo nie moga byc zmienno przecinkowe w drawline(wczesniej nie dzialalo ze zmiennoprzecinkowymi)

        if self.licznik_czasu > 0:
            painter.setPen(Qt.NoPen)
            ilosc_powietrza = 0.1 + (0.9 * (self.doplyw_powietrza / 100.0))  #Minimum ognia to 0.1 zeby nie zgasl przy poziomie powietrza 0%
            wielkosc_najwiekszego = 50 * ilosc_powietrza
            wielkosc_sredniego = 30 * ilosc_powietrza
            wielkosc_malego = 15 * ilosc_powietrza
            dno = self.y + self.wysokosc#dno pieca do zaczepiania plommieni
            #najnizszy plomien
            painter.setBrush(QColor(255, 180, 0))
            y_najwiekszy =dno - wielkosc_najwiekszego - 2
            painter.drawRect(int(self.x + 2), int(y_najwiekszy), int(self.szerokosc - 4), int(wielkosc_najwiekszego))
            #plomien sredni zaczepiony na najnizszym
            painter.setBrush(QColor(255, 200, 0))
            y_sredni = y_najwiekszy - wielkosc_sredniego#zaczyna sie tam gdzie konczy sie najnizszy
            painter.drawRect(int(self.x + 30), int(y_sredni), int(self.szerokosc - 60), int(wielkosc_sredniego))
            #najwyzszy plomien zaczepiony na gorze sredniego
            painter.setBrush(QColor(255, 255, 0, 220))
            y_maly = y_sredni - wielkosc_malego#zaczyna sie tam gdzie konczy sie srdeni
            painter.drawRect(int(self.x + 50), int(y_maly), int(self.szerokosc - 100), int(wielkosc_malego))

            self.licznik_czasu -= 1


class Hopper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.poziom_wegla = 0
        self.wysokosc = 200
        self.szerokosc = 175
        self.max_poziom_wegla = self.wysokosc
        self.poziom_zapelnienia = 0
        self.czy_sie_napelnia = False
        self.czy_zamkniety = True
        self.otwiera_sie = False
        self.zamyka_sie = False
        self.dlugosc_klapy = 25.0
        self.max_dlugosc_klapy = 25.0
        self.predkosc_otwierania = 2.0
        self.lista_wegielkow = [] #lista ma x,y, status czy moze spadac
        self.predkosc_spadania = 1

    def draw(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        #punkty hoppera
        LG = QPointF(self.x, self.y) #lewa gora
        PG = QPointF(self.x + self.szerokosc, self.y) #rawa gora
        PD = QPointF(self.x + self.szerokosc - 75, self.y + self.wysokosc) #prawy doł
        LD = QPointF(self.x + 75, self.y + self.wysokosc) #lewy doł

        #rysowanie konturu hoppera
        path.moveTo(LG)
        path.lineTo(PG)
        path.lineTo(PD)
        path.lineTo(LD)
        path.closeSubpath() #zamyka kontur

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.darkGray, 4))
        painter.drawPath(path)

        #animowana klapa
        painter.setPen(QPen(Qt.black, 4))
        klapa_start = LD
        klapa_koniec = QPointF(LD.x() + self.dlugosc_klapy, LD.y())
        painter.drawLine(klapa_start, klapa_koniec)

        #rysowanie wegla
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.NoPen)
        for kulka in self.lista_wegielkow:
            #rysowanie zaczyna sie od lewego gornego rogu a promien to 10 wiec 5 to srodek kulki (po srodku)
            painter.drawEllipse(int(kulka[0] - 5), int(kulka[1]), 10, 10)

    def animuj_klape(self):
        if self.otwiera_sie:
            self.dlugosc_klapy += self.predkosc_otwierania
            if self.dlugosc_klapy > self.max_dlugosc_klapy:
                self.dlugosc_klapy = self.max_dlugosc_klapy

        if self.zamyka_sie:
            self.dlugosc_klapy -= self.predkosc_otwierania
            if self.dlugosc_klapy < 0:
                self.dlugosc_klapy = 0

    def animuj_wegiel(self):
        dol = self.y + self.wysokosc
        promien = 5

        for i, kulka in enumerate(self.lista_wegielkow): #enumerate zeby znac indeks i wartosci z tablicy wegielkow
            #na poczatku zakladamy ze kulka moze spadac
            moze_spadac = True
            if 200 <= kulka[0] <= 400 and kulka[1] >= 790:#jesli kulka jest w piecu
                self.lista_wegielkow.pop(i)  #usun kulke

            #czy wegiel ktory badmy jest blisko innego wegla z listy
            for j, inna in enumerate(self.lista_wegielkow):
                #jesli indeksy badanego wegla i innego sa te same to to jest ten sam wegiel wiec go pomijamy
                if i == j: continue
                # jesli inny wegiel jest tuz pod nami (w pionie i poziomie) to blokujemy spadanie tego na gorze
                if abs(kulka[0] - inna[0]) < 10 and 0 < inna[1] - kulka[1] < 10:
                    moze_spadac = False
                    # zsuwanie: przesun kulke lekko w bok zeby nie stala na czubku
                    if kulka[0] < inna[0]:
                        kulka[0] -= 1
                    else:
                        kulka[0] += 1
                    break

            #blokada na klapie tylko jesli klapa jest wysunieta
            if self.dlugosc_klapy > 5:
                #prawdzamy czy kulka jest na wysokosci dna i czy klapa tam siega
                if dol - 5 < kulka[1] < dol + 5:
                    #sprawdza czy pozycja wegielka jest w zasiegu wysunietej klapy
                    if kulka[0] < self.x + 75 + self.dlugosc_klapy:
                        #jak klapa blokuje droge to wegielek nie spada
                        moze_spadac = False
                        kulka[1] = dol - promien  #poloz kulke idealnie na linii

            #ruch w doljesli nic nie blokuje to spadaj
            if moze_spadac:
                kulka[1] += kulka[3]

            #sciany lejka dzialaja tylko gdy kulka jest jeszcze w srodku
            if kulka[1] < dol:
                # im nizej jest kulka tym blizej srodka musi byc
                procent_y = (kulka[1] - self.y) / self.wysokosc #oblicza jak nisko jest kulka od 0 do 1 pomocne zeby wiedziec jak bardzo lejek sie zweza
                lewa_sciana = self.x + (75 * procent_y)#oblicza pozycje lewej sciany lejka
                prawa_sciana = self.x + self.szerokosc - (75 * procent_y)#oblicza pozycje prawej sciany lejka

                #odbijanie od lewej i prawej scianki jesi wychodzi to daj ja do srodka
                if kulka[0] < lewa_sciana + promien:
                    kulka[0] = lewa_sciana + promien
                if kulka[0] > prawa_sciana - promien:
                    kulka[0] = prawa_sciana - promien

            cx = 80 + 220  # x_poczatkowe+bok_kwadratu
            cy = 530  # y_poczatkowe
            r_max = 240  # promien zewnetrzny
            r_min = 240 - 50  # promien wewnetrzny (szerokosc rury)
            if kulka[0] < cx and kulka[1] > cy:
                # obliczamy odleglosc od srodka kola uzywajac pitagorasa
                # a^2 + b^2 = c^2, odleglosc = pierwiastek(dx^2 + dy^2)
                dx = kulka[0] - cx
                dy = kulka[1] - cy
                odleglosc = (dx ** 2 + dy ** 2) ** 0.5  # pobieramy dystans od punktu (cx,cy)

                # jesli kulka dotyka scianek luku
                if odleglosc >= r_max:
                    # odbicie od zewnetrznej scianki
                    moze_spadac = False
                    kulka[0] += kulka[3]  # popychamy w prawo
                elif odleglosc <= r_min:
                    # odbicie od wewnetrznej scianki
                    moze_spadac = False
                    kulka[0] -= kulka[3]  # popychamy w lewo

                if 200 <= kulka[0] <= 500 and kulka[1] >= 790:#zeby nie przeszla przez dno
                    moze_spadac = False
                    kulka[3]=0 # ustawienie predkosci spadania kulki na 0
                    kulka[1] = 795  #ustawienie na dnie pieca


    def dodaj_wegiel(self):
        import random #losowo generujemy kulke w przedziale od prawej krawedzi hoppera do lewej krawedzi hoppera z marginesem zeby na bokach sie nie zbieralo duzo wegla
        lewa_granica = self.x +40
        prawa_granica = self.x + self.szerokosc -40
        start_x = random.uniform(lewa_granica, prawa_granica)#losowane pozycji
        predkosc_spadania = 1
        self.lista_wegielkow.append([start_x, self.y - 50, False,predkosc_spadania])#dodawanie wegielka do listy

class Rura:
    def __init__(self, x_poczatkowe, y_poczatkowe, x_koncowe, y_koncowe,czy_logiczna ='', szerokosc=25):
        self.x_poczatkowe= x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.x_koncowe = x_koncowe
        self.y_koncowe = y_koncowe
        self.szerokosc = szerokosc
        self.czy_logiczna = ""
        self.poziom_wody = 0.0
    def draw(self,painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        if self.x_poczatkowe == self.x_koncowe:#rura pionowa
            LG = QPointF(self.x_poczatkowe, self.y_poczatkowe)#lewy gorny rog rury
            PG = QPointF(self.x_poczatkowe + self.szerokosc, self.y_poczatkowe)#prawy gorny rog rury
            LD = QPointF(self.x_koncowe, self.y_koncowe)#lewy dolny rog rury
            PD = QPointF(self.x_koncowe + self.szerokosc, self.y_koncowe)#prawy doly rog rury

            y_dol = max(self.y_poczatkowe, self.y_koncowe)
            wysokosc_rury = abs(self.y_poczatkowe - self.y_koncowe)
            if self.poziom_wody > 0.01:
                poziom_napelnienia = wysokosc_rury * self.poziom_wody
                woda = QRectF(self.x_poczatkowe, y_dol - poziom_napelnienia, self.szerokosc,
                              poziom_napelnienia)  # od dolu w gore
                painter.fillRect(woda, QColor(0, 120, 255, 180))

            #rysowanie rury
            path.moveTo(LD)
            path.lineTo(LG)
            path.moveTo(PG)
            path.lineTo(PD)
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(Qt.darkGray, 4))
            painter.drawPath(path)
        elif self.y_poczatkowe == self.y_koncowe:#rura pozioma
            LG = QPointF(self.x_poczatkowe, self.y_poczatkowe)#lewy gorny rog rury
            PG = QPointF(self.x_koncowe,self.y_koncowe)#prawy gorny rog rury
            PD = QPointF(self.x_poczatkowe, self.y_koncowe+ self.szerokosc)#lewy dolny rog rury
            LD = QPointF(self.x_koncowe, self.y_koncowe+self.szerokosc)#prawy doly rog rury

            if self.poziom_wody > 0.01:
                dlugosc_rury = abs(self.x_poczatkowe - self.x_koncowe)
                wysokosc_wody = self.szerokosc * self.poziom_wody #obiczanei wysokosci wody(niespodziewane)
                x_start = min(self.x_poczatkowe, self.x_koncowe)#lewy bok rury
                y_start = (self.y_poczatkowe + self.szerokosc) - wysokosc_wody#dol rury
                woda = QRectF(x_start, y_start, dlugosc_rury, wysokosc_wody)# peostokat ze stala podstawa ale zmienna wysokoscia
                painter.fillRect(woda, QColor(0, 120, 255, 180))

            # rysowanie rury
            path.moveTo(LG)
            path.lineTo(PG)
            path.moveTo(PD)
            path.lineTo(LD)
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(Qt.darkGray, 4))
            painter.drawPath(path)


class Kolanko:
    def __init__(self, x_poczatkowe, y_poczatkowe,bok_kwadratu,kierunek = " ",czy_logiczny =" ", szerokosc=25):
        self.x_poczatkowe = x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.bok_kwadratu = bok_kwadratu
        self.szerokosc = szerokosc
        self.kierunek = kierunek
        self.czy_logiczny = czy_logiczny
        self.poziom_wody =0.0

    def draw(self, painter):
        #kolanko mozna pojawic w roznych konfiguracjach
        if self.kierunek == "LD":#kolanko pojawi sie w lewej dolnej cwiartce kwadratu
            start_luku = 180
        elif self.kierunek == "PD":
            start_luku = 270
        elif self.kierunek == "PG":
            start_luku = 0
        elif self.kierunek == "LG":
            start_luku = 90
        else:
            start_luku = 0

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.gray,4))
        #skorzystam z drawArc ktory wykorzystuje instrukcje (x,y,szerokosc,wysokosc,start luku,dlugosc luku) kat jest podany w 1/16 stopnia wiec trzeba kat ktory chcemy domnozyc przez 1
        painter.drawArc(self.x_poczatkowe, self.y_poczatkowe, self.bok_kwadratu, self.bok_kwadratu, start_luku * 16,90 * 16)  # zaczynamy od prawego srodka i rysujemy jedna cwiartke
        painter.setPen(QPen(Qt.green,4))
        bok_drugiego_kwadratu = self.bok_kwadratu - (2*self.szerokosc)
        painter.drawArc(self.x_poczatkowe+self.szerokosc,self.y_poczatkowe+self.szerokosc,bok_drugiego_kwadratu, bok_drugiego_kwadratu, start_luku * 16,90*16)
        #proba czegos innego bo w tamtym nie moge rysowac wody maskowaniem(ostatecznie maski nie rysujemy bo nie wyglada to dobrze poniewaz domyka kontur)
        path_maski = QPainterPath()
        painter.setPen(Qt.NoPen)
        path_maski.arcMoveTo(self.x_poczatkowe, self.y_poczatkowe, self.bok_kwadratu, self.bok_kwadratu, start_luku)
        path_maski.arcTo(self.x_poczatkowe, self.y_poczatkowe, self.bok_kwadratu, self.bok_kwadratu, start_luku, 90)
        wewnetrzne = self.bok_kwadratu - (2 * self.szerokosc)
        path_maski.arcTo(self.x_poczatkowe + self.szerokosc, self.y_poczatkowe + self.szerokosc, wewnetrzne, wewnetrzne,start_luku + 90, -90)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_maski)

        if self.czy_logiczny == "TAK" and self.poziom_wody > 0.01:
            painter.save()
            painter.setClipPath(path_maski)
            #prostokat analogiczny jak dla rur tyle ze z maskowaniem zeby woda nie rysowala sie poza kolankiem
            wysokosc_wody = self.bok_kwadratu * self.poziom_wody
            y_dna = self.y_poczatkowe + self.bok_kwadratu
            woda = QRectF(self.x_poczatkowe, y_dna - wysokosc_wody, self.bok_kwadratu, wysokosc_wody)
            painter.fillRect(woda, QColor(0, 120, 255, 180))
            painter.restore()


class Pompa:
    def __init__(self, x_poczatkowe, y_poczatkowe, bok_kwadratu):
        self.dziala = False
        self.x_poczatkowe = x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.bok_kwadratu = bok_kwadratu
        self.czy_wlaczona = False

    def draw(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        if self.czy_wlaczona:
            pen = QPen(Qt.green)
        else:
            pen = QPen(Qt.red)

        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawArc(self.x_poczatkowe, self.y_poczatkowe, self.bok_kwadratu, self.bok_kwadratu, 0, 360 * 16)#rysowanie okregu
        wierzcholek1 = QPointF(self.x_poczatkowe+self.bok_kwadratu/2, self.y_poczatkowe)
        wierzcholek2 = QPointF(self.x_poczatkowe, self.y_poczatkowe+self.bok_kwadratu/2)
        wierzcholek3 = QPointF(self.x_poczatkowe+self.bok_kwadratu/2, self.y_poczatkowe+self.bok_kwadratu)
        #rysowanie trojkata innym sposobem  zeby nie robic caly czas tego samego
        painter.drawLine(wierzcholek1, wierzcholek2)
        painter.drawLine(wierzcholek2, wierzcholek3)
        painter.drawLine(wierzcholek3,wierzcholek1)


class PomieszczeniePradnicy:
    def __init__(self,x_poczatkowe, y_poczatkowe):
        self.x_poczatkowe = x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.bok = 75
    def draw(self,painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        LG = QPointF(self.x_poczatkowe, self.y_poczatkowe)
        PG = QPointF(self.x_poczatkowe + self.bok, self.y_poczatkowe)
        LD = QPointF(self.x_poczatkowe, self.y_poczatkowe + self.bok)
        PD = QPointF(self.x_poczatkowe + self.bok, self.y_poczatkowe + self.bok)

        wlotGora =QPointF(self.x_poczatkowe,self.y_poczatkowe+25)
        wlotDol = QPointF(self.x_poczatkowe,self.y_poczatkowe+ self.bok -25)

        wylotGora = QPointF(self.x_poczatkowe + self.bok, self.y_poczatkowe + 25)
        wylotDol = QPointF (self.x_poczatkowe + self.bok, self.y_poczatkowe + self.bok -25)

        path.moveTo(wlotGora)
        path.lineTo(LG)
        path.lineTo(PG)
        path.lineTo(wylotGora)
        path.moveTo(wylotDol)
        path.lineTo(PD)
        path.lineTo(LD)
        path.lineTo(wlotDol)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.darkGray, 4))
        painter.drawPath(path)

class OknoZRysunkami(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.suma_wody =0.0
        self.czasteczki_pary= []#x,y
        self.setWindowTitle("Zbiorniki projekt")
        self.zbiornik = Zbiornik(600, 550) #wymiary wysokosc:150 szerokosc: 150
        self.piec = Piec(200,300) #wymiary wysokosc: 500 szerokosc: 250
        self.hopper = Hopper(5,400) #wymiary wyokosc:200 szerokosc: 200
        self.rura_pionowa = Rura(80, 600, 80, 630, "NIE")
        self.rura = Rura(600, 675, 450, 675, "TAK")
        self.kolanko1 = Kolanko(400, 600, 100, kierunek="LD",czy_logiczny= "TAK")
        self.kolanko2 = Kolanko(80, 510,240, kierunek="LD", czy_logiczny="NIE")
        self.kolanko3 = Kolanko(325, 325, 100, kierunek="PG",czy_logiczny= "TAK")
        self.kolanko4 = Kolanko(325, 325, 100, kierunek="LG",czy_logiczny= "TAK")
        self.kolanko5 = Kolanko(250, 325, 100, kierunek="PD",czy_logiczny= "TAK")
        self.kolanko6 = Kolanko(250, 325, 100, kierunek="LD",czy_logiczny= "TAK")
        self.rura1 = Rura(400,650,400,375, "TAK")
        self.rura2 = Rura(250,375,250,150,"TAK")
        self.kolanko7 = Kolanko(250,100,100, kierunek="LG")
        self.pomieszczenie_pradnicy = PomieszczeniePradnicy(300,75)
        self.pompa = Pompa(500,657,60)

        self.resize(1280, 920)
        #timer zeby sie zmienialp
        self.timer = QTimer()
        self.timer.timeout.connect(self.aktualizuj_wode)
        self.timer.start(8)#cos kolo 120 fps

    def paintEvent(self, event):
        painter = QPainter(self)
        self.zbiornik.draw(painter)
        self.hopper.draw(painter)
        self.rura_pionowa.draw(painter)
        self.kolanko1.draw(painter)
        self.kolanko2.draw(painter)
        self.piec.draw(painter)
        self.rura.draw(painter)
        self.kolanko3.draw(painter)
        self.kolanko4.draw(painter)
        self.kolanko5.draw(painter)
        self.kolanko6.draw(painter)
        self.rura1.draw(painter)
        self.rura2.draw(painter)
        self.kolanko7.draw(painter)
        self.pomieszczenie_pradnicy.draw(painter)
        self.pompa.draw(painter)
        painter.drawLine(10,100, 1000,100)
        painter.drawLine(10, 150, 1000, 150)
        for p in self.czasteczki_pary:
            painter.setBrush(QColor(220, 220, 220))#jasnoszary
            rozmiar = 3
            painter.drawEllipse(int(p[0]), int(p[1]), rozmiar, rozmiar)

    def aktualizuj_wode(self):#zmienic nazwe funckji na bardziej adekwatna pod koniec
        self.zbiornik.dolej()
        self.hopper.animuj_klape()
        woda_na_rury =0
        if self.zbiornik.napelnia_sie:
            self.suma_wody += self.zbiornik.krok_napelniania
            if self.suma_wody > 3000:
                self.suma_wody = 3000#maksymalna  pojemnosc calego systemu rur

        woda = self.suma_wody
        krok_pompowania = 0.5
        #najpierw zbiornik rura i kolanko napelniaja sie rownoczzesnie
        if woda <= 25:
            procent_wspolny = woda / 25.0
            self.rura.poziom_wody = procent_wspolny
            self.kolanko1.poziom_wody = woda/self.kolanko1.bok_kwadratu
            self.zbiornik.objetosc_teraz = (woda / 150.0) * self.zbiornik.maksymalna_objetosc
            woda_na_rury = 0

            #jesli rura i kolanko sie zapelnily to tylko zbiornik sie napelnia
        elif woda <= 150:
            self.rura.poziom_wody = 1.0
            self.kolanko1.poziom_wody = woda / self.kolanko1.bok_kwadratu
            self.zbiornik.objetosc_teraz = (woda / 150.0) * self.zbiornik.maksymalna_objetosc
            woda_na_rury = woda - 50.0

        if self.pompa.czy_wlaczona and self.zbiornik.objetosc_teraz > 0:
            self.zbiornik.objetosc_teraz = max(0, self.zbiornik.objetosc_teraz - krok_pompowania)

        if self.pompa.czy_wlaczona and woda > 100:
            if self.rura1.poziom_wody < 1.0:#napelniaj rure 1 dokad nie bedzie pelna
                self.rura1.poziom_wody += 0.01
            elif self.kolanko3.poziom_wody < 1.0:#tak samo z kolankiem 3
                self.kolanko3.poziom_wody += 0.01
            elif self.kolanko4.poziom_wody < 1.0:#tak samo z kolankiem 3
                self.kolanko4.poziom_wody += 0.01
            elif self.kolanko5.poziom_wody < 1.0:#tak samo z kolankiem 3
                self.kolanko5.poziom_wody += 0.01
            elif self.kolanko6.poziom_wody < 1.0:
                self.kolanko6.poziom_wody += 0.01

        else:
            #jesli pompa nie dziala woda splywa
            self.rura1.poziom_wody = max(0, self.rura1.poziom_wody - 0.02)
            self.rura2.poziom_wody = max(0, self.rura2.poziom_wody - 0.02)
            self.kolanko3.poziom_wody = max(0,self.kolanko3.poziom_wody - 0.02)
            self.kolanko4.poziom_wody = max(0,self.kolanko4.poziom_wody - 0.02)
            if not self.zbiornik.napelnia_sie:
                self.zbiornik.struga_jest = False

        for kulka in self.hopper.lista_wegielkow:
            #jesli kulka jest w poblizu dna pieca
            if 200 <= kulka[0] <= 400 and kulka[1] >= 790:
                self.piec.licznik_czasu +=1200# zmienic na wiecej potem
                break
        self.zarzadzanie_para()
        self.hopper.animuj_wegiel()
        self.update()

    def zarzadzanie_para(self):
        import random
        czy_sie_pali = self.piec.licznik_czasu > 0
        if czy_sie_pali and self.kolanko6.poziom_wody > 0.1:
            if len(self.czasteczki_pary) < 1000:#limit czasteczek
                for i in range(1):
                    #x, y
                    self.czasteczki_pary.append([262 + random.randint(-8, 8), 375, 255])
#self.rura2 = Rura(250,375,250,150,"TAK")

        for p in self.czasteczki_pary:
            if p[1]>150:
                p[1]-=1.0
                drganie = p[0]+random.uniform(-0.5, 0.5)
                if 250<p[0]+drganie<275:
                    p[0]+=drganie
            elif 110 < p[1] <= 150:#ruch w kolanku
                p[1] -= 1.0#troche w gore
                p[0] += 0.6#troche w prawo
            else:
                p[0] += 1.0#leci w prawo
                dy = random.uniform(-0.5, 10)
                if 105 < p[1] + dy < 125:
                    p[1] += dy#drgania w pionie zeby nie lecialo nudnie ciurkiem

            #usuwanie czasteczek gdy wyleca za ekran
            if p[0] > 1300:
                self.czasteczki_pary.remove(p)


#sterowanie
class OknoSterowania(QWidget):
    def __init__(self, zbiornik, okno_wiz):
        super().__init__()
        self.zbiornik = zbiornik
        self.okno_wiz = okno_wiz
        self.setWindowTitle("Sterowanie")
        self.resize(300, 400)

        budowa_sterowania = QVBoxLayout()#glowny kolumnowy uklad(zobaczymy ile tego bedzie pozniej)

        self.przyciski_box = QGroupBox("Sterowanie pierwszym zbiornikiem (z woda)")
        przyciski_layout = QHBoxLayout()
        self.btn_start = QPushButton("DOLEJ")
        self.btn_start.setStyleSheet("background-color: green;")
        self.btn_stop = QPushButton("STOP")
        self.btn_stop.setStyleSheet("background-color: red;")
        self.btn_reset = QPushButton("OPRÓŻNIJ")
        self.btn_reset.setStyleSheet("background-color: yellow;")

        #dodanie przyciskow do layoutu(rząd)
        przyciski_layout.addWidget(self.btn_start)
        przyciski_layout.addWidget(self.btn_stop)
        przyciski_layout.addWidget(self.btn_reset)

        #w ilu % zapełniony jest zbiornik
        self.label_procent = QLabel(f"Poziom 0%")
        self.label_procent.setStyleSheet("color: black; font-weight: bold;")
        przyciski_layout.addWidget(self.label_procent)

        #dodanie rzędu do kolumny layoutu
        self.przyciski_box.setLayout(przyciski_layout)

        #dodanie podokna do layoutu
        budowa_sterowania.addWidget(self.przyciski_box)

        #główny layout
        self.setLayout(budowa_sterowania)

        #kliczki linkujemy
        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_reset.clicked.connect(self.reset)

        #sterowanie hopperem
        self.hopper_box = QGroupBox("Sterowanie hopperem")
        hopper_layout = QHBoxLayout()  # poziomo przyciski
        self.btn_wrzuc = QPushButton("WRZUC WEGIEL")
        self.btn_wrzuc.setStyleSheet("background-color: gray;")
        self.btn_otworz = QPushButton("OTWORZ KLAPE")
        self.btn_otworz.setStyleSheet("background-color: green;")
        self.btn_zamknij = QPushButton("ZAMKNIJ KLAPE ")
        self.btn_zamknij.setStyleSheet("background-color: red;")
        #przyciski
        hopper_layout.addWidget(self.btn_wrzuc)
        hopper_layout.addWidget(self.btn_otworz)
        hopper_layout.addWidget(self.btn_zamknij)

        self.hopper_box.setLayout(hopper_layout)
        budowa_sterowania.addWidget(self.hopper_box)#dodajemy to co stworzylismy wczesniej do glownej kolumny
        #linkowanie przyciskow
        self.btn_otworz.clicked.connect(self.otworz_hopper)
        self.btn_zamknij.clicked.connect(self.zamknij_hopper)
        self.btn_wrzuc.clicked.connect(self.wrzuc_hopper)

        #sterowanie piecem
        self.piec_box = QGroupBox("Piec")
        piec_layout = QVBoxLayout()

        self.label_powietrze = QLabel("Dopływ powietrza: 100%")
        piec_layout.addWidget(self.label_powietrze)
        self.suwak_powietrza = QSlider(Qt.Horizontal)
        self.suwak_powietrza.setRange(0, 100)
        self.suwak_powietrza.setValue(100)
        self.suwak_powietrza.valueChanged.connect(self.zmien_doplyw)

        piec_layout.addWidget(self.suwak_powietrza)
        self.piec_box.setLayout(piec_layout)

        #Dodanie do głównego układu
        budowa_sterowania.addWidget(self.piec_box)

        # sterowanie pompa
        self.pompa_box = QGroupBox("Sterowanie pompa")
        pompa_layout = QHBoxLayout()  # poziomo przyciski
        self.btn_on = QPushButton("WŁĄCZ POMPĘ")
        self.btn_on.setStyleSheet("background-color: green;")
        self.btn_off= QPushButton("WYŁĄCZ POMPĘ")
        self.btn_off.setStyleSheet("background-color: red;")
        # przyciski
        pompa_layout.addWidget(self.btn_on)
        pompa_layout.addWidget(self.btn_off)
        #dodanie do kwadratu z pompa naszych kliczkow
        self.pompa_box.setLayout(pompa_layout)
        # Dodanie do głównego układu
        budowa_sterowania.addWidget(self.pompa_box)
        #laczenie przyciskow
        self.btn_on.clicked.connect(self.wlacz_pompe)
        self.btn_off.clicked.connect(self.wylacz_pompe)

    #logika przyciskow
    def start(self):
        self.zbiornik.napelnia_sie = True
        self.zbiornik.struga_jest = True

    def stop(self):
        self.zbiornik.napelnia_sie = False
        self.zbiornik.struga_jest = False

    def reset(self):
        self.zbiornik.napelnia_sie = False
        self.zbiornik.objetosc_teraz = 0
        self.okno_wiz.suma_wody = 0.0
        self.okno_wiz.rura.poziom_wody = 0.0
        self.okno_wiz.kolanko1.poziom_wody = 0.0
        self.okno_wiz.rura1.poziom_wody = 0.0
        self.okno_wiz.rura2.poziom_wody = 0.0
        self.okno_wiz.update()
        self.update_status()
        self.zbiornik.struga_jest = False

    #update % napelnienia
    def update_status(self):
        procent = (self.zbiornik.poziomPierwszegoZbiornika() / self.zbiornik.maksymalna_objetosc * 100)
        self.label_procent.setText(f"Poziom: {procent:.1f} %")
        self.update()

    #logika przyciskow hoppera
    def otworz_hopper(self):
        self.okno_wiz.hopper.otwiera_sie = False
        self.okno_wiz.hopper.zamyka_sie = True

    def zamknij_hopper(self):
        self.okno_wiz.hopper.otwiera_sie = True
        self.okno_wiz.hopper.zamyka_sie = False

    def wrzuc_hopper(self):
        self.okno_wiz.hopper.dodaj_wegiel()

    #logika pieca
    def zmien_doplyw(self, wartosc):
        self.okno_wiz.piec.doplyw_powietrza = wartosc
        self.label_powietrze.setText(f"Dopływ powietrza: {wartosc}%")

    #logika pompy
    def wlacz_pompe(self):
        self.okno_wiz.pompa.czy_wlaczona = True

    def wylacz_pompe(self):
        self.okno_wiz.pompa.czy_wlaczona = False

app = QApplication(sys.argv)
okno_wiz = OknoZRysunkami()
okno_ctrl = OknoSterowania(okno_wiz.zbiornik, okno_wiz)
okno_wiz.timer.timeout.connect(okno_ctrl.update_status)#polaczenie timera z funkcja procentow w oknie sterowania
okno_wiz.show()
okno_ctrl.show()
sys.exit(app.exec_())

