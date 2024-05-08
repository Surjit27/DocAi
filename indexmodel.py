import os 
import tensorflow as tf
from keras.models import load_model
import pandas as pd
import numpy as np

class ModelPredictor:
    def __init__(self, column, current_index, input_file):
        self.column = column
        self.current_index = current_index
        self.input_file = input_file
        self.model_path = r"S:\Adacamic Projects\Project 2\keras Models\Main.h5"


    def resulting(self,current_index):
        return current_index
        
    def run(self):
        count = 0
        model = load_model(self.model_path)
        img = tf.keras.preprocessing.image.load_img(self.input_file, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.array([img_array])

        predictions = model.predict(img_array)
        class_id = np.argmax(predictions, axis=1)
        print(class_id)
        df = pd.read_csv(r"A:\Mainres22.csv")
        print(df[f"{self.column}"][class_id[0]])
        self.current_index = df[f"{self.column}"][class_id[0]].replace('\n', '')
        print("Initial current_index:", self.current_index)

        while True:
            count += 1
            result, success = self.change_directory(self.current_index, self.model_path)
            if not success:
                self.resulting(self.current_index)
                break
                
            self.current_index = self.predict(result, self.input_file, self.current_index)
            print("The number of iterations is", count)

        return self.current_index




    def predict(self, result, input_file, current_index):  # Corrected argument order
        model = load_model(result)
        img = tf.keras.preprocessing.image.load_img(input_file, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.array([img_array])
        predictions = model.predict(img_array)
        class_id = np.argmax(predictions, axis=1)
        df = pd.read_csv(r"A:\Mainres22.csv")
        name = (df[current_index][class_id[0]]).replace('\n', '')

        print("Predict function : ",name)
        return name
        
    def change_directory(self, current_index, result):
        print("changing directory:", result)
        try:
            new_model_path = r"S:\Adacamic Projects\Project 2\keras Models\{}.h5".format(current_index.replace('\n', ''))
            print("New model path:", new_model_path)

            if os.path.isfile(new_model_path):
                return new_model_path, True
            else:
                return None, False
            
        except Exception as e:
            print(f"An error occurred while changing directory: {e}")
            return None, False

   

predictor = ModelPredictor(column="Main", current_index=None, input_file=r"S:\Adacamic Projects\data\Orgran Injury\teeth\train\Gingivitis\(8).jpg")
prediction_result = predictor.run() 
