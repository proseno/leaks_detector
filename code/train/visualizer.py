# from ann_visualizer.visualize import ann_viz
import visualkeras
import tensorflow as tf
from tensorflow.keras import layers
# from keras_sequential_ascii import keras2ascii

model = tf.keras.models.load_model('/var/www/html/var/model')
# visualkeras.layered_view(model, to_file='/var/www/html/var/visualization/output3.png', legend=True, draw_volume=True, spacing=30)
# visualkeras.graph_view(model, to_file='/var/www/html/var/visualization/graph1.png')
# ann_viz(model, title="My first neural network", filename='model')

# keras2ascii(model)

tf.keras.utils.plot_model(model, to_file='/var/www/html/var/visualization/plot.png', show_shapes=True)


