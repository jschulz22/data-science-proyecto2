import csv 

lista_importaciones=[]
lista_exportaciones=[]
lista_datos=[]

with open ("C:\\Users\\maxsn\\Documents\\python\\synergy_logistics_database.csv", "r") as archivo: 
    recuento=csv.DictReader(archivo)
    for registro in recuento:
        lista_datos.append(registro)
        if registro["direction"]=="Imports":
           lista_importaciones.append(registro)
        else:
          lista_exportaciones.append(registro)

## Primera parte del ejercicio: Rutas más concurridas de acuerdo con el número de veces que se recorren 

####Función generada para la importación y exportación de productos 
def rutas_exportacion_importacion (direccion):
  contador = 0
  rutas_contadas = []
  rutas_conteo = []

  for ruta in lista_datos:
      if ruta["direction"] == direccion:
         ruta_actual = [ruta["origin"], ruta["destination"]]
         if ruta_actual not in rutas_contadas:
            for ruta_bd in lista_datos:
              if ruta_actual == [ruta_bd["origin"], ruta_bd["destination"]]:
                 contador += 1

            rutas_contadas.append(ruta_actual)
            rutas_conteo.append([ruta["origin"], ruta["destination"], contador])
            contador = 0

  rutas_conteo.sort(reverse = True, key = lambda x:x[2])
  return rutas_conteo

conteo_exportaciones = rutas_exportacion_importacion("Exports")
conteo_importanciones = rutas_exportacion_importacion("Imports") 

##A continuacion se muestran dos listas, en las cuales se almacenaron los 10 valores más significativos para cada ruta de exportación e importación
rutas_exportacion=conteo_exportaciones[0:9]
rutas_importacion=conteo_importanciones[0:9]

##A continuacion se imprimen las rutas más recorridas 
print(f"las 10 rutas más concurridas de importación son:")
for elemento in rutas_importacion:
  print(f" {elemento[0]}-{elemento[1]}   Recorridos {elemento[2]}")

print("\n")

print(f"las 10 rutas de exportación que más se recorren son:")
for elemento in rutas_exportacion:
  print(f"{elemento[0]}-{elemento[1]}    Recorridos {elemento[2]}")

## Parte 2:
###Medios de transporte más utilizados considerando el valor de las importaciones y las exportaciones 
### Rail, earth, sea, road 

 
##Se define la funcion para los transportes mas utilizados de acuerdo con el valor generado para las importaciones y exportaciones
def valor_transporte(direccion):
	contados = []
	valores_transporte = []

	for viaje in lista_datos:
		actual = [direccion, viaje["transport_mode"]] 
		valor = 0
		operaciones = 0

		if actual in contados:
			continue

		for movimiento in lista_datos:
			if actual == [movimiento["direction"], movimiento["transport_mode"]]:
				valor += int(movimiento["total_value"])
				operaciones += 1
		
		contados.append(actual)
		valores_transporte.append([direccion, viaje["transport_mode"], valor, operaciones])
	
	valores_transporte.sort(reverse = True, key = lambda x:x[2])
	return valores_transporte

##A continuación se muestran los resultados generados por la función anterior
print("\n")

print("Exportaciones de acuerdo al transporte utilizado")
valores_paises = valor_transporte("Exports")
for elemento in valores_paises:
  print(f"Tipo de transporte: {elemento[1]}      Valor de exportaciones: {elemento[2]}     Veces utilizado: {elemento[3]}")

print("\n")
print("Importaciones de acuerdo con el transporte utilizado")
valor_importacion=valor_transporte("Imports")
for elemento in valor_importacion: 
   print(f"Tipo de transporte: {elemento[1]}      Valor de exportaciones: {elemento[2]}     Veces utilizado: {elemento[3]}")


###paise que generan el 80% del valor de exportaciones e importaciones 
def mayores_ganancias_por_paises(lista):
#Para obtener el total, cada ganancia obtenida se agregara a "total_de_ganancias". La funcion sum y len 
    #serán utiles para obtener el total de ganancias netas 
    ganancias = {}
    total_de_ganancias = []
    for elemento in lista:
        if elemento['origin'] not in ganancias:
           ganancias[elemento['origin']] = elemento['total_value']
           total_de_ganancias.append(int(elemento['total_value']))
        else:
            sumatoria_de_ganancias = int(elemento['total_value']) + int(ganancias[elemento['origin']])
            ganancias[elemento['origin']] = sumatoria_de_ganancias
            total_de_ganancias.append(int(elemento['total_value']))

##Ganancias totales y paises que aportan con el mayor numero de ganancias 
    print(f"Ganancia Total: {(sum(total_de_ganancias))} ")
    i = 0
    for value, key in sorted(ganancias.items(), key= lambda x: x[1], reverse= True):
        if i <= 80:
            porcentaje= (key * 100) / sum(total_de_ganancias)
            print(value,"   Ganancia: ",(key), " Porcentaje", round(porcentaje, 2), "% del total")
            i += round(porcentaje, 2)

##Resultados
print("\n")
print("Paises que generan el 80% del valor total de las importaciones:")
mayores_ganancias_por_paises(lista_importaciones)

print("\n")
print("Paises que generan el 80% de las exportaciones")
mayores_ganancias_por_paises(lista_exportaciones)