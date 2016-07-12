# coding:utf-8
import cocos
from cocos import scene
from cocos.text import Label
from pyglet.window.key import symbol_string
from paddle import Paddle
from ball import Ball
from cocos.scenes import TurnOffTilesTransition
from level import level_from_file
from util import collides
from random import randint
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.sprite import Sprite
from cocos.actions import *
import LevelCreater


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

class Title(cocos.layer.ColorLayer):
	is_event_handler = True

	def __init__(self):
		super(Title, self).__init__(randint(0, 255), randint(0, 255), randint(0, 255), 255)


class Star(Menu):
	def __init__(self):
		super(Star, self).__init__("Breakout Clone")
		pyglet.font.add_directory('.')
		self.font_title = {
			'text': 'title',
			'font_name': 'ALISON',
			'font_size': 56,
			'color': (255, 255, 255, 255),
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'dpi': 96,
			'x': 0, 'y': 0,
		}

		self.font_item = {
			'font_name': 'ALISON',
			'font_size': 32,
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'color': (192, 192, 192, 255),
			'dpi': 96,
		}
		self.font_item_selected = {
			'font_name': 'ALISON',
			'font_size': 42,
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'color': (255, 255, 255, 255),
			'dpi': 96,
		}
		self.title_height = 0
		items = []
		items.append(MenuItem('New Game', self.on_new_game))
		items.append(MenuItem('Options', self.on_options))
		items.append(MenuItem('Scores', self.on_scores))
		items.append(MenuItem('Level Creater', self.on_creater))
		items.append(MenuItem('Quit', self.on_quit))
		self.create_menu(items, zoom_in(), zoom_out())

	def on_new_game(self):
		scene = Scene(GameLayer())
		director.replace(TurnOffTilesTransition(scene))

	def on_scores(self):
		self.parent.switch_to(2)

	def on_options(self):
		self.parent.switch_to(1)

	def on_creater(self):
		scene = Scene(LevelCreater.LevelCreater())
		director.replace(TurnOffTilesTransition(scene))

	def on_quit(self):
		director.pop()


class OptionMenu(Menu):
	def __init__(self):
		super(OptionMenu, self).__init__("Breakout Clone")
		self.font_title = {
			'text': 'title',
			'font_name': 'ALISON',
			'font_size': 56,
			'color': (192, 192, 192, 255),
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'dpi': 96,
			'x': 0, 'y': 0,
		}

		self.font_item = {
			'font_name': 'ALISON',
			'font_size': 32,
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'color': (192, 192, 192, 255),
			'dpi': 96,
		}
		self.font_item_selected = {
			'font_name': 'ALISON',
			'font_size': 42,
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'color': (255, 255, 255, 255),
			'dpi': 96,
		}
		self.title_height = 0
		self.menu_valign = BOTTOM
		self.menu_halign = RIGHT

		items = []
		items.append(MenuItem('Fullscreen', self.on_fullscreen))
		items.append(ToggleMenuItem('Show FPS: ', self.on_show_fps, True))
		items.append(MenuItem('OK', self.on_quit))
		self.create_menu(items, shake(), shake_back())

	# Callbacks
	def on_fullscreen(self):
		director.window.set_fullscreen(not director.window.fullscreen)

	def on_quit(self):
		self.parent.switch_to(0)

	def on_show_fps(self, value):
		director.show_FPS = value


class ScoreMenu(Menu):
	def __init__(self):
		super(ScoreMenu, self).__init__("Breakout Clone")
		self.font_title = {
			'text': 'title',
			'font_name': 'ALISON',
			'font_size': 56,
			'color': (192, 192, 192, 255),
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'dpi': 96,
			'x': 0, 'y': 0,
		}

		self.font_item = {
			'font_name': 'ALISON',
			'font_size': 32,
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'color': (192, 192, 192, 255),
			'dpi': 96,
		}
		self.font_item_selected = {
			'font_name': 'ALISON',
			'font_size': 42,
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'color': (255, 255, 255, 255),
			'dpi': 96,
		}
		self.title_height = 0
		self.menu_valign = BOTTOM
		self.menu_halign = LEFT

		self.create_menu([MenuItem('Go Back', self.on_quit)])

	def on_quit(self):
		self.parent.switch_to(0)


class GameOver(ColorLayer):
	is_event_handler = True

	def __init__(self):
		super(GameOver, self).__init__(randint(0, 255), randint(0, 255), randint(0, 255), 255)


class OverMenu(Menu):
	def __init__(self):
		super(OverMenu, self).__init__("Game Over")
		pyglet.font.add_directory('.')
		self.font_title = {
			'text': 'title',
			'font_name': 'ALISON',
			'font_size': 56,
			'color': (255, 255, 255, 255),
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'dpi': 96,
			'x': 0, 'y': 0,
		}

		self.font_item = {
			'font_name': 'ALISON',
			'font_size': 32,
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'color': (192, 192, 192, 255),
			'dpi': 96,
		}
		self.font_item_selected = {
			'font_name': 'ALISON',
			'font_size': 42,
			'bold': False,
			'italic': False,
			'anchor_y': 'center',
			'anchor_x': 'center',
			'color': (255, 255, 255, 255),
			'dpi': 96,
		}
		self.title_height = 0
		items = []
		items.append(MenuItem('Restar', self.on_new_game))
		items.append(MenuItem('Options', self.on_options))
		items.append(MenuItem('Scores', self.on_scores))
		items.append(MenuItem('Level Creater', self.on_creater))
		items.append(MenuItem('Quit', self.on_quit))
		self.create_menu(items, zoom_in(), zoom_out())

	def on_new_game(self):
		scene = Scene(GameLayer())
		director.replace(TurnOffTilesTransition(scene))

	def on_scores(self):
		self.parent.switch_to(2)

	def on_options(self):
		self.parent.switch_to(1)

	def on_creater(self):
		scene = Scene(LevelCreater.LevelCreater())
		director.replace(TurnOffTilesTransition(scene))

	def on_quit(self):
		intro_layer = Title()
		menulayer = MultiplexLayer(Star(), OptionMenu(), ScoreMenu())
		main_scene = Scene(intro_layer, menulayer)
		director.replace(TurnOffTilesTransition(main_scene))


class GameLayer(cocos.layer.ColorLayer):
	is_event_handler = True

	def __init__(self):
		super(GameLayer, self).__init__(randint(0, 255), randint(0, 255), randint(0, 255), 255)
		# 添加一个 板子
		self.paddle = Paddle('images/ban.png')
		self.add(self.paddle.sprite)
		self.ball = Ball('images/qiu.png')
		self.add(self.ball.sprite)
		self.level = 0
		# 添加一个 label 显示当前的游戏状态
		self.hud = Label('Score: 0',
						 color=(randint(0, 255), randint(0, 255), randint(0, 255), 255))
		self.hud.position = (0, 450)
		self.add(self.hud)
		self.hud2 = Label('Level: 1',
						  color=(randint(0, 255), randint(0, 255), randint(0, 255), 255))
		self.hud2.position = (100, 450)
		self.add(self.hud2)
		# 添加一个变量来记录金币
		self.score = 0
		# 设置 4 个按键状态
		self.key_pressed_left = False
		self.key_pressed_right = False
		self.key_pressed_up = False
		self.key_pressed_down = False

		self.blocks = []
		# 调用 reset 函数初始化状态
		self.gamestart()
		# 定期调用 self.update 函数
		# FPS frame per second 每秒帧数
		self.schedule(self.update)

	def gamestart(self):
		self.update_hud()
		self.paddle.reset()
		self.ball.reset()

		# 添加砖块并且显示出来
		# 先删除残存的砖块
		for b in self.blocks:
			self.remove(b)
		# 再初始化新的砖块
		self.blocks = []
		self.level += 1
		self.hud2.element.text = 'Level：' + str(self.level)
		if self.level > 4:
			self.level = 1
		levelfile = 'level' + str(self.level) + '.txt'
		positions = level_from_file(levelfile)
		number_of_blocks = len(positions)
		for i in range(number_of_blocks):
			b = Sprite('images/zhuan.png', anchor=(0, 0))
			b.position = positions[i]
			# b.color = (randint(0, 255), randint(0, 255), randint(0, 255))
			# b.position = (randint(0, 500), 400)
			self.add(b)
			self.blocks.append(b)

	def reset(self):
		self.score = 0
		self.update_hud()
		self.paddle.reset()
		self.ball.reset()

		# 添加砖块并且显示出来
		# 先删除残存的砖块
		for b in self.blocks:
			self.remove(b)
		# 再初始化新的砖块
		self.blocks = []
		levelfile = 'level' + str(self.level) + '.txt'
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
		print('游戏结束，跪了。金币是', self.score)
		scene = Scene(GameOver())
		overlayer = MultiplexLayer(OverMenu(), OptionMenu(), ScoreMenu())
		main_scene = Scene(scene, overlayer)
		director.replace(main_scene)

	def game_win(self):
		self.gamestart()

	def update_hud(self):
		self.hud.element.text = 'Score：' + str(self.score)

	def update_blocks(self):
		# 判断是否撞到了砖块
		for b in self.blocks:
			if collides(self.ball.sprite, b):
				# self.ball_speedy = -self.ball_speedy
				self.ball.hit()
				self.remove(b)
				self.blocks.remove(b)
				self.score += 1
				# self.speed += 1
				self.update_hud()
				print('Score', self.score)
				break
		if len(self.blocks) == 0:
			self.game_win()

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
	intro_layer = Title()
	menulayer = MultiplexLayer(Star(), OptionMenu(), ScoreMenu())
	main_scene = Scene(intro_layer, menulayer)
	director.run(scene.Scene(main_scene))
