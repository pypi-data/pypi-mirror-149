from setuptools import setup, find_packages

setup(name='DParty',
      version='0.9',
      descrption='Smart home SDK from DParty',
      author='lolisky',
      author_email='lorisky1214@gmail.com',
      url="https://github.com/lorisky1214/DParty",
      requires=['mediapipe', 'cv2'],
      packages=find_packages(),
      data_files=[('Lib\site-packages\DParty', ['DParty/yolov5s.onnx','DParty/README.md', 'DParty/requirements.txt'])
                ],
      license="apache 3.0")