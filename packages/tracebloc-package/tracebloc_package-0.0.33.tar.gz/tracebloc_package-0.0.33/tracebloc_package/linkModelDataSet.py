import requests, json
from termcolor import colored


class LinkModelDataSet:
    """
    creating a training plan and assign data set
    parameters: modelId, datasetId, token

    methods:get_parameters, get_trainingplan
    """

    def __init__(self, modelId, datasetId, token, weights, total_images, num_classes,
                 url="", environment="production"):
        self.__url = url
        # self.__url = 'http://127.0.0.1:8000/'
        self.__token = token
        self.__earlystopCallback = {}
        self.__reducelrCallback = {}
        self.__modelCheckpointCallback = {}
        self.__terminateOnNaNCallback = {}
        self.__learningRateScheduler = {}
        self.__callbacks = str()
        self.__message = "training"
        self.__datasetId = datasetId
        self.__epochs = 10
        self.__cycles = 1
        self.__modelName = modelId
        self.__optimizer = "adam"
        self.__lossFunction = "categorical_crossentropy"
        self.__learningRate = 0.001
        self.__stepsPerEpoch = "None"
        self.__initialEpoch = 0
        self.__validationSteps = "None"
        self.__batchSize = 32
        self.__featurewise_center = False
        self.__samplewise_center = False
        self.__featurewise_std_normalization = False
        self.__samplewise_std_normalization = False
        self.__zca_whitening = False
        self.__rotation_range = 0
        self.__width_shift_range = 0.0
        self.__height_shift_range = 0.0
        self.__brightness_range = "None"
        self.__shear_range = 0.0
        self.__zoom_range = 0.0
        self.__channel_shift_range = 0.0
        self.__fill_mode = "nearest"
        self.__cval = 0.0
        self.__horizontal_flip = False
        self.__vertical_flip = False
        self.__rescale = "None"
        self.__data_format = "None"
        self.__validation_split = 0.1
        self.__dtype = "None"
        self.__shuffle = True
        self.__layers_non_trainable = ""
        self.__metrics = str(["accuracy"])
        self.__objective = ""
        self.__name = "None"
        self.__modelType = "None"
        self.__category = "None"
        self.__upperboundTime = 0
        self.__weights = weights
        self.__total_images = total_images
        self.__num_classes = num_classes
        self.__eligibility_passed = True
        self.__experimenturl = "https://ai.tracebloc.io/experiments/"
        if environment == "development" or environment == "ds":
            self.__experimenturl = "https://dev.tracebloc.io/experiments/"
        elif environment == "staging":
            self.__experimenturl = "https://stg.tracebloc.io/experiments/"


    def category(self, category: str):
        """
        String.
        Category of experiment, like classification
        example:trainingObject.category('classification')


        """
        if type(category) == str:
            self.__category = category
        else:
            print("Invalid input type given for category\n\n")

    def modelType(self, modelType: str):
        """
        String.
        Type of model used in the experiment, like VGGNET
        example:trainingObject.modelType('VGGNET')


        """
        if type(modelType) == str:
            self.__modelType = modelType
        else:
            print("Invalid input type given for modelType\n\n")

    def name(self, name: str):
        """
        String.
        Name of the experiment
        example:trainingObject.name('Classifying manufacturing defects')


        """
        if type(name) == str:
            self.__name = name
        else:
            print("Invalid input type given for name\n\n")

    def objective(self, objective: str):
        """
        String.
        Objective of the experiment
        example:trainingObject.objective('Classify images using Convolutional Neural Networks (specifically, VGG16)
        pre-trained on the ImageNet dataset with Keras deep learning library.')


        """
        if type(objective) == str:
            self.__objective = objective
        else:
            print("Invalid input type given for objective\n\n")

    def epochs(self, epochs: int):
        """
        Integer.
        Number of epochs to train the model.
        An epoch is an iteration over the entire data provided.
        Note that in conjunction with initial_epoch, epochs is to be understood as "final epoch".
        The model is not trained for a number of iterations given by epochs,
        but merely until the epoch of index epochs is reached.
        example: trainingObject.epochs(100)
        default: 10


        """
        if type(epochs) == int and epochs != 0:
            self.__epochs = epochs
        else:
            print("Invalid input type or value '0' given for epochs\n\n")

    def cycles(self, cycles: int):
        """
        Set number of cycles
        parameters: integer type values.
        example: trainingObject.cycles(10)
        default: 1


        """
        if type(cycles) == int and cycles != 0:
            self.__cycles = cycles
        else:
            print("Invalid input type or value '0' given for cycles\n\n")

    def optimizer(self, optimizer: str):
        """
        String (name of optimizer)
        example: trainingObject.optimizer('rmsprop')
        supported optimizers: ['adam','rmsprop','sgd','adadelta', 'adagrad', 'adamax','nadam', 'ftrl']
        default: 'adam'


        """
        o = ["adam", "rmsprop", "sgd", "adadelta", "adagrad", "adamax", "nadam", "ftrl"]
        try:
            o.index(optimizer.lower())
            self.__optimizer = optimizer.lower()
        except:
            print(f"Please provide supported optimizers: {o}\n\n")

    def lossFunction(self, lossFunction: str):
        """
        Set loss function
        parameters: string type values.
        example: trainingObject.lossFunction('binary_crossentropy')
        supported loss functions: ['binary_crossentropy','categorical_crossentropy']
        default: "categorical_crossentropy"


        """
        l = ["binary_crossentropy", "categorical_crossentropy"]
        try:
            l.index(lossFunction.lower())
            self.__lossFunction = lossFunction.lower()
        except:
            print(f"Please provide supported loss functions: {l}\n\n")

    def learningRate(self, learningRate: float):
        """
        Set learning rate for optimization.
        example: trainingObject.learningRate(0.0001)
        default: 0.001


        """
        if type(learningRate) == float and learningRate != 0:
            self.__learningRate = learningRate
        else:
            print("Invalid input type or value '0' given for learningRate\n\n")

    # def stepsPerEpoch(self, stepsPerEpoch: int):
    #     """
    #     Integer.
    #     Total number of steps (batches of samples) before declaring
    #     one epoch finished and starting the next epoch.
    #     example: setStepsPerEpoch(5)
    #     default: None
    #     """
    #     if type(stepsPerEpoch) == int and stepsPerEpoch >= 15:
    #         self.__stepsPerEpoch = stepsPerEpoch
    #     else:
    #         print(
    #             "Invalid input type or value less than 15 given for stepsPerEpoch\n\n"
    #         )

    # def initialEpoch(self, initialEpoch: int):
    #     """
    #     Integer. Epoch at which to start training
    #     (useful for resuming a previous training run).
    #     example: setInitialEpoch(2)
    #     default: 0
    #     """
    #     if type(initialEpoch) == int:
    #         self.__initialEpoch = initialEpoch
    #     else:
    #         print("Invalid input type given for initialEpoch\n\n")

    # def validationSteps(self, validationSteps: int):
    #     """
    #     Integer. Total number of steps (batches of samples) to draw before stopping
    #     when performing validation at the end of every epoch.
    #     example: setValidationSteps(20)
    #     default: None
    #     """
    #     if type(validationSteps) == int and validationSteps >= 15:
    #         self.__validationSteps = validationSteps
    #     else:
    #         print(
    #             "Invalid input type or value less than 15 given for validationSteps\n\n"
    #         )

    def batchSize(self, batchSize: int):
        """
        Integer or None. Number of samples per gradient update. If unspecified, batch_size will default to 32.
        example: trainingObject.batchSize(16)
        default: 32


        """
        self.__eligibility_passed = True
        # get edge with lowest images
        edge_min = min(self.__total_images, key=self.__total_images.get)
        # get images count for selected edge
        images = int(self.__total_images[edge_min])
        # check for no of batches
        if images // batchSize < 3:
            print("Please choose smaller batch size as dataset selected have less images\n\n")
            self.__eligibility_passed = False
            return
        if type(batchSize) == int:
            self.__batchSize = batchSize
        else:
            print("Invalid input type given for batchSize\n\n")

    def featurewise_center(self, featurewise_center: bool):
        """
        Boolean. Set input mean to 0 over the dataset, feature-wise.
        example: trainingObject.featurewise_center(True)
        default: False


        """
        if type(featurewise_center) == bool:
            self.__featurewise_center = featurewise_center
        else:
            print("Invalid input type given for featurewise_center\n\n")

    def samplewise_center(self, samplewise_center: bool):
        """
        Boolean. Set each sample mean to 0.
        example: trainingObject.samplewise_center(True)
        default: False


        """
        if type(samplewise_center) == bool:
            self.__samplewise_center = samplewise_center
        else:
            print("Invalid input type given for samplewise_center\n\n")

    def featurewise_std_normalization(self, featurewise_std_normalization: bool):
        """
        Boolean. Divide inputs by std of the dataset, feature-wise.
        example: trainingObject.featurewise_std_normalization(True)
        default: False


        """
        if type(featurewise_std_normalization) == bool:
            self.__featurewise_std_normalization = featurewise_std_normalization
        else:
            print("Invalid input type given for featurewise_std_normalization\n\n")

    def samplewise_std_normalization(self, samplewise_std_normalization: bool):
        """
        Boolean. Divide each input by its std.
        example: trainingObject.samplewise_std_normalization(True)
        default: False


        """
        if type(samplewise_std_normalization) == bool:
            self.__samplewise_std_normalization = samplewise_std_normalization
        else:
            print("Invalid input type given for samplewise_std_normalization\n\n")

    def zca_whitening(self, zca_whitening: bool):
        """
        Boolean. Apply ZCA whitening.
        example: trainingObject.zca_whitening(True)
        default: False


        """
        if type(zca_whitening) == bool:
            self.__zca_whitening = zca_whitening
        else:
            print("Invalid input type given for zca_whitening\n\n")

    def rotation_range(self, rotation_range: int):
        """
        Int. Degree range for random rotations.
        example: trainingObject.rotation_range(2)
        default: 0


        """
        if type(rotation_range) == int:
            self.__rotation_range = rotation_range
        else:
            print("Invalid input type given for rotation_range\n\n")

    def width_shift_range(self, width_shift_range):
        """
        Float or int
        float: fraction of total width, if < 1, or pixels if >= 1.
        int: integer number of pixels from interval (-width_shift_range, +width_shift_range)
        With width_shift_range=2 possible values are integers [-1, 0, +1], same as with width_shift_range=[-1, 0, +1],
        while with width_shift_range=1.0 possible values are floats in the interval [-1.0, +1.0).
        example: trainingObject.width_shift_range(0.1)
        default: 0.0


        """
        if type(width_shift_range) == float or type(width_shift_range) == int:
            self.__width_shift_range = width_shift_range
        else:
            print("Invalid input type given for width_shift_range\n\n")

    def height_shift_range(self, height_shift_range):
        """
        Float or int
        float: fraction of total height, if < 1, or pixels if >= 1.
        int: integer number of pixels from interval (-height_shift_range, +height_shift_range)
        With height_shift_range=2 possible values are integers [-1, 0, +1], same as with height_shift_range=[-1, 0, +1],
        while with height_shift_range=1.0 possible values are floats in the interval [-1.0, +1.0).
        example: trainingObject.height_shift_range(0.1)
        default: 0.0


        """
        if type(height_shift_range) == float or type(height_shift_range) == int:
            self.__height_shift_range = height_shift_range
        else:
            print("Invalid input type given for height_shift_range\n\n")

    def brightness_range(self, brightness_range):
        """
        Tuple or list of two floats. Range for picking a brightness shift value from.
        example: trainingObject.brightness_range((0.1,0.4))
        default: None


        """
        if (type(brightness_range) == tuple and len(brightness_range) == 2) or \
                (type(brightness_range) == list and len(brightness_range)) == 2:

            if (
                    type(brightness_range[0]) == float
                    and type(brightness_range[1]) == float
            ):
                brightness_range = str(brightness_range)
                self.__brightness_range = brightness_range
            else:
                print("provide float values for brightness_range\n\n")
        else:
            print("Please provide tuple of two floats for brightness_range\n\n")

    def shear_range(self, shear_range: float):
        """
        Float. Shear Intensity (Shear angle in counter-clockwise direction in degrees)
        example: trainingObject.shear_range(0.2)
        default: 0.0


        """
        if type(shear_range) == float:
            self.__shear_range = shear_range
        else:
            print("Invalid input type given for shear_range\n\n")

    def zoom_range(self, zoom_range):
        """
        Float or [lower, upper]. Range for random zoom. If a float, [lower, upper] = [1-zoom_range, 1+zoom_range].
        example: trainingObject.zoom_range(0.2)
        default: 0.0


        """
        if type(zoom_range) == float or type(zoom_range) == list:
            self.__zoom_range = zoom_range
        else:
            print("Invalid input type given for zoom_range\n\n")

    def channel_shift_range(self, channel_shift_range: float):
        """
        Float. Range for random channel shifts.
        example: trainingObject.channel_shift_range(0.4)
        default: 0.0


        """
        if type(channel_shift_range) == float:
            self.__channel_shift_range = channel_shift_range
        else:
            print("Invalid input type given for channel_shift_range\n\n")

    def fill_mode(self, fill_mode: str):
        """
        One of {"constant", "nearest", "reflect" or "wrap"}. Default is 'nearest'.
        Points outside the boundaries of the input are filled according to the given mode:
        'constant': kkkkkkkk|abcd|kkkkkkkk (cval=k)
        'nearest': aaaaaaaa|abcd|dddddddd
        'reflect': abcddcba|abcd|dcbaabcd
        'wrap': abcdabcd|abcd|abcdabcd
        example: trainingObject.fill_mode("nearest")
        default: "nearest"


        """
        f = ["constant", "nearest", "reflect", "wrap"]
        try:
            f.index(fill_mode.lower())
            self.__fill_mode = fill_mode.lower()
        except:
            print(f"Please provide supported fill modes: {f}\n\n")

    def cval(self, cval: float):
        """
        Float or Int. Value used for points outside the boundaries when fill_mode = "constant".
        example: trainingObject.cval(0.3)
        default: 0.0


        """
        if type(cval) == float:
            self.__cval = cval
        else:
            print("Invalid input type given for cval\n\n")

    def horizontal_flip(self, horizontal_flip: bool):
        """
        Boolean. Randomly flip inputs horizontally.
        example: trainingObject.horizontal_flip(True)
        default: False


        """
        if type(horizontal_flip) == bool:
            self.__horizontal_flip = horizontal_flip
        else:
            print("Invalid input type given for horizontal_flip\n\n")

    def vertical_flip(self, vertical_flip: bool):
        """
        Boolean. Randomly flip inputs vertically.
        example: trainingObject.vertical_flip(True)
        default: False


        """
        if type(vertical_flip) == bool:
            self.__vertical_flip = vertical_flip
        else:
            print("Invalid input type given for vertical_flip\n\n")

    def rescale(self, rescale:float):
        """
        rescaling factor. Defaults to None. If None, no rescaling is applied,
        otherwise we multiply the data by the value provided (after applying all other transformations).
        example: trainingObject.rescale(0.003921568627)
        default: None


        """
        print("\n")
        if type(rescale) == float:
            self.__rescale = rescale
        else:
            print("Invalid input type given for rescale\n\n")

    # def data_format(self, data_format: str):
    #     """
    #     String.
    #     Image data format, either "channels_first" or "channels_last".
    #     "channels_last" mode means that the images should have shape
    #     (samples, height, width, channels),
    #     "channels_first" mode means that the images should have shape
    #     (samples, channels, height, width).
    #     example: setDataFormat("channels_first")
    #     default: None
    #     """
    #     d = ["channels_last"]
    #     try:
    #         d.index(data_format.lower())
    #         self.__data_format = data_format.lower()
    #     except:
    #         print(f"Please provide supported fill modes: {d}\n\n")

    def validation_split(self, validation_split: float):
        """
        Float. Fraction of images reserved for validation (strictly between 0 and 1).
        example: trainingObject.validation_split(0.2)
        default: 0.1


        """
        self.__eligibility_passed = True
        # calculate minimum validation split using the following equation
        # minimum = number of classes / total images
        # get edge with lowest images
        edge_min = min(self.__total_images, key=self.__total_images.get)
        images = int(self.__total_images[edge_min])
        minimum = round(self.__num_classes / images, 2)

        if type(validation_split) == float and minimum <= validation_split <= 1.0:
            self.__validation_split = validation_split
        else:
            self.__eligibility_passed = False
            print(f"Invalid input type or set value not less than {minimum} for validation_split\n\n")

    # def dtype(self, dtype: str):
    #     """
    #     String.
    #     Dtype to use for the generated arrays.
    #     example: dtype('float32')
    #     default: None
    #     """
    #     d = ["float32", "float64"]
    #     try:
    #         d.index(dtype.lower())
    #         self.__dtype = dtype.lower()
    #     except:
    #         print(f"Please provide supported fill modes: {d}\n\n")

    def shuffle(self, shuffle: bool):
        """
        whether to shuffle the data (default: True)
        example: trainingObject.shuffle(False)
        default: True


        """
        if type(shuffle) == bool:
            self.__shuffle = shuffle
        else:
            print("Invalid input type given for shuffle\n\n")

    def layersFreeze(self, layersFreeze: list):
        """
        Provide name of layers in a list to be frozen before training a model.
        example: trainingObject.layersFreeze(['conv1','fc1'])
        default: None


        """
        if type(layersFreeze) == list and all(
                isinstance(sub, str) for sub in layersFreeze
        ):
            layersFreeze = str(layersFreeze)
            self.__layers_non_trainable = layersFreeze
        else:
            print("Provide values as list of strings for layersFreeze\n\n")

    # def metrics(self,metrics:list):
    # 	'''
    # 	List of strings.
    # 	List of metrics to be evaluated by the model
    # 	during training and testing.
    # 	example: setMetrics(['accuracy','mse'])
    # 	default: ['accuracy']
    # 	'''
    # 	if type(metrics)== list and all(isinstance(sub, str) for sub in metrics):
    # 		metrics = str(metrics)
    # 		self.__metrics = metrics
    # 	else:
    # 		print("Provide values as list of strings")

    # def setLearningRateSchedulerCallback(self, factor: float, patience: int):
    #     """
    #     Schedule learning rate at some patience to change by a factor.
    #     parameters: factor: factor by which the learning rate will be reduced. new_lr = lr * tf.math.exp(-factor).
    #                             patience: Number of epochs after which lr will be updated.
    #     example: trainingObject.setLearningRateSchedulerCallback(0.1, 10)
    #
    #
    #     """
    #     if type(factor) == float and type(patience) == int:
    #         c = [factor, patience]
    #         self.__learningRateScheduler["learningRateScheduler"] = c
    #     else:
    #         print(
    #             "Invalid datatype for arguments given for setLearningRateSchedulerCallback\n\n"
    #         )

    def terminateOnNaNCallback(self):
        """
        Callback that terminates training when a NaN loss is encountered.
        example: `trainingObject.`terminateOnNaNCallback()


        """
        c = [""]
        self.__terminateOnNaNCallback["terminateOnNaN"] = c

    def modelCheckpointCallback(self, monitor: str, save_best_only: bool):
        """
        Callback to save the model weights. parameters: monitor: Quantity to be monitored, save_best_only:  if
        save_best_only=True, it only saves when the model is considered the "best" and the latest best model
        according to the quantity monitored will not be overwritten. example: trainingObject.modelCheckpointCallback(
        'val_loss', True)


        """
        f = ["accuracy", "loss", "val_loss", "val_accuracy"]
        try:
            f.index(monitor.lower())
        except:
            print(f"Please provide supported monitor values: {f}\n\n")

        if type(save_best_only) == bool:
            c = [monitor, save_best_only]
            self.__modelCheckpointCallback["modelCheckpoint"] = c
        else:
            print(
                "Invalid datatype for arguments given for save_best_only\n\n"
            )

    def earlystopCallback(self, monitor: str, patience: int):
        """
        Stop training when a monitored metric has stopped improving.
        parameters: monitor: Quantity to be monitored,
                                patience: Number of epochs with no improvement after which training will be stopped.
        example: trainingObject.earlystopCallback('loss', 10)


        """
        f = ["accuracy", "loss", "val_loss", "val_accuracy"]
        try:
            f.index(monitor.lower())
        except:
            print(f"Please provide supported monitor values: {f}\n\n")
        if type(patience) == int:
            c = [monitor, patience]
            self.__earlystopCallback["earlystopping"] = c
        else:
            print("Invalid datatype for arguments given for patience\n\n")

    def reducelrCallback(
            self, monitor: str, factor: float, patience: int, min_delta: float
    ):
        """
        Reduce learning rate when a metric has stopped improving. parameters: monitor: Quantity to be monitored,
        factor: factor by which the learning rate will be reduced. new_lr = lr * factor. patience: number of epochs
        with no improvement after which learning rate will be reduced. min_delta: threshold for measuring the new
        optimum, to only focus on significant changes.
        example: trainingObject.reducelrCallback('loss', 0.1, 10, 0.0001)


        """
        f = ["accuracy", "loss", "val_loss", "val_accuracy"]
        try:
            f.index(monitor.lower())
        except:
            print(f"Please provide supported monitor values: {f}\n\n")
        if (
                type(factor) == float
                and type(patience) == int
                and type(min_delta) == float
        ):
            c = [monitor, factor, patience, min_delta]
            self.__reducelrCallback["reducelr"] = c
        else:
            print("Invalid datatype for arguments given for reducelrCallback\n\n")

    def __setCallbacks(self):
        """
        List of dictionaries.
        List of tensorflow callbacks for training.
        default: []
        """
        c = []
        if len(self.__reducelrCallback) != 0:
            c.append(self.__reducelrCallback)
        if len(self.__earlystopCallback) != 0:
            c.append(self.__earlystopCallback)
        if len(self.__modelCheckpointCallback) != 0:
            c.append(self.__modelCheckpointCallback)
        if len(self.__terminateOnNaNCallback) != 0:
            c.append(self.__terminateOnNaNCallback)
        # if len(self.__learningRateScheduler) != 0:
        #     c.append(self.__learningRateScheduler)

        self.__callbacks = str(c)

    # 	def __display_time(self,seconds, granularity=5):
    # 		intervals = (
    # 		('weeks', 604800),  # 60 * 60 * 24 * 7
    # 		('days', 86400),    # 60 * 60 * 24
    # 		('hours', 3600),    # 60 * 60
    # 		('minutes', 60),
    # 		('seconds', 1),)
    # 		result = []
    #
    # 		for name, count in intervals:
    # 			value = seconds // count
    # 			if value:
    # 				seconds -= value * count
    # 				if value == 1:
    # 					name = name.rstrip('s')
    # 				result.append("{} {}".format(value, name))
    # 		return ', '.join(result[:granularity])
    #
    #
    # 	def getEstimate(self):
    #
    # 		header = {'Authorization' : f"Token {self.__token}"}
    # 		re = requests.post(f"{self.__url}flops/",headers= header,data={'datasetId':self.__datasetId,
    # 			'batchSize':self.__batchSize,'noOfEpochs':self.__epochs,'modelName':self.__modelName})
    # # 		print(re.status_code)
    # 		if re.status_code == 200:
    #
    # 			body_unicode = re.content.decode('utf-8')
    # 			content = int(json.loads(body_unicode))
    # 			self.__upperboundTime = content
    # 			cycleTime = content * self.__cycles
    # 			display = self.__display_time(cycleTime)
    #
    # 			print(f"It will take around {display} to complete {self.__cycles} cycles for given training plan.")
    def __checkTrainingPlan(self):
        # call API to compare current training plan for duplication
        header = {"Authorization": f"Token {self.__token}"}
        data = {"parameters": json.dumps(self.__getParameters())}
        # print(data,"\n\n")
        re = requests.post(
            f"{self.__url}trainingplan/{self.__datasetId}/", headers=header, data=data
        )
        # print(re.text)
        if re.status_code == 200:
            body_unicode = re.content.decode("utf-8")
            content = json.loads(body_unicode)
            # print(content)
            if content["status"]:
                userResponse = input(
                    "You already have an experiment with current Training Plan want to proceed?\n\n"
                )
                if userResponse.lower() == "yes":
                    return True
                return False
            else:
                return True

    def create(self):
        # set callbacks
        self.__setCallbacks()
        # call checkTrainingPlan for duplication check
        duplication = self.__checkTrainingPlan()
        if duplication:
            # Create Experiment
            header = {"Authorization": f"Token {self.__token}"}
            re = requests.post(
                f"{self.__url}experiments/", headers=header, data=self.__getParameters()
            )
            if re.status_code == 201:
                body_unicode = re.content.decode("utf-8")
                content = json.loads(body_unicode)
                text = colored(
                    f"Experiment created with id:{content['experimentKey']}", "green"
                )
                print(text, "\n")
                explink = (
                    self.__experimenturl
                    + self.__datasetId
                    + "/"
                    + content["experimentKey"]
                    + "/"
                )
                data = {"experiment_id": content["id"]}
                # Send training request to server
                r = requests.post(f"{self.__url}training/", headers=header, data=data)
                body_unicode = r.content.decode("utf-8")
                content = json.loads(body_unicode)
                print(content["message"])
                print("\n")
                print(" Link to Experiment is : " + str(explink))
                print(" Training Plan Information for Experiment is :")
                self.getTrainingPlan()
            elif re.status_code == 403:
                body_unicode = re.content.decode("utf-8")
                content = json.loads(body_unicode)
                message = content["message"]
                text = colored(message, "red")
                print(text, "\n")
            elif re.status_code == 400:
                text = colored("Mandatory Fields Missing", "red")
                print(text, "\n")

    def __getParameters(self):

        parameters = {
            "message": "training",
            "datasetId": self.__datasetId,
            "epochs": self.__epochs,
            "cycles": self.__cycles,
            "modelName": self.__modelName,
            "optimizer": self.__optimizer,
            "lossFunction": self.__lossFunction,
            "learningRate": self.__learningRate,
            "stepsPerEpoch": self.__stepsPerEpoch,
            "initialEpoch": self.__initialEpoch,
            "validationSteps": self.__validationSteps,
            "batchSize": self.__batchSize,
            "featurewise_center": self.__featurewise_center,
            "samplewise_center": self.__samplewise_center,
            "featurewise_std_normalization": self.__featurewise_std_normalization,
            "samplewise_std_normalization": self.__samplewise_std_normalization,
            "zca_whitening": self.__zca_whitening,
            "rotation_range": self.__rotation_range,
            "width_shift_range": self.__width_shift_range,
            "height_shift_range": self.__height_shift_range,
            "brightness_range": self.__brightness_range,
            "shear_range": self.__shear_range,
            "zoom_range": self.__zoom_range,
            "channel_shift_range": self.__channel_shift_range,
            "fill_mode": self.__fill_mode,
            "cval": self.__cval,
            "horizontal_flip": self.__horizontal_flip,
            "vertical_flip": self.__vertical_flip,
            "rescale": self.__rescale,
            "data_format": self.__data_format,
            "validation_split": self.__validation_split,
            "dtype": self.__dtype,
            "shuffle": self.__shuffle,
            "layersFreeze": self.__layers_non_trainable,
            "metrics": self.__metrics,
            "objective": self.__objective,
            "name": self.__name,
            "modelType": self.__modelType,
            "category": self.__category,
            "upperboundTime": self.__upperboundTime,
            "callbacks": self.__callbacks,
            "pre_trained_weights": self.__weights,
        }

        return parameters

    def getTrainingPlan(self):
        if not self.__eligibility_passed:
            return
        print(
            f" \033[1mTraining Description\033[0m\n\n",
            f"objective: {self.__objective}\n",
            f"name: {self.__name}\n",
            f"modelType: {self.__modelType}\n",
            f"category: {self.__category}\n",
            f"datasetId: {self.__datasetId}\n",
            "\n \033[1mTraining Parameters\033[0m\n\n",
            f"epochs: {self.__epochs}\n",
            f"cycles: {self.__cycles}\n",
            # f"stepsPerEpoch: {self.__stepsPerEpoch}\n",
            # f"initialEpoch: {self.__initialEpoch}\n",
            # f"validationSteps: {self.__validationSteps}\n",
            f"batchSize: {self.__batchSize}\n",
            f"validation_split': {self.__validation_split}\n",
            "\n \033[1mHyperparameters\033[0m\n\n",
            f"optimizer: {self.__optimizer}\n",
            f"lossFunction: {self.__lossFunction}\n",
            f"learningRate: {self.__learningRate}\n",
            f"layersFreeze: {self.__layers_non_trainable}\n",
            f"earlystopCallback: {self.__earlystopCallback}\n",
            f"reducelrCallback: {self.__reducelrCallback}\n",
            f"modelCheckpointCallback: {self.__modelCheckpointCallback}\n",
            f"terminateOnNaNCallback: {self.__terminateOnNaNCallback}\n",
            "\n \033[1mAugmentation Parameters\033[0m\n\n",
            f"brightness_range: {self.__brightness_range}\n",
            f"channel_shift_range: {self.__channel_shift_range}\n",
            f"cval: {self.__cval}\n",
            f"data_format: {self.__data_format}\n",
            f"dtype: {self.__dtype}\n",
            f"featurewise_center: {self.__featurewise_center}\n",
            f"featurewise_std_normalization: {self.__featurewise_std_normalization}\n",
            f"fill_mode: {self.__fill_mode}\n",
            f"height_shift_range: {self.__height_shift_range}\n",
            f"horizontal_flip: {self.__horizontal_flip}\n",
            f"rescale: {self.__rescale}\n",
            f"rotation_range: {self.__rotation_range}\n",
            f"samplewise_center: {self.__samplewise_center}\n",
            f"samplewise_std_normalization: {self.__samplewise_std_normalization}\n",
            f"shear_range: {self.__shear_range}\n",
            f"shuffle: {self.__shuffle}\n",
            f"vertical_flip: {self.__vertical_flip}\n",
            f"width_shift_range: {self.__width_shift_range}\n",
            f"zca_whitening: {self.__zca_whitening}\n",
            f"zoom_range: {self.__zoom_range}\n",
        )
