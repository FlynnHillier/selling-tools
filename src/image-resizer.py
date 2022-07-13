from typing import Tuple
from os import listdir, getcwd, mkdir
from os.path import join, exists, isfile,abspath
import math
import json

from PIL import Image

def calcTransformDimension(originalDimensions:Tuple[int,int],TransformDimensions:Tuple[int,int]) -> Tuple[int,int]: # [width, height]
    if (TransformDimensions[0] != False & TransformDimensions[1] != False):
        return TransformDimensions

    if TransformDimensions[0] != False:
        return [
            TransformDimensions[0],
            math.floor(TransformDimensions[0] * (originalDimensions[1] / originalDimensions[0]))
        ]

    if TransformDimensions[1] != False:
        return [
            math.floor(TransformDimensions[1] * (originalDimensions[0] / originalDimensions[1])),
            TransformDimensions[1]
        ]

    print("using default resize. 500*500")
    return [500,500]
    

def getConfig():
    configPath = abspath(join(getcwd(),"config.json"))

    try:
        return json.loads(open(configPath,"r").read())
    except:
        raise f"unable to locate configuration file at: '{configPath}'"
        






def main():
    CONFIG = getConfig()

    imageBaseDir = abspath(join(getcwd(),"images"))
    imageSourceDir = join(imageBaseDir,"input")
    imageOutDir = join(imageBaseDir,"out")


    if not exists(imageBaseDir):
        print(f"creating directory '{imageBaseDir}'")
        mkdir(imageBaseDir)


    if not exists(imageSourceDir):
        print(f"image source directory does not exist.")

        print(f"creating directory '{imageSourceDir}' - populate it and re-run.")
        mkdir(imageSourceDir)
        return

    if not exists(imageOutDir):
        mkdir(imageOutDir)
        

    imageFiles = [f for f in listdir(imageSourceDir) if (isfile(join(imageSourceDir,f)) & (f.split(".")[-1] in ["png","jpg"]))]

    transformedCount = 0
    failureCount = 0

    for file in imageFiles:
        try:
            img = Image.open(join(imageSourceDir,file))
            width, height = calcTransformDimension(img.size,(CONFIG["imageResize"]["dimensions"]["width"],CONFIG["imageResize"]["dimensions"]["height"]))
            print(width,height)
            img.resize((width,height)).save(join(imageOutDir,file))
            transformedCount += 1
        except:
            print(f"error transforming '{file}' - skipping.")
            failureCount += 1

    print(f"successfully resized {transformedCount} image(s), with {failureCount} failures.")
    input("press enter to exit.")
        





if __name__ == "__main__":
    main()