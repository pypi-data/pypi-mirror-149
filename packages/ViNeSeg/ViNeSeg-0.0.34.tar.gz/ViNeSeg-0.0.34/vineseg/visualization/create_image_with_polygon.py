from PIL import Image, ImageDraw
import pandas as pd
import numpy as np
import ast 
PATH_POLYGON_CSV = "/home/webern/idsair_public/prediction/Img_190118_spon_11-50-38_mocopolygons.csv"
PATH_IMAGE = "/home/webern/idsair_public/data/mean_images_julian/test/img/Img_190118_spon_11-50-38_moco.png"
PATH_SAVE_IMAGE = "/home/webern/idsair_public/visualization"
im = Image.open(PATH_IMAGE)
im = im.convert('RGB')
draw = ImageDraw.Draw(im)
df = pd.read_csv(PATH_POLYGON_CSV)
df = df.iloc[: , 1:]
for column in df.columns:
    pixel_positions = []
    for pixel in df[column].to_list():
        if not pd.isna(pixel):
            pixel_positions.append(tuple(reversed(tuple(ast.literal_eval(pixel)))))
    draw.polygon(pixel_positions, outline = "red")

im.save(PATH_SAVE_IMAGE + "test.png")
