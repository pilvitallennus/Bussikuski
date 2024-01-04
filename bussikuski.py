import random
from tkinter import *



class Pakka:
    """
    Luokka yksinkertaisesta korttipakasta. Metodien avulla voidaan sekoittaa
    pakka, voidaan nostaa kortti ja tarkistaa korttien määrä pakassa.
    Korttipakan luonti tapahtuu automaattisesti kutsumalla Pakka() .
    """

    def __init__(self):
        #luodaan korttipakka, eli tyhjä lista korteille
        self.__kortit = list()

        #kaikki mahdolliset arvot ja maat
        arvot = ("A", "K", "Q", "J",
                "10", "9", "8", "7",
                "6", "5", "4", "3", "2")

        maat = ("♦", "♣", "♥", "♠")

        #käydään läpi jokainen arvo-maa kombinaatio ja lisätään ne kortteihin
        for arvo in arvot:
            for maa in maat:
                self.__kortit.append(f"{arvo}-{maa}")


    def sekoitus(self):
        """
        "Sekoittaa" korttipakan
        """
        random.shuffle(self.__kortit)

    def korttien_määrä(self):
        """
        Palauttaa pakassa jäljellä olevien korttien lukumäärän
        :return int(), korttien lukumäärä pakassa
        """
        return len(self.__kortit)

    def nosta_kortti(self):
        """
        Metodi yhden kortin nostamista varten, poistaa myös kortin listasta
        :return: str(), palauttaa kortin
        """
        kortti = self.__kortit.pop()
        return kortti

    def nollaa_pakka(self):
        """
        Tyhjentää nykyisen pakan
        """
        self.__kortit.clear()



class Käyttöliittymä:
    def __init__(self, pakka=Pakka()):

        self.__pääikkuna = Tk()                 #pääikkuna
        self.__pakka = pakka                    #korttipakka

        #pääikkunan asetukset
        self.__pääikkuna.title("Bussikuski")
        self.__pääikkuna.geometry("1000x800")
        self.__pääikkuna.configure(background='black')


        #luodaan Frame pöydälle ja pelaajien korteille
        self.__pöytä = Frame(self.__pääikkuna, bg='brown', relief="raised")
        self.__pöytä.place(x=225, y=175, width=485, height=500)


        #asetetaan näytölle myöhemmin
        self.__pelaajatframe = Frame(self.__pääikkuna, bg="CadetBlue3",
                                                        relief="raised")

        #luodaan erilaisia tunnisteita
        self.__idtausta= list()          #taustojen indeksointiin
        self.__idkortti = list()         #korttien indeksointiin

        self.__indeksi = ""              #nostetun kortin indeksi
        self.__nostettu_arvo = ""        #nostetun kortin arvo

        self.__käännetyt = list()        #indeksit joita ei ole vielä korvattu
        self.__käännetyt_arvot = list()  #arvot joita ei ole vielä korvattu

        self.__laskuri = 0               #laskuri bussin ajoon


        #luodaan erilaisia nappeja ohjelmaan
        self.__aloitusnappi = Button(self.__pääikkuna, text="Aloita alusta",
                                                command=self.aloita_alusta)

        self.__lopetusnappi = Button(self.__pääikkuna, text="Lopeta",
                                                command=self.lopeta)

        self.__jakonappi = Button(self.__pääikkuna,
                                        text="Pelaajien lukumäärä (max 7): ",
                                                command=self.jaa_kortit)

        self.__pyramidinappi = Button(self.__pääikkuna, text="Aloita peli",
                                      command=self.kortti_pyramidi, font="40")

        self.__bussikuskinappi = Button(self.__pääikkuna, text="Bussikuski",
                                        command=self.bussikuski, bg="blue",
                                        font="40")

        self.__sääntönappi = Button(self.__pääikkuna, text="Näytä säännöt",
                                     command=self.säännöt)



        #luodaan syöttökenttä pelaajien lukumäärälle, sekä laskuri
        self.__pelaajat_lkm = Entry(self.__pääikkuna, relief="raised",
                                                            justify=CENTER)

        self.__bussi_laskuri = Label(self.__pääikkuna, text=f"Nostetut: "
                                f"{self.__laskuri}", relief='raised', font=20)


        #luodaan valitsin pelaajat_lkm entryn lukitsemista varten
        self.__muuttuja = IntVar()
        self.__pelaajat_lukitsin = Checkbutton(self.__pääikkuna,text="Lukitse",
                                               relief="raised",
                                               variable=self.__muuttuja,
                                               onvalue=1, offvalue=0,
                                               command=self.lukitse)

        #nappien sijoittelu ikkunaan
        self.__aloitusnappi.place(x=10, y=10, width=100, height=30)
        self.__lopetusnappi.place(x=110, y=10, width=100, height=30)
        self.__jakonappi.place(x=10, y=40, width=200, height=30)
        self.__bussikuskinappi.place(x=10, y=175, width=200, height=60)
        self.__sääntönappi.place(x=10, y=500, width=100, height=30)


        self.__pelaajat_lkm.place(x=10, y=70, width=100, height=30)


        #laskurin ja pelaajatframen piilotus
        self.__bussi_laskuri.place_forget() #näytetään vasta kun "bg"="blue"
        self.__pelaajatframe.place_forget() #näytetään käsien jaon yhteydessä


        #käynnistetään käyttöliittymä
        self.__pääikkuna.mainloop()



    #metodit pelaajan käteen liittyen

    def jaa_kortit(self):
        """
        Hakee ensin pelaajien lukumäärän entrystä pelaajat_lkm.
        Jos pelaajien määrä on 1-7, nostaa ja tulostaa näytölle jokaiselle
        pelaajalle 5 korttia, jotka poistuvat klikkaamalla. Kortit tulostetaan
        Frameen pelaajatframe, jotta ne voidaan tarvittaessa poistaa kerralla.

        Poistaminen toteutetaan asettamalla napeille komento "poista_kortti".
        Tämä onnistui vain käyttämällä anonyymiä lambda-funktiota.
        """

        try:
            #haetaan pelaajien lukumäärä Entrystä pelaajat_lkm
            pelaajia = self.__pelaajat_lkm.get()

            #suoritetaan jako vasta, kun pelaajien lukumäärä 1-7
            if int(pelaajia) in [1,2,3,4,5,6,7]:

                #jakonappi toimii seuraavan kerran, kun aloitetaan alusta
                self.__jakonappi.configure(text="Kortit jaettu",
                                           command=lambda: None)

                #asetetaan nappi, joka jakaa korttipyramidin
                self.__pyramidinappi.configure(command=self.kortti_pyramidi)
                self.__pyramidinappi.place(x=10, y=115, width=200, height=60)


                #asetetaan lukitsimen ja framen näytölle
                self.__pelaajat_lukitsin.place(x=110, y=70, width=100,
                                                    height=30)

                self.__pelaajatframe.place(x=725, y=40, width=250, height=710)


                for pelaaja in range(int(pelaajia)):

                    #luodaa tyhjä entry jokaisen korttirivin ylle
                    nimi_kenttä = Entry(self.__pelaajatframe, width=100)
                    nimi_kenttä.place(x=0, y=pelaaja*100)

                    for x in range(5):
                        #nostetaan kortti pakasta, kortti muotoa <arvo>-<maa>
                        self.__pakka.sekoitus()
                        nosto = self.__pakka.nosta_kortti()
                        arvo, maa = nosto.split("-")

                        punaiset = ["♦", "♥"]

                        if maa in punaiset:
                            käsi_kortti = Button(self.__pelaajatframe,
                                           text=f"{arvo} {maa}",
                                           width=5, height=5, relief="solid",
                                           borderwidth=2, foreground="red")

                            #määritetään napille toiminto
                            käsi_kortti.configure(command=lambda
                                    btn=käsi_kortti: self.poista_kortti(btn))


                        else:
                            käsi_kortti = Button(self.__pelaajatframe,
                                           text=f"{arvo} {maa}",
                                           width=5, height=5, relief="solid",
                                           borderwidth=2, foreground="black")

                            # määritetään napille toiminto
                            käsi_kortti.configure(command=lambda
                                    btn=käsi_kortti:self.poista_kortti(btn))

                        käsi_kortti.place(x=1 + x*50, y=20 + pelaaja*100)



            #erilaiset virhetilanteet
            elif int(pelaajia) > 7:
                self.__jakonappi.configure(text="Pelaajia voi olla enintään 7")
                return

            else:
                self.__jakonappi.configure(text="Määrä ei ole kokonaisluku "
                                                "välillä 1-7")
                return

        except ValueError:
            self.__jakonappi.configure(text="Määrä ei ole kokonaisluku "
                                                "välillä 1-7")
            return


    def poista_kortti(self, kortti):
        """
        Luodaan erillinen metodi kädessä olevien korttien poistolle. Syy tälle
        on se, ettei indeksointi häiriinny.
        :param kortti: Button(), poistettava kortti
        """
        kortti.destroy()


    def poista_kädet(self):
        """
        Poistaa jokaisen widgetin pelaajatframesta, sekä piilottaa framen.
        """

        for widget in self.__pelaajatframe.winfo_children():
            widget.destroy()

        self.__pelaajatframe.place_forget()


    def lukitse(self):
        """
        Lukitsee pelaajien määrän entryssä. Poistamalla entryn käytöstä.
        Jotta lukitus onnistuu, täytyy lukittavan arvon olla hyväksyttävä
        arvo pelaajien lukumääräksi, eli muotoa int() väliltä 1-7.
        """
        try:
            if self.__muuttuja.get() == 1:

                x = self.__pelaajat_lkm.get()   #Entryn teksti

                if int(x) in [1,2,3,4,5,6,7]:
                    self.__pelaajat_lkm.configure(state="disabled")

                else:
                    self.__pelaajat_lkm.configure(state="normal")
                    return

            else:
                #palauttaa entryn toiminnan
                self.__pelaajat_lkm.configure(state="normal")

        except ValueError:
            return

        except KeyError:
            return



    #pöydän metodit

    def kortti_pyramidi(self):
        """
        Pyramidi luodaan siten, että pohjalle asetetaan kortti Label muodossa.
        Tämän päälle asetetaan korttitausta button muodossa, joka poistuu sitä
        painamalla. Kortit ja taustat asetetaan frameen pöytä, jotta ne voidaan
        poistaa kerralla tarvittaessa. Taustat luodaan erillisellä
        metodilla tausta_pyramidi, jota kutsutaan Labeleiden luonnin jälkeen.

        Tallennetaan kortin luomisen yhteydessä listaan idkortti juuri luotu
        kortti. Tuloste on seuraavanlainen " .!frame.!label(numero) ".
        Korttitaustalle tulostetaan samanlainen tunniste ja lista, joiden
        avulla kortti ja tausta pystytään yhdistämään toisiinsa.
        """

        self.__pakka.sekoitus()
        #ei jaeta uudestaan napista, ellei peliä aloiteta alusta
        self.__pyramidinappi.configure(command=lambda:None)

        #tulostetaan kortteja kuvaavat labelit
        for n in range(5):
            for m in range(n + 1):

                #nostetaan kortti pakasta, kortti muotoa <arvo>-<maa>
                nosto = self.__pakka.nosta_kortti()
                arvo, maa = nosto.split("-")

                punaiset = ["♦", "♥"]

                if maa in punaiset:
                    kortti = Label(self.__pöytä, text=f"{arvo} {maa}",
                                   width=5, height=5, relief="solid",
                                   borderwidth=2, foreground="red")

                    self.__idkortti.append(kortti) #tunniste listaan


                else:
                    kortti = Label(self.__pöytä, text=f"{arvo} {maa}",
                                   width=5, height=5, relief="solid",
                                   borderwidth=2, foreground="black")

                    self.__idkortti.append(kortti) #tunniste listaan

                #(n,m) in 0...4   x arvoiksi tulee 220 - 265 - 310 - 355 - 400
                kortti.place(x=220 - n*45 + m*90, y=90*n + 10)

        #luodaan labeleiden päälle korttitaustat nappeina
        self.tausta_pyramidi()


    def tausta_pyramidi(self):
        """
        Napit korttipyramidin labeleiden päälle. Poistuvat painettaessa.
        Tallannetaan kortti_tausta listaan idlista. Voidaan käyttää
        painetun napin tunnistamiseen myöhemmin, kun täytyy tietää napin alta
        paljastunut kortti. Toimintaperiaate  samanlainen, selitetty tarkemmin
        kortti_pyramidissa.
        """


        for n in range(5):
            for m in range(n + 1):

                teksti=f"xXxXxXx\nxXxXxXx\nxXxXxXx\nxXxXxXx\nxXxXxXx\nxXxXxXx"

                kortti_tausta = Button(self.__pöytä, text=teksti , width=5,
                                       height=5, relief="solid", borderwidth=2,
                                       foreground="red")

                #määritellään, että komento käännä_kortti tapahtuu painaessa
                #ei jostain syystä toimi ilman lambda-funktiota
                kortti_tausta.configure(command=lambda btn=kortti_tausta:
                                                    self.käännä_kortti(btn))

                #tulostetaan täysin samoilla parametreilla, kuin kortit
                kortti_tausta.place(x=220 - n * 45 + m * 90, y=90 * n + 10)

                self.__idtausta.append(kortti_tausta) #tunniste listaan


    def käännä_kortti(self, kortti_tausta):
        """
        Poistaa luodun napin, joka esittää korttitaustaa. Korttitaustan takaa
        paljastuu generoitu kortti. Kutsuu käännetty_kortti metodia, joka
        tallentaa poistetun kortin indeksin muuttujaan self.__indeksi.

        Jos framen pöytä taustaväri on sininen, on siirrytty "bussin ajamiseen"
        jolloin if lause toteutuu ja metodi alkaa päivittämään bussi_laskuria.

        :param kortti_tausta: Button(), viittaa poistettavaan napin objektiin
        """

        self.käännetty_kortti(kortti_tausta)
        kortti_tausta.destroy()


        #jos ajetaan bussia, laskuri aktivoituu
        if self.__pöytä["bg"] == "blue":
            self.__laskuri += 2
            self.__bussi_laskuri.configure(text=self.__laskuri)


    def käännetty_kortti(self,kortti_tausta):
        """
        Selvittää mistä kohtaa pyramidia kortti on käännetty. Seuraavassa
        kappaleessa avataan, kuinka metodi toimii:

        Taustat on tallennettu listaan idtausta. Käydään ensin listaa läpi,
        kunnes löydetään arvo, joka vastaa parametrin kortti_tausta arvoa.
        Sen jälkeen kiinostaa vain ja ainoastaan taustan sijainti listassa.
        Listaa tyhjennetään siten, että kortin paikka on aina sama, kuin
        tallennetun taustan indexi listassa.
        Pyramidin taustat ja kortit muodostavat listan indekseinään:
                        0
                       1  2
                     3  4  5
                    6  7  8  9
                  10 11 12 13 14

        Tallennetaan indeksi self.__indeksi, joka kertoo aina viimeksi
        poistetun taustan indeksin.

        Metodin alapäässä on mahdollisuus saada metodi tulostamaan k0nsoliin
        samat tiedot, mitä se välittää ohjelmalle.

        :param kortti_tausta: Button(), viittaa poistettavaan napin objektiin
        """

        for tausta in self.__idtausta:
            if tausta == kortti_tausta:

                #tallennetaan taustan sijainti self.__indeksiin.
                self.__indeksi = self.__idtausta.index(tausta)

                #saadaan kortti taustan indeksin avulla listasta idkortti
                tallennettu_kortti = self.__idkortti[self.__indeksi]

                #haetaan kortissa oleva teksti
                kortin_teksti = tallennettu_kortti["text"]

                #pelin kannalta ainoastaan arvolla on väliä
                arvo, maa = kortin_teksti.split(" ")

                #päivitetään käyttöliittymän atribuuteiksi
                self.__nostettu_arvo = arvo

                #lisätään käännettyihin kortteihin
                self.__käännetyt.append(self.__indeksi)
                self.__käännetyt_arvot.append(arvo)

                """
                #tulostaa käännetyn kortin indeksin ja sisällön konsoliin
                print(f"Indeksi: {self.__indeksi}, Sisältö: {kortin_teksti}")
                
                #tulostaa konsoliin listat korteista joita ei olla korvattu
                print(f"Nostetut kortit korvaamatta: {self.__käännetyt}")
                print(f"Nostetut arvot korvaamatta: {self.__käännetyt_arvot}")
                """


    def määritä_sijainti(self, nostettu):
        """
        Selvittää kortin indeksin perusteella  n ja m arvot kortin korvaamista
        varten. n kuvaa riviä ylhäätlä ja m paikkaa vasemmalta.
        Jokaisella kortilla on molemmat arvot ja ne selvitetään rivi kerrallaan
        if-elif-else rakenteella.

        Arvot ovat erittäin tärkeät, koska alkuperäinen korttien tulostettiin
        kahdella for loopilla:
        for n in range(5):
            for m in range(n + 1):

        Indeksi listasssa:      n arvo:        m arvo:
                 0                     0              0
               1  2                    1            0   1
             3  4  5                   2           0  1  2
            6  7  8  9                 3          0  1  2  3
          10 11 12 13 14               4         0  1  2  3  4

        :param nostettu: int(), kortin indeksi listassa self.__käännetyt
        return: int(), n ja m arvot muodossa n, m
        """

        self.__indeksi = nostettu #viimeksi nostetun kortin indeksi

        #hieman törkeä mutta toimiva
        if self.__indeksi == 0:
            n = 0
            m = 0

        elif self.__indeksi in [1, 2]:
            n = 1
            if self.__indeksi == 1:
                m = 0
            else:
                m = 1

        elif self.__indeksi in [3, 4, 5]:
            n = 2
            if self.__indeksi == 3:
                m = 0
            elif self.__indeksi == 4:
                m = 1
            else:
                m = 2

        elif self.__indeksi in [6, 7, 8, 9]:
            n = 3
            if self.__indeksi == 6:
                m = 0
            elif self.__indeksi == 7:
                m = 1
            elif self.__indeksi == 8:
                m = 2
            else:
                m = 3

        else:
            n = 4
            if self.__indeksi == 10:
                m = 0
            elif self.__indeksi == 11:
                m = 1
            elif self.__indeksi == 12:
                m = 2
            elif self.__indeksi == 13:
                m = 3
            else:
                m = 4

        return n, m


    def täytä_pakka(self):
        """
        Luodaan uusi Pakka-olio "lisäpakka". Yhdistetään pakat name mangling
        toiminnon avulla, jonka jälkeen pakka sekoitetaan.
        Toimintoa name mangling joudutaan käyttämään, sillä luokan kutsuminen
        ei jostain syystä onnistu ilman kyseistä toimintoa.
        """

        lisäpakka = Pakka()  # uusi Pakka-olio

        #print(dir(lisäpakka)) #tällä saa ._Pakka__kortit atribuutin selville

        self.__pakka._Pakka__kortit += lisäpakka._Pakka__kortit
        self.__pakka.sekoitus()


    def tyhjennä_pöytä(self):
        """
        Poistaa jokaisen framen self.__pöytä widgetin, eli kortit ja taustat.
        Tyhjentää korttien tunnistamiseen tarvittavat listat.
        """

        #poistetaan kaikki pöydän lapsiwidgetit (jossa master=self.__pöytä)
        for widget in self.__pöytä.winfo_children():
            widget.destroy()


        #listojen tyhjennys
        self.__käännetyt.clear()
        self.__käännetyt_arvot.clear()

        self.__idtausta.clear()
        self.__idkortti.clear()


    def korvaa_kortit(self):
        """
        Poistaa jokaisen "korttitaustan" pöydältä, eli siis poistaa jokaisen
        Framen self.__pöytä napin. Käytetään kaikkien
        korttitaustojen poistamiseen kerralla.

        Jos pöytä on sininen, joku ajaa bussia ja metodi huolehtii myös siitä,
        että käännetyn kortin tilalle luodaan uusi kortti. Vanhaa korttia ei
        poisteta, vaan sen päälle ainoastaan luodaan uusi Label.

        Kortin arvo tunnistetaan kahden listan avulla, jotka yhdistävät
        taustan ja kortin.
        Korvattu kortti sijoitetaan listaan korvatun tilalle.
        """

        #tutkitaan framen widgettejä ja poistetaan kaikki napit
        for widget in self.__pöytä.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()

        #tyhjennetään taustojen tunnistamiseen käytetty lista
        self.__idtausta.clear()


        #jos joku ajaa bussia, eli pöytä on sininen.
        if self.__pöytä["bg"] == "blue":

            #huolehtii, ettei kortit lopu bussia ajaessa
            if self.__pakka.korttien_määrä() <= 30:
                self.täytä_pakka()

                #print(self.__pakka.korttien_määrä())


            #tarkastetaan onko peli loppunut
            if self.tarkista_kuvakortit():
                return


            #käännetyt on lista, jossa käännettyjen korttien indeksit
            for nostettu in self.__käännetyt:
                n, m = self.määritä_sijainti(nostettu) #määritetään mikä kortti

                nosto = self.__pakka.nosta_kortti() #nostetaan kortti tilalle
                arvo, maa = nosto.split("-")

                punaiset = ["♦", "♥"]

                if maa in punaiset:
                    kortti = Label(self.__pöytä, text=f"{arvo} {maa}",
                                   width=5, height=5, relief="solid",
                                   borderwidth=2, foreground="red")

                    self.__idkortti[nostettu] = kortti #korvataan edellinen


                else:
                    kortti = Label(self.__pöytä, text=f"{arvo} {maa}",
                                   width=5, height=5, relief="solid",
                                   borderwidth=2, foreground="black")

                    self.__idkortti[nostettu] = kortti  #korvataan edellinen


                #korttipyramidista poiketen tulostaa joka silmukassa 1 kortin
                kortti.place(x=220 - n*45 + m*90, y=90*n + 10)


            #taustojen korvaus poiston jälkeen
            self.tausta_pyramidi()

        else:
            # taustojen korvaus poiston jälkeen (jos ei sininen tausta)
            self.tausta_pyramidi()

        #kun korvattu, tyhjennetään käännettyjen korttien lista
        self.__käännetyt.clear()
        self.__käännetyt_arvot.clear()



    def bussikuski(self):
        """
        Aktivoi pelin päätteeksi pelattavan minipelin, jossa ajetaan bussia.

        aluksi suoritetaan tarvittavat toiminnot:
        Käsien poisto, pöydän värin vaihto, pöydän tyhjennys, uusien korttien
        jako pyramidiksi, sekä alussa luodun laskurin asettaminen näytölle.
        Lisäksi poistetaan turhien nappien komennot.
        """

        try:
            if self.__pakka.korttien_määrä() <= 30:
                self.täytä_pakka()


            #Aluksi suoritettavat toiminnot
            self.poista_kädet()
            self.__pöytä.configure(bg="blue")
            self.tyhjennä_pöytä()
            self.kortti_pyramidi()
            self.__bussi_laskuri.place(x=225, y=235, width=100, height=35)

            #nappien komennon poisto
            self.__pyramidinappi.configure(command=lambda:None)
            self.__bussikuskinappi.configure(command=lambda:None)
            self.__jakonappi.configure(command=lambda:None)


            #luodaan nappi, jonka avulla minipeliä pelataan
            self.__kuvakortti = Button(self.__pääikkuna, text="Kuvakortti?",
                                  command=self.korvaa_kortit, font=30)


            #asetetaan nappi ja laskuri näytölle
            self.__kuvakortti.place(x=225, y=175, width=100, height=60)
            self.__bussi_laskuri.place(x=225, y=235, width=100, height=35)


        except AttributeError:
            return


    def tarkista_kuvakortit(self):
        """
        Jotta bussilla ajo päättyy, täytyy käyttäjän kääntää vähintään viisi
        numerokorttia. Metodi tarkistaa tämän, sekä sen, että ylin kortti on
        käännetty. Jos ehdot toteutuvat, peli loppuu.

        Metodi korvaa_kortit
        kutsuu tätä metodia if lausekkeen avulla. Jos lauseke toteutuu, ohjelma
        ei suorita korvaa_kortit loppuun, vaan asettaa näytölle napin ja kentän
        pelaajan tietojen tallentamista varten.

        :return: False: jos ehdot eivät toteudu, True: jos ehdot toteutuvat
        """

        #käännetyt_arvot lista, jossa on korttien arvot joita ei ole korvattu
        if len(self.__käännetyt_arvot) >= 5:
            for arvo in self.__käännetyt_arvot:

                if arvo not in ["A", "K", "Q", "J"]:
                    continue
                    #print(f"meni silmukkaan arvolla {arvo}")

                else:
                    return False

            #tutkitaan onko ylin kortti käännetty
            if 0 in self.__käännetyt:

                #viimeisen 5 kortin arvoa ei kuulu laskea mukaan
                self.__laskuri -= 10
                self.__bussi_laskuri.configure(text=self.__laskuri)

                #poistetaan napin komento
                self.__kuvakortti.configure(command=lambda:None)

                #luodaan syöttökenttä ja nappi - tallenna
                self.__tallenna_tiedot = Button(text="Tallenna",
                                                command=self.tilastointi)

                self.__bussia_ajanut = Entry(self.__pääikkuna, relief="raised",
                                                        justify=CENTER)


                self.__tallenna_tiedot.place(x=100, y=250, width=100,
                                                                height=60)

                self.__bussia_ajanut.place(x=100, y=310, width=100, height=30)

                #peli on ohi
                return True

        #kaikki ehdot eivät täyttyneet

            else:
                return False
        else:
            return False


    def tilastointi(self):
        """
        Palautettava versio luo tekstitiedoston, johon tallennetaan bussilla
        ajajan nimimerkki ja tallennetaan laskurin määrä.

        Lopulliseen versioon (omaan käyttöön) tilastojen kirjaaminen
        toteutetaan toimivaksi ratkaisuksi. Aijon palauttaaa tämän yksittäisenä
        tiedostona, joten ohjelma luo jokaista suoritusta varten tiedoston,
        "9d80L33R3NSmxc_tilastot.txt", johon tulokset "tilastoidaan".

        Nimietty siten, että sen ei pitäisi poistaa mitään olemassa olevaa.
        Kirjoittaa itsensä päälle joka kerta kun metodia kutsutaan.
        """

        tulokset = open("9d80L33R3NSmxc_tilastot.txt", "w")
        nimi = self.__bussia_ajanut.get()

        if nimi == "":
            nimi = "anonyymi"

        tulokset.write(f"Bussia ajanut: {nimi}, tuloksella: {self.__laskuri}")

        #piilottaa napit
        self.__tallenna_tiedot.place_forget()
        self.__bussia_ajanut.place_forget()


    def aloita_alusta(self):
        """
        Palauttaa ohjelman siihen tilaan, missä se on ohjelman avatessa.
        """
        #palautetaan ikkuna alkutilanteeseen
        self.__pöytä.configure(bg="brown")
        self.tyhjennä_pöytä()
        self.poista_kädet()
        self.__pakka.nollaa_pakka()
        self.täytä_pakka()

        #palautetaan nappien toiminnat
        self.__jakonappi.configure(text="Pelaajien lukumäärä (max 7):",
                                          command=self.jaa_kortit)
        self.__bussikuskinappi.configure(command=self.bussikuski)

        self.__pyramidinappi.place_forget()

        try:
            #jos pelaaja ei tallentanut tietojaan
            self.__tallenna_tiedot.place_forget()
            self.__bussia_ajanut.place_forget()

        except AttributeError:
            "jatkaa vielä bussikuskitoimintoihin"

        try:
            #piilotetaan bussikuskitoiminnot
            self.__bussi_laskuri.place_forget()
            self.__kuvakortti.place_forget()

            self.__laskuri = 0


        except AttributeError:
            return



    def säännöt(self):
        """
        Näyttää pelin säännöt ja vaihtaa sääntönapin toimintaa piilottamisen
        ja näyttämisen välillä.
        """

        sääntöteksti = """
        Aloittaaksesi pelin, täytyy ensin valita pelaajien määrä väliltä 1-7.
        Tämä tapahtuu syöttämällä numero syöttökenttään, joka sijaitsee napin 
        "Pelaajien lukumäärä (max 7) alla. Kortit saat jaettua painamalla 
        kyseistä nappia. Tämän jälkeen näytölle ilmestyy nappi "Aloita peli", 
        joka jakaa pöydälle korttipyramidin. Kortti kääntyy klikkaamalla 
        valkoista korttitaustaa.
        
        Jokaiselle pelaajalle jaetaan 5 korttia. Pelin ideana on päästä omista 
        korteistaan eroon. Kortista pääsee eroon, jos sen arvo on sama, kuin 
        pyramidista paljastuneen kortin arvo. Ohjelma ei tätä tarkista, joten
        pelin pelaaminen vaatii rehellisiä pelaajia. Omasta kortista pääsee 
        eroon sitä klikkaamalla.
        
        Kun kaikki pyramidin kortit on käännetty, pelin häviää pelaaja, jolla 
        on eniten kortteja jäljellä. Tasatilanteessa pelaajat keksivät itse,
        kuinka hävijäjä ratkaistaan.
        
        Pelin hävinnyt pelaaja "pääsee" bussikuskiksi ajamaan bussia. 
        Bussikuskin tehtävänä on päästä pyramidin huipulle kääntäen jokaiselta
        riviltä yksi kortti. Jos käännetty kortti on kuvakortti, bussikuskin on      
        aloitettava uudestaan alimmalta riviltä lähtien. Peli päättyy kun 
        bussikuski pääsee pyramidin huipulle ja kääntää sieltä kortin, joka ei
        ole kuvakortti. Kuvakorttiin törmätessä pöydän vasemmassa yläreunassa
        on nappi "Kuvakortti?", jota painamalla arvotaan uudet kortit 
        käännettyjen korttien tilalle. Ohjelma laskee jokaisen käännetyn kortin   
        ja kertoo sen kahdella. 
        
        Kun pyramidin huipulle on päästy onnistuneesti, eli yhtään kuvakorttia
        ei olla käännetty, painetaan nappulaa "Kuvakortti?", joka tuo näytölle
        mahdollisuuden tallentaa tuloksensa tiedostoon.
        
        Napit "Aloita alusta", "Lopeta" ja "Bussikuski" toimivat koko ajan. 
        Muiden nappien toimintaa rajoitetaan erilaisissa tilanteissa.
        """


        self.__sääntönappi.configure(text="Piilota säännöt",
                                     command=self.piilota_säännöt)

        self.__sääntölabel = Label(self.__pääikkuna, text=sääntöteksti,
                                   relief="raised")

        self.__sääntölabel.place(x=175, y=150)


    def piilota_säännöt(self):
        """
        Piilottaa sääntö Labelin näytöltä ja vaihtaa sääntönapin toimintaa
        """

        self.__sääntölabel.place_forget()
        self.__sääntönappi.configure(text="Näytä säännöt",
                                        command=self.säännöt)


    def lopeta(self):
        """
        Poistaa käyttöliittymän näytöltä ja lopettaa ohjelman suorituksen.
        Liitetty nappi toimii koko suorituksen ajan.
        """

        self.__pääikkuna.destroy()

def main():

    peli = Käyttöliittymä()


if __name__ == "__main__":
    main()
