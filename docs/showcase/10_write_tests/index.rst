Write tests
=============

Writing test with HIL (Hardware in the loop) is much more complex than just pure software tests.

The goal of a good test is, to just write code of what should be tested and as little as possible boilerplate.

Octoprobe and pytest support you in writing readable and consise tests.

The bright side of Octoprobe/pytest
-----------------------------------

Octoprobe interfaces and abstracts the hardware. This makes writing tests easy.

pytest is a powerful framework which allows to write consise tests, but brings in a lot of complexity.

The dark side of Octoprobe/pytest
---------------------------------

Octoprobe may fail an many levels at it uses heavely usb and talks to many processors on the tentacles.

pytest brings in a lot of complexity. It is non trivial to write fixtures and understand testcollection.

Why should I start with ``testbed_showcase``
--------------------------------------------

``testbed_showcase`` should run out of the box and it includes all layers of Octoprobe and pytest.

With ``testbed_showcase`` running, you have a reference to derive your tests or extensions.

