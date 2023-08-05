# Imports

import colorama
import math

# Progress Bar
progress_bar = False
def progress_bar_all():
    global progress_bar
    if progress_bar == True:
        def progress_bar(progress, total, color=colorama.Fore.CYAN):
            percent = 100 * (progress / float(total))
            bar = '█' * int(percent) + '-' * (100 - int(percent))
            print(color + f"\r|{bar}| {percent:.2f}%", end="\r")
            if progress == total:
                print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")    

        numbers = [x * 5 for x in range(2000, 3000)]
        results = []

        progress_bar(0, len(numbers))
        for i, x in enumerate(numbers):
            results.append(math.factorial(x))
            progress_bar(i + 1, len(numbers))


        print(colorama.Fore.RESET)

    else:
        pass
progress_bar_all()