# 导入所需工具包
from pyzbar import pyzbar
import argparse
import cv2
import requests
from PIL import Image, ImageDraw, ImageFilter
import qrcode
import time
def revertShortLink(url):
    beforeUrl = ''
    for i in range(10):
        # try:
        url = requests.head(url).headers.get('Location')
        print('###revertShortLink=>', url)
        if not url:
            return beforeUrl
        beforeUrl = url
        # except Exception as e:
        #     print('revertShortLink error:{}'.format(e))
        #     return beforeUrl


def getImgQrcode(imgPath):
    image = cv2.imread(imgPath)
    barcodes = pyzbar.decode(image)

    print('barcodes len=====>',len(barcodes))
    print('barcodes=====>',barcodes)

    if len(barcodes) != 1:
        return None

    # 循环检测到的条形码
    for barcode in barcodes:
        # barcode = barcodes[0]
        # 提取条形码的边界框的位置
        # 画出图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        print("rect x:{},y:{},w:{},h:{}".format(x, y, w, h))
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), 2)

        # 条形码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # 绘出图像上条形码的数据和条形码类型
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 0, 255), 2)

        # 向终端打印条形码数据和条形码类型
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        orgLink = revertShortLink(barcodeData)
        print("real link:{}".format(orgLink))

    # return barcodeData, (x, y, w, h)
    return {
        'orgLink': orgLink,
        'x': x,
        'y': y,
        'w': w,
        'h': h
    }
        # image.show()
        # 展示输出图像
        # cv2.imshow("Image", image)
        # cv2.imwrite('./tt.jpg', image, flag)
        # cv2.imwrite('1.png', image, [int(cv2.IMWRITE_JPEG_QUALITY),95])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        # im1 = Image.open('./test.jpeg')
        # im2 = Image.open('./lena.jpg')
        # im1.paste(im2)
        # im1.save('./paste.jpg', quality=95)


def createQrcode(data):
    # 二维码内容
    # data = "https://www.baidu.com"
    # # 生成二维码
    # img = qrcode.make(data=data)
    # return img

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    return qr.make_image()

def createNewLink(orgLink, newShopId):
    orgShopId = orgLink.split('shopId')[1].split('&')[0].split('=')[1]
    print('orgLink:{}'.format(orgLink))
    print('orgShopId:{}'.format(orgShopId))
    newLink = orgLink.replace(orgShopId, newShopId)
    return newLink

def createLinkQrcode(orgLink, newShopId):
    newLink = createNewLink(orgLink, newShopId)
    return createQrcode(newLink)



def createNewImg(imgPath, shopId):
    # shopId = 'r5z8PqwirG'
    ret = getImgQrcode(imgPath)
    if not ret:
        print('no qrcode!')
        return imgPath
        
    im0 = createLinkQrcode(ret['orgLink'], shopId)
    im0.save('newLink.png')
    # print('ret==>', ret)
    im1 = cv2.imread(imgPath)
    im2 = cv2.imread("newLink.png")
    # im2 = cv2.imread("newLink.jpg", -1) 
    # im2 = createQrcode()
    height, width = im2.shape[:2] 
    size = (ret['w'],ret['h']) #(int(width*0.3), int(height*0.5)) 
    im2 = cv2.resize(im2, size, interpolation=cv2.INTER_AREA) 
    im1[ret['y']: (ret['y'] + im2.shape[0]), ret['x']:(ret['x']+im2.shape[1])] = im2
    picName = './file_tmp/{}.jpg'.format(int(time.time()*1000))
    cv2.imwrite(picName, im1, [int(cv2.IMWRITE_JPEG_QUALITY),95])
    return picName

def main():
    # 构建参数解析器并解析参数
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image")
    args = vars(ap.parse_args())
    createNewImg(args['image'], 'r5z8PqwirG')

if __name__ == "__main__":
    main()