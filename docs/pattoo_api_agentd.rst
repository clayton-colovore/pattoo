Pattoo Agent API Daemon
=======================

The ``pattoo_api_agentd`` API daemon accepts data from remote ``pattoo`` agents for storage in a database.

Installation
------------

Follow these steps.


#. Follow the installation steps in the :doc:`installation` file.
#. Configure the main section of the configuration file following the steps in :doc:`configuration` file.
#. Start the desired daemons using the commands below. You may want to make these ``systemd`` daemons, if so follow the steps in the :doc:`installation` file.

Usage
-----

``pattoo_api_agentd`` has a simple command structure.

The daemon will require a configuration file in the ``etc/``\ directory. See the configuration section for details.

.. code-block:: bash

   $ bin/pattoo_api_agentd.py --help
   usage: pattoo_api_agentd.py [-h] [--start] [--stop] [--status] [--restart]
                            [--force]

   optional arguments:
     -h, --help  show this help message and exit
     --start     Start the agent daemon.
     --stop      Stop the agent daemon.
     --status    Get daemon daemon status.
     --restart   Restart the agent daemon.
     --force     Stops or restarts the agent daemon ungracefully when used with --stop or
                 --restart.
   $

Configuration
-------------

No additional configuration steps beyond that in the :doc:`configuration` file are required.

Testing
-------
There are a number of steps you can take to make sure everything is OK.

#. If you have setup the daemon for ``systemd`` then you can use the ``systemctl`` command to get the status of the daemon.
#. The daemon should be running on the port configured with the ``ip_bind_port`` parameter. Use the ``netstat`` command to verify this.
#. The ``pattoo_api_agentd`` temporarily stores all the data it receives from ``pattoo`` agents in the ``cache/`` directory. Check there for recent ``.json`` files.
#. Visit the URL ``http://localhost:20201/pattoo/api/v1/agent/status`` to get the status page.
#. Use the :doc:`troubleshooting` for further steps to take

Making ``pattoo_api_agentd`` Start Automatically After Reboot
-------------------------------------------------------------

The easiest way to do this is to consider :doc:`systemd`. Otherwise you will need to manually restart the daemon after a reboot.
