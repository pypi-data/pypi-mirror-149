colcon-installed-package-information
====================================

Extensions for `colcon-core <https://github.com/colcon/colcon-core>`_ to inspect packages which have already been installed.

Overview
--------

These colcon extensions provide a mechanism which can be used for getting information about packages outside of the workspace, which have already been built and installed prior to the current operation.
In general, it works similarly to and is based on the `PackageDiscoveryExtensionPoint <https://colcon.readthedocs.io/en/released/developer/extension-point.html#packagediscoveryextensionpoint>`_ and `PackageAugmentationExtensionPoint <https://colcon.readthedocs.io/en/released/developer/extension-point.html#packageaugmentationextensionpoint>`_ extensions provided by ``colcon-core``.

Differences
-----------

Installed packages don't generally have a single directory which stores the package content and metadata.
This set of extensions store the "prefix" under which the package resides rather than the package directory (e.g. ``~/workspace/install`` instead of ``~/workspace/install/share/<package_name>`` or ``~/workspace/src/<package_name>``), meaning many packages will likely share the same ``path`` attribute value.

Recursively crawling an entire system or even selective subdirectories to look for installed packages could be very slow, so this process also deviates from the Discover -> Identify -> Augment pipeline used in ``colcon-core``.
Rather than attempting identification on prospective package locations, the discovery phase generally loads a list of installed packages from a database of some kind, such as the file-based colcon index.
In some cases, the database might already populate sufficient information on the descriptor to identify the package.
For others, only presence can be known, and augmentation extensions must add additional information to the descriptor by searching for specific files throughout the prefix directory.

The ``type`` attribute of an installed package works similarly to workspace packages, but must always start with ``installed.`` followed by a more specific package type.
If more information about a package cannot be determined and it is known only to exist under a certain prefix, the ``type`` should be set to ``installed``.

Supported Package Types
-----------------------

This package provides extensions which are able to discover packages using the ``PrefixPathExtensionPoint`` to enumerate install prefixes, and ``FindInstalledPackagesExtensionPoint`` to enumerate names of packages installed under those prefixes.
It can then use the colcon index in those prefixes as well as python eggs to determine dependency information and augment the packages appropriately.

Support for more package databases for discovery and augmentation can be added by other packages by implementing and registering appropriate extensions.
