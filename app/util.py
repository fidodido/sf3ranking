#Dejo 2 funciones.
#Elo_native es la formula original de elo sin cambios, salvo por los diferentes k-values
#Elo_adapted hace una diferencia entre desafios y torneos, donde en los torneos solo considera victorias y 
#derrotas sin tener en cuenta el marcador, ademas de sumarle puntos al ganador. Esto incentiva la participacion
#a torneos.

#Dejo ambas para evidenciar mediante un ejemplo (el torneo del finde pasado) que al utilizar la formula en bruto
#se observan muchos casos de jugadores con considerablemente menos puntos que jugadores que salieron en posicione
#sustancialmente inferiores.

import math

#Funcion de elo original
def elo_native(elo_player_1, elo_player_2, score_player_1, score_player_2):
	#Ftx=2 si es Ft2, 3 si es Ft3, etc.
	ftx=max(score_player_1, score_player_2)
	#El k-value es que tanto puede cambiar el ELO en el enfrentamiento. Es mayor mientras mas alto es FtX
	if ftx<3:
		kval=50
	elif ftx<4:
		kval=60
	elif ftx<6:
		kval=70
	elif ftx<9:
		kval=80
	elif ftx<14:
		kval=90
	else:
		kval=100
	#Las formulas a continuacion son las formulas del ELO sin cambios.
	#Res_1 es el resultado del jugador 1 en proporcion de victorias. 
	#Un 3-0 es un res_1=1 ya que gano el 100% de los match. un 3-2 es un res_1=0.6 ya que gano el 60% de los match, etc.
	res_1=score_player_1*1.0/(score_player_1+score_player_2)
	#Expect_1 es el resultado esperado para el jugador 1 dados los respectivos ELO.
	#Cada 400 de diferencia de ELO el jugador tiene 10 veces mas probabilidad de ganar que el otro.
	#Con eso se calcula la probabilidad teorica de que el jugador 1 gane.
	expect_1=1.0/(1.0+10**((elo_player_2-elo_player_1)/400.0))
	#Luego el cambio en elo es el resultado obtenido por 1 jugador menos su probabilidad de ganar, multiplicada por K-value.   
	change_1=kval*(res_1-expect_1)
	#El ELO ganado por el ganador es igual al ELO perdido por el perdedor.
	return [elo_player_1+change_1,elo_player_2-change_1]

#Funcion de elo modificada. Aca se debe especificar si se trata o no de un enfrentamiento de torneo. Por defecto es True.
#Se podria poner que automaticamente detecte si es un enfrentamiento cuando se trata de Ft10 o Ft20, conversable.
def elo_adapted(elo_player_1, elo_player_2, score_player_1, score_player_2, is_tournament=True):
	#Ftx y K-value siguen las mismas reglas que para elo_native
	ftx=max(score_player_1, score_player_2)
	if ftx<3:
		kval=50
	elif ftx<4:
		kval=60
	elif ftx<6:
		kval=70
	elif ftx<9:
		kval=80
	elif ftx<14:
		kval=90
	else:
		kval=100
	#Si no es torneo, res_1 funciona como en elo_native, de acuerdo a el porcentaje de matches ganados.
	#Si es torneo, una victoria cuenta como res_1=1 independiente del resultado.
	if is_tournament:
		res_1=min(max(score_player_1-score_player_2,0),1)
	else:
		res_1=score_player_1*1.0/(score_player_1+score_player_2)
	#Expect y change siguen las mismas reglas que para elo_native
	expect_1=1.0/(1.0+10**((elo_player_2-elo_player_1)/400.0))
	change_1=kval*(res_1-expect_1)
	#Si es torneo, el ganador suma FtX ELO. Asi, los torneos aumentan levemente el ELO global y los desafios solo redistribuyen.
	if is_tournament:
		elo_player_1+=ftx*min(1,max(score_player_1-score_player_2,0))
		elo_player_2+=ftx*min(1,max(score_player_2-score_player_1,0))

	return math.ceil(abs(change_1))
	
#Simulacion para ver como hubiesen sido los ELO finales luego del torneo del finde utilizando un ELO inicial de 1000.

#Poner 'elo=elo_native' para ver como quedan usando la formula original.
#Poner 'elo=elo_adapted' para ver como quedan usando la formula modificada.
elo=elo_native


