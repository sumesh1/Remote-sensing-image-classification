

#Classification of Remote Sensing Images
## Dataset: RSI-CB

## Install dependencies and create directories
"""

!pip install pyunpack
!pip install patool
!mkdir rsensing
!mkdir rsensing/data
!mkdir rsensing/checkpoints
!mkdir rsensing/data/model

"""## Import Libraries"""

# %matplotlib inline

import time
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import os
import numpy as np
import random
from PIL import Image
import PIL
from tensorflow.python.framework import ops
import math
from urllib.request import urlretrieve
from os.path import isfile, isdir
from tqdm import tqdm
from pyunpack import Archive


# Use second GPU -- change if you want to use a first one
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

path = '/content/rsensing/data/'
file_size = 128
url = 'https://public.sn.files.1drv.com/y4mZZrgruZn4OM__kE-gGKluqBiGRoV51_d_TJAVLak2KMWqnhRKguCK05YiOr6L-6uiM0GNMIAjWHE_fXR2yLbCbLYBmPehbzJ2kSz6MoCPI4foyq3trliEiam-28oMmbw_rwHzSwERusgbjf3Ebi0xUgouXOkgS2xnE0SEG2MN9cBURB4Gm_w7sNC900fyicAVPf4ezgRZhBvW-OGv22WmA/RSI-CB128.rar?access_token=EwD4Aq1DBAAUcSSzoTJJsy%2bXrnQXgAKO5cj4yc8AAWAOH1mGmk7emoypweN3SIxTAfXJRg7MaPUSTJetYRMIkHr4hpc7fdKy7MZbSJJZ1fF9M2ofqFzBByw5bZlU9yjxMvsGbAFqulmeH242Dj0nEpuTbzKCdMPQQoJwfu%2bFBffD5YEYpN04EqvvpmR5eWwotbaQrf7ueuGuu9ZuM%2fQAfYNeBgrubw%2bjrZKkuS23cfhTXNnj4RzfRPUL9QkeJHO%2f3fo5bPTv%2bXlJX%2bNNcWg6DGLItwYkbCVZAugYjpmN8hR0%2faBHah8mK9pwMqgFm4VZFbeS4v1u5iSAYw%2flye0TuTEjd4ChWJTVHVGA6ovjHQ%2berA7CKIN7JMWdJTL8sQMDZgAACHvy4JmzOBZ2yAEBSIBwGKg95M45cfqd3yBa%2fKg1GxGdcl1Wa4jxFcZU21NFiJ28PDLWJzp0Wwn9pgNtemDIWhfkkTwHDI3Umbmu3aH1sndywLS6dSRInZvcue4Ddpz0eWkYqwstq5KggM6AIgZ8hbMKFYf6bwiz6UvupEuq1ND1mvFy1EP4D7p%2b3ctU07t0QyiLdSiqowuk18P5rSik8OPZNziKovdLnDXGELyDH6dQlPK0vtL1nRSwDT9JXKQixlYPbp%2fu1cc8VpUwVivcOoiaG1S4vbIOOxyyA1bKFVKjkXHgE%2bJgt%2bj5i6yqADblEhikWccoh3%2b6ys8%2f7nuWxqPVN8VSTqy7kQnngTg3nFDipEzSLkNXxBA8Q5XGiGfVeXjb9JtqEOqfk941GEKVIkHgqNV34D9q%2bBvuQKuAHnC3gbhaKPO0quN6aSjPHQr76yuYUX5IcYEnzCVA7KPVBgmpXttTJvxQbCh5eC4zw0i%2fE101j71jXPGRuYSacwASk7DKhwXhRT8ivPRH%2baeOxNgj3L%2fuhBGI%2byvEt9DdydUWnzfjZR7NulnNrI3E2gXZxih%2bVki30o9b6dEfyu9CxrCekKutmwRN8ba2aWCs3TVUouYHAg%3d%3d'

"""## Download and Extract dataset"""

# DOWNLOAD DATASET

data_dir = str(path)

class DLProgress(tqdm):
    last_block = 0

    def hook(self, block_num=1, block_size=1, total_size=None):
        self.total = total_size
        self.update((block_num - self.last_block) * block_size)
        self.last_block = block_num


with DLProgress(unit='B', unit_scale=True, miniters=1, desc='RSI-CB Data Set') as pbar:
    urlretrieve(str(url), data_dir + 'RSI-CB128.rar', pbar.hook)

    
# EXTRACT DATASET    

Archive(str(path) + 'RSI-CB128.rar').extractall(str(path))

"""### Define number of train and test images"""

train_size = 18342
test_size = 3690

"""## Generate and save Train Data"""

classes = os.listdir(str(path) + 'RSI-CB' + str(file_size))
index = 0
counter = 0
print('creating')
X_train = np.zeros((train_size, int(file_size), int(file_size), 3), dtype = 'uint8')
Y_train = np.zeros((train_size, 1), dtype = 'uint8')
print('created')
print(classes[2])
for i in classes:
  subclasses = os.listdir(str(path) + 'RSI-CB' + str(file_size) + '/' + str(i))  
  index = classes.index(str(i))
  print(index, i, counter) 
  #print(subclasses[1])
  for kk in subclasses:
    files = os.listdir(str(path) + 'RSI-CB' + str(file_size) + '/' + str(i) + '/' +  str(kk))
    count_temp = 0
    for k in range(0, int(len(files) * 0.5)):
      img = Image.open(str(path) + 'RSI-CB' + str(file_size) + '/' + str(i) + '/' + str(kk) + '/' + str(files[k]))
      img.load
      img = img.resize((int(file_size), int(file_size)), PIL.Image.ANTIALIAS)
      if np.asarray( img, dtype="uint8" ).shape[0] is int(file_size):
        X_train[counter,:,:,:] = np.asarray( img, dtype="uint8" )
        Y_train[counter][0] = index
        counter += 1
        count_temp += 1
      
      
print(counter)

np.save(str(path) + 'X_train_' + str(file_size) + 'X' + str(file_size) + 'X3X' + str(train_size) + '.npy', X_train)
np.save(str(path) + 'Y_train_' + str(file_size) + 'X' + str(file_size) + 'X3X' + str(train_size) + '.npy', Y_train)

"""## Generate and save Test Data"""

#GENERATE TESTING DATASET

classes = os.listdir(str(path) + 'RSI-CB' + str(file_size))
index = 0
counter = 0
print('creating')
X_test = np.zeros((test_size, int(file_size), int(file_size), 3), dtype = 'uint8')
Y_test = np.zeros((test_size, 1), dtype = 'uint8')
print('created')

for i in classes:
  subclasses = os.listdir(str(path) + 'RSI-CB' + str(file_size) + '/' + str(i))
  index = classes.index(str(i))
  print(index, i, counter)  

  for kk in subclasses:
    files = os.listdir(str(path) + 'RSI-CB' + str(file_size) + '/' + str(i) + '/' +  str(kk))
    count_temp = 0
    for k in range(int(len(files) * 0.9), len(files)):
      img = Image.open(str(path) + 'RSI-CB' + str(file_size) + '/' + str(i) + '/' + str(kk) + '/' + str(files[k]))
      img.load
      img = img.resize((int(file_size), int(file_size)), PIL.Image.ANTIALIAS)
      if np.asarray( img, dtype="uint8" ).shape[0] is int(file_size):
        X_test[counter,:,:,:] = np.asarray( img, dtype="uint8" )
        Y_test[counter][0] = index
        counter += 1
        count_temp += 1
           
print(counter)

np.save(str(path) + 'X_test_' + str(file_size) + 'X' + str(file_size) + 'X3X' + str(test_size) + '.npy', X_test)
np.save(str(path) + 'Y_test_' + str(file_size) + 'X' + str(file_size) + 'X3X' + str(test_size) + '.npy', Y_test)

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

"""## Load and Normalize Train and Test Data"""

trainx = np.load(str(path) + 'X_train_' + str(file_size) + 'X' + str(file_size) + 'X3X' + str(train_size) + '.npy')
trainy = np.load(str(path) + 'Y_train_' + str(file_size) + 'X' + str(file_size) + 'X3X' + str(train_size) + '.npy')

testx = np.load(str(path) + 'X_test_' + str(file_size) + 'X' + str(file_size) + 'X3X' + str(test_size) + '.npy')
testy = np.load(str(path) + 'Y_test_' + str(file_size) + 'X' + str(file_size) + 'X3X' + str(test_size) + '.npy')


X_train = trainx/255
X_train = X_train.astype('float16')
X_train = np.resize(X_train, (train_size, 64, 64, 3))

X_test = testx/255
X_test = X_test.astype('float16')
X_test = np.resize(X_test, (test_size, 64, 64, 3))

def convert_to_one_hot(Y, C):
    Y = np.eye(C)[Y.reshape(-1)].T
    return Y
  
Y_train = convert_to_one_hot(trainy, 8).T  
Y_test = convert_to_one_hot(testy, 8).T

print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

"""## Compute cost and minibatches"""

def create_placeholders(n_H0, n_W0, n_C0, n_y):
    """
    Creates the placeholders for the tensorflow session.
    
    n_H0 -- height of an input image
    n_W0 -- width of an input image
    n_C0 -- number of channels of the input
    n_y  --  number of classes
        
    Returns:
    X -- placeholder for the data input, of shape [None, n_H0, n_W0, n_C0] and dtype "float"
    Y -- placeholder for the input labels, of shape [None, n_y] and dtype "float"
    """

    X = tf.placeholder(tf.float32, [None, n_H0, n_W0, n_C0], name = 'X')
    Y = tf.placeholder(tf.float32, [None, n_y], name = 'Y')
    
    return X, Y
   
  
def compute_cost(Z3, Y):
    """
    Computes the cost
    
    Z3   - output of forward propagation (output of the last LINEAR unit), of shape (6, number of examples)
    Y    - "true" labels vector placeholder, same shape as Z3
    cost - Tensor of the cost function
    """
    
    cost = tf.nn.softmax_cross_entropy_with_logits(logits = Z3, labels = Y)
    cost = tf.reduce_mean(cost)
    
    return cost
  
  
def random_mini_batches(X, Y, mini_batch_size = 64, seed = 10):
    """
    Creates a list of random minibatches from (X, Y)

    X               - input data, of shape (input size, number of examples)
    Y               - true "label" vector (containing index of image class
    mini_batch_size - size of the mini-batches    
    mini_batches    - list of synchronous (mini_batch_X, mini_batch_Y)
    """
    
    m = X.shape[0]                  # number of training examples
    mini_batches = []
    np.random.seed(seed)
    
    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation,:,:,:]
    shuffled_Y = Y[permutation,:]

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:,:,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m,:,:,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size : m,:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)
    
    return mini_batches

"""## Define Training Network"""

def forward_propagation(X):
    
    # CONV >> ACTIVATION >> POOL >> FLATTEN >> FULLY CONNECTED
    
    gen1 = tf.layers.conv2d(X, 8, 4, 1, padding = 'SAME')
    A1 = tf.nn.relu(gen1)    
    P1 = tf.nn.max_pool(A1, ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')
    
    gen2 = tf.layers.conv2d(P1, 16, 4, 1, padding = 'SAME')
    A2 = tf.nn.relu(gen2)    
    P2 = tf.nn.max_pool(A2, ksize = [1,4,4,1], strides = [1,4,4,1], padding = 'SAME')
    
    gen3 = tf.layers.conv2d(P2, 32, 4, 1, padding = 'SAME')
    A3 = tf.nn.tanh(gen3)  
    P3 = tf.nn.max_pool(A3, ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')    
    
    gen4 = tf.layers.conv2d(P3, 8, 3, 1, padding = 'SAME')
    A4 = tf.nn.sigmoid(gen4)  
    P4 = tf.nn.max_pool(A4, ksize = [1,2,2,1], strides = [1,2,2,1], padding = 'SAME')    
    
    # FLATTEN
    P_fl = tf.contrib.layers.flatten(P4)
    
    # FULLY CONNECTED
    fc = tf.contrib.layers.fully_connected(P_fl, 8, activation_fn = None)
    
    return fc

"""## Training Model"""

def model(X_train, Y_train, X_test, Y_test, learning_rate = 0.0005,
          num_epochs = 100, minibatch_size = 64, print_cost = True):
    """
    X_train -  training set, shape  (?, 64, 64, 3)
    Y_train -  test set,     shape  (?, n_y = 8)
    X_test  -  training set, shape  (?, 64, 64, 3)
    Y_test  -  test set,     shape  (?, n_y = 8)
    
    learning_rate  -  learning rate of the optimization
    num_epochs     -  number of epochs of the optimization loop
    minibatch_size -  size of a minibatch
    print_cost     -  True to print the cost every 100 epochs
    
    train_accuracy - accuracy on the train set (X_train)
    test_accuracy  - testing accuracy on the test set (X_test)
    """
    
  
    print('X_train shape', X_train.shape)  
    print('Y_train shape', Y_train.shape)  
    print('X_test shape', X_test.shape)  
    print('Y_test shape', Y_test.shape)
    print('Learning rate:', learning_rate)
    
  
  
    ops.reset_default_graph()        # to be able to rerun the model without overwriting tf variables
    tf.set_random_seed(1)                              # to keep results consistent (tensorflow seed)
    seed = 3                                                # to keep results consistent (numpy seed)
    (m, n_H0, n_W0, n_C0) = X_train.shape             
    n_y = Y_train.shape[1]                            
    costs = []                                                            # To keep track of the cost
    
    t1 = 0
    t2 = 0
    
    X, Y = create_placeholders(n_H0, n_W0, n_C0, n_y)
        
    # Forward propagation: Build the forward propagation in the tensorflow graph
     
    Z3 = forward_propagation(X)
    
    # Cost function
     
    cost = compute_cost(Z3, Y)
    
    # defining adam optimizer
     
    optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(cost)
    
    
    # Initialize all the variables globally
    init = tf.global_variables_initializer()
    
    saver = tf.train.Saver()

     
    # Start the session to compute the tensorflow graph
    with tf.Session() as sess:
        
        # Run the initialization
        sess.run(init)
        
        for epoch in range(num_epochs):
            
            minibatch_cost = 0.
            num_minibatches = int(m / minibatch_size) # number of minibatches of size minibatch_size in the train set
            seed = seed + 1
            minibatches = random_mini_batches(X_train, Y_train, minibatch_size, seed)

            for minibatch in minibatches:

                # Select a minibatch
                (minibatch_X, minibatch_Y) = minibatch
                #  runs the graph on a minibatch.
                # Run the session to execute the optimizer and the cost, 
                # the feedict should contain a minibatch for (X,Y).
                 
                _ , temp_cost = sess.run([optimizer, cost], feed_dict = {X: minibatch_X, Y: minibatch_Y})
                
                
                minibatch_cost += temp_cost / num_minibatches
                

            # Print the cost every epoch
            if print_cost == True and epoch % 5 == 0:
                t2 = time.time()
                print ("Cost after epoch %i: %f" % (epoch, minibatch_cost), 'Time:', round(t2-t1, 4))
                t1 = time.time()
            if print_cost == True and epoch % 1 == 0:
                costs.append(minibatch_cost)
                
        print('Saving Model...')
        saver.save(sess, str(path) + 'model/model.ckpt')
        print('Model Saved...')
                
                
        
        
        # plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()

        # Calculate the correct predictions
        predict_op = tf.argmax(Z3, 1)
        correct_prediction = tf.equal(predict_op, tf.argmax(Y, 1))
        # Calculate accuracy on the test set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print('accuracy', accuracy)
        train_accuracy = accuracy.eval({X: X_train, Y: Y_train})
        test_accuracy = accuracy.eval({X: X_test, Y: Y_test})
        print("Train Accuracy:", train_accuracy)
        print("Test Accuracy:", test_accuracy)
                

          
        return train_accuracy

acc = model(X_train, Y_train, X_test, Y_test, learning_rate=0.003, num_epochs = 100,
                       minibatch_size = 64)

