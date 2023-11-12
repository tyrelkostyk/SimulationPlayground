import pygame as game
import math

from common import *

class Particle(game.sprite.Sprite):

    def __init__(self, size, startingPosition=None, velocity=None, acceleration=None, dampening=None):
        super().__init__()

        self.radius = size

        # starting position
        self.positionX = 0
        self.positionY = 0
        if startingPosition is not None:
            self.positionX = startingPosition[0]
            self.positionY = startingPosition[1]

        # starting velocity
        self.velocityX = 0
        self.velocityY = 0
        if velocity is not None:
            self.velocityX = velocity[0]
            self.velocityY = velocity[1]

        # starting acceleration
        self.accelerationX = 0
        self.accelerationY = 9.81
        if acceleration is not None:
            self.accelerationX = acceleration[0]
            self.accelerationY = acceleration[1]

        self.dampening = 0.85
        # self.mass = math.pi * (self.radius * self.radius)
        self.mass = self.radius

    def draw(self, screen):
        game.draw.circle(screen, WHITE, (self.positionX, self.positionY), self.radius, width=0)

    def update(self, particles):
        self.velocityX += self.accelerationX / TICKS_PER_SECOND
        self.velocityY += self.accelerationY / TICKS_PER_SECOND

        self.positionX += self.velocityX
        self.positionY += self.velocityY

        for otherParticle in particles:
            if self is not otherParticle:
                self.handleCollision(otherParticle)

        if self.positionX + self.radius > WINDOW_WIDTH:
            self.positionX = WINDOW_WIDTH - self.radius
            self.velocityX *= -1 * self.dampening
        if self.positionX - self.radius < 0:
            self.positionX = 0 + self.radius
            self.velocityX *= -1 * self.dampening

        if self.positionY + self.radius > WINDOW_WIDTH:
            self.positionY = WINDOW_WIDTH - self.radius
            self.velocityY *= -1 * self.dampening
        if self.positionY - self.radius < 0:
            self.positionY = 0 + self.radius
            self.velocityY *= -1 * self.dampening

    def handleCollision(self, otherParticle):
        deltX = self.positionX - otherParticle.positionX
        deltaY = self.positionY - otherParticle.positionY
        distance = math.hypot(deltX, deltaY)
        combined_radii = self.radius + otherParticle.radius

        # not colliding
        if distance >= combined_radii:
            return

        theta = math.atan2(deltaY, deltX)

        # correct the overlap
        overlap = combined_radii - distance
        self.positionX += math.cos(theta) * overlap / 2
        self.positionY += math.sin(theta) * overlap / 2
        otherParticle.positionX -= math.cos(theta) * overlap / 2
        otherParticle.positionY -= math.sin(theta) * overlap / 2

        # adjust the new velocities after impact
        relativeVelocityX = self.velocityX - otherParticle.velocityX
        relativeVelocityY = self.velocityY - otherParticle.velocityY

        impulse = 2 * (self.mass * otherParticle.mass) / (self.mass + otherParticle.mass) * (relativeVelocityX * math.cos(theta) + relativeVelocityY * math.sin(theta))

        self.velocityX -= (impulse / self.mass) * math.cos(theta) * self.dampening
        self.velocityY -= (impulse / self.mass) * math.sin(theta) * self.dampening
        otherParticle.velocityX += (impulse / otherParticle.mass) * math.cos(theta) * otherParticle.dampening
        otherParticle.velocityY += (impulse / otherParticle.mass) * math.sin(theta) * otherParticle.dampening


