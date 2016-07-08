def intesects(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return x1 + w1 > x2 and x2 + w2 > x1 and \
           y1 + h1 > y2 and y2 + h2 > y1


def rect_of_sprite(s):
    x, y = s.position
    w, h = s.width, s.height
    return [x, y, w, h]


def collides(sprite1, sprite2):
    rect1 = rect_of_sprite(sprite1)
    rect2 = rect_of_sprite(sprite2)
    return intesects(rect1, rect2)
