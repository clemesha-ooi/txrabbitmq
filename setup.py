from setuptools import setup

setup(
  name = "txrabbitmq",
  version="0.2",
  description="RabbitMQ's 'rabbitmqctl' as a Twisted Service",
  
  author="Alex Clemesha",
  author_email="clemesha@ucsd.edu",
  url="http://github.com/clemesha-ooi/txrabbitmq",
  download_url="http://github.com/clemesha-ooi/txrabbitmq/tarball/master",
  classifiers=[ ],
  packages=['txrabbitmq'],
  data_files=[('twisted/plugins', ['twisted/plugins/txrabbitmq_plugin.py'])],
  install_requires = ['twotp', 'twisted', 'simplejson'],
)
