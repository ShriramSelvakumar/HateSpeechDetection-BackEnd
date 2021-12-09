import pandas as pd
import numpy as np
from NLP.HSNLP import HateSpeechNLP
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow import keras
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import bz2
import pickle
import _pickle as cPickle

# Setting display width for panda outputs
pd.set_option('display.max_colwidth', 200)


# Predict Function
def predict(data):
    # Load trained model

    model_path = './ML_Models/'
    vectorizer_name = 'Final_TV_layer_HS'
    model_name = 'Final_CNN_HS-final_label_int-03-0.834'

    # Load Text Vectorizer
    from_disk = pickle.load(open(model_path + vectorizer_name + ".pkl", "rb"))
    loaded_vectorized = TextVectorization.from_config(from_disk['config'])
    loaded_vectorized.set_weights(from_disk['weights'])

    # Load trained model
    trained_NN_model = keras.models.load_model(model_path + model_name + '.h5')

    data_X_NLP = HateSpeechNLP(data)
    data_X = data_X_NLP.fit_transform()

    X_test_vectorized = loaded_vectorized(np.asarray(data_X.cleaned_stemmed_text))

    y = np.argmax(trained_NN_model.predict(X_test_vectorized), axis=-1)
    return y














