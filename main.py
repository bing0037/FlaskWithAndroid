from flask import Flask, request, jsonify

from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

import json
import numpy as np

from multiprocessing import Process  # multiple processing to deal with json data from client.
from PIL import Image
import io

app = Flask(__name__)

def img_save(data):
    '''
    save image and perform post processing
    '''
    try:
        # 2) Color Image Data:
        # 5) Base64.encodeToString(b_base64, Base64.DEFAULT) in java!
        # ref: https://www.programcreek.com/2013/09/convert-image-to-string-in-python/
        # ref: https://stackoverflow.com/questions/2323128/convert-string-in-base64-to-image-and-save-on-filesystem-in-python
        import base64
        Bitmap444 = data.get("ColorImage")
        # String to byte:
        Bit111Byte = str.encode(Bitmap444)
        # String to image: Work!
        import base64
        with open("imageToSave.png", "wb") as fh:
            image_data = base64.decodebytes(Bit111Byte)
            fh.write(image_data)
            image = Image.open(io.BytesIO(image_data))
            #image.show()

            # image to numpy:
            img_array = np.array(image)
            print(type(img_array))
            print(img_array.size)

    except:
        print("Unexpected error while reading: Bitmap444")

def depth_save(data):
    '''
    save depth information and perform post processing
    '''
    try:
        # 1) Depth Data:
        depth = data.get("DepthData")
        print(type(depth))
        # Save data.
        with open("DepthData.txt", "w") as text_file:
            text_file.write(depth) 

        # # Transform data into numpy array form. -libn
        # xyz=np.array(front.split(','))

        #     # # Transform data into numpy array form. -libn
        #     xyz=np.array(depth.split(',')).reshape(-1, )
        #     print(xyz.shape[0]/3)
        #     point_cloud = xyz.reshape(int(xyz.shape[0]/3), 3)
        #     print(point_cloud)

    except:
        print("Unexpected error while reading: front")


# root
@app.route("/")
def index():
    """
    this is a root dir of my server
    :return: str
    """
    return "This is root!!!!"


# GET
@app.route('/users/<user>')
def hello_user(user):
    """
    this serves as a demo purpose
    :param user:
    :return: str
    """
    return "Hello %s!" % user


# POST
@app.route('/api/post_some_data', methods=['POST'])
def get_text_prediction():
    """
    predicts requested text whether it is ham or spam
    :return: json
    """
    json = request.get_json()
    print(json)
    if len(json['text']) == 0:
        return jsonify({'error': 'invalid input'})

    return jsonify({'you sent this': json['text']})

import time
import cv2
    
# POST for Android PointCloudBuilder
@app.route('/jsonData', methods=['POST'])
def get_jsontttt_prediction():
    """
    predicts requested text whether it is ham or spam
    :return: json
    """
    start = time.time()
    jsondata = request.get_json()
    for x in jsondata:
        print(x)
    # data = json.load(jsondata)
    print(type(jsondata))
    print("I got data!: /jsonData")


    # get data from client. -libn
    data = jsondata.get("main_body")
    print(type(data))
 

    # # Image to String: Work!
    # import base64 
    # with open("lena.png", "rb") as imageFile:
    #     str222 = base64.b64encode(imageFile.read())
    #     print(str222)

    # # String to image: Work!
    # import base64
    # with open("imageToSave.png", "wb") as fh:
    #     fh.write(base64.decodebytes(Bit111Byte))
  


    #  Java->Python: Image transfer test! -20190111
    # # 1) Bitmap = rgbFrameBitmap.toString() in java!
    # Bitmap = data.get("Bitmap000")
    # print(type(Bitmap))
    # # String to byte:
    # BitMM = str.encode(Bitmap)
    # size = 320,240
    # im = Image.frombytes("1",size,BitMM,"raw","1;I")
    # im.save("Bitmap.bmp")
    # im.save("Bitmap.png")
    # im.save("Bitmap.jpg")
    # im.save("Bitmap.JPEG")

    # # 2) Bitmap111 = byteBuffer b in java!
    # Bitmap111 = data.get("Bitmap111")
    # # String to byte:
    # Bit111Byte = str.encode(Bitmap111)
    # # Byte to Image:
    # size = 320,240
    # im = Image.frombytes("1",size,Bit111Byte,"raw","1;I")
    # im.save("Bit111Byte.bmp")
    # im.save("Bit111Byte.png")
    # im.save("Bit111Byte.jpg")
    # im.save("Bit111Byte.JPEG")

    # # 3) Bitmap222 = rgbFrameBitmap.compress().toByteArray() in java!
    # Bitmap222 = data.get("Bitmap222")
    # # String to byte:
    # Bit222Byte = str.encode(Bitmap111)
    # # Byte to Image:
    # size = 320,240
    # im = Image.frombytes("1",size,Bit222Byte,"raw","1;I")
    # im.save("Bitmap222.bmp")
    # im.save("Bitmap222.png")
    # im.save("Bitmap222.jpg")
    # im.save("Bitmap222.JPEG")

    # # 4) Bitmap333 = byteBuffer b in java!
    # Bitmap333 = data.get("Bitmap111")
    # # String to byte:
    # Bit111Byte = str.encode(Bitmap333)
    # # Byte to Image:
    # size = 320,240
    # im = Image.frombytes("1",size,Bit111Byte,"raw","1;I")
    # im.save("Bitmap333.bmp")
    # im.save("Bitmap333.png")
    # im.save("Bitmap333.jpg")
    # im.save("Bitmap333.JPEG")

    img_save(data)
    depth_save(data)
    # start multiprocessing to deal with json data received from client.
    # p = Process(target=img_save, args=(data,))
    # p.start()
    # p.join()

    # p2 = Process(target=depth_save, args=(data,))
    # p2.start()
    # p2.join()

    # print(json)
    # if len(json['text']) == 0:
    #     return jsonify({'error': 'invalid input'})

    # return jsonify({'you sent this': json['text']}) 

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(1,2)}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    print('time elapse: ', time.time() - start)
    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=8080)

