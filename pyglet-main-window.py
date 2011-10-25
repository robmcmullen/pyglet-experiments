#!/usr/bin/env python2.6

# Simple main window test for a media player

import os, sys, glob

import pyglet

class MainWindow(pyglet.window.Window):
    def __init__(self, menu, width=1280, height=720):
        super(MainWindow, self).__init__(width, height)
        self.menu = menu
        self.renderer = MenuRenderer(self)
    
    def on_draw(self):
        print "draw"
        self.clear()
        self.renderer.draw(self.menu)
    
    def on_text_motion(self, motion):
        print "here"
        self.menu.process_motion(motion, self.renderer)
        self.flip()


class MenuRenderer(object):
    def __init__(self, window):
        self.window = window
        self.load_fonts()
        self.compute_params()
    
    def load_fonts(self):
        self.font_name = "Droid Sans"
        self.font_size = 20
        self.selected_font_size = 25

    def compute_params(self):
        self.width, self.height = self.window.get_size()
        print self.width
        print self.height
        self.title_height = self.font_size + 10
        self.menu_width = self.width/3
        self.center = (self.height - self.title_height)/2
        self.items_in_half = (self.center - self.selected_font_size) / self.font_size
    
    def draw(self, menu):
        self.draw_title(menu)
        self.draw_menu(menu)
        self.draw_detail(menu)
    
    def draw_title(self, menu):
        title = "Main Window Title"
        label = pyglet.text.Label(title,
                                  font_name=self.font_name,
                                  font_size=self.font_size,
                                  x=self.width/2, y=self.height - self.title_height,
                                  anchor_x='center', anchor_y='bottom')
        label.draw()
        
    def draw_menu(self, menu):
        color = (0, 255, 0, 255)
        text = menu.get_label(menu.cursor)
        # Render center item in larger font
        label = pyglet.text.Label(text,
                                  font_name=self.font_name,
                                  font_size=self.selected_font_size,
                                  color=color, x=30, y=self.center,
                                  anchor_x='left', anchor_y='center')
        label.draw()
        
        y = self.center + self.selected_font_size
        i = menu.cursor - 1
        limit = max(0, menu.cursor - self.items_in_half)
        while i >= limit:
            text = menu.get_label(i)
            label = pyglet.text.Label(text,
                              font_name=self.font_name,
                              font_size=self.font_size,
                              color=color, x=30, y=y,
                              anchor_x='left', anchor_y='center')
            label.draw()
            y += self.font_size
            i -= 1
            
        y = self.center - self.selected_font_size
        i = menu.cursor + 1
        limit = min(menu.num_labels() - 1, menu.cursor + self.items_in_half)
        while i <= limit:
            text = menu.get_label(i)
            label = pyglet.text.Label(text,
                              font_name=self.font_name,
                              font_size=self.font_size,
                              color=color, x=30, y=y,
                              anchor_x='left', anchor_y='center')
            label.draw()
            y -= self.font_size
            i += 1
    
    def draw_detail(self, menu):
        image = menu.get_detail_image(menu.cursor)
        image.blit(self.menu_width, self.height - self.title_height - image.height, 0)
        text = menu.get_details(menu.cursor)
        label = pyglet.text.Label(text,
                                  font_name=self.font_name,
                                  font_size=self.font_size,
                                  x=self.menu_width + image.width + 10, y=self.height - self.title_height,
                                  anchor_x='left', anchor_y='top')
        label.draw()
        

class Menu(object):
    default_image = pyglet.image.load("artwork-not-available.png")
    
    def __init__(self):
        self.cursor = 0
    
    def get_label(self, index):
        return "Entry #%d" % index
    
    def get_detail_image(self, index):
        return self.default_image
    
    def get_details(self, index):
        return "Details for entry #%d" % index
    
    def num_labels(self):
        return 50

    def process_motion(self, motion, renderer):
        print "here"
        if motion == pyglet.window.key.MOTION_UP:
            self.cursor -= 1
        elif motion == pyglet.window.key.MOTION_PREVIOUS_PAGE:
            self.cursor -= renderer.items_in_half
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.cursor += 1
        elif motion == pyglet.window.key.MOTION_NEXT_PAGE:
            self.cursor += renderer.items_in_half
        if self.cursor < 0:
            self.cursor = 0
        elif self.cursor >= self.num_labels():
            self.cursor = self.num_labels() - 1


class MovieMenu(Menu):
    video_extensions = ['.vob', '.mp4', '.avi', '.wmv', '.mov', '.mpg', '.mpeg', '.mpeg4', '.mkv', '.flv']
    
    def __init__(self, path):
        super(MovieMenu, self).__init__()
        self.videos = []
        self.add_videos_in_path(path)
        
    def add_videos_in_path(self, dir):
        videos = glob.glob(os.path.join(dir, "*"))
        for video in videos:
            valid = False
            if os.path.isdir(video):
                if not video.endswith(".old"):
                    if self.exclude:
                        match = self.exclude.search(video)
                        if match:
                            if self.verbose: print("Skipping dir %s" % video)
                            continue
                    print("Checking dir %s" % video)
                    self.add_videos_in_path(video)
            elif os.path.isfile(video):
                print("Checking %s" % video)
                for ext in self.video_extensions:
                    if video.endswith(ext):
                        valid = True
                        print ("Found valid media: %s" % video)
                        break
                if valid:
                    self.add_video(video)
        self.videos.sort()
    
    def add_video(self, filename):
        """Check to see if the filename is associated with a series
        """
        video = MplayerTarget(filename)
        self.videos.append(video)

    def get_label(self, index):
        video = self.videos[index]
        return video.title
    
    def get_detail_image(self, index):
        video = self.videos[index]
        return video.get_image()
    
    def get_details(self, index):
        video = self.videos[index]
        return video.details
    
    def num_labels(self):
        return len(self.videos)


class MplayerTarget(object):
    def __init__(self, pathname):
        self.fullpath = pathname
        self.dirname, self.filename = os.path.split(pathname)
        self.fileroot, self.fileext = os.path.splitext(self.filename)
        self.title = self.fileroot.replace('_n_',' & ').replace('-s_','\'s ').replace('-t_','\'t ').replace('-m_','\'m ').replace('_',' ')
        self.details = "Details for %s" % self.title
        self.image = None
    
    def __cmp__(self, other):
        return cmp(self.title, other.title)
    
    def get_image(self):
        if self.image is None:
            imagedir = os.path.join(self.dirname, ".thumbs")
            for ext in [".jpg", ".png"]:
                imagepath = os.path.join(imagedir, self.fileroot + ext)
                print "checking %s" % imagepath
                if os.path.exists(imagepath):
                    self.image = pyglet.image.load(imagepath)
                    print "loaded %s" % imagepath
                    break
            if self.image is None:
                self.image = Menu.default_image
        return self.image

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    elif os.path.exists("/remote/media2/movies"):
        path = "/remote/media2/movies"
    else:
        path = None
    if path:
        menu = MovieMenu(path)
    else:
        menu = Menu()
    window = MainWindow(menu)
    pyglet.app.run()
