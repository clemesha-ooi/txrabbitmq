#!/usr/bin/env python

"""
@file README.py
@author Alex Clemesha <clemesha@ucsd.edu>
@date 8/18/09

@mainpage 
txrabbitmq - RabbitMQ's `rabbitmqctl` as a Twisted Service.


@section Overview

Implements RabbitMQ's `rabbitmqctl` command line tool as a Twisted Service, 
Expose this functionality over several protocols, most importantly: HTTP and AMQP.


@section Install

The recommend way of using `txrabbitmq` is to create a `virtualenv` and
the install all dependencies with `pip` into the `virtualenv`
@code
    $ virtualenv --no-site-packages txrabbitmq_env 
    $ pip -E txrabbitmq_env install -U twotp orbited twisted simplejson stompservice
@endcode


@section Usage

@subsection Start up the RESTful Command/Data http service:
@code
    $ twistd -n txrabbitmq
@endcode

@subsection Push data from RabbitMQ
From top-level dir run: 
@code
    $ twistd -n txrabbitmq
@endcode

Open 2nd shell, navigate to dir `webui/push` and run:
@code
    $ python data_producer.py #first shell
    $ orbited --config=rabbitmq.cfg #second shell
@endcode

Open ports 8000 and 9000, to see commands data and push, respectively
"""

print "This README's format is a massive Doxygen @mainpage hack. FIXME!!!"
