import mysql.connector

from dao.dbConnect import DBConnect
from voto.voto import Voto


class LibrettoDAO:
    # def __init__(self):
    #     self.dbConnect = DBConnect()

    def getAllVoti(self):
        # cnx = mysql.connector.connect(
        #     user = "root",
        #     password = "rootroot",
        #     host = "127.0.0.1",
        #     database = "libretto")
        cnx = DBConnect.getConnection()

        cursor = cnx.cursor(dictionary=True)

        query = """select * from voti"""
        cursor.execute(query)

        res = []
        for row in cursor:
            # materia = row["materia"] #str
            # punteggio = row["punteggio"] #int
            # lode = row["lode"] #str
            # data = row["data"] #datetime
            # v = Voto(materia, punteggio, data, lode)
            # res.append(v)
            if row["lode"] == "False":
                res.append(Voto(row["materia"], row["punteggio"], row["data"].date(), False))
            else:
                res.append(Voto(row["materia"], row["punteggio"], row["data"].date(), True))
        cnx.close()
        return res

    def addVoto(self, voto: Voto):
        # cnx = mysql.connector.connect(
        #     user = "root",
        #     password = "rootroot",
        #     host = "127.0.0.1",
        #     database = "libretto")
        cnx = DBConnect.getConnection()

        cursor = cnx.cursor()

        query = ("insert into "
                 "voti (materia, punteggio, data, lode) "
                 "values (%s, %s, %s, %s) ")

        cursor.execute(query, (voto.materia, voto.punteggio, voto.data, str(voto.lode)))
        cnx.commit()
        cnx.close()
        return

    def hasVoto(self, voto: Voto):
        # cnx = mysql.connector.connect(
        #     user = "root",
        #     password = "rootroot",
        #     host = "127.0.0.1",
        #     database = "libretto")
        cnx = DBConnect.getConnection()

        cursor = cnx.cursor()
        query = """ select * 
                    from voti v 
                    where v.materia = %s """
        cursor.execute(query, (voto.materia,))
        res = cursor.fetchall()
        return len(res) > 0


if __name__ == "__main__":
    mydao = LibrettoDAO()
    mydao.getAllVoti()