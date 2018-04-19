import libpyAI as ai
import math

class Helper:

	def __init__(self):
		self.coordinateList = [(300, 300), (200,800), (800, 800), (900, 300)]
		self.coordListLength = len(self.coordinateList)
		self.counter = 0

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
		toTurn = (heading - angleDiffDegrees)%360
		return toTurn

	def foundPrey(self, coordinate):
		message = "*** " + str(coordinate)
		ai.talk(message)

	def lostPrey(self):
		message = "--- Lost the enemy!"
		ai.talk(message)

	def AI_loop(self):

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
		message = ai.scanMsg(0)
		x = ai.selfX()
		y = ai.selfY()

		if "***" in message:
			coordMessage = message.split("***")[1]
			coordinatesString = coordMessage.strip().split(" [")[0]
			coordinates = eval(coordinatesString)
			

			closestEnemyX = coordinates[0]
			closestEnemyY = coordinates[1]
			toTurn = self.angleToPoint(x, y, closestEnemyX, closestEnemyY, heading)
			distance = self.distance(x,closestEnemyX,y,closestEnemyY)

			#-------------------- Move to target point --------------------#
			if toTurn > 0 and toTurn < 20 and distance > 300:
				ai.thrust(1)
				ai.turnLeft(0)
				ai.turnRight(0)
			elif toTurn >= 20:
				ai.turnRight(1)
			elif toTurn <= 0:
				ai.turnLeft(1)

		if self.counter % 300 == 0:
			self.foundPrey((900,400))


		self.counter = self.counter + 1

Helper()