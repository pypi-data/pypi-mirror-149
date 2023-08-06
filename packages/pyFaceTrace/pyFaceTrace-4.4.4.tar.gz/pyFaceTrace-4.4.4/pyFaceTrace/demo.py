import pyFaceTrace as ft
#download the samples to 'train' folder
#ft.downloadImageSamples()
# 比對目前webcam擷取到的人臉和指定影像檔案並計算它們之間的距離
im = ft.captureImageFromCam()
VTest = ft.getFeatureVector(im)
Vtrain = ft.loadFeatureFromPic('train\\李國源.jpg')
print(ft.dist(VTest,Vtrain))
    
#載入train資料夾中所有jpg檔之特徵及tag
#並直接預測目前webcam擷取到的人臉對應的TAG
ft.loadDB(folder='train')
result = ft.predictFromDB(VTest)
print(result)
    
#vedio Demo
ft.predictCam()