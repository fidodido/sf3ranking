#Dejo 2 funciones.
#Elo_native es la formula original de elo sin cambios, salvo por los diferentes k-values
#Elo_adapted hace una diferencia entre desafios y torneos, donde en los torneos solo considera victorias y 
#derrotas sin tener en cuenta el marcador, ademas de sumarle puntos al ganador. Esto incentiva la participacion
#a torneos.

#Dejo ambas para evidenciar mediante un ejemplo (el torneo del finde pasado) que al utilizar la formula en bruto
#se observan muchos casos de jugadores con considerablemente menos puntos que jugadores que salieron en posicione
#sustancialmente inferiores.

#Funcion de elo original

"""
import math


class player:
	name=""
	skill=1000
	elo=1000
	likehood=0.5

def log2(num):
	return math.log(num)/math.log(2)

def doblelim(np):
	njug=len(np)
	mxlevel=int(math.ceil(log2(njug)))
	np=np+[""]*(int(2**mxlevel)-njug)
	winners=[]
	for i in range(mxlevel):
		winners=[[True]*int(2**(i+1))]+winners
	for i in range(len(np)):
		print "oli"

#oli=[0]*9
#doblelim(oli)

pkoso=0
size=16
print pkoso
for i in range(1,size):
	sum=1
	while not i%(size/(sum*2))==0:
		sum=2*sum
	if i%(2*size/sum)>size/sum:
		sum=-sum
	pkoso +=sum
	print pkoso

exit()
"""

"""
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
"""

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
	change_2=-change_1
	#Si es torneo, el ganador suma FtX ELO. Asi, los torneos aumentan levemente el ELO global y los desafios solo redistribuyen.
	if is_tournament:
		change_1+=ftx*min(1,max(score_player_1-score_player_2,0))
		change_2+=ftx*min(1,max(score_player_2-score_player_1,0))
	return [change_1,change_2]

"""

#Simulacion para ver como hubiesen sido los ELO finales luego del torneo del finde utilizando un ELO inicial de 1000.

#Poner 'elo=elo_native' para ver como quedan usando la formula original.
#Poner 'elo=elo_adapted' para ver como quedan usando la formula modificada.
elo=elo_adapted
	
#Inicialicacion de los ELO iniciales de los jugadores = 1000
	
seb=1000
ppx=1000
dae=1000
bla=1000
edu=1000
kmi=1000
wir=1000
atm=1000
ron=1000
ech=1000
sak=1000
dej=1000
mrf=1000
rzm=1000
rom=1000
nic=1000
knf=1000
ala=1000
dub=1000
yuu=1000
kla=1000
mor=1000
cam=1000
ozz=1000

#Cambiar para realizar la misma simulacion multiples veces, donde en cada iteracion el elo inicial viene del torneo anterior.
times=1

for t in range(times):

	#Reporte de resultados de Winner bracket
	sak,rom=elo(sak,rom,2,1)
	mrf,cam=elo(mrf,cam,2,1)
	atm,dae=elo(atm,dae,1,2)
	ala,dej=elo(ala,dej,0,2)
	rzm,bla=elo(rzm,bla,0,2)
	ppx,ozz=elo(ppx,ozz,2,0)
	edu,kmi=elo(edu,kmi,0,2)
	ech,kla=elo(ech,kla,2,1)
	mor,yuu=elo(mor,yuu,0,2)
	wir,sak=elo(wir,sak,0,2)
	mrf,dae=elo(mrf,dae,0,2)
	knf,dej=elo(knf,dej,0,2)
	nic,bla=elo(nic,bla,0,2)
	ron,dub =elo(ron,dub,2,1)
	ppx,kmi =elo(ppx,kmi,1,2)
	ech,yuu =elo(ech,yuu,2,0)
	sak,dae =elo(sak,dae,0,2)
	dej,bla =elo(dej,bla,0,2)
	ron,kmi =elo(ron,kmi,0,2)
	seb,ech =elo(seb,ech,2,0)
	dae,bla =elo(dae,bla,2,0)
	kmi,seb =elo(kmi,seb,1,2)
	dae,seb =elo(dae,seb,0,3)

	#Reporte de resultados de Loser bracket

	cam,atm =elo(cam,atm,0,2)
	ozz,edu =elo(ozz,edu,0,2)
	kla,mor =elo(kla,mor,2,1)
	yuu,rom =elo(yuu,rom,0,2)
	ppx,ala =elo(ppx,ala,2,0)
	dub,rzm =elo(dub,rzm,0,2)
	knf,edu =elo(knf,edu,0,2)
	wir,kla =elo(wir,kla,2,0)
	rom,atm =elo(rom,atm,1,2)
	ppx,rzm =elo(ppx,rzm,2,0)
	nic,edu =elo(nic,edu,0,2)
	mrf,wir =elo(mrf,wir,1,2)
	dej,atm =elo(dej,atm,1,2)
	sak,ppx =elo(sak,ppx,0,2)
	ech,edu =elo(ech,edu,0,2)
	ron,wir =elo(ron,wir,1,2)
	atm,ppx =elo(atm,ppx,0,2)
	edu,wir =elo(edu,wir,2,0)
	kmi,ppx =elo(kmi,ppx,1,2)
	bla,edu =elo(bla,edu,2,1)
	ppx,bla =elo(ppx,bla,3,1)
	dae,ppx =elo(dae,ppx,2,3)

	#Reporte de resultados de Gran final

	seb,ppx =elo(seb,ppx,3,1)

	#(deben reportarse en ese orden: winners -> losers -> gran final, para asegurar el orden cronologico de los enfrentamientos de cada jugador)

#Print de los ELO finales
pos=[
seb,
ppx,
dae,
bla,
edu,
kmi,
wir,
atm,
ron,
ech,
sak,
dej,
mrf,
rzm,
rom,
nic,
knf,
ala,
dub,
yuu,
kla,
mor,
cam,
ozz]

lugs=[1,2,3,4,6,6,8,8,12,12,12,12,16,16,16,16,21,21,21,21,21,24,24,24]
for i in range(len(pos)):
	print "Lugar: "+str(lugs[i])+"\telo: "+str(pos[i])
"""
