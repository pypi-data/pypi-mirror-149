# Author:KuoYuan Li
[![N|Solid](https://images2.imgbox.com/8f/03/gv0QnOdH_o.png)](https://sites.google.com/ms2.ccsh.tn.edu.tw/pclearn0915)
本程式簡單地結合dlib,opencv
讓不懂機器學習的朋友可以軟簡單地操作人臉辨識,
程式需另外安裝 dlib
dlib whl 安裝包下載網站: (https://reurl.cc/Y1OvEX)
  - 由於windows中dlib的whl檔只下載得到p36版本
  - 故本套工具只能在python3.6中運行
  - dlib whl 安裝包下載後必需由檔案離線安裝 pip install ...
  - opencv whl  下載點:請下載合適的opencv版本<br>
    (https://pypi.tuna.tsinghua.edu.cn/simple/opencv-contrib-python/)
	
##### Download the samples to 'train' folder(下載各種照片樣本至train資料夾)

```
downloadImageSamples()
```

##### 比對目前webcam擷取到的人臉和指定影像檔案並計算它們之間的距離

```
im = captureImageFromCam()
VTest = getFeatureVector(im)
Vtrain = loadFeatureFromPic('train\\李國源.jpg')
```

##### 載入train資料夾中所有jpg檔之特徵及tag並直接預測目前webcam擷取到的人臉對應的TAG
```
loadDB(folder='train')
result = predictFromDB(VTest)
print(result)
```

### Demo with webcam

```
loadDB(folder='train')
predictCam()
```

License
----

MIT
