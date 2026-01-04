import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QColor
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
        self.krok_napelniania =0.2
        self.struga_y = self.y +60 #struga zaczyna sie nad zbiornikiem
        self.struga_szerokosc = 10
        self.struga_wysokosc = 40
        self.struga_jest = False

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

        #rysowanie zbiornika
        path.moveTo(LG)
        path.lineTo(WLD)
        path.lineTo(WLG)
        path.lineTo(WPG)
        path.lineTo(WPD)
        path.lineTo(PG)
        path.lineTo(PD)
        path.lineTo(LD)
        path.closeSubpath()


        #rysowanie cieczy z maskowaniem (z zajec)
        if self.poziom_zapelnienia > 0:
            painter.save()
            painter.setClipPath(path) #maskowanie do kształtu zbiornika
            liquid_height_px = self.wysokosc * (self.poziom_zapelnienia / self.max_poziom) #przeliczenie na piksele
            rect_liquid = QRectF(
                self.x,
                self.y + self.wysokosc - liquid_height_px,
                self.szerokosc,
                liquid_height_px
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
            poziom_wody_y = self.y + self.wysokosc - (self.wysokosc * (self.poziom_zapelnienia / self.max_poziom))
            #wysokosc strugi to odleglosc od startu do wody
            aktualna_wysokosc_strugi = poziom_wody_y - struga_y
            #rysowanie strugi
            rect_struga = QRectF(struga_x, struga_y, self.struga_szerokosc, aktualna_wysokosc_strugi)
            painter.fillRect(rect_struga, QColor(0, 120, 255, 180))

    def dolej(self):
        if self.napelnia_sie: #tylko jeśli tryb napełniania jest włączony
            self.poziom_zapelnienia += self.krok_napelniania
            #ograniczamy do maksymalnej wysokości
            if self.poziom_zapelnienia > self.max_poziom:
                self.poziom_zapelnienia = self.max_poziom

        if self.poziom_zapelnienia == self.wysokosc:
            self.struga_jest = False

    def poziomPierwszegoZbiornika(self):#getter obencego poziomu cieczy
        return self.poziom_zapelnienia


class Piec:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.poziom_wegla = 0
        self.wysokosc = 500
        self.szerokosc = 200
        self.max_poziom_wegla = 50
        self.poziom_zapelnienia = 0
        self.czy_sie_napelnia = False
        self.otwiera_sie = False


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

        #budowanie ksztaltu pieca
        path.moveTo(RHG)
        path.lineTo(LG)
        path.lineTo(PG)
        path.lineTo(PD)
        path.lineTo(LD)
        path.lineTo(RHD)


        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(Qt.darkGray, 4))
        painter.drawPath(path)


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
        self.lista_wegielkow = [] #lista ma x,y
        self.predkosc_spadania = 0.5

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
                kulka[1] += self.predkosc_spadania

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

    def dodaj_wegiel(self):
        import random #losowo generujemy kulke w przedziale od prawej krawedzi hoppera do lewej krawedzi hoppera z marginesem zeby na bokach sie nie zbieralo duzo wegla
        lewa_granica = self.x +40
        prawa_granica = self.x + self.szerokosc -40
        start_x = random.uniform(lewa_granica, prawa_granica)#losowane pozycji
        self.lista_wegielkow.append([start_x, self.y - 50, False])#dodawanie wegielka do listy

class Rura:
    def __init__(self, x_poczatkowe, y_poczatkowe, x_koncowe, y_koncowe, szerokosc=25):
        self.x_poczatkowe= x_poczatkowe
        self.y_poczatkowe = y_poczatkowe
        self.x_koncowe = x_koncowe
        self.y_koncowe = y_koncowe
        self.szerokosc = szerokosc

    def draw(self,painter):
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        if self.x_poczatkowe == self.x_koncowe:#rura pionowa
            LG = QPointF(self.x_poczatkowe, self.y_poczatkowe)#lewy gorny rog rury
            PG = QPointF(self.x_poczatkowe + self.szerokosc, self.y_poczatkowe)#prawy gorny rog rury
            LD = QPointF(self.x_koncowe, self.y_koncowe)#lewy dolny rog rury
            PD = QPointF(self.x_koncowe + self.szerokosc, self.y_koncowe)#prawy doly rog rury
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
            # rysowanie rury
            path.moveTo(LG)
            path.lineTo(PG)
            path.moveTo(PD)
            path.lineTo(LD)
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(Qt.darkGray, 4))
            painter.drawPath(path)

class OknoZRysunkami(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("Zbiorniki projekt")
        self.zbiornik = Zbiornik(550, 550) #wymiary wysokosc:150 szerokosc: 150
        self.piec = Piec(200,300) #wymiary wysokosc: 500 szerokosc: 200
        self.hopper = Hopper(5,400) #wymiary wyokosc:200 szerokosc: 200
        self.resize(1280, 920)
        #timer zeby sie zmienialp
        self.timer = QTimer()
        self.timer.timeout.connect(self.aktualizuj_wode)
        self.timer.start(8)#cos kolo 120 fps

    def paintEvent(self, event):
        painter = QPainter(self)
        self.zbiornik.draw(painter)
        self.piec.draw(painter)
        self.hopper.draw(painter)

    def aktualizuj_wode(self):#zmienic nazwe funckji na bardziej adekwatna pod koniec
        self.zbiornik.dolej()
        self.hopper.animuj_klape()
        self.hopper.animuj_wegiel()
        self.update()

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

        # sterowanie hopperem
        self.hopper_box = QGroupBox("Sterowanie hopperem")
        hopper_layout = QHBoxLayout()  # poziomo przyciski
        self.btn_wrzuc = QPushButton("WRZUC WEGIEL")
        self.btn_wrzuc.setStyleSheet("background-color: gray;")
        self.btn_otworz = QPushButton("OTWORZ KLAPE")
        self.btn_otworz.setStyleSheet("background-color: green;")
        self.btn_zamknij = QPushButton("ZAMKNIJ KLAPE ")
        self.btn_zamknij.setStyleSheet("background-color: red;")
        # przyciski
        hopper_layout.addWidget(self.btn_wrzuc)
        hopper_layout.addWidget(self.btn_otworz)
        hopper_layout.addWidget(self.btn_zamknij)

        self.hopper_box.setLayout(hopper_layout)
        budowa_sterowania.addWidget(self.hopper_box)  # dodajemy to co stworzylismy wczesniej do glownej kolumny
        # linkowanie przyciskow
        self.btn_otworz.clicked.connect(self.otworz_hopper)
        self.btn_zamknij.clicked.connect(self.zamknij_hopper)
        self.btn_wrzuc.clicked.connect(self.wrzuc_hopper)

    #logika przyciskow
    def start(self):
        self.zbiornik.napelnia_sie = True
        self.zbiornik.struga_jest = True

    def stop(self):
        self.zbiornik.napelnia_sie = False
        self.zbiornik.struga_jest = False

    def reset(self):
        self.zbiornik.napelnia_sie = False
        self.zbiornik.poziom_zapelnienia = 0
        self.okno_wiz.update()
        self.update_status()
        self.zbiornik.struga_jest = False

    #update % napelnienia
    def update_status(self):
        procent = (self.zbiornik.poziomPierwszegoZbiornika() / self.zbiornik.max_poziom * 100)
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

app = QApplication(sys.argv)
okno_wiz = OknoZRysunkami()
okno_ctrl = OknoSterowania(okno_wiz.zbiornik, okno_wiz)
okno_wiz.timer.timeout.connect(okno_ctrl.update_status)#polaczenie timera z funkcja procentow w oknie sterowania
okno_wiz.show()
okno_ctrl.show()
sys.exit(app.exec_())

