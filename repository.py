import pymysql.cursors
from pymysql import connect


class Repository:
    def __init__(self) -> None:
        pass

    def __initiate_connection(self,):
        # connect db
        self.conn = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    database='bdgerencia',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    # TODO: Verificar que el usuario proporcionado tenga información en las tablas gasto y personal

    def check_user_exists(self, userid: int) -> bool:
        self.__initiate_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """SELECT u.usuario_id FROM usuario u WHERE u.usuario_id = %s"""
                cursor.execute(sql, (userid,))
                result = cursor.fetchone()
            return result is not None
        finally:
            self.conn.close()

    def get_gasto_from_userid(self, userid: int, limite=50):
        self.__initiate_connection()
        try:
            with self.conn.cursor() as cursor:
                # consulta a máximo 50 ítems
                sql = """SELECT cg.nombre as categoria, g.nombre, g.monto, g.fecha
                FROM `gasto` g JOIN `categoriagasto` cg WHERE `usuario_id`=%s ORDER BY g.fecha DESC LIMIT 50"""
                cursor.execute(sql, (userid,))
                result = cursor.fetchall()

            return result
        finally:
            self.conn.close()

    def get_info_personal_from_userid(self, userid: int):
        self.__initiate_connection()
        try:
            with self.conn.cursor() as cursor:
                # TODO: Calcular la edad Para no pasar la fecha de nacimiento completa
                sql = """
                SELECT fecha_nacimiento, ocupacion, ingresos 
                FROM Persona 
                WHERE usuario_id = %s
                """
                cursor.execute(sql, (userid,))
                result = cursor.fetchall()
                
            return result
        finally:
            self.conn.close()
