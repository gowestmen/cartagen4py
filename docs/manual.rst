.. _manual:

===========
User Manual
===========

:Authors: Guillaume Touya, Justin Berli, Azelle Courtial
:Copyright:
  This work is licensed under a `European Union Public Licence v1.2`__.
:Abstract:
  This document explains how to use the CartAGen Python library for cartographic generalisation.

.. __: https://eupl.eu/

.. _intro:

Introduction
============

The user manual aims at providing an **overview** of the cartographic generalisation algorithms proposed by CartAGen.
Some complex algorithms and processes are more deeply explained here than in the API Reference, in particular for
those having several steps.

This section is also designed to help you decide **which algorithm best fit your needs**. Indeed, several generalisation
methods are developped to address the same issue, for example to avoid polygon cluttering or to simplify lines and polygons.
Those issues can also depend on the type of geographic objects you are trying to generalise. For example, maybe you
don't want to simplify rivers and roads the same way, as their representation on the map doesn't have the same constraints.

With that in mind, we tried here to offer an overview of the algorithms offered by CartAGen in order to help you make
a choice in your cartographic endeavors. Please keep in mind that **this is not a lecture on cartographic generalisation**
nor a full explanation of the generalisation process. We have designed several **Jupyter notebooks** to serve as learning
material, they are accessible `here. <https://github.com/LostInZoom/cartagen-notebooks>`_

This user manual also assumes you have a certain knowledge of the Python libraries `Shapely <https://github.com/shapely/shapely>`_
and `GeoPandas <https://github.com/geopandas/geopandas>`_ as CartAGen relies on those data format and geometry types.
Furthermore, please ensure you are working with projected geographic data as the vast majority of
generalisation tools provided by this library relies on spatial operations.

.. _points_manual:
.. include:: manual/points.rst
  
.. _lines_manual:
.. include:: manual/lines.rst

.. _polygons_manual:
.. include:: manual/polygons.rst

.. _networks_manual:
.. include:: manual/networks.rst

.. _processes_manual:
.. include:: manual/processes.rst

Bibliography
============

.. footbibliography::