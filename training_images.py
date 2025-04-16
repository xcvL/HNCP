import keras
from sklearn.model_selection import KFold
from keras.api.callbacks import ModelCheckpoint,EarlyStopping, CSVLogger
from winsound import Beep

keras.backend.clear_session() # 초기화

(xTrain,yTrain),(xTest,yTest)=keras.datasets.mnist.load_data() # mnist 데이터 로드

# 데이터 전처리
xTrain=xTrain.reshape((60000,28,28,1))/255.0
xTest=xTest.reshape((10000,28,28,1))/255.0

# cnn 모델 생성
model=keras.Sequential([
    keras.layers.Conv2D(32, kernel_size=(3,3), activation="relu", input_shape=(28,28,1)),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(64, kernel_size=3, activation="relu",padding="same"),
    keras.layers.MaxPooling2D((2,2)),
    keras.layers.Conv2D(128, kernel_size=3, activation="relu",padding="same"),
    keras.layers.Dropout(0.2),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(10,activation="softmax")
])

# 모델 컴파일
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

pred_list=[] # 예측값 저장 리스트
kfold=KFold(n_splits=5, shuffle=True, random_state=42) # k-fold cross validation | k개의 fold를 만들어 교차검증 | k=5

# 반복
for i, (training,validation) in enumerate(kfold.split(xTrain)):
    xTraining, yTraining=xTrain[training], yTrain[training] # 훈련 데이터
    xValidation, yValidation=xTrain[validation], yTrain[validation] # 검증 데이터

    mcp=ModelCheckpoint(filepath=f"w3_{i+1}.weights.h5", save_best_only=True, save_weights_only=True, verbose=0)
    es=EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True, verbose=0)
    csvl=CSVLogger(f"fold3_{i+1}.log")

    # 모델 학습
    history=model.fit(xTraining, yTraining, batch_size=64, epochs=40, 
                      validation_data=(xValidation, yValidation), 
                      callbacks=[mcp,es,csvl], verbose=0)
    
    model.load_weights(f"w3_{i+1}.weights.h5") # 모델 가중치 로드
    pred=model.predict(xTest) # 모델 예측
    pred_list.append(pred) # 예측값 저장

    # 모델 평가
    loss, accuracy=model.evaluate(xTest, yTest, verbose=0)
    print(f"loss : {loss : .4f}, accuracy : {accuracy : .4f}")


    # json 형식으로 저장
    model_json=model.to_json()
    with open(f"model3_{i+1}.json", "w") as f:
        f.write(model_json)
    
    # h5 형식으로 저장
    model.save(f"model3_{i+1}.h5")

    # 모델 가중치 저장
    model.save_weights(f"model3_{i+1}.weights.h5")

Beep(600,1000) # 종료 알림


# 파일 번호(n) : 3

# 실행할 때마다 ModelCheckpoint, load_weights의 filepath 변수에 저장된 파일 이름 바꾸기
# 파일 이름 : f"wn_{i+1}.weights.h5" | n=0, 1, 2, ...
# 위치 표시 :    ^

# 실행할 때마다 CSVLogger의 filename변수에 저장된 파일 이름 바꾸기
# 파일 이름 : f"foldn_{i+1}.log" | n=0, 1, 2, ...
# 위치 표시 :       ^

# 실행할 때마다 open의 file변수에 저장된 파일 이름 바꾸기
# 파일 이름 : f"modeln_{i+1}.json" | n=0, 1, 2, ...
# 위치 표시 :        ^

# 실행할 때마다 save의 filepath변수에 저장된 파일 이름 바꾸기
# 파일 이름 : f"modeln_{i+1}.h5" | n=0, 1, 2, ...
# 위치 표시 :        ^

# 실행할 때마다 save_weights의 filepath변수에 저장된 파일 이름 바꾸기
# 파일 이름 : f"modeln_{i+1}.weights.h5" | n=0, 1, 2, ...
# 위치 표시 :        ^
