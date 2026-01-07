from collections import defaultdict
from itertools import count

import matplotlib.pyplot as plt
import numpy as np
import re

from matplotlib.widgets import Button


class Placement:
    def __init__(self, shape_id, rotation_id, offset_col, offset_row):
        self.shape_id = shape_id
        self.rotation_id = rotation_id
        self.offset_col = offset_col
        self.offset_row = offset_row


class DataProvider:
    INSTANCE:'DataProvider' = None

    def __init__(self):
        if DataProvider.INSTANCE is None:
            self.lines = open("input/12.txt").read()
            self.shapes = self.parse_shapes()
            self.rotations = self.create_all_rotations()
            self.regions = self.parse_regions()
            DataProvider.INSTANCE = self

    def rotate(self, shape):
        rotated = np.array(shape, int)
        rotated = np.rot90(rotated)
        return rotated.tolist()

    def flip_vertically(self, shape):
        flipped = np.array(shape, int)
        flipped = np.flipud(flipped)
        return flipped.tolist()

    def flip_horizontally(self, shape):
        flipped = np.array(shape, int)
        flipped = np.fliplr(flipped)
        return flipped.tolist()

    def parse_shapes(self):
        res = re.findall('[.|#]+', self.lines)
        shapes = []
        for i in range(0, len(res), 3):
            shape = []
            for j in range(i, i + 3):
                row = [0 for _ in range(3)]
                for ci, c in enumerate(res[j]):
                    if c == '#':
                        row[ci] = 1
                shape += [row]
            shapes += [shape]
        return shapes

    def shape_to_coords(self, shape):
        s2c = []
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    s2c += [(i, j)]
        return tuple(s2c)

    def create_all_rotations(self):
        all_rotations = defaultdict(list)
        for i, shape in enumerate(self.shapes):
            rotations = set()
            for s in [shape, self.flip_vertically(shape), self.flip_horizontally(shape)]:
                for j in range(4):
                    shape = self.rotate(s)
                    rotations.add(self.shape_to_coords(shape))
            all_rotations[i] = list(rotations)
        return all_rotations

    def parse_regions(self):
        regions = []
        for size, nums in re.findall(r'(\d+x\d+): (.*)', self.lines):
            w, h = map(int, size.split('x'))
            values = list(map(int, nums.split()))
            regions.append((w, h, values))
        return regions


class State:
    def __init__(self, region_id: int, placements: [Placement]):
        self.region_id = region_id
        self.placements = placements

    def __get_region(self) -> tuple[int, int, list]:
        return DataProvider.INSTANCE.regions[self.region_id]

    def add_placement(self, placement: Placement) -> 'State':
        return State(self.region_id, self.placements + [placement])

    def is_valid(self) -> bool:
        w, h, shape2put_cnts = self.__get_region()
        rotations = DataProvider.INSTANCE.rotations
        occupied_coords = set()
        for placement in self.placements:
            row, col = rotations[placement.shape_id][placement.rotation_id]
            row += placement.offset_row
            col += placement.offset_col
            if 0 > col or col >= w: return False
            if 0 > row or row >= h: return False
            if (col, row) in occupied_coords:
                return False
            occupied_coords.add((col, row))
        return True

    def is_final(self) -> bool:
        if not self.is_valid():
            return False

        for shape_id, cnt in enumerate(self.__get_region()[2]):
            if cnt > 0:
                if len(list(filter(lambda pl: pl.shape_id == shape_id, self.placements))) < cnt:
                    return False
        return True


class Visual:
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

    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
        self.btrotate = None
        self.btflipud = None
        self.btfliplr = None
        self.axes = []
        self.images = []
        self.init_gui()

    def init_gui(self):
        self.fig = plt.figure(constrained_layout=True)
        gs = self.fig.add_gridspec(
            nrows=4, ncols=3,
            height_ratios=[1, 1, 0.3, 4]
        )

        self.axes = []
        self.images = []

        idx = 0
        for r in range(2):
            for c in range(3):
                if idx >= len(self.data_provider.shapes):
                    break
                ax = self.fig.add_subplot(gs[r, c])
                img = ax.imshow(self.colorize_shape(idx, self.data_provider.shapes[idx]))
                ax.set_title(f"Shape {idx}")
                ax.set_axis_off()
                self.axes.append(ax)
                self.images.append(img)
                idx += 1

        ax_btn1 = self.fig.add_subplot(gs[2, 0])
        ax_btn2 = self.fig.add_subplot(gs[2, 1])
        ax_btn3 = self.fig.add_subplot(gs[2, 2])

        self.btrotate = Button(ax_btn1, 'Rotate')
        self.btflipud = Button(ax_btn2, 'Vertical f')
        self.btfliplr = Button(ax_btn3, 'Horizontal f')

        self.btrotate.on_clicked(self.rotate_shapes)
        self.btflipud.on_clicked(self.flip_shapes_vertically)
        self.btfliplr.on_clicked(self.flip_shapes_horizontally)

        ax_region = self.fig.add_subplot(gs[3, :])
        ax_region.set_title("Region")
        ax_region.set_axis_off()

        region_data = np.zeros(
            (self.data_provider.regions[0][0], self.data_provider.regions[0][1])
        )

        self.region_img = ax_region.imshow(region_data)
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
        ax = plt.subplot(1, 1, 1)
        ax.set_axis_off()
        ax.set_title('Region')
        region_data = np.empty(shape=(self.data_provider.regions[0][0], self.data_provider.regions[0][1]))
        region_data.fill(0)
        img = ax.imshow(region_data)
        self.axes.append(ax)
        self.images.append(img)
        plt.draw()

    def refresh_shapes(self):
        for i, (img, shape) in enumerate(zip(self.images, self.data_provider.shapes)):
            img.set_data(self.colorize_shape(i, shape))
        plt.draw()

    def rotate_shapes(self, event):
        rotated_shapes = [data_provider.rotate(sh) for sh in self.data_provider.shapes]
        self.data_provider.shapes = rotated_shapes
        self.refresh_shapes()

    def flip_shapes_vertically(self, event):
        flipped_shapes = [data_provider.flip_vertically(sh) for sh in self.data_provider.shapes]
        self.data_provider.shapes = flipped_shapes
        self.refresh_shapes()

    def flip_shapes_horizontally(self, event):
        flipped_shapes = [data_provider.flip_horizontally(sh) for sh in self.data_provider.shapes]
        self.data_provider.shapes = flipped_shapes
        self.refresh_shapes()

    def colorize_shape(self, idx, shape):
        colored_shape = []
        for _ in range(len(shape)):
            colored_shape += [[Visual.color_map[0].copy() for _ in range(len(shape[0]))]]

        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if shape[row][col] == 1:
                    colored_shape[row][col] = Visual.color_map[idx + 1]
        return np.array(colored_shape)


data_provider = DataProvider()
Visual(data_provider)
