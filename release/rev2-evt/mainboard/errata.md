# Squishy rev2-mainboard-evt Errata

 - [x] ~~48MHz XO specified for the Supervisor, replaced with ASE-32.000MHZ-L-C-T, only BoM needs updating~~
 - [ ] Supervisor MCU pins mixed up, meaning the FPGA comm channel needs to be bit-banged SPI rather than using the built-in SERCOM peripheral
 - [ ] Triggers USB OCP when plugged in, `Q10` and `Q1` heat up, `VUSB` @ `1v27` `VCC` @ `0v66`
	- Cutting trace from `VDC` to `R48C` to isolate the `Q10B` gate was not a fix.
