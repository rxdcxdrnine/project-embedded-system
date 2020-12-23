# Copyright Reserved (2020).
# Donghee Lee, Univ. of Seoul
#
__author__ = 'will'

import tflite_runtime.interpreter as tflite

import numpy as np

class DNN_Driver():
    def __init__(self):
        self.model = None
        self.interpreter = None


    def tf_load(self, path):
        self.interpreter = tflite.Interpreter(model_path = path)
        self.interpreter.allocate_tensors()


    def predict_direction(self, img):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        input_shape = input_details[0]["shape"]
        img = img.reshape((1,)+img.shape)
        self.interpreter.set_tensor(input_details[0]["index"], img)
        self.interpreter.invoke()
        ret = self.interpreter.get_tensor(output_details[0]["index"])
        return ret

        