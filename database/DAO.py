from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAllAlbum():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.AlbumId,a.ArtistId,a.Title
    from album a 
     """

        cursor.execute(query)

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAlbumSoglia(soglia):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.AlbumId, a.Title, a.ArtistId, sum(t.Milliseconds)/1000/60 as dTot
                        from album a, track t
                        where a.AlbumId = t.AlbumId 
                        GROUP BY a.AlbumId 
                        HAVING dTot > %s  """

        cursor.execute(query,(soglia,))

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    # @staticmethod
    # def getEdges():
    #     conn = DBConnect.get_connection()
    #
    #     result = []
    #
    #     cursor = conn.cursor(dictionary=True)
    #     query = """select a.AlbumId,a.ArtistId,a.Title
    # from album a , track t
    # where a.AlbumId =t.AlbumId
    # group by a.AlbumId,a.ArtistId,a.Title
    # having sum(t.Milliseconds) > %s """
    #
    #     cursor.execute(query, (soglia,))
    #
    #     for row in cursor:
    #         result.append(Album(**row))
    #
    #     cursor.close()
    #     conn.close()
    #     return result


    @staticmethod
    def getAllEdges(idMapAlbum):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)

        query = """SELECT DISTINCTROW t1.AlbumId as a1, t2.AlbumId as a2 
                    FROM track t1, track t2, playlisttrack p1, playlisttrack p2
                    WHERE t2.TrackId = p2.TrackId 
                    and t1.TrackId = p1.TrackId
                    and p2.PlaylistId = p1.PlaylistId
                    and t1.AlbumId < t2.AlbumId 
                     """

        cursor.execute(query) # in minuti

        results = []
        for row in cursor:
            if row["a1"] in idMapAlbum and row["a2"] in idMapAlbum:
                results.append((idMapAlbum[row["a1"]], idMapAlbum[row["a2"]]))

        cursor.close()
        cnx.close()
        return results

