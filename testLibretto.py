from scuola import Student
from voto.voto import Libretto, Voto

Harry = Student("Harry", "Potter", 11, "castani",
                "castani", "Grifondoro", "civetta",
                "Expecto Patronum")
mylib = Libretto(Harry, [])

v1 = Voto("Difesa contro le arti oscure", 25, "2022-01-30", False)
v2 = Voto("Babbanologia", 21, "2022-02-12", False)
mylib.append(v1)
mylib.append(v2)

mylib.append(Voto("Pozioni", 21, "2022-06-14", False)) #meglio usare questo metodo e non creare troppe variabili poi inutili
mylib.append(Voto("Trasfigurazione", 21, "2022-06-14", False))

mylib.calcolaMedia()

votiFiltrati = mylib.getVotiByPunti(21, False)
print(votiFiltrati)

votoTrasfigurazione = mylib.getVotoByName("Trasfigurazione")

if votoTrasfigurazione is None:
    print("Voto non trovato")
else:
    print(votoTrasfigurazione.materia)

print("Verifico metodo hasVoto")
print(mylib.hasVoto(v1))
print(mylib.hasVoto(Voto("Aritmanzia", 30, "2023-07-10", False)))
print(mylib.hasVoto(Voto("Difesa contro le arti oscure", 25, "2022-01-30", False)))
print("Verifico metodo hasConflitto")
print(mylib.hasConfitto(Voto("Difesa contro le arti oscure", 21, "2022-01-30", False)))

print("Test append modificata")
mylib.append(Voto("Aritmanzia", 30, "2023-07-10", False))
# mylib.append(Voto("Difesa contro le arti oscure", 21, "2022-01-30", False))


mylib.append(Voto("Divinazione", 27, "2021-02-08", False))
mylib.append(Voto("Cura delle creature magiche", 26, "2021-06-14", False))

print("---------------------------------------")
print("Libretto originario")
print(mylib)

nuovoLib = mylib.creaMigliorato()

print("---------------------------------------")
print("Libretto migliorato")
print(nuovoLib)
print("Libretto originario")
print(mylib)


print("---------------------------------------")
ordinato = mylib.creaLibOrdinatoPerMateria()
print("Libretto ordinato per materia")
print(ordinato)

print("---------------------------------------")
ordinato2 = mylib.creaLibOrdinatoPerVoto()
print("Libretto ordinato per voto")
print(ordinato2)

print("---------------------------------------")
print("Libretto a cui ho eliminato i voti inferiori a 24")
ordinato2.cancellaInferiori(24)
print(ordinato2)