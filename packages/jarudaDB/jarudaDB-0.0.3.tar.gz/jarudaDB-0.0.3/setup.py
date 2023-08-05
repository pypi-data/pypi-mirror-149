from importlib.resources import path
import setuptools
from os import path


this_dir = path.abspath(path.dirname(__name__))
with open(path.join(this_dir, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='jarudaDB', # 패키지 명
version='0.0.3',
description='mysql connector python database module',
long_description=long_description,
long_description_content_type="text/markdown",
author='jaruda',
author_email='jaruda88@gmail.com',
url='https://github.com/jaruda-88',
license='MIT', # MIT에서 정한 표준 라이센스
python_requires='>=3',
install_requires=[
    'mysql-connector-python==8.0.29'
], # 패키지 사용을 위해 필요한 추가 설치 패키지
packages= setuptools.find_packages(), # 패키지가 들어있는 폴더, setuptools.find_packages()
#keywords=['test'],
#py_modules=['database'],
classifiers= [
    # 패키지에 대한 태그
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 5 - Production/Stable',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Visualization',

    # Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.6',

    'Operating System :: OS Independent',
]
)