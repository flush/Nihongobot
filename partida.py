import config
import traceback
import random






class Partida():

    def __init__(self,itemsInfo):
        self.preguntas=[]
        self.aciertos = 0

        random.shuffle(itemsInfo)
        for itemInfo in itemsInfo:
            self.preguntas.append(Pregunta(itemInfo,itemsInfo))




class Pregunta():

    def __init__(self,itemInfo,itemsInfo):


        self.opcionCorrecta = itemInfo
        self.opciones = []
        self.caracteristicaPregunta = None
        self.caracteristicaRespuesta = None
        self.caracteristicaPost = None
        
        self.opciones.append(itemInfo)


        random.shuffle(itemInfo.caracteristicas)


        for caracteristica in itemInfo.caracteristicas:
            if self.caracteristicaPregunta is None and caracteristica.pregunta:
                self.caracteristicaPregunta=caracteristica
            elif self.caracteristicaRespuesta is None and caracteristica.respuesta:
                self.caracteristicaRespuesta=caracteristica
            
        opcionesIncorrectas = {}

        for x in range(0,config.config["numOpciones"]-1):
            
            escogido = False
            while not escogido:
                respuestaIncorrecta = random.choice(itemsInfo)
                if respuestaIncorrecta.id != itemInfo.id and str(respuestaIncorrecta.id) not in opcionesIncorrectas:
                    opcionesIncorrectas[str(respuestaIncorrecta.id)]=respuestaIncorrecta
                    escogido = True
                    

        self.opciones.extend(list(opcionesIncorrectas.values()))

        random.shuffle(self.opciones)
        

    def getTextoPregunta(self):
        return config.mensajes["pregunta_"+self.caracteristicaRespuesta.nombre].format(valor = self.caracteristicaPregunta.valor)
