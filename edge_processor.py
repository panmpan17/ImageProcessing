import math
from color import *
from PIL import Image
from utilities import  ProgressBar


THREAD_HOLD =  20


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


COLOR_STEP = 12 / 255
def color_sigmoid(x):
    return sigmoid(COLOR_STEP * x - 6)


class AbstractImageProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.img = None
        self.new_img = None
        
        self.width = None
        self.height = None

    def __getitem__(self, pos, y=None):
        if self.img is None:
            raise "Image not loaded"

        if not isinstance(pos, tuple):
            if y is None:
                raise "No Y"

            return self.color_process(self.img.getpixel((pos, y)))

        elif len(pos) == 2:
            return self.color_process(self.img.getpixel(pos))

        raise ValueError

    def color_process(self, color_tuple):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def load_img(self):
        self.img = Image.open(self.file_name)
        self.width = self.img.width
        self.height = self.img.height

    @property
    def save_prefix(self):
        return "result-"

    def save(self, filename=None):
        if filename is None:
            self.new_img.save("result/" + self.save_prefix + self.file_name)
        else:
            self.new_img.save(filename)

    def close(self):
        if self.img is not None:
            self.img.close()

        if self.new_img is not None:
            self.new_img.close()


class Laplacian(AbstractImageProcessor):
    def step_1(self, x, y, changeX=True):
        v1 = self[x, y]

        if changeX:
            v2 = self[x + 1, y]
            v3 = self[x - 1, y]
        else:
            v2 = self[x, y + 1]
            v3 = self[x, y - 1]

        return v2 - (v1 * 2) + v3

    def step_2(self, x, y):
        return self.step_1(x, y) + self.step_1(x, y, False)
    
    def color_process(self, color_tuple):
        return RGBColor(*color_tuple).to_HSV().V

    def start(self):
        self.new_img = Image.new("RGB", (self.img.width, self.img.height))

        progress_bar = ProgressBar(
            (self.img.width - 4) * (self.img.height - 4),
            "Progress: ", "Completed", length=50)

        for x in range(2, self.img.width - 2):
            for y in range(2, self.img.height - 2):
                left_value = int(self.step_2(x - 1, y) * 255)
                right_value = int(self.step_2(x + 1, y) * 255)

                is_true = False
                if ((left_value > 0 and right_value < 0) or
                    (left_value < 0 and right_value > 0)):
                    diff = math.fabs(right_value - left_value)
                    is_true = diff > THREAD_HOLD
                
                if not is_true:
                    top_value = int(self.step_2(x, y - 1) * 255)
                    bottom_value = int(self.step_2(x, y + 1) * 255)
                    if ((bottom_value > 0 and top_value < 0) or
                        (bottom_value < 0 and top_value > 0)):
                        diff = math.fabs(top_value - bottom_value)
                        is_true = diff > THREAD_HOLD

                color = WHITE.tuple
                if is_true:
                    color = BLACK.tuple

                self.new_img.putpixel((x, y), color)

                progress_bar.increment()

    @property
    def save_prefix(self):
        return "laplacian-"

class MarrHildreth(AbstractImageProcessor):
    def color_process(self, color_tuple):
        return RGBColor(*color_tuple).to_HSV().V
    
    def start(self):
        temp_data = [[0 for i in range(self.height)] for j in range(self.width)]

        progress_bar = ProgressBar(
            (self.img.width - 4) + 2,
            "Progress: ", "Completed", length=50)

        for x in range(2, self.width - 2):
            for y in range(2, self.height - 2):
                temp_data[x][y] = self[x, y] * 16 - self[x, y - 1] * 2\
                    - self[x, y + 1] * 2 - self[x - 1, y] * 2\
                    - self[x + 1, y] * 2 - self[x - 1, y - 1]\
                    - self[x - 1, y + 1] - self[x + 1, y - 1]\
                    - self[x + 1, y + 1] - self[x, y - 2]\
                    - self[x, y + 2] - self[x - 2, y]\
                    - self[x + 2, y]
                
            progress_bar.increment()

        temp_sum = 0
        pixel_counter = 0
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                pixel_counter += 1
                temp_sum += math.fabs(temp_data[x][y])
        
        progress_bar.increment()
        
        TH = 2 * (temp_sum / pixel_counter)

        self.new_img = Image.new("RGB", (self.width, self.height))

        for x in range(0, self.width - 2):
            for y in range(0, self.height - 2):

                if (temp_data[x][y + 1] >= 0) and (temp_data[x + 2][y + 1] <= 0) and\
                        (temp_data[x][y + 1] - temp_data[x + 2][y + 1] >= TH):
                    self.new_img.putpixel((x + 1, y + 1), BLACK.tuple)

                elif (temp_data[x][y + 1] <= 0) and (temp_data[x + 2][y + 1] >= 0) and\
                        (temp_data[x + 2][y + 1] - temp_data[x][y + 1] >= TH):
                    self.new_img.putpixel((x + 1, y + 1), BLACK.tuple)

                elif (temp_data[x + 1][y] >= 0) and (temp_data[x + 1][y + 2] <= 0) and\
                        (temp_data[x + 1][y] - temp_data[x + 1][y + 2] >= TH):
                    self.new_img.putpixel((x + 1, y + 1), BLACK.tuple)

                elif (temp_data[x + 1][y] <= 0) and (temp_data[x + 1][y + 2] >= 0) and\
                        (temp_data[x + 1][y + 2] - temp_data[x + 1][y] >= TH):
                    self.new_img.putpixel((x + 1, y + 1), BLACK.tuple)

                else:
                    self.new_img.putpixel((x + 1, y + 1), WHITE.tuple)
            
        progress_bar.increment()

    @property
    def save_prefix(self):
        return "marr-"


if __name__ == "__main__":
    lap = Laplacian("test.png")
    lap.load_img()
    lap.start()
    lap.save()
    lap.close()

    marr = MarrHildreth("test.png")
    marr.load_img()
    marr.start()
    marr.save()
    marr.close()
