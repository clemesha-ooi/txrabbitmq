txrabbitmq - RabbitMQ's `rabbitmqctl` as a Twisted Service.
===========================================================


Overview
--------

Implements RabbitMQ's `rabbitmqctl` command line tool as a Twisted Service,
Expose this functionality over several protocols, most importantly: HTTP and AMQP.


Install
-------

Get the latest code::

    $ git://github.com/clemesha-ooi/txrabbitmq.git


The recommend way of using `txrabbitmq` is to create a `virtualenv` and
the install all dependencies with `pip` into the `virtualenv`::

    $ virtualenv --no-site-packages txrabbitmq_env 
    $ pip -E txrabbitmq_env install -U twotp orbited twisted simplejson stompservice


Usage
-----

Start up the RESTful Command/Data http service:

From top-level package directory run::

    $ twistd -n txrabbitmq


Get realtime data from RabbitMQ:

From top-level package directory run::

    $ twistd -n txrabbitmq

Open 2nd shell, navigate to the directory `webui/push` and run::

    $ python data_producer.py #first shell
    $ orbited --config=rabbitmq.cfg #second shell

Open ports 8000 and 9000, to see commands data and push, respectively


License
-------
Apache License:
http://www.opensource.org/licenses/apache2.0.php


Contact
-------
This code is part of the Ocean Observatories Initiative project, 
for more details please see here: http://ci.oceanobservatories.org/
Or email the author: Alex Clemesha <clemesha@ucsd.edu>.
