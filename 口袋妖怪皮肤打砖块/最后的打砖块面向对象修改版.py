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
# 15，开始菜单
# 16，结束菜单
# 17，多个关卡

# 关卡文件该如何配置呢？
# 首先，分析不同关卡的变化
# 关卡一共有两个数据来定义
# 1，砖块的数量
# 2，砖块的 x y 坐标

# 开始画面
class Layer1(cocos.layer.ColorLayer):
	is_event_handler = True

	def __init__(self):
		super(Layer1, self).__init__(246, 226, 76, 255)
		# self.color = (246, 226, 76)
		label = Label("PoKeMoN CLoNe",
					  font_name='Pokemon Hollow',
					  font_size=40,
					  bold=True,
					  color=(80, 152, 247, 255),
					  anchor_x='center', anchor_y='center')
		label.position = (325, 350)
		self.add(label)
		self.hud = Label('按任意鍵開始遊戲',
						 font_name='Kozuka Gothic Pr6N B',
						 font_size=20)
		self.hud.position = (225, 200)
		self.add(self.hud)
		self.ash = Sprite('images/ash(1).png')
		self.ash.position = (80, 60)
		self.add(self.ash)
		self.pokemon = Sprite('images/pokemon.png')
		self.pokemon.position = (490, 80)
		self.add(self.pokemon)

	def on_key_press(self, key, modifiers):
		scene = Scene(GameLayer())
		director.replace(SplitColsTransition(scene))


# 关卡一
class GameLayer(Layer):
	is_event_handler = True

	def __init__(self):
		super(GameLayer, self).__init__()
		# 添加一个 板子
		self.paddle = Paddle('images/ash.png')
		self.add(self.paddle.sprite)
		self.ball = Ball('images/pokem.png')
		self.add(self.ball.sprite)

		# 添加一个 label 显示当前的游戏状态
		self.hud = Label('皮卡丘: 0')
		self.hud.position = (0, 450)
		self.add(self.hud)
		# 添加一个 label 显示当前游戏关卡
		self.level = Label('Level 1')
		self.level.position = (100, 450)
		self.add(self.level)
		# 添加一个变量来记录金币
		self.gold = 0
		# 设置 4 个按键状态
		self.key_pressed_left = False
		self.key_pressed_right = False
		self.key_pressed_up = False
		self.key_pressed_down = False

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
		levelfile = 'level.txt'
		positions = level_from_file(levelfile)
		number_of_blocks = len(positions)
		for i in range(number_of_blocks):
			b = Sprite('images/pikachu.png', anchor=(0, 0))
			b.position = positions[i]
			# b.position = (randint(0, 500), 400)
			self.add(b)
			self.blocks.append(b)

	def game_over(self):
		print('游戏结束，跪了。捉到了', self.gold, '只皮卡丘')
		# 没接到球，跳转到结束画面（失败）
		scene = Scene(GameOver())
		director.replace(SplitColsTransition(scene))

	def game_win(self):
		# 打完所有皮卡丘，跳转到下一关或（成功）
		scene = Scene(GameWin())
		director.replace(SplitColsTransition(scene))

	def update_hud(self):
		self.hud.element.text = '皮卡丘：' + str(self.gold)

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
				print('捉到', self.gold, '只皮卡丘')
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


# 关卡二
class GameTwo(Layer):
	is_event_handler = True

	def __init__(self):
		super(GameTwo, self).__init__()
		# 添加一个 板子
		self.paddle = Paddle('images/ash.png')
		self.add(self.paddle.sprite)
		self.ball = Ball('images/pokem.png')
		self.add(self.ball.sprite)

		# 添加一个 label 显示当前的游戏状态
		self.hud = Label('皮卡丘: 0')
		self.hud.position = (0, 450)
		self.add(self.hud)
		# 添加一个 label 显示当前游戏关卡
		self.level = Label('Level 2')
		self.level.position = (100, 450)
		self.add(self.level)
		# 添加一个变量来记录金币
		self.gold = 0
		# 设置 4 个按键状态
		self.key_pressed_left = False
		self.key_pressed_right = False
		self.key_pressed_up = False
		self.key_pressed_down = False

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
		levelfile = 'level3.txt'
		positions = level_from_file(levelfile)
		number_of_blocks = len(positions)
		for i in range(number_of_blocks):
			b = Sprite('images/pikachu.png', anchor=(0, 0))
			b.position = positions[i]
			# b.position = (randint(0, 500), 400)
			self.add(b)
			self.blocks.append(b)

	def game_over(self):
		print('游戏结束，跪了。捉到了', self.gold, '只皮卡丘')
		scene = Scene(GameOver())
		director.replace(SplitColsTransition(scene))

	def game_win(self):
		scene = Scene(GameWin())
		director.replace(SplitColsTransition(scene))

	def update_hud(self):
		self.hud.element.text = '皮卡丘：' + str(self.gold)

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
				print('捉到', self.gold, '只皮卡丘')
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


# 结束画面（失败）
class GameOver(cocos.layer.ColorLayer):
	is_event_handler = True

	def __init__(self):
		super(GameOver, self).__init__(255, 255, 255, 255)
		self.wp = Label('Game Over',
						  color=(255, 0, 0, 255),
						  font_size=30)
		self.wp.position = (340, 250)
		self.add(self.wp)
		label = Label("妳被皮卡丘吃了！",
					  font_name='Kozuka Gothic Pr6N B',
					  color=(255, 0, 0, 255),
					  font_size=30)
		label.position = (300, 150)
		self.add(label)
		# 添加一个 label 重新开始游戏
		self.restart = Label('按任意键重新开始游戏',
					  color=(255, 0, 0, 255),
					  font_size=15)
		self.restart.position = (330, 100)
		self.add(self.restart)
		self.deadash = Sprite('images/zombie-pikachu.png')
		self.deadash.position = (130, 170)
		self.add(self.deadash)

	def on_key_press(self, key, modifiers):
		scene = Scene(GameLayer())
		director.replace(SplitColsTransition(scene))


# 结束画面（成功）
class GameWin(cocos.layer.ColorLayer):
	is_event_handler = True

	def __init__(self):
		super(GameWin, self).__init__(255, 255, 255, 255)

		self.muscleash = Sprite('images/ashm.jpg')
		self.muscleash.position = (170, 230)
		self.add(self.muscleash)
		self.wp = Label('Well Play!',
						  color=(255, 0, 0, 255),
						  font_size=30)
		self.wp.position = (350, 250)
		self.add(self.wp)
		label = Label("恭喜你捉到了所有皮卡丘！",
					  font_name='Kozuka Gothic Pr6N B',
					  color=(255, 0, 0, 255),
					  font_size=25)
		label.position = (250, 120)
		self.add(label)
		# 添加一个 label 继续游戏
		self.goon = Label('按任意键继续游戏',
					  color=(255, 0, 0, 255),
					  font_size=15)
		self.goon.position = (350, 80)
		self.add(self.goon)

	def on_key_press(self, key, modifiers):
		scene = Scene(GameTwo())
		director.replace(SplitColsTransition(scene))


if __name__ == '__main__':
	director.init()
	director.run(scene.Scene(Layer1()))
