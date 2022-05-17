import random

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
maroon = [128, 0, 0]
darkorange = [255, 69, 0]
orange = [255, 140, 0]
gold = [255, 215, 0]
yellow = [255, 255, 0]
darkgreen = [0, 128, 0]
turquoise = [32, 178, 170]
lightblue = [0, 255, 255]
skyblue = [0, 191, 255]
navy = [0, 0, 128]
purple = [138, 43, 226]
pink = [200, 50, 200]
brown = [139, 69, 19]
grey = [128, 128, 128]
slategrey = [112, 128, 144]
darkgrey = [50, 50, 50]

colourdict = {
    "black": black,
    "white": white,
    "red": red,
    "green": green,
    "blue": blue,
    "maroon": maroon,
    "darkorange": darkorange,
    "orange": orange,
    "gold": gold,
    "yellow": yellow,
    "darkgreen": darkgreen,
    "turquoise": turquoise,
    "lightblue": lightblue,
    "skyblue": skyblue,
    "navy": navy,
    "purple": purple,
    "pink": pink,
    "brown": brown,
    "grey": grey,
    "slategrey": slategrey,
    "darkgrey": darkgrey}

colourlist = ["black", "white", "red", "green", "blue", "maroon", "darkorange",
              "orange", "gold", "yellow", "darkgreen", "turquoise", "lightblue",
              "skyblue", "navy", "purple", "pink", "brown", "grey", "slategrey", "darkgrey"]

def randomcolour():
    col = random.choice(colourlist)
    return(colourdict[col])

if __name__ == '__main__':
    print(randomcolour())
