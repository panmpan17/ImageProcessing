import math


class YIQColor():
    def __init__(self, y, i, q):
        self.Y = y
        self.I = i
        self.Q = q

    def __repr__(self):
        return f"<YIQ {self.Y}, {self.I}, {self.Q}>"


class HSVColor():
    def __init__(self, h, s, v):
        self.H = h
        self.S = s
        self.V = v

    def __repr__(self):
        return f"<HSV {self.H}, {self.S}, {self.V}>"


class RGBColor():
    def __init__(self, r, g, b, a=1):
        self.R = r
        self.G = g
        self.B = b
        self.A = 1

    def __repr__(self):
        return f"<RGB {self.R}, {self.G}, {self.B}>"

    @property
    def tuple(self):
        return (self.R, self.G, self.B)

    def to_YIQ(self):
        Y = 0.299 * self.R + 0.587 * self.G + 0.114 * self.B
        I = 0.596 * self.R - 0.275 * self.G - 0.321 * self.B
        Q = 0.212 * self.R - 0.523 * self.G + 0.311 * self.B
        return YIQColor(Y, I, Q)

    def to_HSV(self):
        max_ = max(self.R, self.G, self.B)
        min_ = min(self.R, self.G, self.B)
        diff = max_ - min_

        if max_ == 0:
            S = 0
        else:
            S = (max_ - min_) / max_
        V = max_ / 255

        if diff == 0:
            H = 0
        else:
            r_diff = max_ - self.R / 6 / diff + 1 / 2
            g_diff = max_ - self.G / 6 / diff + 1 / 2
            b_diff = max_ - self.B / 6 / diff + 1 / 2

            if self.R == max_:
                H = b_diff - g_diff
            elif (self.G == max_):
                H = (1 / 3) + r_diff - b_diff
            else:
                H = (2 / 3) + g_diff - r_diff
            
            if H < 0:
                H += 1
            elif H > 1:
                H -= 1
            H *= 360

        return HSVColor(H, S, V)


WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(0, 0, 0)


if __name__ == "__main__":
    color = RGBColor(151, 194, 212)
    print(color, color.to_YIQ(), color.to_HSV())

