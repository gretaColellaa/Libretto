import math
import operator
from dataclasses import dataclass
import flet

cfuTot = 180


@dataclass(order=True) #instanza tutti i metodi minimi
class Voto:
    materia: str   #il tipo serve solo per l'editor che ci suggerisce che tipo di dato inserire
    punteggio: int
    data: str
    lode: bool
#dataclass crea automaticamente il costruttore con questi parametri e tutti i metodi base
    def __str__(self): #overrides lo str fatto da dataclass
        if self.lode:
            return f"In {self.materia} hai preso {self.punteggio} e lode il {self.data}"
        else:
            return f"In {self.materia} hai preso {self.punteggio} il {self.data}"

    def copy(self):
        return Voto(self.materia, self.punteggio,
                    self.data, self.lode)
    # def __eq__(self, other):
    #     return (self.materia == other.materia and
    #             self.punteggio == other.punteggio and
    #             self.lode == other.lode)
    def __hash__(self):
        return hash((self.materia, self.punteggio, self.lode))


class Libretto:
    def __init__(self, proprietario, voti=[]):
        self.proprietario = proprietario
        self.voti = voti

    def append(self, voto):  # duck!
        if (self.hasConfitto(voto) is False
                and self.hasVoto(voto) is False):
            self.voti.append(voto)
        else:
            raise ValueError("Il voto è già presente")

    def __str__(self):
        mystr = f"Libretto voti di {self.proprietario} \n"
        for v in self.voti:
            mystr += f"{v} \n" #delego la costruzione della stringa
        return mystr

    def __len__(self): #quanti elementi ha la lista voti
        return len(self.voti)

    def calcolaMedia(self):
        """
        restituisce la media dei voti attualmente presenti nel libretto
        :return: valore numerico della media, oppure ValueError in caso la lista fosse vuota
        """

        # media = sommaVoti / numeroEsamisami
        # v = []
        # for v1 in self.voti:
        #     v.append(v1.punteggio)
        if len(self.voti) == 0:
            raise ValueError("Attenzione, lista esami vuota.")

        v = [v1.punteggio for v1 in self.voti] #sintassi semplificata per fare il ciclo che aggiunge elementi alla lista
        return sum(v) / len(v)
        # return math.mean(v)

    def getVotiByPunti(self, punti, lode):
        """
        restituisce una lista di esami con punteggio uguale a punti (e lode se applicabile)
        :param punti: variabile di tipo intero che rappresenta il punteggio
        :param lode: booleano che indica se presente la lode
        :return: lista di voti
        """
        votiFiltrati = []
        for v in self.voti:
            if v.punteggio == punti and v.lode == lode: #essendo dataclass __eq__ è già definita per voto
                votiFiltrati.append(v)
        return votiFiltrati #mi usa il __repr__ che ha autoimplementato in quanto è una lista

    def getVotoByName(self, nome):
        """
        restituisce un oggetto Voto il cui campo materia è uguale a nome
        :param nome: stringa che indica il nome della materia
        :return: oggetto di tipo Voto, oppure None in caso di voto non trovato
        """
        for v in self.voti:
            if v.materia == nome:
                return v

    def hasVoto(self, voto):
        """
        Questo metodo verifica se il libretto contiene già il voto
        "voto". Due voti sono considerati uguali per questo metodo
        se hanno lo stesso campo materia e lo stesso voto
        (voto è formato da due campi: punteggio e lode)
        :param voto: istanza dell'oggetto di tipo Voto
        :return: True se voto è già presente, False altrimenti
        """

        for v in self.voti:
            # modo numero 1
            # if v == voto:
            # pass
            if (v.materia == voto.materia and #cosi si procede con la verifica dei campi
                    v.punteggio == voto.punteggio and
                    v.lode == voto.lode):
                return True
        return False

    def hasConfitto(self, voto):
        """
        Questo metodo controlla che il voto "voto" non
        rappresenti un conflitto con i voti già presenti nel libretto.
        Consideriamo due voti in conflitto quando hanno lo stesso
        campo materia ma diversa coppia (punteggio, lode)
        :param voto: instanza della classe Voto
        :return: True se voto è in conflitto, False altrimenti
        """

        for v in self.voti:
            if (v.materia == voto.materia
                    and not (v.punteggio == voto.punteggio and v.lode == voto.lode)):
                return True
        return False

    def copy(self):
        """
        crea una nuova copia del libretto
        :return: istanza della classe Libretto
        """
        nuovo = Libretto(self.proprietario.copy(), [])
        for v in self.voti:
            nuovo.append(v.copy()) #i metodi copy e append riscritti nella classe libretto, appendo la COPIA del voto
        return nuovo

    def creaMigliorato(self):
        """
        Crea un nuovo oggetto Libretto, in cui i voti sono migliorati secondo
        la seguente logica:
        se il voto è >= 18 e < 24 aggiungo +1
        se il voto è >= 24 e < 29 aggiungo +2
        se il voto è 29 aggiungo +1
        se il voto è 30 rimane 30
        :return: nuovo libretto
        """
        nuovo = self.copy() #la copy della classe libretto che utilizza in essa la copy della classe voto
        # modifico i voti in nuovo
        for v in nuovo.voti:
            if 18 <= v.punteggio < 24:
                v.punteggio += 1
            elif 24 <= v.punteggio < 29:
                v.punteggio += 2
            elif v.punteggio == 29:
                v.punteggio = 30
        return nuovo

    def sortByMateria(self):
        # self.voti.sort(key=estraiMateria)
        self.voti.sort(key=operator.attrgetter("materia"))  # voto.materia

    # Opzione 1: creo due metodi di stampa,
    #   che prima ordinano e poi stampano
    # Opzione 2: creo due metodi che ordinano
    #   la lista di self e poi un unico metodo che stampa
    # Opzione 3: creo due metodi che si fanno una copia (deep)
    # autonoma della lista, la ordinano, e la restituiscono.
    # Poi, un altro metodo si occuperà di stamapre le nuove liste
    # Opzione 4: creo una shallow copy di self.voti e ordino quella

    def creaLibOrdinatoPerMateria(self):
        """
        Crea un nuovo oggetto Libretto, e lo ordina per materia.
        :return: nuova istanza dell'oggetto Libretto
        """
        nuovo = self.copy()
        nuovo.sortByMateria()
        return nuovo

    def creaLibOrdinatoPerVoto(self):
        """
        Crea un nuovo oggetto Libretto, e lo ordina per voto.
        :return: nuova istanza dell'oggetto Libretto
        """
        nuovo = self.copy()
        nuovo.voti.sort(key=lambda v: (v.punteggio, v.lode), #crea una tupla con i valori che specifico, e li ordina (True > False) python sa farlo da se
                        reverse=True) #operator.attrgetter prenderebbe solo il punteggio, a me serve considerare anche la lode
        return nuovo

    def cancellaInferiori(self, punteggio):
        """
        Questo metodo agisce sul libretto corrente, eliminando
        tutti i voti inferiori al parametro punteggio
        :param punteggio: intero indicante il valore minimo accettato
        :return:
        """
        # Modo 1
        # for i in range(len(self.voti)):
        #     if self.voti[i].punteggio < punteggio:
        #         self.voti.pop(i)
        # T=0 -- [18 18 18 26 27 28]
        # T=1 -- [18 18 26 27 28]
        # T=2 -- [18 26 27 28]
        # out -- [18 26 27 28]
        #NON SI TOLGONO ELEMENTI DELLA LISTA CHE STO CICLANDO

        # Modo 2
        # for v in self.voti:
        #     if v.punteggio < punteggio:
        #         self.voti.remove(v)

        # Modo 3
        # nuovo = []
        # for v in self.voti:
        #     if v.punteggio >= punteggio:
        #         nuovo.append(v)
        # self.voti = nuovo

        self.voti = [v for v in self.voti if v.punteggio >= punteggio]
        #

def estraiMateria(voto):
    """
    Questo metodo restustuisce il campo materia
    dell'oggetto voto
    :param voto: istanza della classe Voto
    :return: stringa rappresentante il nome
    della materia
    """
    return voto.materia


def testVoto():
    print("Ho usato Voto in maniera standalone")
    v1 = Voto("Trasfigurazione", 24, "2022-02-13", False)
    v2 = Voto("Pozioni", 30, "2022-02-17", True)
    v3 = Voto("Difesa contro le arti oscure", 27, "2022-04-13", False)
    print(v1)

    mylib = Libretto(None, [v1, v2])
    print(mylib)
    mylib.append(v3)
    print(mylib)
    print((flet.Text(mylib)))


if __name__ == "__main__":
    testVoto()

# class Voto:
#     def __init__(self, materia, punteggio, data, lode):
#         if  punteggio == 30:
#             self.materia = materia
#             self.punteggio = punteggio
#             self.data = data
#             self.lode = lode
#         elif punteggio < 30:
#             self.materia = materia
#             self.punteggio = punteggio
#             self.data = data
#             self.lode = False
#         else:
#             raise ValueError(f"Attenzione, non posso creare un voto con punteggio {punteggio}")
#     def __str__(self):
#         if self.lode:
#             return f"In {self.materia} hai preso {self.punteggio} e lode il {self.data}"
#         else:
#             return f"In {self.materia} hai preso {self.punteggio} il {self.data}"
