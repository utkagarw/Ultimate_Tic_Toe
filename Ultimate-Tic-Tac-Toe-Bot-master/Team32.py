import sys
import random
import signal
#Timer handler, helper function

class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class Manual_player:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))
		

class Player32:
	
	timeclass = __import__('time')


	def __init__(self):
		self.starttime = 0

	def terminal_state_reached(self, game_board, block_stat):

	        #Check if game is won!
	        bs = block_stat
		## Row win
		if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		#	print block_stat
			return True, 'W'
		## Col win
		elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		#	print block_stat
			return True, 'W'
		## Diag win
		elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		#	print block_stat
			return True, 'W'
		else:
			smfl = 0
			for i in xrange(9):
				for j in xrange(9):
					if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
						smfl = 1
						break
			if smfl == 1:
	                        #Game is still on!
				return False, 'Continue'
			
			else:
				return False, 'Tie'
	                        #Changed scoring mechanism
	                        # 1. If there is a tie, player with more boxes won, wins.
	                        # 2. If no of boxes won is the same, player with more corner move, wins. 
	                        point1 = 0
	                        point2 = 0
	                        for i in block_stat:
	                            if i == 'x':
	                                point1+=1
	                            elif i=='o':
	                                point2+=1
				if point1>point2:
					return True, 'P1'
				elif point2>point1:
					return True, 'P2'
				else:
	                                point1 = 0
	                                point2 = 0
	                                for i in xrange(len(game_board)):
	                                    for j in xrange(len(game_board[i])):
	                                        if i%3!=1 and j%3!=1:
	                                            if game_board[i][j] == 'x':
	                                                point1+=1
	                                            elif game_board[i][j]=='o':
	                                                point2+=1
				        if point1>point2:
					    return True, 'P1'
				        elif point2>point1:
					    return True, 'P2'
	                                else:
					    return True, 'D'	


	def update_overall_board(self, game_board, block_stat, move_ret, fl):
		#check if we need to modify block_stat

		updated_block = -1

		block_no = (move_ret[0]/3)*3 + move_ret[1]/3
		id1 = block_no/3
		id2 = block_no%3
		mg = 0
		mflg = 0
		if block_stat[block_no] == '-':
			if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
				mflg=1
			if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
				mflg=1
			
	                if mflg != 1:
	                    for i in xrange(id2*3,id2*3+3):
	                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
	                                mflg = 1
	                                break

	                ### row-wise
			if mflg != 1:
	                    for i in xrange(id1*3,id1*3+3):
	                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
	                                mflg = 1
	                                break

		
		if mflg == 1:
			block_stat[block_no] = fl
			updated_block = block_no
		
	        #check for draw on the block.

		id1 = block_no/3
		id2 = block_no%3
		cells = []
		for i in xrange(id1*3,id1*3+3):
		    for j in xrange(id2*3,id2*3+3):
			if game_board[i][j] == '-':
			    cells.append((i,j))

	        if cells == [] and mflg!=1:
	            block_stat[block_no] = 'd' #Draw
	            updated_block = block_no
	        
	        return [block_stat, updated_block]

	def weighted_status(self, board, mul):
		value = 0
		if board[1][1] == 'x':
			value += 1.5*mul
		elif board[1][1] == 'o':
			value -= 1.5*mul
		if board[0][0] == 'x':
			value += mul
		elif board[0][0] == 'o':
			value -= mul
		if board[0][2] == 'x':
			value += mul
		elif board[0][2] == 'o':
			value -= mul
		if board[2][0] == 'x':
			value += mul
		elif board[2][0] == 'o':
			value -= mul
		if board[2][2] == 'x':
			value += mul
		elif board[2][2] == 'o':
			value -= mul
		if board[0][1] == 'x':
			value += 0.7*mul
		elif board[0][1] == 'o':
			value -= 0.7*mul
		if board[1][0] == 'x':
			value += 0.7*mul
		elif board[1][0] == 'o':
			value -= 0.7*mul
		if board[1][2] == 'x':
			value += 0.7*mul
		elif board[1][2] == 'o':
			value -= 0.7*mul
		if board[2][1] == 'x':
			value += 0.7*mul
		elif board[2][1] == 'o':
			value -= 0.7*mul
		
		return value

	def checksame( self, x, y, z, mul):
		l = [x,y,z]
		l.sort()
		val = 0
		if(l[0] == '-' and (l[1] == l[2] == 'x')):
			val += 3*mul
		elif(l[0]=='-' and l[1] == l[2] == 'o'):
			val -= 3*mul
		elif((l[0] == l[1] == '-') and l[2] == 'o' and y=='o'):
			val -= 1*mul
		elif((l[0] == l[1] == '-') and l[2] == 'o'):
			val -= 1.5*mul
		elif((l[0] == l[1] == '-') and l[2] == 'x' and y=='x'):
			val += 1*mul
		elif((l[0] == l[1] == '-') and l[2] == 'x'):
			val += 1.5*mul
		elif(l[0] == 'o' and (l[1] == l[2] == 'x')):
			val -= 0.5*mul
		elif(l[0] == 'x' and (l[1] == l[2] == 'o')):
			val += 0.5*mul

		return val

	def Heuristic(self, temp_board, temp_block, flag, depth):


		mytempblock = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
		for i in xrange(0, 3):								#Counting basic x and o
			for j in xrange(0, 3):
				mytempblock[i][j] = temp_block[i*3+j]


		value = 0

		#for block status
		value += self.weighted_status(mytempblock, 1000)				#Weights of block status

		for i in xrange(0, 3):
			value += self.checksame(mytempblock[i][0],mytempblock[i][1],mytempblock[i][2],550)

		for i in xrange(0, 3):
			value += self.checksame(mytempblock[0][i],mytempblock[1][i],mytempblock[2][i],550)

		value += self.checksame(mytempblock[0][0],mytempblock[1][1],mytempblock[2][2],700)
		value += self.checksame(mytempblock[2][0],mytempblock[1][1],mytempblock[0][2],700)

		#for mini board
		for i in xrange(0, 3):
			for j in xrange(0, 3):
				if(temp_block[3*i + j] == '-'):
					for k in xrange(0, 3):
						for l in xrange(0, 3):
							mytempblock[k][l] = temp_board[3*i+k][3*j+l]

		#			value += self.weighted_status(mytempblock, 20)

					for i in xrange(0, 3):
						value += self.checksame(mytempblock[i][0],mytempblock[i][1],mytempblock[i][2],50)

					for i in xrange(0, 3):
						value += self.checksame(mytempblock[0][i],mytempblock[1][i],mytempblock[2][i],50)

					value += self.checksame(mytempblock[0][0],mytempblock[1][1],mytempblock[2][2],60)
					value += self.checksame(mytempblock[2][0],mytempblock[1][1],mytempblock[0][2],60)
		if depth%2 == 1:
			if not flag:
				value = -value
		else:
			if flag:
				value = -value
		return value;

	def alpha_beta_pruning(self, temp_board, temp_block, old_move, alpha, beta, flag, depth):
		flag = int(flag)
		sym = ''
		if(flag):
			sym = 'o'
		else:
			sym = 'x'

		updated_block = -1

		cells = self.blocks(temp_board, temp_block, old_move)
		random.shuffle(cells)

		if(depth == 4):
			H = self.Heuristic(temp_board,temp_block,flag, depth)
			return [old_move[0], old_move[1], H]

		else:
			curtime = int(round(self.timeclass.time() * 1000))

			if ((curtime - self.starttime)/1000) > 4:
				return [old_move[0],old_move[1],self.Heuristic(temp_board,temp_block,flag, depth)]


			if depth%2 == 0:
				maxv = [-1, -1 , -1000000]
				for i in cells:
					a, b = i

					temp_board[a][b] = sym
					temp_block, updated_block = self.update_overall_board(temp_board, temp_block, (a, b), sym)
					verdict, comment = self.terminal_state_reached(temp_board, temp_block)
					if verdict:
						temp_board[a][b] = '-'
						
						if(updated_block!=-1):
							temp_block[updated_block] = '-'
						return [a, b, 100000]	
					val = self.alpha_beta_pruning(temp_board, temp_block, (a,b), alpha, beta, (flag+1)%2, depth+1)
					if(updated_block!=-1):
						temp_block[updated_block] = '-'

					if( val[2] > maxv[2]):
						maxv[0] = a  # saving the move with max utility uptil now
						maxv[1] = b
						maxv[2] = val[2]
					elif( val[2] == maxv[2] and (maxv[0]%3 != 1 or maxv[1]%3 !=1) and (maxv[0]/3 != 1 or maxv[1]/3 != 1) and (a%2 ==1 or b%2 ==1) ):
						maxv[0] = a  # saving the move with max utility uptil now
						maxv[1] = b

					alpha = max(alpha, maxv[2])
					temp_board[a][b] = '-'
					
					if(beta <= alpha):
						break
				if maxv[0]%3 == 1 and maxv[1]%3 == 1:
					maxv[2] += 70
				elif ((maxv[0]%3 == 0) or (maxv[0]%3 == 2) and (maxv[1]%3 == 0) or (maxv[1]%3 == 2)):
					maxv[2] += 50
				else:
					maxv[2] -= 10
				return maxv

			else:
				minv = [-1, -1 , 1000000]
				for i in cells:
					a, b = i

					temp_board[a][b] = sym
					temp_block, updated_block = self.update_overall_board(temp_board, temp_block, (a, b), sym)
					verdict, comment = self.terminal_state_reached(temp_board, temp_block)
					if verdict:
						temp_board[a][b] = '-'
						
						if(updated_block!=-1):
							temp_block[updated_block] = '-'
						return [a, b, -100000]	
					
					val = self.alpha_beta_pruning(temp_board, temp_block, (a,b), alpha, beta, (flag+1)%2, depth+1)
					if(updated_block!=-1):
						temp_block[updated_block] = '-'

					if( val[2] < minv[2]):
						minv[0] = a
						minv[1] = b
						minv[2] = val[2]
					elif( val[2] == minv[2] and (minv[0]%3 != 1 or minv[1]%3 !=1) and (minv[0]/3 != 1 or minv[1]/3 != 1) and (a%2 ==1 or b%2 ==1) ):
						minv[0] = a  # saving the move with max utility uptil now
						minv[1] = b

					beta = min(beta, minv[2])
					temp_board[a][b] = '-'

					if(beta <= alpha):
						break
				minv[2] -= 7*len(cells)
				return minv

	def move(self,temp_board,temp_block,old_move,flag):

		self.starttime = int(round(self.timeclass.time() * 1000))

		if(flag == 'o'):
			turn = 1
		else:
			turn = 0

	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cell = self.alpha_beta_pruning(temp_board, temp_block, old_move, -1000000, 1000000, turn, 0)
		cell = cell[0:2]
		cell = (cell[0],cell[1])
		if cell[0] == -1:
			cells = self.blocks(temp_board, temp_block, old_move)
			return cells[random.randrange(len(cells))] 
		print "we played with ", flag, cell[0], cell[1]
		return cell

	def blocks(self,temp_board,temp_block, old_move):
		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]

			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = self.get_empty_cells_out_of(temp_board, blocks_allowed,temp_block)
		return cells

	def get_empty_cells_out_of(self,gameb, blal,block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in xrange(id1*3,id1*3+3):
				for j in xrange(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			for i in xrange(9):
				for j in xrange(9):
					no = (i/3)*3
					no += (j/3)
					if gameb[i][j] == '-' and block_stat[no] == '-':
						cells.append((i,j))	
		return cells

