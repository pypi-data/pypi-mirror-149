import requests, json, pickle
from importlib.machinery import SourceFileLoader
from termcolor import colored
import os

# hide warnings from tensorflow
import warnings

warnings.filterwarnings("ignore")


class Model:

    """
    Make sure model file and weights are in current directory
    Parameters: modelname

    modelname: model file name eg: vggnet, if file name is vggnet.py

    """

    def __init__(self, modelname, token, weights=False, url=""):
        self.__modelname = modelname
        self.__token = token
        self.weights = weights
        self.__url = url + "upload/"
        # self.__url = 'http://127.0.0.1:8000/upload/'
        self.__recievedModelname = self.upload()

    def getNewModelId(self):
        if self.__recievedModelname is not None:
            return self.__recievedModelname

    def checkModel(self):
        # load model from current directory
        try:
            modelFile = open(f"{self.__modelname}.py", "rb")
            modelFile.close()
            # check for model channels to be 3
            model = SourceFileLoader(
                self.__modelname, f"{self.__modelname}.py"
            ).load_module()
            model = model.MyModel()
            if model.input_shape[3] != 3:
                text = colored(
                    "Please provide model input shape with 3 channels", "red"
                )
                print(text, "\n")
                return False
            if self.weights == True:
                w = self.checkWeights()
                return w
            return True
        except FileNotFoundError:
            print(
                f"There is no model with the name '{self.__modelname}' in your folder '{os.getcwd()}'.\n"
            )
            print(f"Your model should be of a python file: '{self.__modelname}.py'")
            text = colored("Model upload failed!", "red")
            print(text, "\n")
            return False

    def checkWeights(self):
        # load model weights from current directory
        try:
            weightsFile = open(f"{self.__modelname}_weights.pkl", "rb")
        except FileNotFoundError:
            print(f"The model weights file does not meet the convention.")
            print(
                f"Expected weights name: '{self.__modelname}_weights.pkl'.\n Please check your model weights file name."
            )
            text = colored("Weights upload failed!", "red")
            print(text, "\n")
            return False
        # Load weights to check if it works
        try:
            # w = open(f"{self.__modelname}_weights.pkl", "rb")
            we = pickle.load(weightsFile)
            model = SourceFileLoader(
                self.__modelname, f"{self.__modelname}.py"
            ).load_module()
            model = model.MyModel()
            model.set_weights(we)
            weightsFile.close()
            return True
        except ValueError:
            weightsFile.close()
            text = colored("Weights not compatible with model.", "red")
            print(text, "\n")
            text = colored("Weights upload failed! Provide weights compatible with provided model!", "red")
            print(text, "\n")
            return False

    def upload(self):
        m = self.checkModel()
        if m:
            if self.weights == True:
                modelFile = open(f"{self.__modelname}.py", "rb")
                weightsFile = open(f"{self.__modelname}_weights.pkl", "rb")
                files = {"upload_file": modelFile, "upload_weights": weightsFile}
                values = {"model_name": self.__modelname, "setWeights": True}
            else:
                modelFile = open(f"{self.__modelname}.py", "rb")
                files = {"upload_file": modelFile}
                values = {"model_name": self.__modelname, "setWeights": False}
            # upload on the server
            header = {"Authorization": f"Token {self.__token}"}
            r = requests.post(self.__url, headers=header, files=files, data=values)
            if r.status_code == 202:
                body_unicode = r.content.decode("utf-8")
                content = json.loads(body_unicode)
                return content["model_name"]
            else:
                return None
        else:
            return None
