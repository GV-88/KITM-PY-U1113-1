# 3. Programa prašo įvesti sveiką teigiamą skaičių n (tarkim 100). Programa sugeneruoja atsitiktinį skaičių nuo 1 iki n.
# Sugeneravus atsitiktinį skaičių vartotojui siūloma atspėti kokį skaičių sugeneravo programa.
# Įvedus spėjamą skaičių (tarkim 75) programa praneša ar sugeneruotas skaičius didesnis ar mažesnis už įvestą skaičių ir siūlo spėti dar kartą
# (tarkim „Sugeneruotas skaičius didesnis už 75. Atliksite 3 spėjimą...“).
# Įvedus didesnius skaičius už n ar neigiamus skaičius programa prašo kartoti įvedimą ir jo neprisumuoja prie spėjimų skaičiaus.
# Vartotojui atspėjus skaičių - pranešimas, koks buvo sugeneruotas skaičius ir kiek spėjimų buvo atlikta ir kiek buvo bandymų įvesti netinkamą skaičių.
# Pabaigus žaidimą – siūloma sužaisti dar kartą.

from random import randint

def registruotiSpejima(spejimoNr, spejimas, sugeneruotoSkirtumas, failas):
	if(failas):
		if sugeneruotoSkirtumas == 0:
			print(f'{spejimoNr} spėjimu vartotojas atspėjo skaičių')
		else:
			print(f'{spejimoNr} spėjimu vartotojas įvedė {spejimas}. Atsakymas - sugeneruotas skaičius {"didesnis" if sugeneruotoSkirtumas > 0 else "mažesnis"}')


def tikrintiBandyma(spejimoNr, spejimas, atsakymas, nuo, iki, failas):
	if spejimas < nuo or spejimas > iki:
		print(f'{spejimas} nesiskaito, turi būti nuo {nuo} iki {iki}.', end=' ')
		return {'atspejo': False, 'tinkamasBandymas': False}
	if atsakymas > spejimas:
		print(f'Sugeneruotas skaičius didesnis už {spejimas}.', end=' ')
		registruotiSpejima(spejimoNr, spejimas, 1, failas)
		return {'atspejo': False, 'tinkamasBandymas': True}
	if atsakymas < spejimas:
		print(f'Sugeneruotas skaičius mažesnis už {spejimas}.', end=' ')
		registruotiSpejima(spejimoNr, spejimas, -1, failas)
		return {'atspejo': False, 'tinkamasBandymas': True}
	if(failas):
		registruotiSpejima(spejimoNr, spejimas, 1, failas)
	return {'atspejo': True, 'tinkamasBandymas': False}

kiekZaidimu = 0
zaidziam = True
failas = 'reg.txt'

with open(failas, 'a+', encoding='utf8') as f:
	print('--------------------------------', file=failas)
	while zaidziam:
		n = 0
		kiekSpejimu = kiekNetinkamu = 0
		while n <= 1:
			n = int(input('Nuo 1 iki kiek?...'))
		print(f'Vartotojas įvedė skaičių {n}.', file=failas)
		spejimas = 0
		atsakymas = randint(1, n)
		print(f'Sugeneruotas atsitiktinis skaičius {n}.', file=failas)
		print(f'Atspėkite skaičių nuo 1 iki {n}.', end=(' '))
		# vidinis ciklas; būtų galima tikrinti spejimas==atsakymas, bet jeigu tai resursų reikalaujantis tikrinimas, nėra reikalo tikrinti su kiekvienu nereikšmingu bandymu
		while zaidziam:
			spejimas = int(input(f'Atliksite {kiekSpejimu+1} spėjimą...'))

			tarpinisRezultatas = tikrintiBandyma(kiekSpejimu+1, spejimas, atsakymas, 1, n, failas)

			if tarpinisRezultatas['tinkamasBandymas']:
				kiekSpejimu += 1
			else:
				kiekNetinkamu += 1
				continue
			if not tarpinisRezultatas['atpejo']:
				continue

			# čia logiškai turėtų atitikti spejimas==atsakymas
			zaidziam = False
			kiekZaidimu += 1
			print(f'PAVYKO! Atsakymas {atsakymas}, atspėta iš {kiekSpejimu} kartų, neskaitant {kiekNetinkamu} netinkamų bandymų')
			dar = '?'
			while dar == '?':
				dar = input('Žaisim dar kartą? [T/N]...')
				match(dar):
					case 't' | 'T':
						zaidziam = True
						print(f'Į užklausą „Ar žaisite dar“ pasirinko „Taip“', file=failas)
					case 'n' | 'N':
						zaidziam = False
						print(f'Į užklausą „Ar žaisite dar“ pasirinko „Ne“', file=failas)
					case _: dar = '?'
			break # išeiname iš vidinio ciklo su atnaujinta reikšme zaidziam
	print(f'Vartotojas žaidė {kiekZaidimu} kartus(ų)', file=failas)
