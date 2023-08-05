import base64
import six.moves.urllib as urllib

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open("./"+fileName, 'wb') as f:
        f.write(imgdata)
        f.close()


def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())


def download_model(base_url, model_path, model_name):
    opener = urllib.request.URLopener()
    opener.retrieve(base_url + model_path, model_name)
