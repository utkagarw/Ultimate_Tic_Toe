import sys
import random
import signal
import time

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
			return True, 'W'
		## Col win
		elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
			return True, 'W'
		## Diag win
		elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
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

		#for each mini board
		for i in xrange(0, 3):
			for j in xrange(0, 3):
				if(temp_block[3*i + j] == '-'):
					for k in xrange(0, 3):
						for l in xrange(0, 3):
							mytempblock[k][l] = temp_board[3*i+k][3*j+l]

		#			value += self.weighted_status(mytempblock, 20)

					for i in xrange(0, 3):
						value += self.checksame(mytempblock[i][0],mytempblock[i][1],mytempblock[i][2],60)

					for i in xrange(0, 3):
						value += self.checksame(mytempblock[0][i],mytempblock[1][i],mytempblock[2][i],60)

					value += self.checksame(mytempblock[0][0],mytempblock[1][1],mytempblock[2][2],70)
					value += self.checksame(mytempblock[2][0],mytempblock[1][1],mytempblock[0][2],70)
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
				minv[2] -= 4*len(cells)
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
	#	print "we played with ", flag, cell[0], cell[1]
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

	def monte(self,temp_board,temp_block,old_move,flag):
		if(flag == 'o'):
			notflag = 'x'
		else:
			notflag = 'o'

		cells = self.blocks(temp_board, temp_block, old_move)

		best = [-1, -1, -1000]
		for i in cells:
			a, b = i
			maxv = 0
			for j in range(0,30):
				#write to append
				temp_board[a][b] = flag
				
				temp_block, updated_block = self.update_overall_board(temp_board, temp_block, (a, b), flag)
				verdict, comment = self.terminal_state_reached(temp_board, temp_block)
				if verdict:
					temp_board[a][b] = '-'
					
					if(updated_block!=-1):
						temp_block[updated_block] = '-'
					return (a,b)

				val = self.carlo(temp_board,temp_block,[a, b], notflag)
				if(val == flag):
					maxv += 1
				elif(val == notflag):
					maxv-=1
				#write to !append
				temp_board[a][b] = '-'
					
				if(updated_block!=-1):
					temp_block[updated_block] = '-'
			if(maxv > best[2]):
				best = [a,b,maxv]
		#	print maxv
		if a==-1 and b==-1:
			return cells[cells.randrange(len(cells))]
		else:
			return (best[0],best[1])

	def carlo(self,temp_board,temp_block,old_move,flag):
		if(flag == 'o'):
			notflag = 'x'
		else:
			notflag = 'o'

		cells = self.blocks(temp_board, temp_block, old_move)

		if len(cells) == 0:
			return 'd';
		a,b = cells[random.randrange(len(cells))]
		temp_board[a][b] = flag
		
		temp_block, updated_block = self.update_overall_board(temp_board, temp_block, (a, b), flag)
		verdict, comment = self.terminal_state_reached(temp_board, temp_block)
		if verdict:
			temp_board[a][b] = '-'
			
			if(updated_block!=-1):
				temp_block[updated_block] = '-'
			return flag
		if comment == 'Tie':
			temp_board[a][b] = '-'
				
			if(updated_block!=-1):
				temp_block[updated_block] = '-'

			return 'd'
		elif comment == 'D':
			temp_board[a][b] = '-'
			
			if(updated_block!=-1):
				temp_block[updated_block] = '-'

			return 'd'

		#write to append and check
		val = self.carlo(temp_board, temp_block, [a,b], notflag)
		#write to !append
		temp_board[a][b] = '-'
			
		if(updated_block!=-1):
			temp_block[updated_block] = '-'

		return val

class Player40:
	
	def __init__(self):
		pass
	
	def Winning_Heurisitic(self, temp_board, block_stat, flag):
		game_state, message = self.terminal_state_reached(temp_board, block_stat)
		if game_state == True:
			if message != 'D':
				return 100000 if flag == 1 else -100000
			else:
				return 0
		
		start_row, start_col, ret = 0, 0, 0

		if flag == 0:
			flag, opponent_flag = 'x', 'o'
		else:
			flag, opponent_flag = 'o', 'x'

		POSSIBLE_WIN_SEQUENCES = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
		for seq in POSSIBLE_WIN_SEQUENCES:
			temp_seq = [block_stat[index] for index in seq if block_stat[index] != '-' and block_stat[index] != 'd']
			if flag in temp_seq:
				if opponent_flag in temp_seq:
					continue
				if len(temp_seq) > 1:
					ret += 7
				ret += 1
			elif opponent_flag in temp_seq:
				if len(temp_seq) > 1:
					ret -= 7
				ret -= 1
		ret = ret * 23
		
		for i in xrange(9):
			if block_stat[i] == 'd':
				start_col = (start_col + 3) % 9
				if start_col == 0:
					start_row += 3
				continue
			elif block_stat[i] == '-':
				temp_block = [ row[start_row:start_row + 3] for row in temp_board[start_col:start_col+3] ]
				for seq in POSSIBLE_WIN_SEQUENCES:
					temp_seq = [temp_block[index/3][index%3] for index in seq if temp_block[index/3][index%3] != '-']
					if flag in temp_seq:
						if opponent_flag in temp_seq:
							continue
						if len(temp_seq) > 1:
							ret += 7
						ret += 1
					elif opponent_flag in temp_seq:
						if len(temp_seq) > 1:
							ret -= 7
						ret -= 1
			elif flag == block_stat[i]:
				ret += 8
			else:
				ret -= 8
			
			start_col = (start_col + 3) % 9
			if start_col == 0:
				start_row += 3

		for i in [0, 2, 6, 8]:
			if block_stat[i] == flag:
				ret += 2
			else:
				ret -= 2
		return ret

	def get_blocks(self, temp_board, temp_block, old_move):
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
		return self.get_empty_cells(temp_board, blocks_allowed,temp_block)

	def terminal_state_reached(self, game_board, block_stat):
		#Check if game is won!
		## Row win
		if (block_stat[0] == block_stat[1] and block_stat[1] == block_stat[2] and block_stat[1]!='-' and block_stat[1]!='d') or (block_stat[3]!='d' and block_stat[3]!='-' and block_stat[3] == block_stat[4] and block_stat[4] == block_stat[5]) or (block_stat[6]!='d' and block_stat[6]!='-' and block_stat[6] == block_stat[7] and block_stat[7] == block_stat[8]):
			return True, 'W'
		## Col win
		elif (block_stat[0]!='d' and block_stat[0] == block_stat[3] and block_stat[3] == block_stat[6] and block_stat[0]!='-') or (block_stat[1]!='d'and block_stat[1] == block_stat[4] and block_stat[4] == block_stat[7] and block_stat[4]!='-') or (block_stat[2]!='d' and block_stat[2] == block_stat[5] and block_stat[5] == block_stat[8] and block_stat[5]!='-'):
			return True, 'W'
		## Diag win
		elif (block_stat[0] == block_stat[4] and block_stat[4] == block_stat[8] and block_stat[0]!='-' and block_stat[0]!='d') or (block_stat[2] == block_stat[4] and block_stat[4] == block_stat[6] and block_stat[2]!='-' and block_stat[2]!='d'):
			return True, 'W'
		else:
			smflag = 0
			for i in range(9):
				for j in range(9):
					if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
						smflag = 1
						break
			if smflag == 1:
			#Game is still on!
				return False, 'Continue'
			else:
				return False, 'Tie'

	def update_overall_board(self, game_board, block_stat, move_ret, fl):
		#check if we need to modify block_stat
		block_no = (move_ret[0]/3)*3 + move_ret[1]/3
		updated_block, id1, id2, mflg = -1, block_no/3, block_no%3, 0
		if block_stat[block_no] == '-':
			if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-':
				mflg=1
			if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-':
				mflg=1
			
			### col-wise
			if mflg != 1:
				for i in range(id2*3,id2*3+3):
					if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
						mflg = 1
						break
			### row-wise
			if mflg != 1:
				for i in range(id1*3,id1*3+3):
					if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
						mflg = 1
						break
		
		if mflg == 1:
			block_stat[block_no], updated_block = fl, block_no
			return [block_stat, updated_block]
		
		#check for draw on the block if not modified
		flag = 0
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if game_board[i][j] == '-':
					flag = 1
					break
		if flag == 0:
			#Draw
			block_stat[block_no], updated_block = 'd', block_no 
		return [block_stat, updated_block]

	def alpha_beta_pruning(self, temp_board, board_stat, old_move, alpha, beta, flag, depth):
		if(depth == 4):
			'''
				Heuristic
			'''
			return [old_move[0], old_move[1], self.Winning_Heurisitic(temp_board, board_stat, flag)]
			
		cells = self.get_blocks(temp_board, board_stat, old_move)
		
		symbol = 'o' if flag else 'x'
		if depth%2 == 0:
			'''Max Node'''
			max_list = [-1, -1 , -100000]
			for i in cells:
				a, b = i
				temp_board[a][b] = symbol

				board_stat, updated_block = self.update_overall_board(temp_board, board_stat, (a, b), symbol)
				game_state, message = self.terminal_state_reached(temp_board, board_stat)
				if game_state:
					temp_board[a][b] = '-'
					if updated_block!=-1:
						board_stat[updated_block] = '-'
					return [a, b, 10000]
				
				val = self.alpha_beta_pruning(temp_board, board_stat, (a,b), alpha, beta, flag^1, depth+1)
				
				if( val[2] > max_list[2]):
					max_list[0], max_list[1], max_list[2] = a, b, val[2]
				
				alpha = max(alpha, max_list[2])
				temp_board[a][b] = '-'

				if updated_block != -1:
					board_stat[updated_block] = '-'

				if(beta <= alpha):
					break
			return max_list
		else:
			'''Min Node'''
			min_list = [-1, -1 , 100000]
			for i in cells:
				a, b = i
				temp_board[a][b] = symbol
				
				board_stat, updated_block = self.update_overall_board(temp_board, board_stat, (a, b), symbol)
				game_state, message = self.terminal_state_reached(temp_board, board_stat)
				if game_state:
					temp_board[a][b] = '-'
					if updated_block!=-1:
						board_stat[updated_block] = '-'
					return [a, b, -10000]
				
				val = self.alpha_beta_pruning(temp_board, board_stat, (a,b), alpha, beta, flag^1, depth+1)
				
				if( val[2] <= min_list[2]):
					min_list[0], min_list[1], min_list[2] = a, b, val[2]
				
				beta = min(beta, min_list[2])
				temp_board[a][b] = '-'
				if updated_block != -1:
					board_stat[updated_block] = '-'

				if(beta <= alpha):
					break
			return min_list

	def move(self, temp_board, temp_block, old_move, flag):
		flag = 1 if flag == 'x' else 0
		cell = tuple(self.alpha_beta_pruning(temp_board, temp_block, old_move, -10**6-1, 10**6, flag, 0)[0:2])
		if cell[0] == -1 or cell[1] == -1:
			cells = self.get_blocks(temp_board, temp_block, old_move)
			return cells[random.randrange(len(cells))] 
		return cell

	def get_empty_cells(self,gameb, blal, block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1, id2 = idb/3, idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			for i in range(9):
				for j in range(9):
					no = (i/3)*3 + j/3
					if gameb[i][j] == '-' and block_stat[no] == '-':
						cells.append((i,j))	
		return cells


class Player2:
	
	def __init__(self):
		pass
	def move(self,temp_board,temp_block,old_move,flag):
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
		cells = get_empty_out_of(temp_board,blocks_allowed,temp_block)
		return cells[random.randrange(len(cells))]

class Player3:
	
	def __init__(self):
		pass
	
	def Winning_Heurisitic(self, temp_board, block_stat, flag):
		
		gamestate, msg = self.terminal_state_reached(temp_board, block_stat)
		if gamestate == True:
			if msg != 'D':
				return 10**6 if flag == 1 else -10**6
			else:
				return 0
		
		start_row, start_col = 0, 0
		count, count2 = 0, 0
		if flag == 0:
			flag, opponent_flag = 'x', 'o'
		else:
			flag, opponent_flag = 'o', 'x'

		POSSIBLE_WIN_SEQUENCES = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
		for seq in POSSIBLE_WIN_SEQUENCES:
			temp_seq = [block_stat[index] for index in seq if block_stat[index] != '-']
			if flag in temp_seq:
				if opponent_flag in temp_seq:
					continue
				if len(temp_seq) > 1:
					count += 7
				count += 1
			elif opponent_flag in temp_seq:
				if len(temp_seq) > 1:
					count2 += 7
				count2 += 1

		ret = (count - count2) * 23
		
		for i in xrange(9):
			if block_stat[i] == '-':
				temp_block = [ row[start_row:start_row + 3] for row in temp_board[start_col:start_col+3] ]
				count, count2 = 0, 0
				opponent_flag = 'x' if flag == 'o' else 'o'
				for seq in POSSIBLE_WIN_SEQUENCES:
					temp_seq = [temp_block[index/3][index%3] for index in seq if temp_block[index/3][index%3] != '-']
					if flag in temp_seq:
						if opponent_flag in temp_seq:
							continue
						if len(temp_seq) > 1:
							count += 7
						count += 1
					elif opponent_flag in temp_seq:
						if len(temp_seq) > 1:
							count2 += 7
						count2 += 1
				ret += count2 - count
			elif flag == block_stat[i]:
				if flag == 'x':
					ret += 7
				else:
					ret -= 7
			else:
				if flag == 'x':
					ret -= 7
				else:
					ret += 7	
			
			start_col = (start_col + 3) % 9
			if start_col == 0:
				start_row += 3

		return ret

	def blocks(self, temp_board, temp_block, old_move):
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

	def terminal_state_reached(self, game_board, block_stat):

		#Check if game is won!
		bs = block_stat
		## Row win
		if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		#	print block_stat
			return True, 'W'
		## Col win
		elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		#   print block_stat
			return True, 'W'
		## Diag win
		elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		#	print block_stat
			return True, 'W'
		else:
			smfl = 0
			for i in range(9):
				for j in range(9):
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
	                                for i in range(len(game_board)):
	                                    for j in range(len(game_board[i])):
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
	                    for i in range(id2*3,id2*3+3):
	                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
	                                mflg = 1
	                                break

	                ### row-wise
			if mflg != 1:
	                    for i in range(id1*3,id1*3+3):
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
		for i in range(id1*3,id1*3+3):
		    for j in range(id2*3,id2*3+3):
			if game_board[i][j] == '-':
			    cells.append((i,j))

	        if cells == [] and mflg!=1:
	            block_stat[block_no] = 'd' #Draw
	            updated_block = block_no
	        
	        return [block_stat, updated_block]

	def alpha_beta_pruning(self, temp_board, board_stat, old_move, alpha, beta, flag, depth):

		cells = self.blocks(temp_board, board_stat, old_move)
		
		if(depth == 4):
			'''
				Heuristic
			'''
			'''util = 10**7 if flag else -10**7 - 1
			best_move = old_move
			for i in cells:
				a, b  = i
				temp_board[a][b] = 'o' if flag else 'x'
				temp = self.Winning_Heurisitic(temp_board, board_stat, (a, b), flag)
				if flag:
					if temp < util:
						best_move = (a, b)
						util = temp
				else:
					if temp > util:
						best_move = (a, b)
						util = temp	
				temp_board[a][b] = '-'
			if best_move == old_move:
				return [old_move[0], old_move[1], 0] 
			return [best_move[0], best_move[1], util]
			'''
			return [old_move[0], old_move[1], self.Winning_Heurisitic(temp_board, board_stat, flag)]
			
		symbol = 'o' if flag else 'x'
		if depth%2 == 0:
			'''Max Node'''
			maxv = [-1, -1 , -100000]
			for i in cells:
				a, b = i
				temp_board[a][b] = symbol

				board_stat, updated_block = self.update_overall_board(temp_board, board_stat, (a, b), symbol)
				gamestate, msg = self.terminal_state_reached(temp_board, board_stat)
				if gamestate:
					temp_board[a][b] = '-'
					if updated_block!=-1:
						board_stat[updated_block] = '-'
					return [a, b, 10000]
				
				val = self.alpha_beta_pruning(temp_board, board_stat, (a,b), alpha, beta, flag^1, depth+1)
				
				if( val[2] > maxv[2]):
					maxv[0], maxv[1], maxv[2] = a, b, val[2]
				
				alpha = max(alpha, maxv[2])
				temp_board[a][b] = '-'

				if updated_block != -1:
					board_stat[updated_block] = '-'

				if(beta <= alpha):
					break
			return maxv
		else:
			'''Min Node'''
			minv = [-1, -1 , 100000]
			for i in cells:
				a, b = i
				temp_board[a][b] = symbol
				
				board_stat, updated_block = self.update_overall_board(temp_board, board_stat, (a, b), symbol)
				gamestate, msg = self.terminal_state_reached(temp_board, board_stat)
				if gamestate:
					temp_board[a][b] = '-'
					if updated_block!=-1:
						board_stat[updated_block] = '-'
					return [a, b, -10000]
				
				val = self.alpha_beta_pruning(temp_board, board_stat, (a,b), alpha, beta, flag^1, depth+1)
				
				if( val[2] <= minv[2]):
					minv[0], minv[1], minv[2] = a, b, val[2]
				
				beta = min(beta, minv[2])
				temp_board[a][b] = '-'

				if updated_block != -1:
					board_stat[updated_block] = '-'

				if(beta <= alpha):
					break
			return minv

	def move(self, temp_board, temp_block, old_move, flag):
		flag = 1 if flag == 'x' else 0
		cell = tuple(self.alpha_beta_pruning(temp_board, temp_block, old_move, -10**7-1, 10**7, flag, 0)[0:2])
		if cell[0] == -1 or cell[1] == -1:
			cells = self.blocks(temp_board, temp_block, old_move)
			return cells[random.randrange(len(cells))] 
		print "Us: ", flag, cell[0], cell[1]
		return cell

	def get_empty_cells_out_of(self,gameb, blal, block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			for i in range(9):
				for j in range(9):
					no = (i/3)*3
					no += (j/3)
					if gameb[i][j] == '-' and block_stat[no] == '-':
						cells.append((i,j))	
		return cells

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		for i in range(9):
			for j in range(9):
                                no = (i/3)*3
                                no += (j/3)
				if gameb[i][j] == '-' and block_stat[no] == '-':
					cells.append((i,j))	
	return cells
		
# Note that even if someone has won a block, it is not abandoned. But then, there's no point winning it again!
# Returns True if move is valid
def check_valid_move(game_board,block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True


	for_corner = [0,2,3,5,6,8]

	#List of permitted blocks, based on old move.
	blocks_allowed  = []

	if old_move[0] in for_corner and old_move[1] in for_corner:
		## we will have 3 representative blocks, to choose from

		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			## top left 3 blocks are allowed
			blocks_allowed = [0,1,3]
		elif old_move[0] % 3 == 0 and old_move[1] in [2,5,8]:
			## top right 3 blocks are allowed
			blocks_allowed = [1,2,5]
		elif old_move[0] in [2,5,8] and old_move[1] % 3 == 0:
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

        #Check if the block is won, or completed. If so you cannot move there. 

        for i in reversed(blocks_allowed):
            if block_stat[i] != '-':
                blocks_allowed.remove(i)
        
        # We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
        cells = get_empty_out_of(game_board, blocks_allowed,block_stat)

	#Checks if you made a valid move. 
        if current_move in cells:
     	    return True
        else:
    	    return False

def update_lists(game_board, block_stat, move_ret, fl):
	#move_ret has the move to be made, so we modify the game_board, and then check if we need to modify block_stat
	game_board[move_ret[0]][move_ret[1]] = fl

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
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-':
                                mflg = 1
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-':
                                mflg = 1
                                break

	
	if mflg == 1:
		block_stat[block_no] = fl
	
        #check for draw on the block.

        id1 = block_no/3
	id2 = block_no%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if game_board[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            block_stat[block_no] = 'd' #Draw
        
        return

def terminal_state_reached(game_board, block_stat):
	
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
		for i in range(9):
			for j in range(9):
				if game_board[i][j] == '-' and block_stat[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
                        #Game is still on!
			return False, 'Continue'
		
		else:
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
                                for i in range(len(game_board)):
                                    for j in range(len(game_board[i])):
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


def decide_winner_and_get_message(player,status, message):
	if player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NO ONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list, block_stat is a 1D list of 9 elements
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2

	### basically, player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''

        #Make your move in 6 seconds!
	TIMEALLOWED = 6

	print_lists(game_board, block_stat)

	while(1):

		# Player1 will move
		#time.sleep(5);
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player1 to complete in TIMEALLOWED secs. 
		try:
			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)
	
                #Checking if list hasn't been modified! Note: Do not make changes in the lists passed in move function!
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			#Player1 loses - he modified something
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the move made is valid
		if not check_valid_move(game_board, block_stat,ret_move_pl1, old_move):
			## player1 loses - he made the wrong move.
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl

                #So if the move is valid, we update the 'game_board' and 'block_stat' lists with move of pl1
                update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

                # Now player2 plays
               #	time.sleep(5);
                temp_board_state = game_board[:]
                temp_block_stat = block_stat[:]


		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
		except TimedOutExc as e:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
                if not check_valid_move(game_board, block_stat,ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
                
                update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat)
                if gamestatus == True:
			print_lists(game_board, block_stat)
                        WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
                        break
		old_move = ret_move_pl2
		print_lists(game_board, block_stat)
	
	print WINNER + " won!"
	print MESSAGE


if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player32()
		obj2 = Player40()

	elif option == '2':
		obj1 = Player32()
		obj2 = Manual_player()
	elif option == '3':
		obj1 = Manual_player()
		obj2 = Manual_player()
        
        # Deciding player1 / player2 after a coin toss
        # However, in the tournament, each player will get a chance to go 1st. 
        num = random.uniform(0,1)
        if num > -1.5:
		simulate(obj2, obj1)
	else:
		simulate(obj1, obj2)
