# Board-to-Board

This document details the interface between the main module and the PHY module, and the PHY module and the connector module.

## Connector choice

The mezzanine connectors used between the Squishy mainboard, PHY, and connector interface are from [Amphenol FCI].

* [10144518-101802LF] From mainboard to PHY and PHY to connector interface
* [10144517-102802LF] Mating connector for [10144518-101802LF]


> [!NOTE]
> To ensure proper keying, the [10144517-102802LF] mezzanine on the connector boards is
> rotated 180° to prevent you from plugging them into the mainboard in a sensable way, thus
> damaging the device.


## Main to PHY

Squishy Mainboard PHY Pinout:

|      Signal | Pin # | Pin # |      Signal |
|-------------|-------|-------|-------------|
|        +5v0 |     1 |     2 |        +3v3 |
|        +5v0 |     3 |     4 |        +3v3 |
|        +5v0 |     5 |     6 |        +3v3 |
|        +5v0 |     7 |     8 |        +3v3 |
|         GND |    09 |    10 |         GND |
|      ID_SCL |    11 |    12 |          NC |
|      ID_SCA |    13 |    14 |          NC |
|         GND |    15 |    16 |         GND |
|  ~PHY_PRSNT |    17 |    18 |          NC |
|  TERMPWR_EN |    19 |    20 |          NC |
|         GND |    21 |    22 |         GND |
|  LS_CTRL[0] |    23 |    24 |     DBH_DIR |
|  LS_CTRL[1] |    25 |    26 |      DB[13] |
|         GND |    27 |    28 |         GND |
|      DB[12] |    29 |    30 |      DB[15] |
|      DB[14] |    31 |    32 |     DBL_DIR |
|         GND |    33 |    34 |         GND |
|       DP[1] |    35 |    36 |      DB[00] |
|      DB[01] |    37 |    38 |      DB[02] |
|         GND |    39 |    40 |         GND |
|      DB[03] |    41 |    42 |      DB[04] |
|      DB[05] |    43 |    44 |      DB[06] |
|         GND |    45 |    46 |         GND |
|      DB[07] |    47 |    48 |       DP[0] |
|         BSY |    49 |    50 |         ATN |
|         GND |    51 |    52 |         GND |
|     BSY_DIR |    53 |    54 |         ACK |
|         RST |    55 |    56 |    INIT_DIR |
|         GND |    57 |    58 |         GND |
|     RST_DIR |    59 |    60 |         MSG |
|         SEL |    61 |    62 |         C/D |
|         GND |    63 |    64 |         GND |
|     SEL_DIR |    65 |    66 |         I/O |
|         REQ |    67 |    68 |    TRGT_DIR |
|         GND |    69 |    70 |         GND |
|      DB[08] |    71 |    72 |      DB[09] |
|      DB[10] |    73 |    74 |      DB[11] |
|         GND |    75 |    76 |         GND |
|  LS_CTRL[4] |    77 |    78 |  LS_CTRL[2] |
|  LS_CTRL[5] |    79 |    80 |  LS_CTRL[3] |
|         GND |    81 |    82 |         GND |
|          NC |    83 |    84 |          NC |
|          NC |    85 |    86 |          NC |
|         GND |    87 |    88 |         GND |
|          NC |    89 |    90 |          NC |
|          NC |    91 |    92 |          NC |
|         GND |    93 |    94 |         GND |
|          NC |    95 |    96 |          NC |
|          NC |    97 |    98 |          NC |
|         GND |    99 |   100 |         GND |


* `ID_SCA`/`ID_SCL`: PHY And connector I2C Bus
* `~PHY_PRSNT`: PHY Presence detect (pulled to GND on PHY side)
* `TERMPWR_EN`: PHY Termination power enable
* `DB[0..7]`: PHY Lower data bus
* `DB[8..15]`: PHY Upper data bus
* `DP[0..1]`: PHY Lower/Upper data bus parity
* `*_DIR`: PHY Transiciver direction control signals
* `LS_CTRL[0..5]`: Low-speed control signals
* `NC`: No-Connect


## PHY to Connector

Squishy PHY to Connector Pinout:

|      Signal | Pin # | Pin # |      Signal |
|-------------|-------|-------|-------------|
|         GND |     1 |     2 |         GND |
|        +3v3 |     3 |     4 |      ID_SDA |
|          NC |     5 |     6 |      ID_SCL |
|         GND |     7 |     8 |         GND |
|         GND |    09 |    10 |         GND |
|     DB[12]+ |    11 |    12 |     DB[12]- |
|     DB[13]+ |    13 |    14 |     DB[13]- |
|         GND |    15 |    16 |         GND |
|     DB[14]+ |    17 |    18 |     DB[14]- |
|     DB[15]+ |    19 |    20 |     DB[15]- |
|         GND |    21 |    22 |         GND |
|     DP[01]+ |    23 |    24 |     DP[01]- |
|     DB[00]+ |    25 |    26 |     DB[00]- |
|         GND |    27 |    28 |         GND |
|     DB[01]+ |    29 |    30 |     DB[01]- |
|     DB[02]+ |    31 |    32 |     DB[02]- |
|         GND |    33 |    34 |         GND |
|     DB[03]+ |    35 |    36 |     DB[03]- |
|     DB[04]+ |    37 |    38 |     DB[04]- |
|         GND |    39 |    40 |         GND |
|     DB[05]+ |    41 |    42 |     DB[05]- |
|     DB[06]+ |    43 |    44 |     DB[06]- |
|         GND |    45 |    46 |         GND |
|     DB[07]+ |    47 |    48 |     DB[07]- |
|     DP[01]+ |    49 |    50 |     DP[01]- |
|         GND |    51 |    52 |         GND |
|   DIFFSENSE |    53 |    54 |          NC |
|     TERMPWR |    55 |    56 |     TERMPWR |
|     TERMPWR |    57 |    58 |     TERMPWR |
|         GND |    59 |    60 |         GND |
|        ATN+ |    61 |    62 |        ATN- |
|         GND |    63 |    64 |         GND |
|        BSY+ |    65 |    66 |        BSY- |
|        ACK+ |    67 |    68 |        ACK- |
|         GND |    69 |    70 |         GND |
|        RST+ |    71 |    72 |        RST- |
|        MSG+ |    73 |    74 |        MSG- |
|         GND |    75 |    76 |         GND |
|        SEL+ |    77 |    78 |        SEL- |
|        C/D+ |    79 |    80 |        C/D- |
|         GND |    81 |    82 |         GND |
|        REQ+ |    83 |    84 |        REQ- |
|        I/O+ |    85 |    86 |        I/O- |
|         GND |    87 |    88 |         GND |
|     DB[08]+ |    89 |    90 |     DB[08]- |
|     DB[09]+ |    91 |    92 |     DB[09]- |
|         GND |    93 |    94 |         GND |
|     DB[10]+ |    95 |    96 |     DB[10]- |
|     DB[11]+ |    97 |    98 |     DB[11]- |
|         GND |    99 |   100 |         GND |


* `ID_SCA`/`ID_SCL`: PHY And connector I2C Bus
* `DB[00..07][+-]`: PHY Lower data bus
* `DB[08..15][+-]`: PHY Upper data bus
* `DP[00..01][+-]`: PHY Lower/Upper data bus parity
* `NC`: No-Connect

**Note:** When a single ended PHY is connected, all `+` pins act as signal return paths

[10144518-101802LF]: https://www.amphenol-cs.com/product/10144518101802lf.html
[10144517-102802LF]: https://www.amphenol-cs.com/product/10144517102802lf.html
[Amphenol FCI]: https://www.amphenol-cs.com/
