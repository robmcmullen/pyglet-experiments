#!/usr/bin/env python2.6

# Simple app to draw text in a window and interact using the arrow keys

import pyglet

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.cursor = 0
    
    def on_draw(self):
        print "draw"
        self.clear()
        y = 0
        for i in range(20):
            label = pyglet.text.Label('Hello, world #%d' % i,
                              font_name='Times New Roman',
                              font_size=36,
                              x=30, y=y,
                              anchor_x='left', anchor_y='bottom')
            label.draw()
            if i == self.cursor:
                label = pyglet.text.Label('->',
                              font_name='Times New Roman',
                              font_size=36,
                              x=0, y=y,
                              anchor_x='left', anchor_y='bottom')
                label.draw()
                
            y += 36
    
    def on_text_motion(self, motion):
        print "here"
        if motion == pyglet.window.key.MOTION_UP:
            self.cursor += 1
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.cursor -= 1
        self.flip()

window = MainWindow()
pyglet.app.run()
