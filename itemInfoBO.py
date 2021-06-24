import config
import traceback

class ItemInfoDB():
    def __init__(self, pool):

        self.pool = pool

    def getItemsInfoByCategoria(self,idCategoria):
        con = self.pool.get_connection()
        itemsInfo={}
        try:
            cur = con.cursor()
            sql = """
            select
            item.id,item.idCategoria,categ.nombre,valor,caract.nombre,caract.id, caract_categ.pregunta, caract_categ.respuesta, caract_categ.postRespuesta
            from ITEM_INFO item,
            VALOR_CARACTERISTICA valor,
            CARACTERISTICAS caract,
            CARACTERISTICAS_CATEGORIAS caract_categ,
            CATEGORIAS categ
            where categ.id=item.idCategoria
            and item.id=valor.idItem
            and caract.id=valor.idCaracteristica
            and caract_categ.idCaracteristica=caract.id
            and caract_categ.idCategoria=categ.id
            and item.idCategoria=?"""
            cur.execute(sql,(idCategoria,))
            filas = cur.fetchall()
            for fila in filas:
                idItem = str(fila[0])
                if idItem not in itemsInfo:
                    itemsInfo[idItem]  = ItemInfo(fila[0],fila[1],fila[2])
                itemsInfo[idItem].addCaracteristica(fila[3],fila[4],fila[5],fila[6],fila[7],fila[8])

        except:
            traceback.print_exc()
        finally:
            con.close()
        return list(itemsInfo.values())

       
class ItemInfo():

    def __init__(self, id, idCategoria,nombreCategoria):
        self.id = id
        self.idCategoria=idCategoria
        self.nombreCategoria = nombreCategoria
        self.caracteristicas = []

    def addCaracteristica(self,valor,nombre,idCaracteristica,pregunta,respuesta,postRespuesta):
        self.caracteristicas.append(Caracteristica(idCaracteristica,valor,nombre,pregunta,respuesta,postRespuesta))


    def getValorCaracteristica(self,idCaracteristica):
        for caracteristica in self.caracteristicas:
            if caracteristica.id == idCaracteristica:
                return caracteristica.valor

        
        

class Caracteristica():
    def __init__(self,id,valor,nombre,pregunta,respuesta,postRespuesta):
        self.id = id
        self.valor = valor
        self.nombre = nombre
        self.pregunta = pregunta
        self.respuesta =respuesta
        self.postRespuesta = postRespuesta
        
