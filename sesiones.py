import mariadb
import functools
from datetime import datetime, timedelta
class SesionHandler():
    def __init__(self):
        self.sesiones = []

    #crea una nueva sesion
    def crearSesion(self,usuario):
        #Si existe una sesión anterior, se borrar
        sesion = self.getSesion(usuario.id)
        if sesion:
            self.sesiones.remove(sesion);
        sesion = Sesion(usuario)
        self.sesiones.append(sesion);
        return sesion

                
    #Obitene la sesión actual del usuario
    def getSesion(self,id):
        for sesion in self.sesiones:
            if sesion.usuario.id == id:
                sesion.fechaInicio = datetime.now()
                return sesion
        
class Sesion():

    def __init__(self,usuario):
        self.usuario = usuario;
        
        
        


