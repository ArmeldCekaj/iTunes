from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    @staticmethod
    def getAlbums(dMin):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)

        query = """
                SELECT a.*, sum(t.Milliseconds)/1000/60 as dTot
                FROM album a, track t
                WHERE a.AlbumId = t.AlbumId 
                GROUP BY a.AlbumId 
                having dTot > %s
                """
        cursor.execute(query, (dMin,))
        result = []
        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        cnx.close()

        return result

    @staticmethod
    def getAllEdges(idMApAlbum):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """
                    SELECT DISTINCTROW t.AlbumId as a1, t2.AlbumId as a2
                    FROM track t , track t2, playlisttrack p , playlisttrack p2 
                    WHERE t2.TrackId  = p2.TrackId 
                    AND t.TrackId  = p.TrackId 
                    ANd p2.PlaylistId = p.PlaylistId
                    AND t.AlbumId < t2.AlbumId 

                    """
        cursor.execute(query)
        result = []
        for row in cursor:
            if row["a1"] in idMApAlbum and row["a2"] in idMApAlbum:
                result.append((idMApAlbum[row["a1"]], idMApAlbum[row["a2"]]))

        cursor.close()
        cnx.close()

        return result