class ProgressBar:
    def __init__(self, progress_length, prefix="", suffix="", decimals=1,
                 length=50, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            progress_length       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """

        self.progress = 0
        self.progress_length = progress_length
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd
        print()
    
    def increment(self):
        self.progress += 1

        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.progress / self.progress_length))
        filledLength = int(self.length * self.progress // self.progress_length)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end=self.printEnd)

        # Print New Line on Complete
        if self.length == self.progress_length: 
            print()


class Utilities:
    @staticmethod
    def convert_ROC_year(year):
        """
        Convert year into Taiwan year
        """

        if year > 1990:
            year -= 1911
        elif year < 50:
            year = (2000 + year) - 1911

        return year


class Print:
    @staticmethod
    def gray(*kwargs):
        print("\033[0;49;90m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def red(*kwargs):
        print("\033[0;49;91m", end="")
        print(*kwargs, end="")
        print("\033[0m")
    
    @staticmethod
    def alt_red(*kwargs):
        print("\033[0;49;31m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def green(*kwargs):
        print("\033[0;49;92m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def yellow(*kwargs):
        print("\033[0;49;93m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def blue(*kwargs):
        print("\033[0;49;94m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def gray_bg(*kwargs):
        print("\033[7;49;90m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def red_bg(*kwargs):
        print("\033[7;49;91m", end="")
        print(*kwargs, end="")
        print("\033[0m")
    
    @staticmethod
    def alt_red_bg(*kwargs):
        print("\033[7;49;31m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def green_bg(*kwargs):
        print("\033[7;49;92m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def yellow_bg(*kwargs):
        print("\033[7;49;93m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def blue_bg(*kwargs):
        print("\033[7;49;94m", end="")
        print(*kwargs, end="")
        print("\033[0m")

    @staticmethod
    def begin_gray(*kwargs):
        print("\033[0;49;90m", end="")

    @staticmethod
    def begin_red(*kwargs):
        print("\033[0;49;91m", end="")

    @staticmethod
    def begin_alt_red(*kwargs):
        print("\033[0;49;31m", end="")

    @staticmethod
    def begin_green(*kwargs):
        print("\033[0;49;92m", end="")

    @staticmethod
    def begin_yellow(*kwargs):
        print("\033[0;49;93m", end="")

    @staticmethod
    def begin_blue(*kwargs):
        print("\033[0;49;94m", end="")
    
    @staticmethod
    def end(*kwargs):
        print("\033[0m", end="")
