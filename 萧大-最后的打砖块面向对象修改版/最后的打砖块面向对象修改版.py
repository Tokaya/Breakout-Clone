import cocos
from cocos import scene
from cocos.layer import Layer
from cocos.director import director
from cocos.sprite import Sprite
from cocos.text import Label
# from cocos.rect import Sprite
from pyglet.window.key import symbol_string
from cocos.scene import Scene
from paddle import Paddle
from ball import Ball
from cocos.scenes import FadeTransition
from cocos.scenes import SplitColsTransition
from level import level_from_file
from util import collides
from random import randint
# 打砖块游戏步骤
# 1，只能上下移动
# 2，限定移动范围
# 3，初始化一个小球
# 4，让球运动
# 5，添加发射的功能（按了按键，球才发射）
# 6，球发射之前，让它跟着板子一起走
# 7，让挡板来接球，否则就游戏结束
# 8，挡板接球一次，就金币 +1
# 9，添加一个 HUD(heads up display)，来显示金币数量
# 10，添加一个砖块，并显示出来
# 11，添加球和砖块的碰撞检测，并且让砖块消失
# 12，添加 3 个砖块
# 13，游戏结束后，重置游戏
# 14，关卡载入

# 关卡文件该如何配置呢？
# 首先，分析不同关卡的变化
# 关卡一共有两个数据来定义
# 1，砖块的数量
# 2，砖块的 x y 坐标


class GameLayer(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__(246, 226, 76, 255)
        # 添加一个 板子
        self.paddle = Paddle('images/ban.png')
        self.add(self.paddle.sprite)
        self.ball = Ball('images/qiu.png')
        self.add(self.ball.sprite)

        # 添加一个 label 显示当前的游戏状态
        self.hud = Label('金币: 0',
                         color=(0, 0, 0, 255))
        self.hud.position = (0, 450)
        self.add(self.hud)
        # 添加一个变量来记录金币
        self.gold = 0
        # 设置 4 个按键状态
        self.key_pressed_left   = False
        self.key_pressed_right  = False
        self.key_pressed_up     = False
        self.key_pressed_down   = False

        self.blocks = []
        # 调用 reset 函数初始化状态
        self.reset()
        # 定期调用 self.update 函数
        # FPS frame per second 每秒帧数
        self.schedule(self.update)

    def reset(self):
        self.gold = 0
        self.update_hud()
        self.paddle.reset()
        self.ball.reset()

        # 添加砖块并且显示出来
        # 先删除残存的砖块
        for b in self.blocks:
            self.remove(b)
        # 再初始化新的砖块
        self.blocks = []
        levelfile = 'level1.txt'
        positions = level_from_file(levelfile)
        number_of_blocks = len(positions)
        for i in range(number_of_blocks):
            b = Sprite('images/zhuan.png', anchor=(0, 0))
            b.position = positions[i]
            b.color = (randint(0, 255), randint(0, 255), randint(0, 255))
            # b.position = (randint(0, 500), 400)
            self.add(b)
            self.blocks.append(b)

    def game_over(self):
        print('游戏结束，跪了。金币是', self.gold)
        self.reset()

    def update_hud(self):
        self.hud.element.text = '金币：' + str(self.gold)

    def update_blocks(self):
        # 判断是否撞到了砖块
        for b in self.blocks:
            if collides(self.ball.sprite, b):
                # self.ball_speedy = -self.ball_speedy
                self.ball.hit()
                self.remove(b)
                self.blocks.remove(b)
                self.gold += 1
                # self.speed += 1
                self.update_hud()
                print('金币', self.gold)
                break

    def update_ball(self):
        if self.ball.fired:
            self.ball.update()
        else:
            bx, by = self.ball.sprite.position
            px, py = self.paddle.sprite.position
            self.ball.sprite.position = (px, by)

        collide = collides(self.ball.sprite, self.paddle.sprite)
        if collide:
            self.ball.hit()
        if self.ball.dead():
            self.game_over()

    def update_paddle(self):
        self.paddle.update()

    def update_input(self):
        self.paddle.move_left = self.key_pressed_left
        self.paddle.move_right = self.key_pressed_right
        if self.key_pressed_up:
            self.ball.fire()

    # 这个函数每帧都会被调用
    def update(self, dt):
        self.update_input()
        # 更新挡板
        self.update_paddle()
        # 更新球的位置
        self.update_ball()
        # 更新砖块
        self.update_blocks()

    def on_key_press(self, key, modifiers):
        k = symbol_string(key)
        status = True
        if k == "LEFT":
            self.key_pressed_left = status
        elif k == "RIGHT":
            self.key_pressed_right = status
        elif k == "UP":
            self.key_pressed_up = status

    def on_key_release(self, key, modifiers):
        k = symbol_string(key)
        print('release', k)
        if k == "LEFT":
            self.key_pressed_left = False
        if k == "RIGHT":
            self.key_pressed_right = False
        if k == "UP":
            self.key_pressed_up = False


if __name__ == '__main__':
    director.init()
    director.run(scene.Scene(GameLayer()))
