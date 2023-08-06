from setuptools import setup, find_packages

setup(name='image-segmentation-aicore',
      version='1.0.2',
      packages=find_packages(),
      install_requires=[
          'pycocotools',
          'tensorflow',
          'matplotlib',
          'fastapi',
          'uvicorn',
          'python-multipart',
          'boto3'
          ])
