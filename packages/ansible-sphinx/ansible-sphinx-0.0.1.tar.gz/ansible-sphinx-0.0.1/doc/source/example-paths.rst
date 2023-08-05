ZooKeeper Paths
---------------

.. path:: zuul

   This is an example Zookeeper path

.. path:: zuul/tenant

   A sub path.  Since paths can get quite long, you may choose to
   indent or to specify the full path.  The signature will appear the
   same either way.

   .. path:: <bar>
      :ephemeral:

      Another sub path.

      .. path:: lock
         :type: RLock
         :ephemeral:

         Another sub path.

.. path:: zuul-system

   Another top level path.

References
==========

This is a path role: :path:`zuul/tenant/<bar>/lock`
