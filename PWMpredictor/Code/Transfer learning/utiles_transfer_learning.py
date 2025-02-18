import numpy as np
import time
from sklearn.model_selection import KFold
from sklearn.utils import shuffle
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout,  concatenate, Input
from tensorflow.keras.backend import clear_session
from tensorflow.keras.optimizers import Adam
import pickle


def model_func(x_train):
    in_1 = Input(shape=x_train.shape[1:])
    dense = Dense(100, input_shape=x_train.shape[1:], activation='sigmoid')(in_1)
    drop = Dropout(0.1)(dense)
    logits = Dense(12, activation='sigmoid')(drop)
    dna_pos_1 = Dense(4, activation='softmax')(logits[..., 0:4])
    dna_pos_2 = Dense(4, activation='softmax')(logits[..., 4:8])
    dna_pos_3 = Dense(4, activation='softmax')(logits[..., 8:12])
    concat = concatenate([dna_pos_1, dna_pos_2, dna_pos_3])
    model = Model(inputs=in_1, outputs=concat)
    return model


def b1h_main_model_func(data_input_model, label_mat, folder_address, lr, epochs):
    """B1H model: in vitro data"""
    """model training"""
    x_train, y_train = shuffle(data_input_model, label_mat, random_state=42)
    model_b1h = model_func(x_train)
    opt = Adam(learning_rate=lr)
    model_b1h.compile(loss='categorical_crossentropy', optimizer=opt)
    history = model_b1h.fit(x_train, y_train, epochs=epochs, batch_size=10, verbose=2, validation_split=0.1,
                            validation_batch_size=5)
    model_b1h.summary()
    model_b1h.save(folder_address + '/models/' + 'model_b1h' + '.h5')
    with open(folder_address + '/history/' + 'history_b1h', 'wb') as hist_file:
        pickle.dump(history.history, hist_file)

    clear_session()
    return model_b1h


def set_trainable_layers(b1h_model, t_v):
    # set trainable layers according to transfer version: fine tuning or retrain
    if t_v == 'fine_tuning':  # train only the dna layers
        for layer in b1h_model.layers:
            if layer.name in ['dense_2', 'dense_3', 'dense_4']:
                layer.trainable = True
            else:
                layer.trainable = False

    else: # train all layers
        for layer in b1h_model.layers:
            layer.trainable = True
    return


def leave_out_out_func(crc_input_data, crc_label_mat, b1h_model, folder_address, lr, epochs, start1):
    """ leave one out model: each time only one zinc finger is in the test set
        C_RC input data: in vivo data"""
    n_split = crc_label_mat.__len__()
    keep_test_index_track = []

    """model training"""
    for train_index, test_index in KFold(n_split).split(crc_input_data):
        keep_test_index_track.append(test_index)
        x_train, x_test = crc_input_data[train_index], crc_input_data[test_index]
        y_train, y_test = np.asarray(crc_label_mat)[train_index], np.asarray(crc_label_mat)[test_index]

        model = b1h_model
        opt = Adam(learning_rate=lr)
        model.compile(loss='categorical_crossentropy', optimizer=opt)
        history = model.fit(x_train, y_train, epochs=epochs, batch_size=10, verbose=2, validation_split=0.1,
                            validation_batch_size=5)
        model.summary()
        model.save(folder_address + '/models/' + 'transfer_model' + str(test_index) + '.h5')
        with open(folder_address + '/history/' + 'transfer_history' + str(test_index), 'wb') as hist_file:
            pickle.dump(history.history, hist_file)

        # model evaluating on test set
        y_predicted = model.predict(x_test).flatten()
        np.save(folder_address + '/predictions/' + 'pred' + str(test_index), y_predicted)
        clear_session()

    end1 = time.time()
    print((end1 - start1) / 60)

    return


def cv_func(data_input_model, label_mat, b1h_model, folder_address, lr, epochs, start1):
    """ cross validation model, C_RC input data: in vivo data"""

    n_split = 5
    model_counter = 1
    keep_val_index_track = []

    """model training"""
    for train_index, test_index in KFold(n_split).split(data_input_model):
        keep_val_index_track.append(test_index)
        x_train, x_test = data_input_model[train_index], data_input_model[test_index]
        y_train, y_test = np.asarray(label_mat)[train_index], np.asarray(label_mat)[test_index]

        model = b1h_model
        opt = Adam(learning_rate=lr)
        model.compile(loss='categorical_crossentropy', optimizer=opt)
        history = model.fit(x_train, y_train, epochs=epochs, batch_size=10, verbose=2,validation_split=0.1,
                            validation_batch_size=5)
        model.summary()
        model.save(folder_address + '/models/' + 'model' + str(model_counter) + '.h5')
        with open(folder_address + '/history/' + 'history' + str(model_counter), 'wb') as hist_file:
            pickle.dump(history.history, hist_file)
        model_counter = model_counter+1

        # model evaluating on test
        for i in range(x_test.shape[0]):
            y_predicted = (model.predict(x_test[i].reshape(1, x_test[i].shape[0]))).flatten()
            np.save(folder_address + '/predictions/' + 'pred' + str(test_index[i]), y_predicted)

        clear_session()

    end1 = time.time()
    print((end1 - start1) / 60)

    return
