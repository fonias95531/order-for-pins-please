import random
from pyglet import *

width = 800
height = 600

imgs = [image.load('assets/pins.png'), image.load('assets/board.png')]
texts = ['0 совпадений', '1 совпадение', '2 совпадения', '3 совпадения', '4 совпадения', '5 совпадений']
window = window.Window(width, height)
gl.glClearColor(255, 255, 255, 255)
points = [width//2-188, width//2-112, width//2-36, width//2+40, width//2+116]
position = [*points]
hidden_order = random.shuffle([0, 1, 2, 3, 4])
order = [0, 1, 2, 3, 4]
heights = [348, 348, 348, 348, 348, 456, 148]
board = sprite.Sprite(imgs[1].get_region(0, 0, imgs[1].width, imgs[1].height), points[0]-4, heights[6]-4)
pins = [sprite.Sprite(imgs[0].get_region(i*72, 0, 72, 100), points[order[i]], heights[i]) for i in range(5)]
label = text.Label(text='', font_size=40, bold=True, color=(0, 0, 0, 255), x = points[0]+12, y = heights[6]+40)
select = [0, 0]
selected = False
mouse_x = 0
mouse_y = 0
compare = True

def comparison():
    global order, hidden_order
    count = 0
    for i in range(5):
        if order[i] == hidden_order[i]:
            count += 1
    return count

@window.event
def on_mouse_press(x, y, button, modifiers):
    global selected
    if select[selected] == select[0] or select[selected] == 0:
        selected = not selected
    else:
        order[select[0]-1], order[select[1]-1] = order[select[1]-1], order[select[0]-1]

@window.event
def on_mouse_motion(x, y, dx, dy):
    global select, mouse_x, mouse_y
    mouse_x = x
    mouse_y = y
    for i in range(5):
        mid_pos = [position, points][selected][[order[i], i][selected]]
        if mid_pos<x<mid_pos+72 and heights[i]<y<heights[i]+100:
            select[selected] = i+1
            break
    else:
        select[selected] = 0

@window.event
def on_draw():
    window.clear()
    global compare
    if compare:
        label.text = texts[comparison()]
    for i in range(5):
        pins[i].y = heights[6]
        pins[hidden_order[i]].x = points[i]
        pins[i].draw()
        index_solution = int(i==select[0]-1) + int(selected) - int(i!=select[0]-1 and selected)
        heights[order[i]] += ([348, 358, mouse_y-50][index_solution] - heights[order[i]])/4
        position[order[i]] += ([points[i], points[i], mouse_x-36][index_solution] - position[order[i]])/4
        pins[i].y = heights[i]
        pins[i].x = position[i]
        pins[i].draw()
    if comparison()<5:
        board.draw()
        label.draw()
    else:
        compare = False

app.run()