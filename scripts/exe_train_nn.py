#!/usr/bin/env python

"""
This program trains a neural network with hyperparameters that are read from a
user-specified configuration file. The user may also provide a hyperparameter
and value to override the configuration file.
"""

print("Loading libraries. May take a few minutes.")

import awkward as ak
import numpy as np
import os
import sys
import tensorflow as tf
import vector
vector.register_awkward()

from argparse import ArgumentParser
from configparser import ConfigParser
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping
from keras.regularizers import l1, l2, l1_l2
from keras.constraints import max_norm
from pandas import DataFrame
from pickle import dump
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow import compat
from tqdm import tqdm
from sys import argv
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # suppress Keras/TF warnings
compat.v1.logging.set_verbosity(compat.v1.logging.ERROR) # suppress Keras/TF warnings

# Custom libraries and modules
from colors import CYAN, W
from kinematics import calcDeltaR
from logger import info, error
from trsm import trsm_combos

print("Libraries loaded.")
print()


### ------------------------------------------------------------------------------------
## Implement command line parser

learning_rate = float(sys.argv[1])
beta_1 = float(sys.argv[2])
beta_2 = float(sys.argv[3])
epsilon = float(sys.argv[4])
config_name = float(sys.argv[5])


### ------------------------------------------------------------------------------------
## Prepare output directories

lr_folder = str(learning_rate).split('.')[1]
beta1_folder = str(beta_1).split('.')[1]
beta2_folder = str(beta_2).split('.')[1]

out_dir = f"~/public/condor/training/{config_name}/"
out_dir += f"lr_pt{lr_folder}/beta1_pt{beta1_folder}/beta2_pt{beta2_folder}"
model_dir = out_dir + "model/"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

### ------------------------------------------------------------------------------------
## Import configuration file

cfg_location = '~/public/condor/training'
cfg_name = f'classifier_6jet/{config_name}.cfg'

cfg = cfg_location + cfg_name

# Load the configuration using configparser
config = ConfigParser()
config.optionxform = str
config.read(cfg)

# Hidden hyperparameters
hidden_activations = config['HIDDEN']['HiddenActivations']
nodes              = config['HIDDEN']['Nodes'].split('\n')
nlayers            = len(nodes)

# Output hyperparameters
output_activation  = config['OUTPUT']['OutputActivation']
output_nodes       = int(config['OUTPUT']['OutputNodes'])

# Nadam defaults:
# learning_rate = 0.001
# beta_1 = 0.9
# beta_2 = 0.999
optimizer = tf.keras.optimizers.Nadam(
    learning_rate=float(args.lr), beta_1=float(args.beta1), beta_2=float(args.beta2), epsilon=float(args.epsilon), name="Nadam")
loss_function      = config['LOSS']['LossFunction']
nepochs            = int(config['TRAINING']['NumEpochs'])
batch_size         = int(config['TRAINING']['BatchSize'])
    
inputs_filename    = config['INPUTS']['InputFile']

nn_type            = config['TYPE']['Type']


### TEMPORARY FILENAME
combos = trsm_combos(inputs_filename)
combos.build_p4()
info("p4s loaded.")

signal_p4 = combos.sgnl_p4
background_p4 = combos.bkgd_p4

inputs = combos.construct_training_features()

sgnl_node_targets = np.concatenate((np.repeat(1, len(inputs)/2), np.repeat(0, len(inputs)/2)))
bkgd_node_targets = np.where(sgnl_node_targets == 1, 0, 1)
targets = np.column_stack((sgnl_node_targets, bkgd_node_targets))

### ------------------------------------------------------------------------------------
## 

scaler = MinMaxScaler()
scaler.fit(inputs)
x = scaler.transform(inputs)

val_size = 0.10
x_train, x_val, y_train, y_val = train_test_split(x, targets, test_size=val_size)

# Save training examples
np.savez(out_dir + "training_examples_1.npz", x_train=x_train, y_train=y_train)

param_dim = np.shape(inputs)[1]

### ------------------------------------------------------------------------------------
## 

info("Defining the model.")
# Define the keras model
model = Sequential()

# Input layers
model.add(Dense(nodes[0], input_dim=param_dim, activation=hidden_activations))

# # Hidden layers
for i in range(1,nlayers):
    if 'classifier' in args.task:
        model.add(Dense(int(nodes[i]), activation=hidden_activations, kernel_constraint=max_norm(1.0), kernel_regularizer=l1_l2(), bias_constraint=max_norm(1.0)))
    elif args.task == 'regressor':
        model.add(Dense(int(nodes[i]), activation=hidden_activations, kernel_regularizer=l1_l2()))

# Output layer
model.add(Dense(output_nodes, activation=output_activation))

# Stop after epoch in which loss no longer decreases but save the best model.
es = EarlyStopping(monitor='loss', restore_best_weights=True)
met = ['accuracy']

model.compile(loss=loss_function, 
              optimizer=optimizer, 
              metrics=met)

# Make a list of the hyperparameters and print them to the screen.
nn_info_list = [
    f"Input parameters:            {param_dim},\n",
    f"Optimizer:                   {optimizer}\n",
    f"Learning Rate:               {args.lr}\n",
    f"beta_1:                      {args.beta1}\n",
    f"beta_2:                      {args.beta2}\n",
    f"epsilon:                     {args.epsilon}\n",
    f"Loss:                        {loss_function}\n",
    f"Num epochs:                  {nepochs}\n",
    f"Batch size:                  {batch_size}\n",
    f"Num hidden layers:           {nlayers}\n",
    f"Input activation function:   {hidden_activations}\n",
    f"Hidden layer nodes:          {nodes}\n",
    f"Hidden activation functions: {hidden_activations}\n",
    f"Num output nodes:            {output_nodes}\n",
    f"Output activation function:  {output_activation}"]

# for line in nn_info_list:
#     print(line)

### ------------------------------------------------------------------------------------
## Fit the model

history = model.fit(x_train,
                    y_train, 
                    validation_data=(x_val, y_val), 
                    epochs=nepochs, 
                    batch_size=batch_size, 
                    callbacks=[es])

### ------------------------------------------------------------------------------------
## Apply the model (predict)

# scores = model.predict(x_test)

### ------------------------------------------------------------------------------------
## Save the model, history, and predictions

# np.savez(out_dir + f"scores_{args.run}", scores=scores)

# convert the history.history dict to a pandas DataFrame   
hist_df = DataFrame(history.history) 

# Save to json:  
hist_json_file = model_dir + f'history_{args.run}.json' 

with open(hist_json_file, mode='w') as f:
    hist_df.to_json(f)

# Save model to json and weights to h5
model_json = model.to_json()

json_save = model_dir + f"model_{args.run}.json"
h5_save   = json_save.replace(".json", ".h5")

with open(json_save, "w") as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights(h5_save)

dump(scaler, open(model_dir + f'scaler_{args.run}.pkl', 'wb'))

info(f"Saved model and history to disk in location:"
      f"\n   {json_save}\n   {h5_save}\n   {hist_json_file}")


### ------------------------------------------------------------------------------------
## 

nn_info_list[3] = f"Num epochs:                  {len(hist_df)}\n"

with open(out_dir + 'nn_info.txt', "w") as f:
    for line in nn_info_list:
        f.writelines(line)

# print("-"*45 + CYAN + " Training ended " + W + "-"*45)