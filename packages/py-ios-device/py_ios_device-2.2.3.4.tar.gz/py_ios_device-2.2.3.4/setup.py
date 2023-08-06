from setuptools import setup,find_packages

setup(name='py_ios_device',
      version="2.2.3.4",
      description='Get ios data and operate ios devices',
      author='chenpeijie',
      author_email='cpjsf@163.com',
      maintainer='chenpeijie',
      maintainer_email='',
      url='https://github.com/YueChen-C/py-ios-device',
      packages=find_packages(),
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      platforms=["any"],
      install_requires=open('requirements.txt').read(),  # 第三方库依赖
      entry_points={
          'console_scripts':{
              'pyidevice=ios_device.main:cli'
          }
      },
      )
