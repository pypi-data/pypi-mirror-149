__version__='90.12.4.0.dev1'

import os
import fitz
from PIL import Image

NDD_left = 220
NDD_top = 60
NDD_right = 4650
NDD_bottom = 3230

NFD_left = 220
NFD_top = 220
NFD_right = 3090
NFD_bottom = 3255

Station_left = 220
Station_top = 220
Station_right = 4425
Station_bottom = 3255

ZK_left = 70
ZK_top = 230
ZK_right = 3230
ZK_bottom = 2260

def fPngFromPdf(
    file # PDF-File
   ,crop='ZK' # how to crop PNG-File after extraction: 'ZK', 'NDD', 'Station', 'NFD' or None or (left,top,right,bottom)
    ):
    """
    generates PNG-Files for every Page in PDF-File

    cropping options:

        * ZK
        * NDD
        * Station
        * NFD
        * None
        * (left, top, right, bottom)
    """

    dirname=os.path.dirname(file)
    dummy,filename=os.path.split(file)
    filenameNetto,fileExt=os.path.splitext(filename)


    zoom_x = 4.0  # horizontal zoom
    zoom_y = 4.0  # vertical zoom
    mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension


    with fitz.open(file)as doc:  # open document

        if crop=='ZK':
            (crop_left,crop_top,crop_right,crop_bottom)=(ZK_left,ZK_top,ZK_right,ZK_bottom)
        elif crop=='NDD':
            (crop_left,crop_top,crop_right,crop_bottom)=(NDD_left,NDD_top,NDD_right,NDD_bottom)
        elif crop=='NFD':
            (crop_left,crop_top,crop_right,crop_bottom)=(NFD_left,NFD_top,NFD_right,NFD_bottom)
        elif crop=='Station':
            (crop_left,crop_top,crop_right,crop_bottom)=(Station_left,Station_top,Station_right,Station_bottom)
        elif crop == None:
            pass
        else:
            (crop_left,crop_top,crop_right,crop_bottom)=crop

        for idxPage,page in enumerate(doc):  # iterate through the pages

            # Ausgabedatei
            if len(doc)>1:
                png_name="{:s}_{:d}.png".format(filenameNetto,idxPage+1)
            else:
                png_name="{:s}.png".format(filenameNetto)
            png_NameFull=os.path.join(dirname,png_name)

            pix = page.get_pixmap(matrix=mat)  # render page to an image
            pix.save(png_NameFull)  # store image as a PNG

            # Nachbearbeitung
            if crop != None:
                im = Image.open(png_NameFull)
                im = im.crop((crop_left,crop_top,crop_right,crop_bottom))
                im.save(png_NameFull)