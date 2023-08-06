# coding:utf-8

#from setuptools import setup
from setuptools import setup, Extension
# or
# from distutils.core import setup  
foruser = '''# Author:KuoYuan Li

[![N|Solid](https://images2.imgbox.com/8f/03/gv0QnOdH_o.png)](https://sites.google.com/ms2.ccsh.tn.edu.tw/pclearn0915)
本程式簡單地結合dlib,opencv
讓不懂機器學習的朋友可以軟簡單地操作人臉辨識,
dlib==19.7.0
dlib whl 安裝包下載網站： (https://reurl.cc/Y1OvEX)
 '''
with open('README.md',encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='pyFaceTrace',   
        version='4.4.6',   
        description='easy Face Recognition for python',#long_description=foruser,
        long_description=long_description,
        long_description_content_type='text/markdown',
        author='KuoYuan Li',  
        author_email='funny4875@gmail.com',  
        url='https://pypi.org/project/pyFaceTrace',      
        packages=['pyFaceTrace'],   
        include_package_data=True,
        keywords = ['Face recognition', 'Face Trace'],   # Keywords that define your package best
          install_requires=[            # I get to this in a second
          'dlib==19.7.0',#dlib==19.21.1 ==>for python3.7
          'numpy',
          'scikit-image',#'opencv-contrib-python',
          'requests',
          'zipfile36',
          'bz2file'
          ],
      classifiers=[
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3.6',
      ]
)
