from cocos import scene
from cocos.director import director
from cocos.layer import Layer
from cocos.text import Label
from cocos.sprite import Sprite
from pyglet.window.key import symbol_string
from cocos.menu import *
from cocos.scene import *
from cocos.scenes import SplitColsTransition
import game


class LevelCreater(Layer):
	is_event_handler = True

	def __init__(self):
		super(LevelCreater, self).__init__()
		label = Label("关卡编辑器, 按空格保存关卡文件")
		self.add(label)
		self.list = []
		self.zhuan = Sprite('images/zhuan.png')
		self.add(self.zhuan)

	def on_mouse_motion(self, x, y, dx, dy):
		self.zhuan.position = (x, y)

	def on_mouse_press(self, x, y, buttons, modifiers):
		x1 = x // 35 * 35
		y1 = y // 15 * 15
		self.block = Sprite('images/zhuan.png', anchor=(0, 0))
		self.block.position = (x1, y1)
		self.add(self.block)
		self.list.append((x1, y1))
		print('mouse press', x1, y1, buttons)
		print('size', self.block.width, self.block.height, self.list)

	def on_key_press(self, key, modifiers):
		level = self.list
		k = symbol_string(key)
		filename = 'level.txt'
		status = True
		lines = []
		for p in level:
			print('打印点', type(p), p)
			line = '{}, {}'.format(p[0], p[1])
			lines.append(line)
		level = '\n'.join(lines)
		if k == "SPACE":
			self.key_pressed_left = status
			print(level)
			with open(filename, 'w') as f:
				f.write(level)


class Back(Menu):
	def __init__(self, back):
		super(Back, self).__init__()
		self.back = back
		self.menu_valign = BOTTOM
		self.menu_halign = RIGHT
		self.font_item = {
			'font_name': 'ALISON',
			'font_size': 32,
			'bold': False,
			'italic': False,
			# 'anchor_y': 'center',
			# 'anchor_x': 'center',
			'color': (192, 192, 192, 255),
			'dpi': 96,
		}
		self.font_item_selected = {
			'font_name': 'ALISON',
			'font_size': 42,
			'bold': False,
			'italic': False,
			# 'anchor_y': 'center',
			# 'anchor_x': 'center',
			'color': (255, 255, 255, 255),
			'dpi': 96,
		}
		items = []
		items.append(MenuItem('Back', self.back))
		self.create_menu(items, zoom_in(), zoom_out())

	def back(self):
		scene = Scene(game.Title())
		director.replace(SplitColsTransition(scene))


if __name__ == '__main__':
	director.init()
	hello_layer = LevelCreater()
	main_scene = Scene(hello_layer)
	main_scene.add(Back(hello_layer))
	director.run(main_scene)
