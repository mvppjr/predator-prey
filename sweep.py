import libpyAI as ai
import math

class Helper:

	def __init__(self):
		self.coordinateList = [(300, 300), (200,800), (800, 800), (900, 300)]
		self.coordListLength = len(self.coordinateList)
		self.counter = 0
		self.frames = 0

		ai.start(self.AI_loop,["-name","Dumbodore","-join","localhost"])

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
		# toTurn = (heading - angleDiffDegrees)%360
		toTurn = ai.angleDiff(heading, int(angleDiffDegrees))
		return toTurn

	def AI_loop(self):

		# Release keys
		ai.thrust(0)
		ai.turnLeft(0)
		ai.turnRight(0)
		# ai.setPower(30)

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
		targetX = self.coordinateList[self.counter%self.coordListLength][0]
		targetY = self.coordinateList[self.counter%self.coordListLength][1]

		toTurn = self.angleToPoint(x,y,targetX,targetY,heading)
		distance = self.distance(x,targetX,y,targetY)
		
		
		#-------------------- Print statements --------------------#
		print("(x, y): (",x,",",y,")")
		print("destination: ", self.coordinateList[self.counter%self.coordListLength])
		print("distance: ", distance)
		# print("closestEnemyX: ", closestEnemyX)
		# print("closestEnemyY: ", closestEnemyY)
		# print("difference x: ", differenceX)
		# print("difference y: ", differenceY)
		# print("degrees: ", degrees)
		# print("screen enemy? ", ai.screenEnemyXId(ai.closestShipId()))
		print("toTurn: ", toTurn)
		print()		

		#-------------------- Move to target point --------------------#
		# if toTurn > 0 and toTurn < 30 and distance > 300 and speed <= 15 and speed >= 4:
		if abs(toTurn) < 20 and distance > 200:
			print("Lock!")
			ai.turnLeft(0)
			ai.turnRight(0)
			if self.frames % 40 == 0:
				ai.thrust(1)
		elif toTurn >= 20:
			print("Turning right!")
			ai.turnLeft(1)
		elif toTurn <= -20:
			ai.turnRight(1)
			print("Turning left!")
		if distance < 200:
			# ai.thrust(0)
			self.counter = self.counter + 1

		# #-------------------- Thrust rules --------------------#
		# if speed <= 3 and frontWall >= 200:
		# 	print("Front wall far")
		# 	ai.thrust(1)
		# elif trackWall < 50:
		# 	print("Close to track wall")
		# 	ai.thrust(1)
		# elif backWall < 40:
		# 	print("Close to back wall")
		# 	ai.thrust(1)

		# #---------------- Turn rules ----------------#

		# # Figures out what corner we are in and turns the right directon 
		# if (backWall < 30) and (rightWallStraight < 200):
		# 	print("Corners 1")
		# 	ai.turnLeft(1)
		# elif backWall < 30 and (leftWallStraight < 200):
		# 	print("Corners 2")
		# 	ai.turnRight(1)

		# # Walls along our periphery (90 degree feelers)
		# elif leftWallStraight < rightWallStraight and trackWall < 75:
		# 	print("90 left danger")
		# 	ai.turnRight(1)
		# elif leftWallStraight > rightWallStraight and trackWall < 75:
		# 	print("90 right danger")
		# 	ai.turnLeft(1)


		self.frames = self.frames + 1
		
	
Helper()