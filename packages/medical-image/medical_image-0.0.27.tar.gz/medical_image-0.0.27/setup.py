from setuptools import setup, find_packages
import medical_image

setup(
    name="medical_image",
    version=medical_image.__version__,
    license='MIT',
    author="Hwa Pyung Kim",
    author_email="hpkim0512@deepnoid.com",
    description="DICOM Networking Library for AI Apps",
    long_description=open('README.md').read(),
    url="https://gl.deepnoid.com:9443/deep-ai/general/medical-image",
    packages=find_packages(),
    package_data = {
        'medical_image': [
            'fonts/NotoSansCJKkr-Thin.otf',
            'fonts/NotoSansCJKkr-DemiLight.otf',
            'fonts/NotoSansCJKkr-Medium.otf',
            'fonts/NotoSansCJKkr-Bold.otf',
            'logo/*.png'
        ],
    },
    include_package_data=True,
    python_requires='>=3',
    install_requires=[
        'opencv-python==4.3.0.36',
        'opencv-python-headless==4.3.0.36',
        'pydicom==2.1.2',
        'numpy==1.19.5',
        'pillow'
    ]
)
