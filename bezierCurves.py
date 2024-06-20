import math
import pygame
import pygame.draw
pygame.init()
screenSize = (600, 600)
screen = pygame.display.set_mode(screenSize)
while not pygame.display.get_active():
	time.sleep(0.1)
pygame.display.set_caption("bezier", "bezier")
clock = pygame.time.Clock()
framerate = 60

class Curve:
	def __init__(self, bounds, index):
		self.bounds = bounds# start, control, end
		self.index = index
		self.length = [[bounds[1][0]-bounds[0][0], bounds[1][1]-bounds[0][1]],
					   [bounds[2][0]-bounds[1][0], bounds[2][1]-bounds[1][1]]]
	def adjustLegLength(self):
		self.length = [[self.bounds[1][0]-self.bounds[0][0], self.bounds[1][1]-self.bounds[0][1]],
					   [self.bounds[2][0]-self.bounds[1][0], self.bounds[2][1]-self.bounds[1][1]]]
	def getLegPoints(self, leg, quality):
		points = []
		for i in range(quality+1):
			x = self.bounds[leg][0] + self.length[leg][0]/quality*i
			y = self.bounds[leg][1] + self.length[leg][1]/quality*i
			points.append([x, y])
		return points
	def draw(self, quality):
		#self.bounds[0][0] += 0.5
		#self.adjustLegLength()
		pointsChanged = False
		for i in range(3):
			if self.bounds[i] != points[self.index*3 + i]:
				self.bounds[i] = points[self.index*3 + i]
				pointsChanged = True
		if pointsChanged:
			self.adjustLegLength()

		legPoints = [self.getLegPoints(0, quality), self.getLegPoints(1, quality)]
		for i in range(quality+1):
			pygame.draw.line(screen, (255, 0, 0), legPoints[0][i], legPoints[1][i])

maxCurves = 10
curves = [0 for i in range(maxCurves)]
points = [0 for i in range(maxCurves*3)]

mousePos = [0, 0]

currentCurve = []
closestPoint = None
selectedPoint = None
while True:
	clock.tick(framerate)
	events = pygame.event.get()

	if selectedPoint == None:
		dist = math.inf
		index = None
		for i in range(len(points)):
			if points[i] == 0:
				continue
			distToPoint = (points[i][0] - mousePos[0])**2 + (points[i][1] - mousePos[1])**2
			if distToPoint < dist:
				dist = distToPoint
				index = i
		if index != None:
			closestPoint = index

	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 3:
				selectedPoint = closestPoint
				closestPoint = None

		if event.type == pygame.MOUSEMOTION:
			mousePos = event.pos
			if selectedPoint != None:
				points[selectedPoint] = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				currentCurve.append(list(event.pos))
				if len(currentCurve) == 3:
					if 0 in curves:
						i = curves.index(0)
						curves[i] = Curve(currentCurve, i)
						points[i*3] = currentCurve[0]
						points[i*3+1] = currentCurve[1]
						points[i*3+2] = currentCurve[2]
						currentCurve = []
					else:
						print("too many curves! D:")
						currentCurve = []
			if event.button == 3:
				selectedPoint = None

	screen.fill((0, 0, 0))
	for curve in curves:
		if curve == 0:
			continue
		curve.draw(25)

	for point in currentCurve:
		pygame.draw.circle(screen, (0, 255, 0), point, 5, width=1)

	for i, point in enumerate(points):
		if point == 0:
			continue
		color = (0, 0, 255)
		if i == closestPoint or i == selectedPoint:
			color = (255, 255, 255)
		pygame.draw.circle(screen, color, point, 3, width=1)

	pygame.display.flip()
