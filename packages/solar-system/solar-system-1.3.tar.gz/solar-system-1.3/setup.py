import solar_system,sys,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="""Solar system gravity simulation using Python turtle graphics. \
使用turtle模块的天体引力模拟程序。"""

try:
    with open("README.rst") as f:
        long_desc=f.read()
except OSError:
    long_desc=''

setup(
    name='solar-system',
    version=solar_system.__version__,
    description=desc,
    long_description=long_desc,
    author=solar_system.__author__,
    author_email=solar_system.__email__,
    url="https://github.com/qfcy/Python/tree/main/solar_system",
    packages=['solar_system'],
    keywords=["solar","system","solarsys","turtle","graphics","太阳系","引力"
              "astronomy","gravity","physics"],
    classifiers=[
        'Programming Language :: Python',
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Multimedia :: Graphics",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: Education"],
)
