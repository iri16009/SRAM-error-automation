# Modificar el .spf de la SRAM matrix
# El error que salía era The Source net of transistor ld_M999 is not connected
# he Source net of transistor ld_M999 is not connected to net ln_N8479 (PARS-002)
# Entonces para cada net hay que agregar una resistencia así:
# Rgrupo5_1 ln_N8479:12 ln_N8479 1

# LEYENDO EL ARCHIVO LOG PARA ENCONTRAR LOS NODOS CON PROBLEMA
import numpy as np

log = open("ntlogact.log", "r")
count = 0
transistores = []
port = []
nodos = []
while True:
    count += 1
    line = log.readline()
    x = line.split()
    if not line:
        break
    #print("Line{}: {}".format(count, line.strip()))
    transistores.append(x[6])
    nodos.append(x[12])
    if x[2] == "Drain":
        port.append("DRN")
    elif x[2] == "Gate":
        port.append("GATE")
    elif x[2] == "Source":
        port.append("SRC")

log.close()

#nodos1 = list(dict.fromkeys(nodos)) # Esto era para que n

archivo_spf = "prueba13.spf"
# MODIFICANDO EL ARCHIVO starrc_results_SRAMmatrix
# with is like your try .. finally block in this case
with open(archivo_spf, 'r') as file:
    # read a list of lines into data
    data = file.readlines()
file.close()

spf = open(archivo_spf, "a+")
spf.seek(0) # Porque por default se pone al final del archivo
count1 = 0;
count3 = 0;
stop = False
lineas = []
texto = []
#for i in np.arange(0, len(nodos1)-1):
while True:
    line = spf.readline()
    xx = line.split()
    count1 += 1
    if not line:
        break
    elif not xx:
        pass
    elif xx[0] == "*|NET":
        #print("Line{}: {}".format(count1, x[1]))
        stop = True
        while stop:
            line = spf.readline()
            x = line.split()
            count1 += 1
            #print(count1)
            if x == []:
                #print("vacio")
                lineas.append(count1)
                # Rgrupo1_1 transistor[i]:port[i] nodos[i] 1
                # Rgrupo1_1 ln_N8479:DRN ln_N8479 1
                #texto.append("\r\nRgrupo1_{} {}:12 {} 1\r\n".format(count1, xx[1], xx[1]))
                #print("Line{}: {}".format(count1, line.strip()))

                count2 = 0;
                bandera = 0;
                mi_string = ["\r\nRgrupo1_{} {}:12 {} 1\r\n".format(count1, xx[1], xx[1])]
                for nodo in nodos:
                    if xx[1] == nodo:
                        bandera = 1;
                        mi_string.append("Rgrupo1a_{} {}:{} {} 1\r\n".format(count3,transistores[count2],port[count2],nodo))
                        count3 += 1 # contamos las apariciones del nodo
                    count2 += 1 # contamos las iteraciones del for porque representa el index para lo de los nodos
                if bandera:
                    mi_nuevo_texto = "\r\n".join(mi_string)
                    #texto.append("{}\r\nRgrupo1_{} {}:12 {} 1\r\nRgrupo1a_{} {}:{} {} 1\r\n".format(line.strip(), count1, xx[1], xx[1],count1,transistores[count2],port[count2],nodo))
                    texto.append(mi_nuevo_texto)
                else:
                    texto.append(mi_string[0])
                stop = False
            elif (x[0] != "*|S") and (x[0] != "*|I") and (x[0] != "*|P"):
                #print("Line{}: {}".format(count1, line.strip()))
                lineas.append(count1)

                #print("Line{}: {}".format(count1, line.strip()))
                #texto.append("{}\r\nRgrupo1_{} {}:12 {} 1\r\n".format(line.strip(), count1, xx[1], xx[1]))

                count2 = 0;
                bandera = 0;
                mi_string = ["{}\r\nRgrupo1_{} {}:12 {} 1\r\n".format(line.strip(), count1, xx[1], xx[1])]
                for nodo in nodos:
                    if xx[1] == nodo:
                        bandera = 1;
                        mi_string.append("Rgrupo1a_{} {}:{} {} 1\r\n".format(count3,transistores[count2],port[count2],nodo))
                        count3 += 1 # contamos las apariciones del nodo
                    count2 += 1 # contamos las iteraciones del for porque representa el index para lo de los nodos
                if bandera:
                    mi_nuevo_texto = "\r\n".join(mi_string)
                    #texto.append("{}\r\nRgrupo1_{} {}:12 {} 1\r\nRgrupo1a_{} {}:{} {} 1\r\n".format(line.strip(), count1, xx[1], xx[1],count1,transistores[count2],port[count2],nodo))
                    texto.append(mi_nuevo_texto)
                else:
                    texto.append(mi_string[0])
                #spf.write("{}\r\nRgrupo1_{} {}:12 {} 1\r\n".format(line.strip(), count1, x[1], x[1]))
                stop = False
    #spf.write("Rgrupo1_{} {}:12 {} 1\r\n".format(i+1757, nodos1[i], nodos1[i]))

#print(lineas[-1])
#print(texto[-1])
#print(texto[0:15])
#print(lineas[0:15])

spf.close()

# Ahora sí... escribamos en el archivo :D

for i in np.arange(0, len(lineas)):
    #k = len(lineas)-i
    #kk = lineas[k]
    #data[kk] = texto[k]
    data[lineas[i]-1] = texto[i]

#print(lineas[len(lineas)-1]-1)
#print(data[lineas[len(lineas)-1]-1])
#print(texto[len(lineas)-1])
#print(len(texto))
#print(len(lineas))

with open(archivo_spf, 'w') as file:
    file.writelines( data )
file.close()
