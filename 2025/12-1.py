import matplotlib.pyplot as plt
import numpy as np
import re

from matplotlib.widgets import Button

# define color map
color_map = {
    0: np.array([255, 255, 255]),  # white
    1: np.array([255, 0, 0]),  # red
    2: np.array([0, 255, 0]),  # green
    3: np.array([0, 0, 255]),  # blue
    4: np.array([128, 0, 255]),  # purple
    5: np.array([255, 0, 255]),  # magenta
    6: np.array([0, 255, 255]),  # cyan
    7: np.array([255, 128, 0]),  # orange
    8: np.array([128, 255, 0]),  # lime green
    9: np.array([0, 128, 255]),  # sky blue
    10: np.array([255, 255, 0]),  # yellow
}


def parse_shapes(lines):
    res = re.findall('[.|#]+', lines)
    default_color = color_map[0]
    shapes = []
    for i in range(0, len(res), 3):
        shape = []
        shape_id = (i // 3) + 1
        for j in range(i, i + 3):
            row = [default_color.copy() for _ in range(3)]
            for ci, c in enumerate(res[j]):
                if c == '#':
                    row[ci] = color_map[shape_id]
            shape += [row]
        shapes += [shape]
    return shapes


def parse_regions(lines):
    regions = []
    for size, nums in re.findall(r'(\d+x\d+): (.*)', lines):
        w, h = map(int, size.split('x'))
        values = list(map(int, nums.split()))
        regions.append((w, h, values))
    return regions


def rotate(shape):
    rotated = np.array(shape, int)
    rotated = np.rot90(rotated)
    return rotated.tolist()


def flip_vertically(shape):
    flipped = np.array(shape, int)
    flipped = np.flipud(flipped)
    return flipped.tolist()


def flip_horizontally(shape):
    flipped = np.array(shape, int)
    flipped = np.fliplr(flipped)
    return flipped.tolist()


class Visual:
    def __init__(self, shapes, regions):
        self.shapes = shapes
        self.regions = regions
        self.btrotate = None
        self.btflipud = None
        self.btfliplr = None
        self.axes = []
        self.images = []
        self.init_gui()

    def init_gui(self):
        plt.subplots_adjust(bottom=0.25)  # make room for buttons

        # Button positions: [left, bottom, width, height]
        ax_btn1 = plt.axes((0.3, 0.1, 0.15, 0.075))
        ax_btn2 = plt.axes((0.5, 0.1, 0.15, 0.075))
        ax_btn3 = plt.axes((0.7, 0.1, 0.15, 0.075))
        self.btrotate = Button(ax_btn1, 'Rotate')
        self.btflipud = Button(ax_btn2, 'Vertical f')
        self.btfliplr = Button(ax_btn3, 'Horizontal f')
        self.btrotate.on_clicked(self.rotate_shapes)
        self.btflipud.on_clicked(self.flip_shapes_vertically)
        self.btfliplr.on_clicked(self.flip_shapes_horizontally)
        self.init_shapes()
        plt.show()

    def init_shapes(self):
        for i, shape in enumerate(self.shapes):
            ax = plt.subplot(2, 3, i + 1)
            img = ax.imshow(np.array(shape, dtype=np.uint8))
            ax.set_title(f'Shape {i}')
            ax.set_axis_off()
            self.axes.append(ax)
            self.images.append(img)
        # region
        #plt.subplot
        plt.draw()

    def refresh_shapes(self):
        for img, shape in zip(self.images, self.shapes):
            img.set_data(np.array(shape, dtype=np.uint8))
        plt.draw()

    def rotate_shapes(self, event):
        rotated_shapes = [rotate(sh) for sh in self.shapes]
        self.shapes = rotated_shapes
        self.refresh_shapes()

    def flip_shapes_vertically(self, event):
        flipped_shapes = [flip_vertically(sh) for sh in self.shapes]
        self.shapes = flipped_shapes
        self.refresh_shapes()

    def flip_shapes_horizontally(self, event):
        flipped_shapes = [flip_horizontally(sh) for sh in self.shapes]
        self.shapes = flipped_shapes
        self.refresh_shapes()




lines = open("input/12.txt").read()
shapes = parse_shapes(lines)
regions = parse_regions(lines)

print(regions)
Visual(shapes, regions)
