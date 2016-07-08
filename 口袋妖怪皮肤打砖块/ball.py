from cocos.sprite import Sprite


class Ball(object):
    def __init__(self, imagepath):
        super(Ball, self).__init__()
        self.sprite = Sprite(imagepath)
        self.fired = False
        self.alive = True
        self.speedx = 5
        self.speedy = 5

    def reset(self):
        self.fired = False
        self.alive = True
        self.sprite.position = (320, 20)

    def fire(self):
        self.fired = True

    def hit(self):
        self.speedy = -self.speedy

    def dead(self):
        return not self.alive

    def update(self):
        if not self.fired:
            return
        s = self.sprite
        ballx, bally = s.position
        if self.fired:
            if ballx + s.width > 640 or ballx < 0:
                self.speedx = -self.speedx
            if bally + s.height > 480:
                self.speedy= -self.speedy
        ballx += self.speedx
        bally += self.speedy
        s.set_position(ballx, bally)
        if bally < 0:
            self.alive = False
