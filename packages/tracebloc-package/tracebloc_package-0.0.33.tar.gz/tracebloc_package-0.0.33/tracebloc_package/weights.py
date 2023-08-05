# import useful libraries
import pickle
from importlib.machinery import SourceFileLoader
import pickle
import tensorflow as tf
import os


class ModelWeights():
    '''
    Parameters: username, password

    ***
    Please provide a valid username and password
    Call getToken method on Login to get new token for provided
    username and password
    '''

    def __init__(self):

        self.__modelname = input("Enter Model Name : ")

    def generateweights(self):

        '''
        Make sure model file is in current directory
        Parameters: modelname

        modelname: model file name eg: vggnet, if file name is vggnet.py
        *******
        return: weights file
        '''
        try:
            if os.path.exists(self.__modelname+'.py'):
                model = SourceFileLoader(self.__modelname, f'{self.__modelname}.py').load_module()
                model = model.MyModel()
            else:
                print("Model file missing")
                return
        except FileNotFoundError:
            print(f"There is no model with the name {self.__modelname} in your folder {os.getcwd()}\n")
            print(f"Your model should be of a python file: {self.__modelname}.py")

        try:
            tf.keras.backend.clear_session()
            # print model input and output
            print("Model input shape: ", int(model.input_shape[2]))
            print("Model output shape: ", model.output_shape[-1])
            # Dump weights
            try:
                w = model.get_weights()
                output = open(f"{self.__modelname}_weights.pkl", "wb")
                pickle.dump(w, output)
                output.close()
                print(f"Dumped new weights for {self.__modelname} model")
            except Exception as e:
                print(f"Weights dump failed.\n")
        except Exception as e:
            print(f"{self.__modelname} Model load failed.\n")

    def checkweights(self):

        """
        Role: Check if weight are correct
        return: weights Summary
        """
        # Load weights to check if it works
        try:
            if os.path.exists(self.__modelname + '.py'):
                model = SourceFileLoader(self.__modelname, f'{self.__modelname}.py').load_module()
                model = model.MyModel()
            else:
                print("Model file missing")
                return
        except FileNotFoundError:
            print(f"There is no model with the name {self.__modelname} in your folder {os.getcwd()}\n")
            print(f"Your model should be of a python file: {self.__modelname}.py")

        try:
            w = open(f'{self.__modelname}_weights.pkl', 'rb')
            we = pickle.load(w)
            try:
                model.set_weights(we)
                model.summary()
            except Exception as e:
                print("Corrupt or Incompatible weights")
        except Exception as e:
            print(f"There is no weights with the name {self.__modelname} in your folder {os.getcwd()}\n")
