Beta
====

Coiled v2 is our rewritten backend.

It was written with the following objectives:

-   **Reliability**: clusters come up with greater certainty, especially at larger scale.
-   **Cost**: we provide a richer and more responsive access to sets of instance types and spot instances.
-   **Visibility**: when situations occur, issues are more plainly visible and easier to debug.

V2 provides both a richer and more robust interaction with the underlying cloud,
and delivers this information to you so that you can understand what is going
on.

    .. figure:: images/widget.png
       :alt: Terminal dashboard displaying the Coiled cluster status overview, configuration, and Dask worker states.

Here's how to try v2 now:

Step 1: Does v2 have what you need?
-----------------------------------

For now, v2 is missing a few features:

- GPU support is not implemented.
- Spot instance support is not implemented for GCP.
- Fetching GCP cluster logs via Coiled is disabled temporarily (however, if you're using GCP in your own account, you can still get to the logs via GCP Logging)

If any of those are essential to you, you may not want to switch to v2 quite yet.

Step 2: Updated IAM Permissions
-------------------------------

If you're not running Coiled in your own AWS/GCP account, then you can ignore this section.

The IAM permissions we need in v2 are slightly different, so refer to the updated policy documents can here: :ref:`GCP <gcp-policy-doc>`  /  :ref:`AWS <aws-iam-policy>`

Step 3: Code Changes
--------------------

You can opt in to v2 by changing your import:

.. code-block:: python

    # from coiled import Cluster
    from coiled.v2 import Cluster

    cluster = Cluster(scheduler_vm_types=["t3.medium"], worker_vm_types=["t3.medium"])
    cluster.close()


For most purposes, that's it! Just ``coiled.v2.Cluster`` instead of ``coiled.Cluster``.

If you're using options like ``worker_memory``, ``worker_cpu``, ``scheduler_memory``, ``scheduler_cpu`` then you may need
small changes to accommodate v2's stricter (more correct) logic for selecting instance types.

You might have this in v1:

.. code-block:: python

    from coiled import Cluster

    cluster = Cluster(worker_memory="32GiB", worker_cpu=1)

In v2, this gives an error because we couldn't find an instance type with that much memory and only one core.

Instead, you can leave out the ``worker_cpu`` argument, or give us a range of acceptable core counts:

.. code-block:: python

    from coiled.v2 import Cluster

    cluster = Cluster(worker_memory="32GiB", worker_cpu=[1, 8])


Continued Support of v1
-----------------------

We will continue to support the original Coiled system for some months to allow you to adapt your workflows and make any required changes. We want to ensure a smooth experience and don't expect many breaking changes.

If you want to stay with the existing system, even after v2 is launched, pin
your ``coiled`` library to ``<0.2`` in your Python environment:

.. code-block:: python

    coiled < 0.2


Deprecations
------------

Cluster configurations have been deprecated so the ``configuration`` argument is no longer allowed.
Instead, configuration is now directly passed to the ``Cluster`` class at creation time.

The ``protocol`` parameter (which was used for proxying through Coiled to the scheduler) is not planned for v2.

API Reference
-------------

.. autoclass:: coiled._beta.cluster.ClusterBeta
.. autoclass:: coiled._beta.core.BackendOptions
.. autoclass:: coiled._beta.core.AWSOptions
.. autoclass:: coiled._beta.core.FirewallOptions
