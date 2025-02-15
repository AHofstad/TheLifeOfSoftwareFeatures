commit 1ad53cee1f4e2768310fca98de0381df9c39b617
Author: Bob Kuhn <bob.kuhn@att.net>
Date:   Mon Jan 13 18:47:30 2020 -0600

    Improved STMicro L64XX stepper driver support (#16452)

diff --git a/Marlin/src/libs/L6470/000_l6470_read_me.md b/Marlin/src/libs/L6470/000_l6470_read_me.md
deleted file mode 100644
index 712ced551b..0000000000
--- a/Marlin/src/libs/L6470/000_l6470_read_me.md
+++ /dev/null
@@ -1,105 +0,0 @@
-Arduino-6470 library revision 0.7.0 or above is required.
-
-This software can be used with any L647x chip and the powerSTEP01. L647x and powerSTEP01 devices can not be mixed within a system. A flag in the library must be set to enable use of a powerSTEP01.
-
-These devices use voltage PWMs to drive the stepper phases. Phase current is not directly controlled. Each microstep corresponds to a particular PWM duty cycle. The KVAL\_HOLD register scales the PWM duty cycle.
-
-This software assumes that all L6470 drivers are in one SPI daisy chain.
-
-```
-    The hardware setup is:
-
-      MOSI from controller tied to SDI on the first device
-
-      SDO of the first device is tied to SDI of the next device
-
-      SDO of the last device is tied to MISO of the controller
-
-      all devices share the same SCK, SS\_PIN and RESET\_PIN
-
-      Each L6470 passes the data it saw on its SDI to its neighbor on the **NEXT** SPI cycle (8 bit delay).
-
-      Each L6470 acts on the **last** SPI data it saw when the SS\_PIN **goes high**.
-```
-
-The L6470 drivers operate in STEP\_CLOCK mode. In this mode the direction and enable are done via SPI commands and the phase currents are changed in response to step pulses (generated in the usual way).
-
-There are two different SPI routines used.
-
--   **uint8\_t** L6470\_Transfer(uint8\_t data, int \_SSPin, const uint8\_t chain\_position) is used to setup the chips and by the maintenance/status code. This code uses the Arduino-6470 library.
-
--   **void** L6470\_Transfer(uint8\_t L6470\_buf[], const uint8\_t length) is used by the set\_directions() routine to send the direction/enable commands. The library is NOT used by this code.
-
-**HARDWARE/SOFTWARE interaction**
-
-Powering up a stepper and setting the direction are done by the same command. Can't do one without the other.
-
-**All** directions are set **every time** a new block is popped off the queue by the stepper ISR.
-
-SPI transfers, when setting the directions, are minimized by using arrays and a SPI routine dedicated to this function. L6470 library calls are not used. For N L6470 drivers, this results in a N byte transfer. If library calls were used then N\*N bytes would be sent.
-
-**Power up (reset) sequence:**
-
-1.  Stepper objects are created before the **setup()** entry point is reached.
-
-2.  After the **setup()** entry point is reached and before the steppers are initialized, L6470\_init() is called to do the following
-
-3.  If present, the hardware reset is pulsed.
-
-4.  The L6470\_chain array is populated during **setup()**. This array is used to tell where in the SPI stream the commands/data for an stepper is positioned.
-
-5.  The L6470 soft SPI pins are initialized.
-
-6.  The L6470 chips are initialized during **setup()**. They can be re-initialized using the **L6470\_init\_to\_defaults()** function
-
-The steppers are **NOT** powered up during this sequence.
-
-**L6470\_chain** array
-
-This array is used by all routines that transmit SPI data.
-
-```
-  Location 0 - number of drivers in chain
-
-  Location 1 - axis index for first device in the chain (closest to MOSI)
-
-  ...
-
-  Location N - axis index for last device in the N device long chain (closest to MISO)
-```
-
-**Direction set and enable**
-
-The DIR\_WRITE macros for the L6470 drivers are written so that the standard X, Y, Z and extruder logic used by the set\_directions() routine is not altered. These macros write the correct forward/reverse command to the corresponding location in the array *L6470\_dir\_commands*.
-
-At the end of the set\_directions() routine, the array *L6470\_chain* is used to grab the corresponding direction/enable commands out of the array *L6470\_dir\_commands* and put them in the correct sequence in the array *L6470\_buf*. Array *L6470\_buf* is then passed to the **void** L6470\_Transfer function which actually sends the data to the devices.
-
-**Utilities and misc**
-
-The **absolute position** registers should accurately reflect Marlin’s stepper position counts. They are set to zero during initialization. G28 sets them to the Marlin counts for the corresponding axis after homing. NOTE – these registers are often the negative of the Marlin counts. This is because the Marlin counts reflect the logical direction while the registers reflect the stepper direction. The register contents are displayed via the M114 D command.
-
-The **L6470\_monitor** feature reads the status of each device every half second. It will report if there are any error conditions present or if communications has been lost/restored. The KVAL\_HOLD value is reduced every 2 – 2.5 seconds if the thermal warning or thermal shutdown conditions are present.
-
-**M122** displays the settings of most of the bits in the status register plus a couple of other items.
-
-**M906** can be used to set the KVAL\_HOLD register one driver at a time. If a setting is not included with the command then the contents of the registers that affect the phase current/voltage are displayed.
-
-**M916, M917 & M918**
-
-These utilities are used to tune the system. They can get you in the ballpark for acceptable jerk, acceleration, top speed and KVAL\_HOLD settings. In general they seem to provide an overly optimistic KVAL\_HOLD setting because of the lag between setting KVAL\_HOLD and the driver reaching final temperature. Enabling the **L6470\_monitor** feature during prints will provide the **final useful KVAL\_HOLD setting**.
-
-The amount of power needed to move the stepper without skipping steps increases as jerk, acceleration and top speed increase. The power dissipated by the driver increases as the power to the stepper increases. The net result is a balancing act between jerk, acceleration, top speed and power dissipated by the driver.
-
-**M916 -** Increases KVAL\_HOLD while moving one axis until get thermal warning. This routine is also useful for determining the approximate KVAL\_HOLD where the stepper stops losing steps. The sound will get noticeably quieter as it stops losing steps.
-
-**M917 -** Find minimum current thresholds. This is done by doing the following steps while moving an axis:
-
-1.  Decrease OCD current until overcurrent error
-
-2.  Increase OCD until overcurrent error goes away
-
-3.  Decrease stall threshold until stall error
-
-4.  Increase stall until stall error goes away
-
-**M918 -** Increase speed until error or max feedrate achieved.

commit fa236e9718cd2feb85a1986b8f56ad97cd2f4871
Author: Scott Lahteine <github@thinkyhead.com>
Date:   Fri Mar 1 19:29:48 2019 -0600

    General cleanup ahead of L64XX

diff --git a/Marlin/src/libs/L6470/000_l6470_read_me.md b/Marlin/src/libs/L6470/000_l6470_read_me.md
index 170ba6596e..712ced551b 100644
--- a/Marlin/src/libs/L6470/000_l6470_read_me.md
+++ b/Marlin/src/libs/L6470/000_l6470_read_me.md
@@ -6,20 +6,20 @@ These devices use voltage PWMs to drive the stepper phases. Phase current is not
 
 This software assumes that all L6470 drivers are in one SPI daisy chain.
 
-``` {.gcode}
+```
     The hardware setup is:
 
-        MOSI from controller tied to SDI on the first device
+      MOSI from controller tied to SDI on the first device
 
-        SDO of the first device is tied to SDI of the next device
+      SDO of the first device is tied to SDI of the next device
 
-        SDO of the last device is tied to MISO of the controller
+      SDO of the last device is tied to MISO of the controller
 
-        all devices share the same SCK, SS\_PIN and RESET\_PIN
+      all devices share the same SCK, SS\_PIN and RESET\_PIN
 
-        Each L6470 passes the data it saw on its SDI to its neighbor on the **NEXT** SPI cycle (8 bit delay).
+      Each L6470 passes the data it saw on its SDI to its neighbor on the **NEXT** SPI cycle (8 bit delay).
 
-        Each L6470 acts on the **last** SPI data it saw when the SS\_PIN **goes high**.
+      Each L6470 acts on the **last** SPI data it saw when the SS\_PIN **goes high**.
 ```
 
 The L6470 drivers operate in STEP\_CLOCK mode. In this mode the direction and enable are done via SPI commands and the phase currents are changed in response to step pulses (generated in the usual way).
@@ -58,12 +58,12 @@ The steppers are **NOT** powered up during this sequence.
 
 This array is used by all routines that transmit SPI data.
 
-``` {.gcode}
+```
   Location 0 - number of drivers in chain
 
   Location 1 - axis index for first device in the chain (closest to MOSI)
 
-  …
+  ...
 
   Location N - axis index for last device in the N device long chain (closest to MISO)
 ```

commit 2f35747f294c4b3dc3e6920b34e208f89bd4841d
Author: Bob Kuhn <bob.kuhn@att.net>
Date:   Wed Jan 23 19:06:54 2019 -0600

    L6470 SPI daisy chain support (#12895)

diff --git a/Marlin/src/libs/L6470/000_l6470_read_me.md b/Marlin/src/libs/L6470/000_l6470_read_me.md
new file mode 100644
index 0000000000..170ba6596e
--- /dev/null
+++ b/Marlin/src/libs/L6470/000_l6470_read_me.md
@@ -0,0 +1,105 @@
+Arduino-6470 library revision 0.7.0 or above is required.
+
+This software can be used with any L647x chip and the powerSTEP01. L647x and powerSTEP01 devices can not be mixed within a system. A flag in the library must be set to enable use of a powerSTEP01.
+
+These devices use voltage PWMs to drive the stepper phases. Phase current is not directly controlled. Each microstep corresponds to a particular PWM duty cycle. The KVAL\_HOLD register scales the PWM duty cycle.
+
+This software assumes that all L6470 drivers are in one SPI daisy chain.
+
+``` {.gcode}
+    The hardware setup is:
+
+        MOSI from controller tied to SDI on the first device
+
+        SDO of the first device is tied to SDI of the next device
+
+        SDO of the last device is tied to MISO of the controller
+
+        all devices share the same SCK, SS\_PIN and RESET\_PIN
+
+        Each L6470 passes the data it saw on its SDI to its neighbor on the **NEXT** SPI cycle (8 bit delay).
+
+        Each L6470 acts on the **last** SPI data it saw when the SS\_PIN **goes high**.
+```
+
+The L6470 drivers operate in STEP\_CLOCK mode. In this mode the direction and enable are done via SPI commands and the phase currents are changed in response to step pulses (generated in the usual way).
+
+There are two different SPI routines used.
+
+-   **uint8\_t** L6470\_Transfer(uint8\_t data, int \_SSPin, const uint8\_t chain\_position) is used to setup the chips and by the maintenance/status code. This code uses the Arduino-6470 library.
+
+-   **void** L6470\_Transfer(uint8\_t L6470\_buf[], const uint8\_t length) is used by the set\_directions() routine to send the direction/enable commands. The library is NOT used by this code.
+
+**HARDWARE/SOFTWARE interaction**
+
+Powering up a stepper and setting the direction are done by the same command. Can't do one without the other.
+
+**All** directions are set **every time** a new block is popped off the queue by the stepper ISR.
+
+SPI transfers, when setting the directions, are minimized by using arrays and a SPI routine dedicated to this function. L6470 library calls are not used. For N L6470 drivers, this results in a N byte transfer. If library calls were used then N\*N bytes would be sent.
+
+**Power up (reset) sequence:**
+
+1.  Stepper objects are created before the **setup()** entry point is reached.
+
+2.  After the **setup()** entry point is reached and before the steppers are initialized, L6470\_init() is called to do the following
+
+3.  If present, the hardware reset is pulsed.
+
+4.  The L6470\_chain array is populated during **setup()**. This array is used to tell where in the SPI stream the commands/data for an stepper is positioned.
+
+5.  The L6470 soft SPI pins are initialized.
+
+6.  The L6470 chips are initialized during **setup()**. They can be re-initialized using the **L6470\_init\_to\_defaults()** function
+
+The steppers are **NOT** powered up during this sequence.
+
+**L6470\_chain** array
+
+This array is used by all routines that transmit SPI data.
+
+``` {.gcode}
+  Location 0 - number of drivers in chain
+
+  Location 1 - axis index for first device in the chain (closest to MOSI)
+
+  …
+
+  Location N - axis index for last device in the N device long chain (closest to MISO)
+```
+
+**Direction set and enable**
+
+The DIR\_WRITE macros for the L6470 drivers are written so that the standard X, Y, Z and extruder logic used by the set\_directions() routine is not altered. These macros write the correct forward/reverse command to the corresponding location in the array *L6470\_dir\_commands*.
+
+At the end of the set\_directions() routine, the array *L6470\_chain* is used to grab the corresponding direction/enable commands out of the array *L6470\_dir\_commands* and put them in the correct sequence in the array *L6470\_buf*. Array *L6470\_buf* is then passed to the **void** L6470\_Transfer function which actually sends the data to the devices.
+
+**Utilities and misc**
+
+The **absolute position** registers should accurately reflect Marlin’s stepper position counts. They are set to zero during initialization. G28 sets them to the Marlin counts for the corresponding axis after homing. NOTE – these registers are often the negative of the Marlin counts. This is because the Marlin counts reflect the logical direction while the registers reflect the stepper direction. The register contents are displayed via the M114 D command.
+
+The **L6470\_monitor** feature reads the status of each device every half second. It will report if there are any error conditions present or if communications has been lost/restored. The KVAL\_HOLD value is reduced every 2 – 2.5 seconds if the thermal warning or thermal shutdown conditions are present.
+
+**M122** displays the settings of most of the bits in the status register plus a couple of other items.
+
+**M906** can be used to set the KVAL\_HOLD register one driver at a time. If a setting is not included with the command then the contents of the registers that affect the phase current/voltage are displayed.
+
+**M916, M917 & M918**
+
+These utilities are used to tune the system. They can get you in the ballpark for acceptable jerk, acceleration, top speed and KVAL\_HOLD settings. In general they seem to provide an overly optimistic KVAL\_HOLD setting because of the lag between setting KVAL\_HOLD and the driver reaching final temperature. Enabling the **L6470\_monitor** feature during prints will provide the **final useful KVAL\_HOLD setting**.
+
+The amount of power needed to move the stepper without skipping steps increases as jerk, acceleration and top speed increase. The power dissipated by the driver increases as the power to the stepper increases. The net result is a balancing act between jerk, acceleration, top speed and power dissipated by the driver.
+
+**M916 -** Increases KVAL\_HOLD while moving one axis until get thermal warning. This routine is also useful for determining the approximate KVAL\_HOLD where the stepper stops losing steps. The sound will get noticeably quieter as it stops losing steps.
+
+**M917 -** Find minimum current thresholds. This is done by doing the following steps while moving an axis:
+
+1.  Decrease OCD current until overcurrent error
+
+2.  Increase OCD until overcurrent error goes away
+
+3.  Decrease stall threshold until stall error
+
+4.  Increase stall until stall error goes away
+
+**M918 -** Increase speed until error or max feedrate achieved.
