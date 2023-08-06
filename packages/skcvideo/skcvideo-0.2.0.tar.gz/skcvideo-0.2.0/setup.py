from setuptools import setup


setup(
    name='skcvideo',
    version='0.2.0',
    description='video utils',
    author='SkillCorner',
    author_email='timothe.collet@skillcorner.com',
    license='MIT',
    packages=[
        'skcvideo',
    ],
    install_requires=[
        'click>=7.1.2',
        'numpy>=1.21.6',
        'opencv-python>=4.5.5.64',
        'imageio>=2.19.0',
        'imageio-ffmpeg>=0.4.2',
    ])
