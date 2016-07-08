from cocos.sprite import Sprite


class Paddle(object):
    def __init__(self, imagepath):
        super(Paddle, self).__init__()
        self.sprite = Sprite(imagepath, anchor=(0, 0))
        self.speed = 10
        self.move_left = False
        self.move_right = False

    def reset(self):
        self.sprite.position = (270, 0)

    def update(self):
        x, y = self.sprite.position
        if self.move_left:
            x -= self.speed
        if self.move_right:
            x += self.speed
        #
        if x < 0:
            x = 0
        if x + self.sprite.width > 640:
            x = 640 - self.sprite.width
        self.sprite.set_position(x, y)

