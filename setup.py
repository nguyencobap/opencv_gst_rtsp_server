import io
from setuptools import setup, find_packages

long_description = io.open("README.md", encoding="utf-8").read()

setup(
    name='opencv_gst_rtsp_server',
    version='0.1.3',    
    description='Restream rtsp with opencv frame using gst-rtsp-server',
    url='https://github.com/nguyencobap/opencv_gst_rtsp_server',
    author='Nguyen Hai Nguyen',
    author_email='nguyenhainguyen97@gmail.com',
    license='MIT License',
    python_requires=">=3.5",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gstreamer', 'gst', 'opencv', 'rtsp'],
    install_requires=['opencv-python>=4.6.0.66',
                        'pycairo>=1.24.0',
                        'PyGObject>=3.44.1'
                        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)
