import base64, re
from PIL import Image
from io import BytesIO

def saveToBmp(fileIn,fileOut,width=None,fmt="BMP",base64Input=False):
    if (type(fileIn) == str and fileIn.startswith("data:image")) or base64Input:
        b64 = re.sub('^data:image/.+;base64,', '', fileIn)
        image_data = base64.b64decode(b64)
        img = Image.open(BytesIO(image_data))
    else:    
        img = Image.open(fileIn)


    w, h = img.size
    if h > 128 or w > 160 or fmt.upper() == 'BMP':
        img = img.convert("RGB")

    if h > 128 or w > 160:
        # do resize
        ratio_h = 128/h
        ratio_w = 160/w
        
        _w = int(round(w*ratio_h, 0))
        _h = int(round(h*ratio_h, 0))
        if _w<160:
            _w = int(round(w*ratio_w, 0))
            _h = int(round(h*ratio_w, 0))
        # print("resize img {} {}".format((w,h), (_w,_h)))
        img = img.resize((_w,_h))

    img.save(fileOut, fmt.upper())

if __name__ == "__main__":
    from hashlib import md5
    saveToBmp('down.png', 'down_cvt.png', fmt='png')
    print("md5 oss:", md5(open('down_oss.png', "rb").read()).hexdigest())
    print("md5 converted:", md5(open('down_cvt.png', "rb").read()).hexdigest())
    # encoded = base64.b64encode(data)
    # saveToBmp("data:image/jpeg;base64,"+encoded.decode(), 'test2.bmp')

