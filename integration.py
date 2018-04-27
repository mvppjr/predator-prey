import libpyAI as ai
import math

class Helper:

	def __init__(self, name):
		self.grid = [ ["", (100, 100)], ["", (300, 100)], ["", (500, 100)], ["", (700, 100)], ["", (900, 100)],
					["", (900, 250)], ["", (700, 250)], ["", (500, 250)], ["", (300, 250)], ["", (100, 250)],  
					["", (100, 450)], ["", (300, 450)], ["", (500, 450)], ["", (700, 450)], ["", (900, 450)],
					["", (900, 650)], ["", (700, 650)], ["", (500, 650)], ["", (300, 650)], ["", (100, 650)], 
					["", (100, 850)], ["", (300, 850)], ["", (500, 850)], ["", (700, 850)], ["", (900, 850)]]	
		self.name = name 
		self.gridLength = len(self.grid)
		self.counter = 0
		self.frames = 0
		self.team = False 
		self.MessageBuffer = ["Blah blah blah"]

		ai.start(self.AI_loop,["-name",name,"-join","localhost"])

	def checkSearchComplete(self):
		counter = 0
		for spot in self.grid:
			if spot[0] == "checked!":
				counter = counter + 1
		if counter == self.gridLength:
			self.counter = 0			

			# clears grids
			for spot in self.grid:
				spot[0] = ""

			return True
		else: 
			return False 		

	def markSpotChecked(self, coordinate, flag):
		for spot in self.grid:
			if spot[1] == coordinate:
				spot[0] = "checked!"
				finished = self.checkSearchComplete()
				if finished != True and flag == "me":
					while self.grid[self.counter][0] == "checked!":
						self.counter = (self.counter + 1) % self.gridLength

					print("destination: ", self.grid[self.counter][1])

	def foundPrey(self, coordinate):
		message = "*** " + str(coordinate)
		ai.talk(message)

	def lostPrey(self):
		message = "--- Lost the enemy!"
		ai.talk(message)

	def checkMessage(self, message):

		splitMessage = message.split(" ")
		
		# Checks if message is sent by one of the predators
		if "[" in splitMessage[-1]:
			sender = splitMessage[-1][1:-1]

			# Checks if message wasn't sent by itself
			if sender != self.name:

				# Another grid coordinate checked
				if splitMessage[0] == "checked!":

					coordinate = str(eval(splitMessage[1]))
					self.markSpotChecked(coordinate, "not me")
					self.checkSearchComplete()

		self.MessageBuffer.append(message)


	def angleDiff(self, a1, a2):
		return 180 - abs( abs(a1 - a2) - 180)

	def distance(self, xi, xii, yi, yii):
	    sq1 = (xi-xii)*(xi-xii)
	    sq2 = (yi-yii)*(yi-yii)
	    return math.sqrt(sq1 + sq2)

	def angleToPoint(self, x, y, targetX, targetY, heading):
		differenceX = targetX - x
		differenceY = targetY - y
		angleDiffRad = math.atan2(differenceY, differenceX)
		angleDiffDegrees = math.degrees(angleDiffRad)
		toTurn = ai.angleDiff(heading, int(angleDiffDegrees))
		return toTurn

	def AI_loop(self):

		if self.team == False:
			ai.talk("/team 2")
			self.team = True

		# Release keys
		ai.thrust(0)
		ai.turnLeft(0)
		ai.turnRight(0)

		#-------------------- Set variables --------------------#
		heading = int(ai.selfHeadingDeg())
		tracking = int(ai.selfTrackingDeg())
		frontWall = ai.wallFeeler(500,heading)
		leftWall = ai.wallFeeler(500,heading+45)
		rightWall = ai.wallFeeler(500,heading-45)
		leftWallStraight = ai.wallFeeler(500,heading+90)
		rightWallStraight = ai.wallFeeler(500,heading-90)
		leftBack = ai.wallFeeler(500,heading+135)
		rightBack = ai.wallFeeler(500,heading-135)
		backWall = ai.wallFeeler(500,heading-180)
		trackWall = ai.wallFeeler(500,tracking)
		R = (heading-90)%360
		L = (heading+90)%360
		aim = ai.aimdir(0)
		bullet = ai.shotAlert(0)
		speed = ai.selfSpeed()
		x = ai.selfX()
		y = ai.selfY()
		coordinate = self.grid[self.counter][1]
		targetX = coordinate[0]
		targetY = coordinate[1]
		toTurn = self.angleToPoint(x,y,targetX,targetY,heading)
		distance = self.distance(x,targetX,y,targetY)
		message = ai.scanMsg(0)

		if message != self.MessageBuffer[-1]:
			self.checkMessage(message)


		if speed > 5:
			turning = ai.angleDiff(heading, tracking)
			if abs(turning) > 165 and abs(turning) <= 180:
				ai.turnLeft(0)
				ai.turnRight(0)
				if self.frames % 10 == 0:
					ai.thrust(1)
			elif abs(turning) <= 165:
				ai.turnRight(1)
			elif negateAngle >= 10:
				ai.turnLeft(1)

		else: 

			#-------------------- Print statements --------------------#
			# print("(x, y): (",x,",",y,")")
			# print("destination: ", self.grid[self.counter%self.gridLength])
			# print("distance: ", distance)
			# print("closestEnemyX: ", targetX)
			# print("closestEnemyY: ", targetY)
			# print("screen enemy? ", ai.screenEnemyXId(ai.closestShipId()))
			# print("toTurn: ", toTurn)
			# print("speed: ", speed)
			# print("")

			#-------------------- Move to target point --------------------#
			if abs(toTurn) < 10 and distance > 100:
				# print("Lock!")
				ai.turnLeft(0)
				ai.turnRight(0)
				if self.frames % 3 == 0:
					ai.thrust(1)
			elif toTurn >= 10:
				ai.turnLeft(1)
			elif toTurn <= -10:
				ai.turnRight(1)
			if distance < 150:
				self.markSpotChecked(coordinate, "me")
				ai.talk("checked! " + str(coordinate))


			#-------------------- Thrust rules --------------------#
			if speed <= 3 and frontWall >= 200:
				ai.thrust(1)
			elif trackWall < 50:
				ai.thrust(1)
			elif backWall < 40:
				ai.thrust(1)

			#---------------- Turn rules ----------------#

			# Figures out what corner we are in and turns the right directon 
			if (backWall < 30) and (rightWallStraight < 200):
				ai.turnLeft(1)
			elif backWall < 30 and (leftWallStraight < 200):
				ai.turnRight(1)

			# Walls along our periphery (90 degree feelers)
			elif leftWallStraight < rightWallStraight and trackWall < 75:
				ai.turnRight(1)
			elif leftWallStraight > rightWallStraight and trackWall < 75:
				ai.turnLeft(1)


		self.frames = self.frames + 1
		
	
Helper("SiriusBot")
