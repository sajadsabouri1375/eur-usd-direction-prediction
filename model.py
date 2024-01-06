'''
    Designing LSTM model architecture, training the model, and model evaluation are implemented in LstmModel class.
'''

from operation_abstract import OperationParentAbstract
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Softmax
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from matplotlib import pyplot as plt
import os
from sklearn import metrics
from utils.plot_utils import PlotUtils
import tensorflow
import keras
from utils.utils import Utils
import json

class LstmModel(OperationParentAbstract):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._saving_directory = kwargs.get('saving_directory')
        self._dataset = kwargs.get('modelling_dataset')
        self._model = None
        self._training_percent = kwargs.get('training_percent', 0.7)
        self._validation_percent = kwargs.get('validation_percent', 0.2)
        
    def define_model_architecture(self, training_inputs):

        self._model = Sequential()
        
        self._model.add(LSTM(120, input_shape=(training_inputs.shape[1], training_inputs.shape[2])))
        # self._model.add(Dense(40, activation='sigmoid'))
        self._model.add(Dense(3, activation='softmax'))
        
        self._model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
        
        self._model.summary()
        
    def fit_model(self, training_inputs, training_outputs, validation_inputs, validation_outputs):
        
        mc = ModelCheckpoint(
            os.path.join(self._saving_directory, "lstm_model"),
            monitor="val_accuracy",
            verbose=2,
            save_best_only=True,
            save_weights_only=False,
            mode="auto",
            save_freq="epoch",
            initial_value_threshold=None
        )
        
        history = self._model.fit(
            training_inputs,
            training_outputs,
            epochs=500,
            batch_size=200,
            validation_data=(validation_inputs, validation_outputs), 
            shuffle=False,
            callbacks=mc
        )
        
        self._model = keras.models.load_model(os.path.join(self._saving_directory, "lstm_model"))

        return history
    
    def encode_labels(self):
        encoder = LabelEncoder()
        self._labels = pd.DataFrame(encoder.fit_transform(self._dataset['label']))
    
    def normalize_data(self):
        input_scaler = MinMaxScaler(feature_range=(0, 1))
        inputs = input_scaler.fit_transform(self._dataset)
        self._dataset = pd.DataFrame(inputs)
        
        # output_scalar = MinMaxScaler(feature_range=(0, 1))
        # outputs = output_scalar.fit_transform(self._labels)
        # self._labels = pd.DataFrame(outputs)
        
    def shift_dataset(self):
        
        n_vars = self._dataset.shape[1]
        
        cols, names = list(), list()
        
        n_in = 120
        for i in range(n_in, 0, -1):
            cols.append(self._dataset.shift(i))
            names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        
        n_out = 1
        for i in range(0, n_out):
            cols.append(self._labels.shift(-i))
        
        if i == 0:
            names += [('var%d(t)' % (n_vars))]
        else:
            names += [('var%d(t+%d)' % (n_vars))]
        
        aggregation = pd.concat(cols, axis=1)
        aggregation.columns = names
        
        aggregation.dropna(inplace=True)
        
        self._dataset = aggregation.values
                
    def split_dataset(self):
        n_data = self._dataset.shape[0]
        
        n_training = round(self._training_percent * n_data)
        n_validation = round(self._validation_percent * n_data)
        n_test = n_data - n_training - n_validation
        
        training_dataset, validation_dataset, test_dataset = self._dataset[0:n_training], self._dataset[n_training: n_training + n_validation], self._dataset[-n_test:]
        
        return training_dataset, validation_dataset, test_dataset
    
    def prepare_dataset(self, training_dataset, validation_dataset, test_dataset):
        self._training_inputs = training_dataset[:, :-1]
        self._training_inputs = self._training_inputs.reshape((self._training_inputs.shape[0], 1, self._training_inputs.shape[1]))
        training_outputs = training_dataset[:, -1]
        self._training_outputs_cm = training_outputs
        self._training_outputs = tensorflow.keras.utils.to_categorical(training_outputs, 3)
        
        self._validation_inputs = validation_dataset[:, :-1]
        self._validation_inputs = self._validation_inputs.reshape((self._validation_inputs.shape[0], 1, self._validation_inputs.shape[1]))
        validation_outputs = validation_dataset[:, -1]
        self._validation_outputs_cm = validation_outputs
        self._validation_outputs = tensorflow.keras.utils.to_categorical(validation_outputs, 3)
        
        self._test_inputs = test_dataset[:, :-1]
        self._test_inputs = self._test_inputs.reshape((self._test_inputs.shape[0], 1, self._test_inputs.shape[1]))
        test_outputs = test_dataset[:, -1]
        self._test_outputs_cm = test_outputs
        self._test_outputs = tensorflow.keras.utils.to_categorical(test_outputs, 3)
        
    def plot_model_history(self, history):
        # plot history
        figure = plt.figure(figsize=(25.6, 14.4))
        plt.plot(history.history['loss'], label='Training')
        plt.plot(history.history['val_loss'], label='Validation')
        plt.legend()
        plt.xlabel('Epoch', fontsize=20)
        plt.ylabel('Loss', fontsize=20)
        plt.tight_layout()
        plt.show(block=False)
        plt.savefig(os.path.join(self._plot_saving_directory, "training_validation_losses.jpg"), dpi=400)
        
        figure = plt.figure(figsize=(25.6, 14.4))
        plt.plot(history.history['accuracy'], label='Training')
        plt.plot(history.history['val_accuracy'], label='Validation')
        plt.legend()
        plt.xlabel('Epoch', fontsize=20)
        plt.ylabel('Accuracy', fontsize=20)
        plt.tight_layout()
        plt.show(block=False)
        plt.savefig(os.path.join(self._plot_saving_directory, "training_validation_accuracies.jpg"), dpi=400)
        
    def test_model(self, test_inputs, test_outputs):
        self._model.evaluate(
            test_inputs, 
            test_outputs    
        )
    
    def generate_predictions(self):
        self._training_predictions = self._model.predict(self._training_inputs).argmax(axis=1)
        # self._training_predictions = self._model.predict(self._training_inputs)
        
        self._validation_predictions = self._model.predict(self._validation_inputs).argmax(axis=1)
        # self._validation_predictions = self._model.predict(self._validation_inputs)
        
        self._test_predictions = self._model.predict(self._test_inputs).argmax(axis=1)
        # self._test_predictions = self._model.predict(self._test_inputs)
        
    def generate_confusion_matrices(self):
        training_cm = metrics.confusion_matrix(self._training_outputs_cm, self._training_predictions)
        validation_cm = metrics.confusion_matrix(self._validation_outputs_cm, self._validation_predictions)
        test_cm = metrics.confusion_matrix(self._test_outputs_cm, self._test_predictions)
        
        return training_cm, validation_cm, test_cm
    
    def plot_confusion_matrices(self):
        training_cm, validation_cm, test_cm = self.generate_confusion_matrices()
        PlotUtils.plot_confusion_matrix(training_cm, os.path.join(self._plot_saving_directory, "conf_matrix_training.jpg"), "Training Confusion Matrix")
        PlotUtils.plot_confusion_matrix(validation_cm, os.path.join(self._plot_saving_directory, "conf_matrix_validation.jpg"), "Validation Confusion Matrix")
        PlotUtils.plot_confusion_matrix(test_cm, os.path.join(self._plot_saving_directory, "conf_matrix_test.jpg"), "Test Confusion Matrix")
        
    def report_metrics(self):
        training_accuracy = metrics.accuracy_score(self._training_outputs_cm, self._training_predictions)
        validation_accuracy = metrics.accuracy_score(self._validation_outputs_cm, self._validation_predictions)
        test_accuracy = metrics.accuracy_score(self._test_outputs_cm, self._test_predictions)
        print(f'Accuracy => Training: {training_accuracy}  |  Validation:  {validation_accuracy}  |  Test: {test_accuracy}')
        
        training_recall = metrics.recall_score(self._training_outputs_cm, self._training_predictions, average="macro")
        validation_recall = metrics.recall_score(self._validation_outputs_cm, self._validation_predictions, average="macro")
        test_recall = metrics.recall_score(self._test_outputs_cm, self._test_predictions, average="macro")
        print(f'Recall => Training: {training_recall}  |  Validation  {validation_recall}  |  Test: {test_recall}')
        
        training_precision = metrics.precision_score(self._training_outputs_cm, self._training_predictions, average="macro")
        validation_precision = metrics.precision_score(self._validation_outputs_cm, self._validation_predictions, average="macro")
        test_precision = metrics.precision_score(self._test_outputs_cm, self._test_predictions, average="macro")
        print(f'Precision => Training: {training_precision}  |  Validation  {validation_precision}  |  Test: {test_precision}')
    
        training_f1_score = metrics.f1_score(self._training_outputs_cm, self._training_predictions, average="macro")
        validation_f1_score = metrics.f1_score(self._validation_outputs_cm, self._validation_predictions, average="macro")
        test_f1_score = metrics.f1_score(self._test_outputs_cm, self._test_predictions, average="macro")
        print(f'F1 Score => Training: {training_f1_score}  |  Validation  {validation_f1_score}  |  Test: {test_f1_score}')
        
        with open(os.path.join(self._saving_directory, "metrics.json"), 'w') as f:
            json.dump(
                {
                    'accuracy': {
                        'training': training_accuracy,
                        'validation': validation_accuracy,
                        'test': test_accuracy
                    },
                    'precision': {
                        'training': training_precision,
                        'validation': validation_precision,
                        'test': test_precision
                    },
                    'recall': {
                        'training': training_recall,
                        'validation': validation_recall,
                        'test': test_recall
                    },
                    'f1_score': {
                        'training': training_f1_score,
                        'validation': validation_f1_score,
                        'test': test_f1_score
                    }
                }, 
                f
            )
        
        return training_accuracy, test_accuracy
    
    def run_model(self):
        
        self.encode_labels()
        
        self.normalize_data()
        
        self.shift_dataset()
        
        training_dataset, validation_dataset, test_dataset = self.split_dataset()
        
        self.prepare_dataset(training_dataset, validation_dataset, test_dataset)

        self.define_model_architecture(training_inputs=self._training_inputs)
        
        history = self.fit_model(self._training_inputs, self._training_outputs_cm, self._validation_inputs, self._validation_outputs_cm)
        
        self.plot_model_history(history)
        
        self.test_model(self._test_inputs, self._test_outputs_cm)

        self.generate_predictions()
        
        self.plot_confusion_matrices()
        
        training_accuracy, test_accuracy = self.report_metrics()
        
        return training_accuracy, test_accuracy
                
