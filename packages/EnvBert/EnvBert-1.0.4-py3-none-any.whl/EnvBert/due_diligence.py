# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 17:00:39 2022

@author: EL221XK
"""

#Loading Packages
import os
import numpy as np
import pandas as pd
import transformers
import sklearn
import tensorflow as tf
import sentence_transformers
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
similarity_model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(path, "data/embeddings.csv")

#%% 
#Classification Model
env_tokenizer = AutoTokenizer.from_pretrained("d4data/environmental-due-diligence-model")
env_model = TFAutoModelForSequenceClassification.from_pretrained("d4data/environmental-due-diligence-model")
classifier = pipeline('text-classification', model=env_model, tokenizer=env_tokenizer) # cuda = 0,1 based on gpu availability

#%%

def load_embeddings(path):
    return pd.read_csv(file_path)

def envbert_predict(text_input):
    #running the classification model to predict the classes
    edd_classification = classifier(text_input)
    edd_label = edd_classification[0]['label']
    edd_score = edd_classification[0]['score']
    
    #running due diligence ranking module
    # due diligence ranking dictionary
    embeddings_text = np.float64(similarity_model.encode([text_input]))
    embeddings_df = load_embeddings(path)
    
    
    if edd_label == 'Remediation Activities':
        embeddings_dict = np.array(embeddings_df.iloc[0, :]).reshape(1, -1) 
    
    if edd_label == 'Groundwater-Surfacewater interaction':
        embeddings_dict = np.array(embeddings_df.iloc[1, :]).reshape(1, -1)

    if edd_label == 'Contaminants':
        embeddings_dict = np.array(embeddings_df.iloc[2, :]).reshape(1, -1)
    
    if edd_label == 'Extent of contamination':
        embeddings_dict = np.array(embeddings_df.iloc[3, :]).reshape(1, -1)
        
    if edd_label == 'Contaminated media':
        embeddings_dict = np.array(embeddings_df.iloc[4, :]).reshape(1, -1)        
        
    if edd_label == 'Source of contamination':
        embeddings_dict = np.array(embeddings_df.iloc[5, :]).reshape(1, -1)
        
    if edd_label == 'Depth to Water':
        embeddings_dict = np.array(embeddings_df.iloc[6, :]).reshape(1, -1)

    if edd_label == 'GW Velocity':
        embeddings_dict = np.array(embeddings_df.iloc[7, :]).reshape(1, -1)
        
    if edd_label == 'Remediation Standards':
        embeddings_dict = np.array(embeddings_df.iloc[8, :]).reshape(1, -1)
            
    if edd_label == 'Remediation Goals':
        embeddings_dict = np.array(embeddings_df.iloc[9, :]).reshape(1, -1)  
        
    if edd_label == 'Geology':
        embeddings_dict = np.array(embeddings_df.iloc[10, :]).reshape(1, -1)
                                          
    cosine_scores = util.cos_sim(embeddings_text, embeddings_dict)
    
    final_probability = np.float64(cosine_scores)
    
    if final_probability > 0.3:
        return [edd_label, np.float64(cosine_scores)]
    else:
        return ["Not Relevant", np.float64(cosine_scores)]

def finetune(data, training_config):
    try:        
        #unwrapping training configurations
        if 'learning_rate' in training_config.keys():
            l_r = training_config['learning_rate']
        else:
            l_r = 5e-5
        
        if 'epochs' in training_config.keys():
            epoch_count = training_config['epochs']
        else:
            epoch_count = 10
        
        if 'batch_size' in training_config.keys():
            batch_size = training_config['batch_size']
        else:
            batch_size = 16
        
        if 'sentence column name' in training_config.keys():
            sentence = training_config['sentence column name']
            
        if 'label column name' in training_config.keys():
            encoded_label = training_config['label column name']
        
        if sentence and encoded_label:
            data.dropna(subset=[sentence, encoded_label], how='any', inplace=True)
            # features and labels
            data_texts = data[sentence].to_list() # Features (not-tokenized yet)
            data_labels = data[encoded_label].to_list() # Lables
            
            # tokenizing the text
            train_encodings = env_tokenizer(data_texts, truncation=True, padding=True)
            
            train_dataset = tf.data.Dataset.from_tensor_slices((
                dict(train_encodings),
                data_labels
            ))
            
            optimizer = tf.keras.optimizers.Adam(learning_rate=l_r)
            env_model.compile(optimizer=optimizer, loss=env_model.compute_loss,  
                              metrics=['accuracy'])
            
            env_model.fit(train_dataset.shuffle(1000).batch(batch_size), epochs=epoch_count, batch_size=batch_size,
                          validation_data=train_dataset.shuffle(1000).batch(batch_size))
            print("Model trained successfully!!!")
            
            try:
                if 'save_dir' in training_config.keys():
                    env_model.save_pretrained(training_config['save_dir'])
                    env_tokenizer.save_pretrained(training_config['save_dir'])
                    print("Model saved successfully")
            except:
                print("Model save unsuccessfull, please save it yourself from the returned models")
                      
            return env_model, env_tokenizer
        else:
            print("There is an error, Model cannot be trained")
            return None, None
    except:
        return None, None
        print("There is an error, Model cannot be trained")

class finetune_predict:
    def __init__(self, load_directory):
        self.new_tokenizer = AutoTokenizer.from_pretrained(load_directory)
        self.new_model = TFAutoModelForSequenceClassification.from_pretrained(load_directory)
    
    def sent(self, test_text):
        predict_input = self.new_tokenizer.encode(test_text,
                                         truncation=True,
                                         padding=True,
                                         return_tensors="tf")

        output = self.new_model(predict_input)[0]
        prediction_value = tf.argmax(output, axis=1).numpy()[0]
        return prediction_value
    
    def predict_proba(self, test_list):  
        #tokenize the text
        encodings = self.new_tokenizer(test_list, 
                              truncation=True, 
                              padding=True)
        #transform to tf.Dataset
        dataset = tf.data.Dataset.from_tensor_slices((dict(encodings)))
        #predict
        preds = self.new_model.predict(dataset.batch(1)).logits  
        
        #transform to array with probabilities
        res = tf.nn.softmax(preds, axis=1).numpy()      
        
        return res
    
    def df(self, df, sentence, proba=False):
        finetune_prediction = df[sentence].apply(lambda x: finetune_predict.sent(self, x))
        
        if proba==True:
            prediction_probability = finetune_predict.predict_proba(self, df[sentence].to_list())
            
            return finetune_prediction, prediction_probability
        else:
            return finetune_prediction
        
#%%

