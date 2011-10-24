#!/usr/bin/env python2.6

# Simple app to draw text in a window and interact using the arrow keys

import pyglet

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

cursor = 0
@window.event
def on_draw():
    global cursor
    
    print "draw"
    window.clear()
    y = 0
    for i in range(20):
        label = pyglet.text.Label('Hello, world #%d' % i,
                          font_name='Times New Roman',
                          font_size=36,
                          x=30, y=y,
                          anchor_x='left', anchor_y='bottom')
        label.draw()
        if i == cursor:
            label = pyglet.text.Label('->',
                          font_name='Times New Roman',
                          font_size=36,
                          x=0, y=y,
                          anchor_x='left', anchor_y='bottom')
            label.draw()
            
        y += 36
        
@window.event
def on_text_motion(motion):
    global cursor
    
    print "here"
    if motion == pyglet.window.key.MOTION_UP:
        cursor += 1
    elif motion == pyglet.window.key.MOTION_DOWN:
        cursor -= 1
    window.flip()

pyglet.app.run()
