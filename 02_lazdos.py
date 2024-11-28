# 2. Suprogramuokite seną kinų žaidimą lazdomis. Žaidžia du žaidėjai. Yra 10 lazdelių. Žaidėjai paeiliui ima nuo vienos iki trijų lazdų.
# Pirmas žaidimą pradeda kompiuterio atsitiktiniu būdu sugeneruotas žaidėjas
# (tai gali būti žaidėjas Nr.1 arba žaidėjas Nr.2, jei yra suvedami žaidėjų vardai kompiuteris atsitiktiniu būdu parenka žaidėjo vardą)*.
# Žaidimas tęsiasi tol, kol nesibaigia lazdelės. Pralaimi tas, kuris paėmė paskutinę lazdelę.
# Suprogramuokite žaidimą taip, kad galėtų žaisti du žmonės. Žaidimo pradžioje yra 10 lazdelių*.
# Kiekviename žaidimo etape atspausdinamas žaidėjo numeris, lazdelių skaičius, ir užklausa, kiek lazdelių paims žaidėjas.
# Nepamirškite pakeisti žaidėjų eilės numerius ir mažinti lazdelių skaičių. Nepamirškite, pabaigoje išvesti laimėjusio žaidėjo numerio.
# Nepamirškite, kad žaidėjas negali paimti daugiau nei tris lazdeles (apsaugokite ir nuo 0 ir neigiamų skaičių), ir taip pat negali paimti lazdelių daugiau nei liko.
# *Žaidimo detalės gali skirtis. Galime suvesti žaidėjų vardus. Galima keisti pradinį lazdelių skaičių.
# Be žaidimo paslaugos programa sukuria žaidimo „registravimo“ failą reg.txt, kuriame yra pateikiama informacija apie žaidimo eigą...

#GV: paremta akmenų žaidimo programa iš ankstesnės užduoties

from collections import namedtuple
from random import randint

def pritaikytiLinksni(skaicius, vienas, keli, daug):
	skaicius = abs(skaicius)
	if skaicius != 11 and skaicius % 10 == 1:
		return vienas
	elif (11 <= skaicius <= 19) or skaicius % 10 == 0:
		return daug
	return keli

def isvardinti(sarasas):
	if(len(sarasas) <= 1):
		return sarasas[0]
	return ' ir '.join([', '.join(sarasas[:-1]), sarasas[-1]])

def numerisEinantRatu(nenormalusIndeksas, sarasas):
	'''normalizuoja indeksą einant ratu iš naujo'''
	return nenormalusIndeksas % len(sarasas)

def traukimasAts(tmin, tmax, kiekLiko):
	if(kiekLiko <= tmin):
		return kiekLiko # nebėra pasirinkimo
	return randint(tmin, min(kiekLiko,tmax))

def traukimas(tmin, tmax, kiekLiko, paskutinisLaimi, zaidejuSk):
	'''"dirbtinio intelekto" pseudo-strategiškas traukimas'''
	# galima dar tobulinti algoritmą...
	if(kiekLiko <= tmin):
		return kiekLiko # nebėra pasirinkimo
	if(zaidejuSk == 2 and paskutinisLaimi):
		if(kiekLiko <= tmax):
			return kiekLiko # stveriu paskutinius kada tik galiu
		if(kiekLiko - (tmin + tmax * 1) <= tmax):
			return max(kiekLiko - (tmin + tmax * 1), tmin) # stengiuosi palikti tmin + tmax * 1
		if(kiekLiko - (tmin + tmax * 2) <= tmax):
			while True:
				t = min(kiekLiko, randint(tmin, tmax))
				if (t != kiekLiko - (tmin + tmax * 2)): # stengiuosi nepalikti tmin + tmax * 2
					break
			return t
		if(kiekLiko - (tmin + tmax * 3) <= tmax):
			return max(kiekLiko - (tmin + tmax * 3), tmin) # stengiuosi palikti tmin + tmax * 3 (kad paskui man paliktų tmin + tmax * 2)
	if(zaidejuSk == 2 and not paskutinisLaimi):
		if(tmin < kiekLiko - (tmin + tmax * 0) <= tmin + tmax):
			return max(kiekLiko - (tmin + tmax * 0), tmin) # stengiuosi palikti tmin
	# jeigu nepritaikė jokios strategijos, tada atsitiktinis
	return traukimasAts(tmin, tmax, kiekLiko)

Taisykles = namedtuple('Taisykles', [
	'pradziojeMin',
	'pradziojeMax',
	'kiekGalimaPaimtiMin',
	'kiekGalimaPaimtiMax',
	'paskutinisLaimi',
	'pradedaBetKuris'
])
#GV: dar buvo mintis kad pralaimėjęs iškrenta sekančiam raundui, bet šitam žaidimui nelabai logiška

# taisykles = Taisykles(
# 	pradziojeMin = 15,
# 	pradziojeMax = 30,
# 	kiekGalimaPaimtiMin = 1,
# 	kiekGalimaPaimtiMax = 3,
# 	paskutinisLaimi = True,
# 	pradedaBetKuris = True
# )

taisykles = Taisykles(
	pradziojeMin = 10,
	pradziojeMax = 10,
	kiekGalimaPaimtiMin = 1,
	kiekGalimaPaimtiMax = 3,
	paskutinisLaimi = False,
	pradedaBetKuris = True
)

zaidejai = []
while True:
	naujasZaidejas = input(f"Nurodykite žaidėjo vardą{', arba tęskite norėdami pradėti žaidimą' if len(zaidejai) > 0 else ''}:...")
	if(naujasZaidejas.strip() != ''):
		zaidejai.append(naujasZaidejas)
	elif len(zaidejai) > 0:
		break

kiekZaidimu = 0
zaidziam = True
failas = 'reg.txt'

with open(failas, 'a+', encoding='utf8') as f:
	print('--------------------------------', file=f)
	while zaidziam:
		print(f"Žaidžia {isvardinti(zaidejai)}.")
		print(f"Žaidėjų vardai: {isvardinti(zaidejai)}.", file=f)
		kiekLiko = taisykles.pradziojeMin
		if(taisykles.pradziojeMin < taisykles.pradziojeMax):
			kiekLiko = input("Kiek pradžioje lazdelių? (jei nepateiksit skaičiaus, aš sugalvosiu)...")
			if(kiekLiko.isnumeric()):
				kiekLiko = min(taisykles.pradziojeMax, max(taisykles.pradziojeMin, int(kiekLiko)))
			else:
				kiekLiko = randint(taisykles.pradziojeMin, taisykles.pradziojeMax)
		
		print(f"Pradėkime žaidimą!")
		print(f"Yra {kiekLiko} {pritaikytiLinksni(kiekLiko, 'lazdelė','lazdelės','lazdelių')}.")
		print(f"Lazdelių pasirinktas skaičius yra: {kiekLiko}.", file=f)
		kienoEile = randint(0, len(zaidejai)-1) if taisykles.pradedaBetKuris else 0
		print(f"Žaidimą pradeda {zaidejai[kienoEile]}.", file=f)
		while kiekLiko > 0:
			traukiam = ''
			if ('NPC' in zaidejai[kienoEile].upper()):
				if('random' in zaidejai[kienoEile].lower()):
					traukiam = traukimasAts(taisykles.kiekGalimaPaimtiMin, taisykles.kiekGalimaPaimtiMax, kiekLiko)
				else:
					traukiam = traukimas(taisykles.kiekGalimaPaimtiMin, taisykles.kiekGalimaPaimtiMax, kiekLiko, taisykles.paskutinisLaimi, len(zaidejai))
			else:
				while not (traukiam.isnumeric() and taisykles.kiekGalimaPaimtiMin <= int(traukiam) <= min(kiekLiko, taisykles.kiekGalimaPaimtiMax)):
					traukiam = input(f"Įveskite, kiek lazdelių nori paimti {zaidejai[kienoEile]} ({taisykles.kiekGalimaPaimtiMin}–{min(kiekLiko, taisykles.kiekGalimaPaimtiMax)}):...")
				traukiam = int(traukiam)
			kiekLiko -= traukiam
			print(f"{zaidejai[kienoEile]} paėmė {traukiam} {pritaikytiLinksni(traukiam, 'lazdelę','lazdeles','lazdelių')}. Liko {kiekLiko}")
			print(f"{zaidejai[kienoEile]} paima {traukiam} {pritaikytiLinksni(traukiam, 'lazdelę','lazdeles','lazdelių')}. Liko {kiekLiko}", file=f)
			kienoEile = numerisEinantRatu(kienoEile+1, zaidejai)
		kiekZaidimu += 1 #skaičiuojam tik sužaistus iki galo :)
		# kadangi kienoEile pasikeičia ėjimo pabaigoje ciklo viduje, tai po paskutinio ciklo tenka tikrinti kieno eilė buvo prieš pasikeitimą;
		# šito būtų galima išvengti keitimą darant ėjimo pradžioje, bet tada klaidinančiai atrodytų pradinis nustatymas kas pradeda žaidimą;
		paskutinioVardas = zaidejai[numerisEinantRatu(kienoEile-1, zaidejai)]
		print(f"{paskutinioVardas} paėmė paskutinę lazdelę!", end=' ')
		print(f"{paskutinioVardas} {'laimėjo!' if (taisykles.paskutinisLaimi) else 'pralaimėjo!'}")
		print(f"Žaidimą laimėjo {paskutinioVardas if taisykles.paskutinisLaimi else zaidejai[numerisEinantRatu(kienoEile-2, zaidejai)]}.", file=f)
		zaidziam = input("Ar norėtumėte žaisti dar kartą? (taip/ne)...").lower() in (['t', 'taip'])
		print(f"Į užklausą „Ar žaisite dar“ pasirinko „{'Taip' if zaidziam else 'Ne'}“", file=f)
	print("Viso gero.")
	print(f"Žaidimą žaidė {kiekZaidimu} {pritaikytiLinksni(kiekZaidimu, 'kartą', 'kartus', 'kartų')}", file=f)

#GV: "žaidimas" sau: įrašyti žaidėjų vardus NPC-random ir NPC-smart ir stebėti iš kelinto karto laimi NPC-random prie taisykles.paskutinisLaimi
