import sys

def Blackjack(NCards,LTarget,UTarget):
	play = []
	prob = []
	# initialize
	for i in range(0,LTarget):
		tmp1 = []
		tmp2 = []
		for j in range(0,LTarget):
			tmp1.append(-1)
			tmp2.append(False)
		play.append(tmp2.copy())
		prob.append(tmp1.copy())
	
	# the set to compute
	cpt = [(LTarget - 1,LTarget - 1)]

	while len(cpt) != 0:
		tmp = []
		# compute the set in cpt here
		for ele in cpt:
			ProbWinning = 0.0
			for CARD in range(1, NCards + 1):
				if ele[0] + CARD > UTarget:
					ProbYWins = 1
				elif ele[0] + CARD >= LTarget:
					ProbYWins = 0
				else: 
					ProbYWins = prob[ele[1]][ele[0] + CARD]
				ProbWinning = ProbWinning + (1 - ProbYWins) / NCards
				
			if ele[0] < ele[1]:
				play[ele[0]][ele[1]] = True
				prob[ele[0]][ele[1]] = ProbWinning
			elif ele[0] == ele[1]:
				if ProbWinning >= 1 - ProbWinning:
					play[ele[0]][ele[1]] = True
					prob[ele[0]][ele[1]] = ProbWinning
				else:
					play[ele[0]][ele[1]] = False
					prob[ele[0]][ele[1]] = 1 - ProbWinning
			else:
				if ProbWinning >= 1 - prob[ele[1]][ele[0]] or prob[ele[1]][ele[0]] == -1 :
					play[ele[0]][ele[1]] = True
					prob[ele[0]][ele[1]] = ProbWinning
				else:
					play[ele[0]][ele[1]] = False
					prob[ele[0]][ele[1]] = 1 - prob[ele[1]][ele[0]]
				
		# compute the next cpt
			if ele[0] != 0:
				if (ele[0] - 1,ele[1]) not in tmp:
					tmp.append((ele[0] - 1,ele[1]))
			if ele[1] != 0:
				if (ele[0],ele[1] - 1) not in tmp:
					tmp.append((ele[0],ele[1] - 1))
		cpt = tmp.copy()
		
	print(play)
	print(prob)

Blackjack(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
		