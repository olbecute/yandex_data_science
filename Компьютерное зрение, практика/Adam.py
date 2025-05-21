from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import numpy as np


# 1. Загрузка обучающей выборки
def load_train(path):
    features_train = np.load(path + "train_features.npy")
    target_train = np.load(path + "train_target.npy")
    # Нормализация пикселей в диапазон [0, 1] и изменение формы для свёрточных слоёв
    features_train = features_train.reshape(features_train.shape[0], 28, 28, 1) / 255.0
    return features_train, target_train


# 2. Создание модели
def create_model(input_shape):
    model = Sequential()

    # Первый свёрточный слой с макс-пулингом
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))

    # Второй свёрточный слой с макс-пулингом
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D((2, 2)))

    # Преобразование в плоский вид для полносвязных слоёв
    model.add(Flatten())

    # Полносвязный слой
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.4))  # Dropout для предотвращения переобучения

    # Выходной слой для классификации
    model.add(Dense(10, activation="softmax"))  # 10 классов одежды

    # Компиляция модели
    optimizer = Adam(lr=0.001)  # Оптимизатор Adam с шагом обучения
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


# 3. Запуск и обучение модели
def train_model(
    model,
    train_data,
    test_data,
    batch_size=32,
    epochs=10,
    steps_per_epoch=None,
    validation_steps=None,
):
    features_train, target_train = train_data
    features_test, target_test = test_data

    # Обучение модели
    model.fit(
        features_train,
        target_train,
        validation_data=(features_test, target_test),
        batch_size=batch_size,
        epochs=epochs,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        verbose=2,
        shuffle=True,
    )

    return model
