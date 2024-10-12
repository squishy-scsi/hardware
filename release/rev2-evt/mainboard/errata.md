# Squishy rev2-mainboard-evt Errata

 - [x] ~~48MHz XO specified for the Supervisor, replaced with ASE-32.000MHZ-L-C-T, only BoM needs updating~~
 - [ ] Supervisor MCU pins mixed up, meaning the FPGA comm channel needs to be bit-banged SPI rather than using the built-in SERCOM peripheral
 - [ ] Q1's Source and Drain are swapped (schematic symbol issue)
 - [ ] U16/U17/U20's BIAS pin left floating not connected to Vin
 - [ ] SWCLK and SWDIO swapped on J4
