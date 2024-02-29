from BMH import BMHMatching

class RegEx:
    def __init__(self):
        self.text = ""
        self.pattern = ""
        self.flag_global = False
        self.flag_i = False

    def set_text(self, text):
        """Establece el texto en el que se realizará la coincidencia."""
        self.text = text
        
    def get_text(self):
        return self.text
    
    #Búsqueda simple
    def busqueda_simple(self, pattern):
        bmh = BMHMatching()
        bmh.set_text(self.text)
        pattern_to_find = pattern
        return list(set(bmh.search(pattern_to_find)))

    #Rango de letras y numeros entre corchetes cuadrados
    def rangos(self, pattern):
        pattern_to_find = pattern
        dentro = pattern_to_find.split('[')[1].split(']')[0]
        despues = pattern_to_find.split(']')[1]  # Para analizar lo después
        antes = pattern_to_find.split('[')[0]  # Para analizar el antes

        palabras = []

        #rangos
        inicio = ord(dentro[0])
        final = ord(dentro[2]) + 1

        # Generar las palabras con el rango de letras y buscarlas
        for i in range(inicio, final):
            nueva_letra = chr(i)
            if nueva_letra in self.text:
                nueva_palabra = antes + nueva_letra + despues
                total = self.busqueda_simple(nueva_palabra)
                if total:  
                    palabras.extend(total)

                
        return list(set(palabras))

    #Conjunto de letras entre corchetes
    def conjuntos(self, pattern):
        pattern_to_find = " "
        pre = pattern.split('[')[0]
        post = pattern.split(']')[1]
        
        conjunto = pattern.split('[')[1].split(']')[0]
        patrones=[]
        
        for char in conjunto:
            pattern_to_find = pre + char + post
            # Imprime el patrón con el carácter del conjunto
            resultado = self.busqueda_simple(pattern_to_find)
            patrones.extend(resultado)
      
        return list(set(patrones))

    #Letra intermedia antes del signo ? puede o no aparecer en el match encontrado
    def puede_aparecer(self, pattern):
        pattern_to_find = pattern
        antes, despues = pattern_to_find.split('?')  # Para analizar el antes

        if len(antes) == 0:
            raise ValueError("El operador ? no puede estar en la primera posición")

        palabra1= antes + despues
        palabra2 = antes[:-1] + despues


        resultados = []

        resultado1 = self.busqueda_simple(palabra1)
        resultado2 = self.busqueda_simple(palabra2)

        resultados.extend(resultado1)  # Agregar resultados de palabra1 a la lista
        resultados.extend(resultado2)  # Agregar resultados de palabra2 a la lista
        resul=self.sortingalg(list(set(resultados)))
        return resul
        
    
    #El operador | funciona como un or lógico. El texto puede hacer match con la string de la izq o der
    def izq_or_der(self, pattern):
        pattern_to_find = pattern
        buscar1 = pattern_to_find.split('|')[0]# Para analizar el antes
        buscar2 = pattern_to_find.split('|')[1]  # Para analizar lo después
        
        coincidencia1= self.leer(buscar1)
        coincidencia2=self.leer(buscar2)
        
        coincidencia_total= coincidencia1+coincidencia2
        resul=self.sortingalg(list(set(coincidencia_total)))
        return resul

    def comodin(self, pattern):
        pattern_to_find = pattern
        despues = pattern_to_find.split('*')[1]  # Para analizar lo después
        antes = pattern_to_find.split('*')[0]  # Para analizar el antes

        palabras = []

        for i in range(48, 122):
            letter = chr(i)
            if letter in self.text:
                nueva_palabra = antes + letter + despues
                total = self.busqueda_simple(nueva_palabra)
                if total:
                    palabras.extend(total)
                    
        resul=self.sortingalg(list(set(palabras)))
        return resul
       
    #Operador de repetición
    def repeticion(self, pattern):
        char_antes=""
        
        char_antes = pattern.split('{')[0]
        char_repetido = char_antes[-1]
        char_antes = char_antes[:-1]

        
        repeticiones = int(pattern.split('{')[1].split('}')[0])
        complemento = pattern.split('{')[1].split('}')[1]
        
        for i in range(len(pattern)):
            if repeticiones > 1:
                
                pattern_to_find = char_antes+(char_repetido * repeticiones) + complemento
            else:
                if repeticiones == 0:
                    pattern_to_find = char_antes+complemento
                else:
                   
                    pattern_to_find += pattern[i]
        
        return list(set(self.busqueda_simple(pattern_to_find)))
        
    def sortingalg(self, coincidencia):
        max_val = max(coincidencia)
        count = [0] * (max_val + 1)
        for num in coincidencia:
            count[num] += 1
        sorted_arr = []
        for i in range(len(count)):
            sorted_arr.extend([i] * count[i])
        
        return sorted_arr
    
    # Leer funciones y realizar el comodin
    def leer(self, pattern):
        pattern_to_find = pattern  # Obtener el patrón procesado con match

        if pattern_to_find.isalpha():
            return self.busqueda_simple(pattern_to_find)
        elif '|' in pattern_to_find:
            return self.izq_or_der(pattern_to_find)
        elif '[' in pattern_to_find and ']' in pattern_to_find and '-' in pattern_to_find:
            return self.rangos(pattern_to_find) 
        elif '[' in pattern_to_find and ']' in pattern_to_find:
            return self.conjuntos(pattern_to_find)
        elif '*' in pattern_to_find:
            return self.comodin(pattern_to_find)
        elif '?' in pattern_to_find:
            return self.puede_aparecer(pattern_to_find)
        elif '{' in pattern_to_find and '}' in pattern_to_find:
            return self.repeticion(pattern_to_find)
        else:
            print("Patrón no válido")
          
    

RE = RegEx()
RE.set_text('hola adios arboool holo holu holi palo malo')
\
entrada = input("Introduce un patrón a buscar: ")  # Lee el patrón desde la entrada estándar
#
#Leer el patrón (f/fr, regEx, g/i)
pattern = entrada
pattern_to_find = pattern  # Inicializar pattern_to_find con el valor original del patrón
        
if pattern[0] == "f":  # checa que la primera posicion sea 'f'
    if pattern[1] == "r":  # checa que la segunda sea 'r'
        #pattern_to_find = pattern[3:]  # a partir del tercer elemento
        #pattern_to_replace = pattern[(pattern_to_find +1):]  
        pattern_parts = pattern.split()
        pattern_to_find = pattern_parts[1]  # La parte después de 'fr '
        pattern_to_replace = pattern_parts[2]
        flag_replace = True
    else:
        pattern_to_find = pattern[2:]  # a partir del segundo elemento
        flag_replace = False

    # Verifica las banderas al final del patrón
    if pattern[-4:] == " g i":
        flag_global = True
        flag_i = True
        pattern_to_find = pattern_to_find[:-4]
        if pattern[0] == "f":  
            if pattern[1] == "r": 
                pattern_to_find = pattern_parts[1]
    elif pattern[-2:] == " i":
        flag_global = False
        flag_i = True
        pattern_to_find = pattern_to_find[:-2]
        if pattern[0] == "f":  
            if pattern[1] == "r": 
                pattern_to_find = pattern_parts[1]
    elif pattern[-2:] == " g":
        flag_global = True
        flag_i = False
        pattern_to_find = pattern_to_find[:-2]
        if pattern[0] == "f":  
            if pattern[1] == "r": 
                pattern_to_find = pattern_parts[1]

    else:
        flag_global = False
        flag_i = False

if flag_i:
    str = RE.get_text().lower()
    RE.set_text(str)
    pattern_to_find.lower()
    

ans = RE.leer(pattern_to_find)

if flag_global:
    print(ans)
else:
    print(ans[:1])
#

# replace
if flag_replace:

    occurrences = RE.leer(pattern_to_find)


    if occurrences:
        while occurrences:
            # Obtener el texto antes y después de la ocurrencia
            occurrence = occurrences.pop()
            before_occurrence = RE.get_text()[:occurrence]
            after_occurrence = RE.get_text()[occurrence + len(pattern_to_find):]
            # Construir el nuevo texto con la nueva palabra
            new_text = before_occurrence + pattern_to_replace + " " + after_occurrence
            
            RE.set_text(new_text)


print(" ")
print(RE.get_text())  
