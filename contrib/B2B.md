# Board-to-Board

This document details the interface between the main module and the PHY module, and the PHY module and the connector module.

## Common

There are a few common features between the board-to-board connections, mainly the connectors being used.

 * Connector: [LSHM-150-06.0-L-DV-A-S-K-TR] from [samtec]


[LSHM-150-06.0-L-DV-A-S-K-TR]: https://www.samtec.com/products/lshm-150-06.0-l-dv-a-s-k-tr
[samtec]: https://www.samtec.com/


Due to the connector being self-mating, the connector on the main board is rotated 180° from the connector on the PHY module, which means that the pins from row 1 are connected to row 2 and vis-versa, as the connector uses an even-odd pin mapping, this means that pin 1 is connected to pin 2, 3 to 4, etc.


## Main to PHY


## PHY to Connector
