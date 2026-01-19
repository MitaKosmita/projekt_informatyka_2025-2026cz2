import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QSlider
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor
from PyQt5.QtCore import Qt, QPointF, QTimer,QRectF
import pyqtgraph as pg
class Zbiornik:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.szerokosc = 150.0
        self.wysokosc = 150.0
        self.max_poziom = self.wysokosc
        self.napelnia_sie = False
        self.krok_napelniania =0.5
        self.struga_y = self.y +60 #struga zaczyna sie nad zbiornikiem
        self.struga_szerokosc = 10
        self.struga_wysokosc = 40
        self.struga_jest = False
        self.maksymalna_objetosc =  1000.0
        self.objetosc_teraz =0.0
        self.struga2_jest = False

    def draw(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()

        #punkty zbiornika
        LG = QPointF(self.x, self.y) #lewy gorny
        PG = QPointF(self.x + self.szerokosc, self.y) #prawy górny
        PD = QPointF(self.x + self.szerokosc, self.y + self.wysokosc) #prawy dolny
        LD = QPointF(self.x, self.y + self.wysokosc) #lewy dolny

        #punkty wlewu
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
            woda = QRectF(struga_x, struga_y, self.struga_szerokosc, aktualna_wysokosc_strugi)
            painter.fillRect(woda, QColor(0, 120, 255, 180))

        if self.struga2_jest:
            struga_x =  665
            struga_y = 450
            # gdzie jest poziom wody w pikselach
            poziom_wody_zbiornika = self.y + self.wysokosc - (self.wysokosc * (self.objetosc_teraz / self.maksymalna_objetosc))
            # wysokosc strugi to odleglosc od startu do wody
            aktualna_wysokosc_strugi = poziom_wody_zbiornika- struga_y
            szerokosc_strugi = 25
            # rysowanie strugi
            woda = QRectF(struga_x, struga_y, szerokosc_strugi, aktualna_wysokosc_strugi)
            painter.fillRect(woda, QColor(0, 120, 255, 180))

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
        self.wysokosc = 500
        self.szerokosc = 250
        self.max_poziom_wegla = 50
        self.czy_jest_ogien = False
        self.licznik_czasu = 0
        self.doplyw_powietrza = 100


    def draw(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        LG = QPointF(self.x, self.y)
        PG = QPointF(self.x+self.szerokosc, self.y)
        PD = QPointF(self.x+self.szerokosc, self.y+ self.wysokosc)
        LD = QPointF(self.x, self.y+self.wysokosc)

        RHG= QPointF(self.x, self.y+425)#gora rury hoppera na wegiel
        RHD = QPointF(self.x, self.y+ 450)#dol rury hoppera na wegiel

        ZPG = QPointF(self.x,self.y+10)#zasuwa powietrza góra
        ZPD = QPointF(self.x, self.y+60)#zasówa powietrza dół

        WPG= QPointF(self.x+50, self.y)#wylot pary gora
        WPG2 = QPointF(self.x+75, self.y)#wylot pary gora 2 czesc

        WWD = QPointF(self.x+self.szerokosc, self.y+self.wysokosc -125)#wlot wody dol
        WWD2 = QPointF(self.x+self.szerokosc, self.y+self.wysokosc-100)

        #budowanie ksztaltu pieca
        path.moveTo(RHG)
        path.lineTo(ZPD)
        path.moveTo(ZPG)
        path.lineTo(LG)
        path.lineTo(WPG)
        path.moveTo(WPG2)
        path.lineTo(PG)
        path.lineTo(WWD)
        path.moveTo(WWD2)
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
        self.wysokosc = 200
        self.szerokosc = 175
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
        predkosc_w_prawo = 1.3

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
                    #zsuwanie: przesun kulke lekko w bok zeby nie stala na czubku
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

            if moze_spadac:
                if kulka[1] < 650:
                    kulka[1] += self.predkosc_spadania

                elif 650 <= kulka[1] < 700:
                    kulka[1] += self.predkosc_spadania
                    kulka[0] += predkosc_w_prawo

                else:
                    kulka[1] += self.predkosc_spadania * 0.5
                    kulka[0] += predkosc_w_prawo*2


    def dodaj_wegiel(self):
        import random #losowo generujemy kulke w przedziale od prawej krawedzi hoppera do lewej krawedzi hoppera z marginesem zeby na bokach sie nie zbieralo duzo wegla
        lewa_granica = self.x +40
        prawa_granica = self.x + self.szerokosc -40
        start_x = random.uniform(lewa_granica, prawa_granica)#losowane pozycji
        predkosc_spadania = 1
        self.lista_wegielkow.append([start_x, self.y - 50, False,predkosc_spadania])#dodawanie wegielka do listy

class Rura:
    def __init__(self, x_poczatkowe, y_poczatkowe, x_koncowe, y_koncowe,czy_zaworowa ='',lewa_prawa = " ", szerokosc=25):
        self.x_poczatkowe= x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.x_koncowe = x_koncowe
        self.y_koncowe = y_koncowe
        self.szerokosc = szerokosc
        self.czy_zaworowa = czy_zaworowa
        self.poziom_wody = 0.0
        self.lewa_prawa = lewa_prawa
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
                x_min = min(self.x_poczatkowe, self.x_koncowe)
                wysokosc_wody = self.szerokosc * self.poziom_wody
                y_start_wody = (self.y_poczatkowe + self.szerokosc) - wysokosc_wody

                if self.czy_zaworowa == 'TAK':
                    zasieg_poziomy = dlugosc_rury * 0.5

                    if self.lewa_prawa == 'PRAWA':
                        #woda od prawej do srodka
                        x_start_rysowania = x_min + (dlugosc_rury * 0.5)
                    else:
                        #woda od lewej do srodka
                        x_start_rysowania = x_min

                    woda = QRectF(x_start_rysowania, y_start_wody, zasieg_poziomy, wysokosc_wody)
                    painter.fillRect(woda, QColor(0, 120, 255, 180))
                else:
                    #jak otworzymy zawor to jest na calej rurze woda
                    woda = QRectF(x_min, y_start_wody, dlugosc_rury, wysokosc_wody)
                    painter.fillRect(woda, QColor(0, 120, 255, 180))

            # rysowanie rury
            path.moveTo(LG)
            path.lineTo(PG)
            path.moveTo(PD)
            path.lineTo(LD)
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(Qt.darkGray, 4))
            painter.drawPath(path)

    def ustaw_zawor(self, czy_blokuje):
        if czy_blokuje:
            self.czy_zaworowa = 'TAK'
        else:
            self.czy_zaworowa = 'NIE'

class Kolanko:
    def __init__(self, x_poczatkowe, y_poczatkowe,bok_kwadratu,kierunek = " ",czy_logiczny =" ",kolor=" ", szerokosc=25):
        self.x_poczatkowe = x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.bok_kwadratu = bok_kwadratu
        self.szerokosc = szerokosc
        self.kierunek = kierunek
        self.czy_logiczny = czy_logiczny
        self.poziom_wody =0.0
        self.kolor = kolor

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
        painter.setPen(QPen(Qt.darkGray, 4))
        #skorzystam z drawArc ktory wykorzystuje instrukcje (x,y,szerokosc,wysokosc,start luku,dlugosc luku) kat jest podany w 1/16 stopnia wiec trzeba kat ktory chcemy domnozyc przez 1
        painter.drawArc(self.x_poczatkowe, self.y_poczatkowe, self.bok_kwadratu, self.bok_kwadratu, start_luku * 16,90 * 16)  # zaczynamy od prawego srodka i rysujemy jedna cwiartke
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

        if self.kolor == "NORMALNY":
            kolor_wody =QColor(0, 120, 255, 180)
        else:
            kolor_wody = QColor(173, 216, 230, 180)
        if self.czy_logiczny == "TAK" and self.poziom_wody > 0.01:
            painter.save()
            painter.setClipPath(path_maski)
            #prostokat analogiczny jak dla rur tyle ze z maskowaniem zeby woda nie rysowala sie poza kolankiem
            wysokosc_wody = self.bok_kwadratu * self.poziom_wody
            y_dna = self.y_poczatkowe + self.bok_kwadratu
            woda = QRectF(self.x_poczatkowe, y_dna - wysokosc_wody, self.bok_kwadratu, wysokosc_wody)
            painter.fillRect(woda, kolor_wody)
            painter.restore()

class Pompa:
    def __init__(self, x_poczatkowe, y_poczatkowe, bok_kwadratu):
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

class Pradnica:
    def __init__(self,x_srodka, y_srodka):
        self.x_srodka = x_srodka
        self.y_srodka = y_srodka
        self.obraca_sie = False
        self.predkosc_obrotu =1.0
        self.kat_obrotu =0.0
        self.generowany_prad = 0.0

    def draw(self,painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.save()#zaspisanie ustawien rysowania
        painter.translate(self.x_srodka, self.y_srodka)#ustawienie wspolrzednych na srodek wirnika
        painter.rotate(self.kat_obrotu)#obrot pradnicy
        painter.setPen(QPen(Qt.black, 4))
        painter.drawLine(-25, 0, 25, 0)
        painter.drawLine(0, -25, 0, 25)#dwie prostopadle linie
        painter.restore()#zeby reszta rysunkow nie byla krzywo

        painter.setPen(QPen(Qt.darkYellow))
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        tekst = f"{int(self.generowany_prad)} V"
        painter.drawText(self.x_srodka -10, self.y_srodka - 40, tekst)

    def aktualizuj_obrot(self):
        self.kat_obrotu += self.predkosc_obrotu

class Skraplanie_pary:
    def __init__(self,x_poczatkowe,y_poczatkowe):
        self.x_poczatkowe = x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.szerokosc = 200
        self.wysokosc = 200
        self.poziom_wody =0.0
        self.czy_schladza = False
        self.para_w_srodku=[]#czasteczki ktore wpadly do skraplacza
        self.predkosc_opadania = 2.0

    def draw(self,painter):
        painter.setRenderHint(QPainter.Antialiasing)


        path = QPainterPath()
        LGW = QPointF(self.x_poczatkowe, self.y_poczatkowe + 50)
        LG = QPointF(self.x_poczatkowe, self.y_poczatkowe)
        PG = QPointF(self.x_poczatkowe + self.szerokosc, self.y_poczatkowe)
        PD = QPointF(self.x_poczatkowe + self.szerokosc, self.y_poczatkowe + self.wysokosc)
        LD = QPointF(self.x_poczatkowe, self.y_poczatkowe + self.wysokosc)
        LDW = QPointF(self.x_poczatkowe, self.y_poczatkowe + 75)

        PWC1 = QPointF(self.x_poczatkowe+50, self.y_poczatkowe)#kolejne otwory
        PWC2 = QPointF(self.x_poczatkowe+75, self.y_poczatkowe)
        PWC3 = QPointF(self.x_poczatkowe+125, self.y_poczatkowe)
        PWC4 = QPointF(self.x_poczatkowe + 150, self.y_poczatkowe)

        PGW = QPointF(self.x_poczatkowe+self.szerokosc, self.y_poczatkowe + self.wysokosc -25)

        path.moveTo(LGW)
        path.lineTo(LG)
        path.lineTo(PWC1)
        path.moveTo(PWC2)
        path.lineTo(PWC3)
        path.moveTo(PWC4)
        path.lineTo(PG)
        path.lineTo(PGW)
        path.moveTo(PD)
        path.lineTo(LD)
        path.lineTo(LDW)
        painter.setPen(QPen(Qt.darkGray, 4))
        painter.drawPath(path)
        painter.setPen(QPen(QColor(220, 220, 220), 3))#rysowanie pary z nowej listy
        for p in self.para_w_srodku:
            painter.drawPoint(int(p[0]), int(p[1]))

        if self.poziom_wody > 1.0:
            painter.setBrush(QColor(0, 120, 255, 180))
            painter.setPen(Qt.NoPen)
            x = int(self.x_poczatkowe + 2)
            y = int(self.y_poczatkowe + self.wysokosc - self.poziom_wody)
            w = int(self.szerokosc - 4)
            h = int(self.poziom_wody)
            painter.drawRect(x, y, w + 2, h)
    def logika_skraplania(self):
        import random
        for p in list(self.para_w_srodku):
            p[0] += random.uniform(-1, 1)
            p[1] += random.uniform(-0.5, 0.5)
            if self.czy_schladza:
                if random.random() < 0.02:#2%szasny na spadniecie bo inaczej to spadalo ciurkiem i mi wylaczalao program caly czas
                    p[1] += self.predkosc_opadania * 5#szybki spadek w dol
            if self.poziom_wody>100.0:
                self.poziom_wody = 100.0
            granica_wody = self.y_poczatkowe + self.wysokosc - self.poziom_wody
            if p[1] >= granica_wody or p[1] > self.y_poczatkowe + self.wysokosc:#woda rosnie tylko ponizej 100px
                if self.poziom_wody < self.wysokosc:
                    self.poziom_wody += 0.2
                if p in self.para_w_srodku:
                    self.para_w_srodku.remove(p)

            if p[1] > self.y_poczatkowe + self.wysokosc:#czasteczka znika przy dotknieciu dna
                if p in self.para_w_srodku:
                    self.para_w_srodku.remove(p)

class Zbiornik_Retencyjny():
    def __init__(self, x_poczatkowe, y_poczatkowe):
        self.x_poczatkowe = x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.szerokosc = 300
        self.wysokosc = 200
        self.poziom_wody = 0.0

    def draw(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        LG=QPointF(self.x_poczatkowe, self.y_poczatkowe)
        PG =QPointF(self.x_poczatkowe+self.szerokosc,self.y_poczatkowe)
        PD =QPointF(self.x_poczatkowe+self.szerokosc,self.y_poczatkowe+self.wysokosc)
        LD = QPointF(self.x_poczatkowe, self.y_poczatkowe + self.wysokosc)
        LDW = QPointF(self.x_poczatkowe,self.y_poczatkowe +25)
        LDWW = QPointF(self.x_poczatkowe, self.y_poczatkowe + self.wysokosc-25)#lewy olny wylot wody
        path.moveTo(LG)
        path.lineTo(PG)
        path.lineTo(PD)
        path.lineTo(LD)
        path.moveTo(LDWW)
        path.lineTo(LDW)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.darkGray, 4))
        painter.drawPath(path)

        # rysowanie cieczy z maskowaniem (z zajec) skopiowane ze zbiornika
        if self.poziom_wody > 0:
            painter.save()
            painter.setClipPath(path)  # maskowanie do kształtu zbiornika
            wysokosc_zapelnieniapx = self.wysokosc * (
                        self.poziom_wody / self.wysokosc)  # przeliczenie na piksele
            rect_liquid = QRectF(
                self.x_poczatkowe,
                self.y_poczatkowe + self.wysokosc - wysokosc_zapelnieniapx,
                self.szerokosc,
                wysokosc_zapelnieniapx
            )
            painter.fillRect(rect_liquid, QColor(0, 120, 255, 180))  # niebieska ciecz z przezroczystością
            painter.restore()


class Zawor:
    def __init__(self, x_poczatkowe, y_poczatkowe):
        self.x_poczatkowe = x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.wysokosc = 25
        self.szerokosc = 50
        self.czy_otwarty = False

    def draw(self,painter):
        painter.setRenderHint(QPainter.Antialiasing)
        pol_wysokosci = self.wysokosc/2
        pol_szerokosci = self.szerokosc/2

        if self.czy_otwarty:
            pen = QPen(Qt.green, 4)
        else:
            pen = QPen(Qt.red, 4)
        path = QPainterPath()
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        #trojkat po lewo
        path.moveTo(self.x_poczatkowe - pol_szerokosci, self.y_poczatkowe - pol_wysokosci)
        path.lineTo(self.x_poczatkowe- pol_szerokosci, self.y_poczatkowe + pol_wysokosci)
        path.lineTo(self.x_poczatkowe, self.y_poczatkowe)
        path.closeSubpath()
        #prawy trojkat
        path.moveTo(self.x_poczatkowe + pol_szerokosci, self.y_poczatkowe - pol_wysokosci)
        path.lineTo(self.x_poczatkowe +pol_szerokosci, self.y_poczatkowe +pol_wysokosci)
        path.lineTo(self.x_poczatkowe, self.y_poczatkowe)
        path.closeSubpath()

        painter.drawPath(path)

class OknoZRysunkami(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.moc_plynna = 0.0  #przechowuje wygladzona wartosc powietrza
        self.akumulator_pary = 0.0  #przechowuje ulamek wygenerwoanej pary
        self.napiecie_wygladzone = 0.0
        self.suma_wody =0.0
        self.licznik_opoznienia = 0
        self.licznik_czasu_pary = 0
        self.czasteczki_pary= []#x,y
        self.regulator_aktywny = False
        self.licznik_klatek_auto = 0
        self.pierwszy_wegiel_wpadl = False
        self.pompa_wystartowala = False
        self.setWindowTitle("Zbiorniki projekt")
        self.zbiornik = Zbiornik(600, 550) #wymiary wysokosc:150 szerokosc: 150
        self.piec = Piec(200,300) #wymiary wysokosc: 500 szerokosc: 250
        self.hopper = Hopper(5,400) #wymiary wyokosc:200 szerokosc: 200
        self.rura_pionowa = Rura(80, 600, 80, 630, "NIE")
        self.rura = Rura(600, 675, 450, 675, "NIE")
        self.kolanko1 = Kolanko(400, 600, 100, kierunek="LD",czy_logiczny= "TAK",kolor="NORMALNY")
        self.kolanko2 = Kolanko(80, 510,240, kierunek="LD", czy_logiczny="NIE",kolor="NORMALNY")
        self.kolanko3 = Kolanko(325, 325, 100, kierunek="PG",czy_logiczny= "TAK",kolor="NORMALNY")
        self.kolanko4 = Kolanko(325, 325, 100, kierunek="LG",czy_logiczny= "TAK",kolor="NORMALNY")
        self.kolanko5 = Kolanko(250, 325, 100, kierunek="PD",czy_logiczny= "TAK",kolor="NORMALNY")
        self.kolanko6 = Kolanko(250, 325, 100, kierunek="LD",czy_logiczny= "TAK",kolor="NORMALNY")
        self.rura1 = Rura(400,650,400,375, "NIE")
        self.rura2 = Rura(250,375,250,150,"NIE")
        self.kolanko7 = Kolanko(250,100,100, kierunek="LG",kolor="NORMALNY")
        self.pomieszczenie_pradnicy = PomieszczeniePradnicy(300,75)
        self.pompa = Pompa(500,657,60)
        self.pradnica = Pradnica(337, 112)
        self.rura3 = Rura(375,100,500,100,"NIE")
        self.Skraplanie_pary = Skraplanie_pary(500,50)#szerokosc:200 wysokosc:200
        self.kolanko8 = Kolanko(550,0,100,kierunek="LD",czy_logiczny= "TAK",kolor="dadsa")
        self.kolanko9 = Kolanko(550, 0, 100, kierunek="PD",czy_logiczny= "TAK",kolor="dsadas")
        self.rura4 = Rura(700,225,900,225,"TAK","LEWA")
        self.zbiornik_retencyjny = Zbiornik_Retencyjny(900,225)#szerooksc:200 wysokosc:275
        self.zawor1 = Zawor(800,235)
        self.rura5 = Rura(900,400,715,400,"TAK", "PRAWA")
        self.kolanko10 = Kolanko(665,400, 100,kierunek="LG",czy_logiczny= "TAK",kolor="NORMALNY")
        self.zawor2 = Zawor(807,410)
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
        self.pradnica.draw(painter)
        self.pompa.draw(painter)
        self.Skraplanie_pary.draw(painter)
        self.rura3.draw(painter)
        self.kolanko8.draw(painter)
        self.kolanko9.draw(painter)
        self.rura4.draw(painter)
        self.zbiornik_retencyjny.draw(painter)
        self.zawor1.draw(painter)
        self.rura5.draw(painter)
        self.kolanko10.draw(painter)
        self.zawor2.draw(painter)
        for p in self.czasteczki_pary:
            painter.setPen(QPen(QColor(220, 220, 220), 3))
            painter.drawPoint(int(p[0]), int(p[1]))

    def aktualizuj_wode(self):
        self.zarzadzaj_trybem_auto()
        self.logika_obiegu_wtornego()
        self.zbiornik.dolej()

        roznica = self.piec.doplyw_powietrza - self.moc_plynna
        self.moc_plynna += roznica * 0.02
        woda = self.suma_wody

        if self.zbiornik.napelnia_sie:
            if self.suma_wody < 1000:
                self.suma_wody += self.zbiornik.krok_napelniania
                self.zbiornik.struga_jest = True
            else:
                self.suma_wody = 1000#jesli pelny
                self.zbiornik.napelnia_sie = False
                self.zbiornik.struga_jest = False
        else:
            self.zbiornik.struga_jest = False

        #zmiana wody w pare
        krok_obiegu = 0.15
        if self.pompa.czy_wlaczona and woda > 0:
            #jesli piec sie grzeje to woda znika
            if self.piec.licznik_czasu > 0:
                self.suma_wody = max(0, self.suma_wody - krok_obiegu)

            #napelnianie rur
            if woda > 10:
                if self.rura1.poziom_wody < 1.0:
                    self.rura1.poziom_wody += 0.01
                elif self.kolanko3.poziom_wody < 1.0:
                    self.kolanko3.poziom_wody += 0.01
                elif self.kolanko4.poziom_wody < 1.0:
                    self.kolanko4.poziom_wody += 0.01
                elif self.kolanko5.poziom_wody < 1.0:
                    self.kolanko5.poziom_wody += 0.01
                elif self.kolanko6.poziom_wody < 1.0:
                    self.kolanko6.poziom_wody += 0.01
        else:
            #jak wylaczymy pompe to woda splywa
            self.rura1.poziom_wody = max(0, self.rura1.poziom_wody - 0.02)
            self.kolanko3.poziom_wody = max(0, self.kolanko3.poziom_wody - 0.02)
            self.kolanko4.poziom_wody = max(0, self.kolanko4.poziom_wody - 0.02)
            self.kolanko5.poziom_wody = max(0, self.kolanko5.poziom_wody - 0.02)
            self.kolanko6.poziom_wody = max(0, self.kolanko6.poziom_wody - 0.02)

        if self.suma_wody > 1000:
            self.suma_wody = 1000

        woda = self.suma_wody

        #wizualizacja poziomow wody
        self.rura.poziom_wody = min(1.0, woda / 25.0)
        self.kolanko1.poziom_wody = min(1.0, woda / 50.0)
        self.zbiornik.objetosc_teraz = min(self.zbiornik.maksymalna_objetosc, woda)

        self.hopper.animuj_klape()
        if self.Skraplanie_pary.czy_schladza:
            if self.kolanko8.poziom_wody < 1.0: self.kolanko8.poziom_wody += 0.02
            if self.kolanko9.poziom_wody < 1.0: self.kolanko9.poziom_wody += 0.02
        else:
            self.kolanko8.poziom_wody = max(0, self.kolanko8.poziom_wody - 0.02)
            self.kolanko9.poziom_wody = max(0, self.kolanko9.poziom_wody - 0.02)

        for kulka in self.hopper.lista_wegielkow:
            if 200 <= kulka[0] <= 400 and kulka[1] >= 790:
                self.piec.licznik_czasu += 7000#zmienic na mniej
                break

        self.zarzadzanie_para()
        self.obrot_wirnika()
        self.pradnica.aktualizuj_obrot()
        self.hopper.animuj_wegiel()
        self.update()

    def zarzadzanie_para(self):
        import random
        if self.piec.licznik_czasu > 0 and self.kolanko6.poziom_wody > 0.1:#sprawdzamy czy piec grzeje i jest woda
            if self.licznik_opoznienia < 300: #opoznienie kolo 3 skund
                self.licznik_opoznienia += 1
        else:
            if self.licznik_opoznienia > 0:#piec zgasl
                self.licznik_opoznienia -= 1

        if self.licznik_opoznienia >= 300:
            self.akumulator_pary += self.moc_plynna

            # Wyciągamy cząsteczki z akumulatora (pętla while obsłuży nawet dużą produkcję)
            while self.akumulator_pary >= 100.0:
                if len(self.czasteczki_pary) < 750:
                    self.czasteczki_pary.append([262 + random.randint(-8, 8), 375])
                    self.suma_wody = max(0, self.suma_wody - 0.2)
                self.akumulator_pary -= 100.0
#self.rura2 = Rura(250,375,250,150,"TAK")

        for p in list(self.czasteczki_pary):
            if p[0] > 600:
                self.Skraplanie_pary.para_w_srodku.append(p)
                if p in self.czasteczki_pary:
                    self.czasteczki_pary.remove(p)
                continue

            if p[1] > 150:
                p[1] -= 1.0
                drganie = p[0]+random.uniform(-0.5, 0.5)
                if 250<p[0]+drganie<275:
                    p[0]+=drganie
            elif 110 < p[1] <= 150:
                p[1] -= 1.0
                p[0] += 0.6
            else:
                p[0] += 1.0
                dy = random.uniform(-2, 10)
                if 90 < p[1] + dy < 125:
                    p[1] += dy
        self.Skraplanie_pary.logika_skraplania()

    def logika_obiegu_wtornego(self):
        predkosc_transferu =0.25
        czy_jest_miejsce = self.suma_wody < 3000#sprawdzamy czy zbiornik pierwszy jest pelny
        #stosunek poziomu wody do jej wysokosci
        nowy_poziom = self.Skraplanie_pary.poziom_wody / 25.0
        #gdy w skaplaczu ubywa wody to w rurze tez
        self.rura4.poziom_wody = nowy_poziom
        if self.rura4.poziom_wody > 1.0:
            self.rura4.poziom_wody = 1.0
        elif self.rura4.poziom_wody < 0.0:
            self.rura4.poziom_wody = 0.0

        #przelewanie zaworu???? to jak dziala zawor po prostu
        if self.zawor1.czy_otwarty:
            self.rura4.ustaw_zawor(False)
            ile_miejsca_zostalo_kurde_faja = self.zbiornik_retencyjny.poziom_wody < self.zbiornik_retencyjny.wysokosc
            if self.Skraplanie_pary.poziom_wody > 0 and ile_miejsca_zostalo_kurde_faja:
                self.Skraplanie_pary.poziom_wody -= predkosc_transferu#zabieramy wode ze skraplaca
                self.zbiornik_retencyjny.poziom_wody += predkosc_transferu#dodajemy ja do zbiornika retencyjnego
        else:
            self.rura4.ustaw_zawor(True)

        #tak samo dla rury 5 i zbiornika retencyjnego
        poziom_rury5 = self.zbiornik_retencyjny.poziom_wody / 25.0
        self.rura5.poziom_wody = poziom_rury5

        if self.rura5.poziom_wody > 1.0:
            self.rura5.poziom_wody = 1.0
        elif self.rura5.poziom_wody < 0.0:
            self.rura5.poziom_wody = 0.0

        #przelewanie przez zawor2
        if self.zawor2.czy_otwarty:
            self.rura5.ustaw_zawor(False)
            if self.zbiornik_retencyjny.poziom_wody >= 1.0:
                self.zbiornik_retencyjny.poziom_wody -= predkosc_transferu
                if self.kolanko10.poziom_wody < 1.0:
                    self.kolanko10.poziom_wody += 0.5
                self.zbiornik.struga2_jest = True
                self.suma_wody += 0.7
            elif self.kolanko10.poziom_wody > 0:#jesli woda ucieka ze zbiornika i rur to z kolanka tez
                self.kolanko10.poziom_wody -= 0.02
                self.zbiornik.struga2_jest = True
                self.suma_wody += 0.7
            else:
                self.zbiornik.struga2_jest = False
        else:
            if not czy_jest_miejsce:
                self.zawor2.czy_otwarty = False#automatyczne zamkniecie zaworu gdy zbiornik 1 jest pelny
            self.rura5.ustaw_zawor(True)#zawor zamkniety
            if self.kolanko10.poziom_wody >0:#wylewanie wody z kolanka
                self.kolanko10.poziom_wody -= 0.01
                self.zbiornik.struga2_jest = True
                self.suma_wody += 0.7
            else:
                self.zbiornik.struga2_jest = False

    def obrot_wirnika(self):
        ile_pary = sum(1 for p in self.czasteczki_pary if 310 < p[0] < 380)#ilosc pary w wirniku
        cel = (ile_pary / 50.0) * 20.0   #obliczenie docelowej predkosci
        self.pradnica.predkosc_obrotu += (cel - self.pradnica.predkosc_obrotu) * 0.01 #wygladzanie ruchu wirnika
        v_surowe = self.pradnica.predkosc_obrotu * 6.5#wygladzanie napiecia
        self.napiecie_wygladzone += (v_surowe - self.napiecie_wygladzone) * 0.05#wyslanie czystego wyniku do pradnicy
        self.pradnica.generowany_prad = self.napiecie_wygladzone

    def zarzadzaj_trybem_auto(self):
        if self.regulator_aktywny:
            if self.suma_wody >= 1000:
                self.pompa_wystartowala = True #pierwszy start pompy dopiero przy pelnym zbiorniku

            if self.pompa_wystartowala:#jesli byl juz pierwszy start to pompa i osprzet dzialaja non stop
                self.pompa.czy_wlaczona = True
                self.Skraplanie_pary.czy_schladza = True
                self.zawor1.czy_otwarty = True
                self.hopper.otwiera_sie = False
                self.hopper.zamyka_sie = True

                if not self.pierwszy_wegiel_wpadl:
                    self.hopper.dodaj_wegiel()
                    self.pierwszy_wegiel_wpadl = True
                    self.licznik_klatek_auto = 0
                else:
                    self.licznik_klatek_auto += 1
                    if self.licznik_klatek_auto >= 500:
                        self.hopper.dodaj_wegiel()
                        self.licznik_klatek_auto = 0

            if self.suma_wody < 300:# logika uzupelniania wody
                if self.zbiornik_retencyjny.poziom_wody > 0:  #najpierw bierzemy ze zbiornika retencyjnego
                    self.zawor2.czy_otwarty = True
                    self.zbiornik.napelnia_sie = False
                    self.zbiornik.struga_jest = False
                else: #gdy retencyjny pusty to dolewamy z zewnatrz
                    self.zawor2.czy_otwarty = False
                    self.zbiornik.napelnia_sie = True
                    self.zbiornik.struga_jest = True

            if self.suma_wody >= 1000: #wylaczenie lania gdy pelny
                self.zbiornik.napelnia_sie = False
                self.zbiornik.struga_jest = False
                self.zawor2.czy_otwarty = False

        else:
            self.pierwszy_wegiel_wpadl = False
            self.pompa_wystartowala = False
#sterowanie
class OknoSterowania(QWidget):
    def __init__(self, zbiornik, okno_wiz):
        super().__init__()
        #zmienne stanu
        self.v_zadane = 230.0
        self.licznik_czekania = 0
        self.poprzedni_blad = 0.0
        self.regulator_aktywny = False
        self.licznik_klatek_wykresu = 0
        self.licznik_klatek_auto = 0
        self.zbiornik = zbiornik
        self.okno_wiz = okno_wiz
        self.setWindowTitle("Sterowanie")
        self.resize(600, 800)


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

        # sterowanie chlodzeniem
        self.chlodzenie_box = QGroupBox("Sterowanie chlodzeniem")
        chlodzenie_layout = QHBoxLayout()  # poziomo przyciski
        self.btn_ch_on = QPushButton("WŁĄCZ CHŁODZENIE")
        self.btn_ch_on.setStyleSheet("background-color: green;")
        self.btn_ch_off= QPushButton("WYŁĄCZ CHŁODZENIE")
        self.btn_ch_off.setStyleSheet("background-color: red;")

        chlodzenie_layout.addWidget(self.btn_ch_on)
        chlodzenie_layout.addWidget(self.btn_ch_off)

        self.chlodzenie_box.setLayout(chlodzenie_layout)
        # Dodanie do głównego układu
        budowa_sterowania.addWidget(self.chlodzenie_box)
        #laczenie przyciskow
        self.btn_ch_on.clicked.connect(self.wlacz_chlodzenie)
        self.btn_ch_off.clicked.connect(self.wylacz_chlodzenie)
        # sterowanie zaworem1
        self.zawor_box = QGroupBox("Sterowanie zaworem 1")
        zawor_layout = QHBoxLayout()  # poziomo przyciski
        self.btn_za_on = QPushButton("OTWORZ ZAWOR")
        self.btn_za_on.setStyleSheet("background-color: green;")
        self.btn_za_off= QPushButton("ZAMKNIJ ZAWOR")
        self.btn_za_off.setStyleSheet("background-color: red;")

        zawor_layout.addWidget(self.btn_za_on)
        zawor_layout.addWidget(self.btn_za_off)

        self.zawor_box.setLayout(zawor_layout)
        # Dodanie do głównego układu
        budowa_sterowania.addWidget(self.zawor_box)
        #laczenie przyciskow
        self.btn_za_on.clicked.connect(self.otworz_zawor_1)
        self.btn_za_off.clicked.connect(self.zamknij_zawor_1)

        # sterowanie zaworem2
        self.zawor2_box = QGroupBox("Sterowanie zaworem 2")
        zawor2_layout = QHBoxLayout()  # poziomo przyciski
        self.btn_za2_on = QPushButton("OTWORZ ZAWOR")
        self.btn_za2_on.setStyleSheet("background-color: green;")
        self.btn_za2_off = QPushButton("ZAMKNIJ ZAWOR")
        self.btn_za2_off.setStyleSheet("background-color: red;")

        zawor2_layout.addWidget(self.btn_za2_on)
        zawor2_layout.addWidget(self.btn_za2_off)

        self.zawor2_box.setLayout(zawor2_layout)
        # Dodanie do głównego układu
        budowa_sterowania.addWidget(self.zawor2_box)
        # laczenie przyciskow
        self.btn_za2_on.clicked.connect(self.otworz_zawor_2)
        self.btn_za2_off.clicked.connect(self.zamknij_zawor_2)
        #PID
        self.regulator_box = QGroupBox("Automatyczny Regulator Napięcia")
        regulator_layout = QVBoxLayout()

        self.label_v_zadane = QLabel("Napięcie zadane: 230 V")
        self.label_v_zadane.setStyleSheet("font-weight: bold; color: red;")
        regulator_layout.addWidget(self.label_v_zadane)

        self.suwak_v_zadane = QSlider(Qt.Horizontal)
        self.suwak_v_zadane.setRange(0, 250)
        self.suwak_v_zadane.setValue(230)
        self.suwak_v_zadane.valueChanged.connect(self.aktualizuj_etykiete_v)
        regulator_layout.addWidget(self.suwak_v_zadane)

        przyciski_reg_layout = QHBoxLayout()
        self.btn_reg_on = QPushButton("AUTO ON")
        self.btn_reg_on.setStyleSheet("background-color: green; color: white;")
        self.btn_reg_off = QPushButton("AUTO OFF")
        self.btn_reg_off.setStyleSheet("background-color: red; color: white;")

        przyciski_reg_layout.addWidget(self.btn_reg_on)
        przyciski_reg_layout.addWidget(self.btn_reg_off)
        regulator_layout.addLayout(przyciski_reg_layout)

        self.regulator_box.setLayout(regulator_layout)
        budowa_sterowania.addWidget(self.regulator_box)
        #laczenie kliczkow
        self.btn_reg_on.clicked.connect(self.wlacz_regulator)
        self.btn_reg_off.clicked.connect(self.wylacz_regulator)

        #wykres przerobiony kod z zajec
        self.historia_len = 100
        self.x_h = list(range(self.historia_len))
        self.y_zadane_h = [self.v_zadane] * self.historia_len
        self.y_gora_h = [self.v_zadane + 5] * self.historia_len
        self.y_dol_h = [self.v_zadane - 5] * self.historia_len
        self.y_v_aktualne_h = [0.0] * self.historia_len

        self.graph = pg.PlotWidget()
        self.graph.setBackground('w')
        self.graph.showGrid(x=False, y=False)
        self.graph.setYRange(0, 260)
        self.graph.setMinimumHeight(200)  # Rezerwuje miejsce na dole

        self.line_zadana = self.graph.plot(self.x_h, self.y_zadane_h, pen=pg.mkPen('b', width=2))
        self.line_gora = self.graph.plot(self.x_h, self.y_gora_h, pen=pg.mkPen('r', style=Qt.DashLine))
        self.line_dol = self.graph.plot(self.x_h, self.y_dol_h, pen=pg.mkPen('r', style=Qt.DashLine))
        self.line_aktualne = self.graph.plot(self.x_h, self.y_v_aktualne_h, pen=pg.mkPen('orange', width=2))
        budowa_sterowania.addWidget(self.graph)


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
        self.oblicz_regulator()
        self.licznik_klatek_wykresu +=1
        if self.licznik_klatek_wykresu >= 60:
            self.aktualizuj_wykres()
            self.licznik_klatek_wykresu = 0

        procent = (self.zbiornik.poziomPierwszegoZbiornika() / self.zbiornik.maksymalna_objetosc * 100)
        self.label_procent.setText(f"Poziom: {procent:.1f} %")
        if procent == 100:
            self.btn_za2_on.setEnabled(False)
            self.btn_za2_on.setText("ZABLOKOWANE (PEŁNY)")
            self.btn_za2_on.setStyleSheet("background-color: #555555; color: white;")

            self.okno_wiz.zawor2.czy_otwarty = False#jesli zawor byl otwarty tedy gdy mozna przelac zbiornik to go wylacz
        else:
            self.btn_za2_on.setEnabled(True)
            self.btn_za2_on.setText("OTWÓRZ ZAWÓR")
            self.btn_za2_on.setStyleSheet("background-color: green;")
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

    def wlacz_chlodzenie(self):
        self.okno_wiz.Skraplanie_pary.czy_schladza = True

    def wylacz_chlodzenie(self):
        self.okno_wiz.Skraplanie_pary.czy_schladza = False
    #sterowanie zaworami
    def otworz_zawor_1(self):
        self.okno_wiz.zawor1.czy_otwarty = True

    def zamknij_zawor_1(self):
        self.okno_wiz.zawor1.czy_otwarty = False

    def otworz_zawor_2(self):
        self.okno_wiz.zawor2.czy_otwarty = True

    def zamknij_zawor_2(self):
            self.okno_wiz.zawor2.czy_otwarty = False

    def wlacz_regulator(self):
        self.regulator_aktywny = True
        self.okno_wiz.regulator_aktywny = True
        self.label_v_zadane.setStyleSheet("font-weight: bold; color: green;")

    def wylacz_regulator(self):
        self.regulator_aktywny = False
        self.okno_wiz.regulator_aktywny = False
        self.label_v_zadane.setStyleSheet("font-weight: bold; color: red;")

    def oblicz_regulator(self):
        if not self.regulator_aktywny:
            return

        self.licznik_czekania += 1  #zwiekszamy licznik klatek
        if self.licznik_czekania < 125:  #sprawdzamy czy minelo wystarczajaco duzo czasu
            return
        self.licznik_czekania = 0  #zerujemy licznik przed nastepnym cyklem

        v_teraz = self.okno_wiz.pradnica.generowany_prad  #pobieramy aktualne napiecie
        powietrze_teraz = self.okno_wiz.piec.doplyw_powietrza  #pobieramy obecny stan suwaka
        roznica = self.v_zadane - v_teraz  #obliczamy roznice od celu

        if abs(roznica) <= 5:  #jesli blad jest maly
            return  #nic nie robimy

        if roznica > 50:  #jesli brakuje bardzo duzo napiecia
            nowe_powietrze = powietrze_teraz + 10  #robimy wielki skok o 10 procent
        elif roznica > 0:  #jesli brakuje tylko troche
            nowe_powietrze = powietrze_teraz + 1  #robimy maly krok o 1 procent
        elif roznica < -50:  #jesli napiecie jest o wiele za duze
            nowe_powietrze = powietrze_teraz - 10  #robimy wielki skok w dol o 10 procent
        else:  #jesli jestesmy powyzej celu ale blisko
            nowe_powietrze = powietrze_teraz - 1  #robimy maly krok w dol o 1 procent

        if nowe_powietrze > 100: #sprawdzamy czy nie przekraczamy limitu gornego
            nowe_powietrze = 100
        if nowe_powietrze < 0: #sprawdzamy czy nie spadamy ponizej zera
            nowe_powietrze = 0

        self.okno_wiz.piec.doplyw_powietrza = nowe_powietrze  # ustawiamy nowa wartosc w symulacji
        self.suwak_powietrza.setValue(int(nowe_powietrze))  # przesuwamy suwak na ekranie
        self.label_powietrze.setText(f"Doplyw: {int(nowe_powietrze)}%")  # aktualizujemy tekst etykiety

    def aktualizuj_etykiete_v(self, wartosc):
        self.v_zadane = wartosc
        self.label_v_zadane.setText(f"Napięcie zadane: {wartosc} V")
        self.calka = 0  #resetujemy pamiec regulatora przy zmianie celu
        self.poprzedni_blad = 0

    def aktualizuj_wykres(self):
        v_teraz = self.okno_wiz.pradnica.generowany_prad #pobieramy aktualne napiecie z pradnicy
        #usuwamy najstarsza wartosc z poczatku kazdej listy
        self.y_zadane_h.pop(0)
        self.y_gora_h.pop(0)
        self.y_dol_h.pop(0)
        self.y_v_aktualne_h.pop(0)
        # dodajemy nowa wartosc na koniec kazdej listy
        self.y_zadane_h.append(self.v_zadane)
        self.y_gora_h.append(self.v_zadane + 5)
        self.y_dol_h.append(self.v_zadane - 5)
        self.y_v_aktualne_h.append(v_teraz)
        # wysylamy nowe dane do linii na wykresie
        self.line_zadana.setData(self.x_h, self.y_zadane_h)
        self.line_gora.setData(self.x_h, self.y_gora_h)
        self.line_dol.setData(self.x_h, self.y_dol_h)
        self.line_aktualne.setData(self.x_h, self.y_v_aktualne_h)

app = QApplication(sys.argv)
okno_wiz = OknoZRysunkami()
okno_ctrl = OknoSterowania(okno_wiz.zbiornik, okno_wiz)
okno_wiz.timer.timeout.connect(okno_ctrl.update_status)#polaczenie timera z funkcja procentow w oknie sterowania
okno_wiz.show()
okno_ctrl.show()
sys.exit(app.exec_())

