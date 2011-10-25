#!/usr/bin/env python2.6

# Simple main window test for a media player

import pyglet

class MainWindow(pyglet.window.Window):
    def __init__(self, width=1280, height=720):
        super(MainWindow, self).__init__(width, height)
        self.cursor = 0
        self.font_name = "Droid Sans"
        self.font_size = 20
        self.selected_font_size = 25
        
        self.load_fonts()
        self.compute_params()
    
    def compute_params(self):
        self.width, self.height = self.get_size()
        print self.width
        print self.height
        self.title_height = self.font_size + 10
        self.menu_width = self.width/3
        self.center = (self.height - self.title_height)/2
        self.items_in_half = (self.center - self.selected_font_size) / self.font_size
    
    def load_fonts(self):
        self.title_font = pyglet.font.load(self.font_name, self.font_size, bold=True, italic=False)
    
    def on_draw(self):
        print "draw"
        self.clear()
        self.draw_title()
        self.draw_menu()
        #self.draw_detail()
    
    def draw_title(self):
        title = "Main Window Title"
        label = pyglet.text.Label(title,
                                  font_name=self.font_name,
                                  font_size=self.font_size,
                                  x=self.width/2, y=self.height - self.title_height,
                                  anchor_x='center', anchor_y='bottom')
        label.draw()
    
    def draw_menu(self):
        color = (0, 255, 0, 255)
        text = self.get_label(self.cursor)
        # Render center item in larger font
        label = pyglet.text.Label(text,
                                  font_name=self.font_name,
                                  font_size=self.selected_font_size,
                                  color=color, x=30, y=self.center,
                                  anchor_x='left', anchor_y='center')
        label.draw()
        
        y = self.center + self.selected_font_size
        i = self.cursor - 1
        limit = max(0, self.cursor - self.items_in_half)
        while i >= limit:
            text = self.get_label(i)
            label = pyglet.text.Label(text,
                              font_name=self.font_name,
                              font_size=self.font_size,
                              color=color, x=30, y=y,
                              anchor_x='left', anchor_y='center')
            label.draw()
            y += self.font_size
            i -= 1
            
        y = self.center - self.selected_font_size
        i = self.cursor + 1
        limit = min(self.num_labels() - 1, self.cursor + self.items_in_half)
        while i <= limit:
            text = self.get_label(i)
            label = pyglet.text.Label(text,
                              font_name=self.font_name,
                              font_size=self.font_size,
                              color=color, x=30, y=y,
                              anchor_x='left', anchor_y='center')
            label.draw()
            y -= self.font_size
            i += 1
    
    def on_text_motion(self, motion):
        print "here"
        if motion == pyglet.window.key.MOTION_UP:
            self.cursor -= 1
        elif motion == pyglet.window.key.MOTION_PREVIOUS_PAGE:
            self.cursor -= self.items_in_half
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.cursor += 1
        elif motion == pyglet.window.key.MOTION_NEXT_PAGE:
            self.cursor += self.items_in_half
        if self.cursor < 0:
            self.cursor = 0
        elif self.cursor >= self.num_labels():
            self.cursor = self.num_labels() - 1
            
        self.flip()
    
    def get_label(self, index):
        return "Entry #%d" % index
    
    def num_labels(self):
        return 50

window = MainWindow()
pyglet.app.run()
