import sys
import random

# initial variables
NCards = int(sys.argv[1])
LTarget = int(sys.argv[2])
UTarget = int(sys.argv[3])
K = int(sys.argv[4])
M = float(sys.argv[5])
NGames = int(sys.argv[6])

WinCount = {}
LoseCount = {}

# given distribution
def distribution(p):
	u = []
	u.append(p[0])
	for i in range(1,len(p)):
		u.append(u[i - 1] + p[i])
	x = random.random()
	for i in range(0,len(p)):
		if x < u[i]:
			return i

# add WinCount and LoseCount
def add_up(Win,Lose,WinCount,LoseCount):
	for ele in Win:
		WinCount[ele] += 1
	for ele in Lose:
		LoseCount[ele] += 1

# initialize
for x in range(0,LTarget):
	for y in range(0,LTarget):
		for d in range(0,2):
			for j in range(0,K + 1):
				WinCount[(x,y,d,j)] = 0
				LoseCount[(x,y,d,j)] = 0

tmp = 1 / NCards
pCard = []
for i in range(0,NCards):
	pCard.append(tmp)

# game play
# play NGames times
for i in range(0,NGames):
	X = 0
	Y = 0
	D = 1
	stateA = []
	stateB = []
	isA = True
	# each game
	while True:
		# compute f B g T
		f = []
		B = -1
		Bmax = 0
		g = 0
		T = 0
		for j in range(0,K + 1):
			if (WinCount[(X,Y,D,j)] + LoseCount[(X,Y,D,j)]) == 0:
				tmp = 0.5
			else:
				tmp = WinCount[(X,Y,D,j)] / (WinCount[(X,Y,D,j)] + LoseCount[(X,Y,D,j)])
			g += tmp
			if tmp >= Bmax:
				Bmax = tmp
				B = j
			f.append(tmp)
			T += (WinCount[(X,Y,D,j)] + LoseCount[(X,Y,D,j)])
		g = g - Bmax
		
		# compute p
		p = []
		PB = (T*f[B] + M) / (T*f[B] + (K+1)*M)
		for j in range(0, K + 1):
			if j == B:
				p.append(PB)
			else:
				p.append((1 - PB)*(T*f[j] + M)/(g*T + K*M)) 
		
		# draw J cards
		J = distribution(p)
		if isA:
			stateA.append((X,Y,D,J))
		else:
			stateB.append((X,Y,D,J))
		
		# judge pass
		if J == 0:
			# if pass at previous move, X <= Y, X lose
			if X <= Y and D == 0:
				if isA:
					add_up(stateB,stateA,WinCount,LoseCount)
				else:
					add_up(stateA,stateB,WinCount,LoseCount)
				break
			elif X > Y and D == 0:
				if isA:
					add_up(stateA,stateB,WinCount,LoseCount)
				else:
					add_up(stateB,stateA,WinCount,LoseCount)
				break
			D = 0
		else:
			D = 1
		
		# draw J times
		state_after_draw = X
		for j in range(0, J):
			state_after_draw += random.randint(1, NCards)
			
		# judge if the game is done
		if state_after_draw > UTarget:
			if isA:
				add_up(stateB,stateA,WinCount,LoseCount)
			else:
				add_up(stateA,stateB,WinCount,LoseCount)
			break
		elif state_after_draw >= LTarget:
			if isA:
				add_up(stateA,stateB,WinCount,LoseCount)
			else:
				add_up(stateB,stateA,WinCount,LoseCount)
			break
		
		# switch the states
		X = Y
		Y = state_after_draw
		if isA:
			isA = False
		else:
			isA = True
		
# compute output 
play = []
prob = []
for i in range(0,LTarget):
	tmp1 = []
	tmp2 = []
	for j in range(0,LTarget):
		maxprob = -1
		'''
		for key in WinCount.keys():
			if key[0] == i and key[1] == j:
				if maxprob <= WinCount[key]:
					maxprob = WinCount[key]
					k = key
		
		tmp1.append(k[3])
		if maxprob != 0:
			tmp2.append((maxprob / (WinCount[k] + LoseCount[k])))
		else:
			tmp2.append(0.0)
		'''
		for J in range(0, K + 1):
			if WinCount[(i,j,1,J)] + LoseCount[(i,j,1,J)] == 0:
				tmp = 0.5
			else:
				tmp = WinCount[(i,j,1,J)] / (WinCount[(i,j,1,J)]+LoseCount[(i,j,1,J)])
			if maxprob < tmp:
				maxprob = tmp
				key = J
		tmp1.append(key)
		tmp2.append(maxprob)
		
	play.append(tmp1.copy())
	prob.append(tmp2.copy())

#print(WinCount)
#print(LoseCount)
#print(play)
#print(prob)
s = ''
for X in range(LTarget):
	for Y in range(LTarget):
		s += str(play[X][Y]) + ' '
	s += '\n'
s += '\n'
for X in range(LTarget):
	for Y in range(LTarget):
		s += str("%.4f" %prob[X][Y]) + '\t'
	s += '\n'
print(s)
			