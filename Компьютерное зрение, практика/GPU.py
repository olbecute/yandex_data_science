from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy as np


# 1. Загрузка обучающей выборки
def load_train(path):
    features_train = np.load(path + "train_features.npy")
    target_train = np.load(path + "train_target.npy")
    features_train = features_train.reshape(features_train.shape[0], 28 * 28) / 255.0
    return features_train, target_train


# 2. Создание модели
def create_model(input_shape):
    model = Sequential()
    # Входной слой + первый скрытый слой
    model.add(Dense(128, activation="relu", input_shape=input_shape))
    model.add(Dropout(0.2))  # Уменьшает переобучение
    # Второй скрытый слой
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.2))
    # Выходной слой
    model.add(Dense(10, activation="softmax"))  # 10 классов предметов одежды

    # Компиляция модели
    model.compile(
        optimizer="adam",  # Оптимизатор Adam
        loss="sparse_categorical_crossentropy",  # Категориальная целевая переменная
        metrics=["accuracy"],
    )  # Метрика точности
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
