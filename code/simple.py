import tensorflow as tf
from config import *
import numpy as np
from keras import layers
import mysql.connector

with open('/var/www/logs/mysql.log', 'r') as log:
    logs_text = log.read()

batch_size = 32
seed = 42

raw_train_ds = tf.keras.utils.text_dataset_from_directory(
    TRAIN_FOLDER,
    batch_size=batch_size,
    validation_split=0.2,
    subset='training',
    seed=seed)

raw_val_ds = tf.keras.utils.text_dataset_from_directory(
    TRAIN_FOLDER,
    batch_size=batch_size,
    validation_split=0.2,
    subset='validation',
    seed=seed)

raw_test_ds = tf.keras.utils.text_dataset_from_directory(
    TEST_FOLDER,
    batch_size=batch_size)