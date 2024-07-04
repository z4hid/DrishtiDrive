from DrishtiDrive.logger import logging
from DrishtiDrive.exception import AppException
from DrishtiDrive.utils.main_utils import decodeImage, encodeImageIntoBase64
import sys,os

from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS, cross_origin
from DrishtiDrive.pipeline.training_pipeline import TrainingPipeline
from DrishtiDrive.constant.training_pipeline.application import APP_HOST, APP_PORT

# obj = TrainingPipeline()
# obj.run_pipeline()


app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = 'inputimage.jpg'
           

@app.route('/train')
def trainingRoute():
    obj = TrainingPipeline()
    obj.run_pipeline()
    return 'Training successfull'

@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/predict', methods=['POST', 'GET'])
# @cross_origin()
# def predictRoute():
#     try:
#         image = request.json['image']
#         decodeImage(image, clApp.filename)
#         os.system("cd yolov5/ && python detect.py --weights best.pt --img 416 --conf 0.5 --source ../data/inputimage.jpg")
#         opencodedbase64 = encodeImageIntoBase64("yolov5/runs/detect/exp/inputimage.jpg")
#         result = {"image": opencodedbase64.decode('utf-8')}
#         os.system("rm -rf yolov5/runs")
#     except ValueError as val:
#         print(val)
#         return Response("Value not found inside  json data")
#     except KeyError:
#         return Response("Key value error incorrect key passed")
#     except Exception as e:
#         print(e)
#         result = "Invalid input"

#     return jsonify(result)

@app.route('/predict', methods=['POST', 'GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image, clApp.filename)
        
        # Debugging: Print current directory and its contents
        print("Current Working Directory:", os.getcwd())
        print("Files in current directory:", os.listdir(os.getcwd()))
        print("Files in yolov5 directory:", os.listdir('yolov5'))
        

        
        # Execute detection script with correct paths
        os.system(f"cd yolov5 && python detect.py --weights best.pt --img 416 --conf 0.5 --source ../data/inputimage.jpg")
        
        # Find the latest run folder dynamically
        exp_folder = max([os.path.join('yolov5/runs/detect', d) for d in os.listdir('yolov5/runs/detect')], key=os.path.getmtime)
        output_image_path = os.path.join(exp_folder, 'inputimage.jpg')
        
        if not os.path.exists(output_image_path):
            return Response(f"Output image not found at {output_image_path}", status=404)
        
        opencodedbase64 = encodeImageIntoBase64(output_image_path)
        result = {"image": opencodedbase64.decode('utf-8')}
        os.system("rm -rf yolov5/runs")
    except ValueError as val:
        print(val)
        return Response("Value not found inside json data", status=400)
    except KeyError:
        return Response("Key value error: incorrect key passed", status=400)
    except Exception as e:
        print(e)
        result = "Invalid input"
        return Response(str(e), status=500)

    return jsonify(result)






@app.route("/live", methods=['GET'])
@cross_origin()
def predictLive():
    try:
        os.system("cd yolov5/ && python detect.py --weights best.pt --img 416 --conf 0.5 --source 0")
        os.system("rm -rf yolov5/runs")
        return "Camera starting!!" 

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    



if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host=APP_HOST, port=APP_PORT)