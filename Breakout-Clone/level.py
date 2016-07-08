
def level_from_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        number_of_blocks = int(lines[0])
        positions = []
        for pos in lines[1:]:
            # '0, 100'
            # 字符串的方法 split 可以依据一个分隔符获得一个列表
            p = pos.split(', ')
            # ['0', '100']
            x = int(p[0])
            y = int(p[1])
            positions.append([x, y])
            print('关卡', x, y)
        return positions
