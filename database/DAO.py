from database.DB_connect import DBConnect
from model.art_object import ArtObject


class DAO:
    @staticmethod
    def getAllArtObjects():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary = True)

        res = []
        query = """SELECT o.title, o.style, o.object_name, o.object_id, o.nationality, o.dated, o.classification FROM objects o"""

        cursor.execute(query)

        for row in cursor:
            res.append(ArtObject(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        query = """
                SELECT eo1.object_id AS o1, eo2.object_id AS o2, COUNT(eo1.exhibition_id) AS weight
                FROM exhibition_objects eo1
                JOIN exhibition_objects eo2 ON eo1.exhibition_id = eo2.exhibition_id
                WHERE eo1.object_id > eo2.object_id
                GROUP BY eo1.object_id, eo2.object_id
                """

        cursor.execute(query)
        res = cursor.fetchall()

        cursor.close()
        conn.close()
        return res
