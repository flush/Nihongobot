import config
import traceback

class CategoriasDB():
    def __init__(self, pool):

        self.pool = pool

    def getCategorias(self):
        con = self.pool.get_connection()
        categorias=[]
        try:
            cur = con.cursor()
            sql = "SELECT * FROM CATEGORIAS "
            cur.execute(sql)
            filas = cur.fetchall()
            for fila in filas:
                categorias.append(Categoria(fila[0],fila[1]))
            
        except:
            traceback.print_exc()
        finally:
            con.close()
        return categorias


    def getCategoria(self, id):
        con = self.pool.get_connection()
        try:
            cur = con.cursor()
            sql = "SELECT * FROM CATEGORIAS WHERE id = %s"
            cur.execute(sql, (id,))
            categoria = cur.fetchone()
            if categoria:
                return Categoria(categoria[0], categoria[1])
            else:
                return None
        except:
            traceback.print_exc()
        finally:
            con.close()
       
class Categoria():

    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

