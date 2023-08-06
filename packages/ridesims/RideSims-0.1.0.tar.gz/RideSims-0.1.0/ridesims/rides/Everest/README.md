# Everest


## Ride Set Up Instructions:

 1. Power ON the ride and reset e-stop status.
 2. Switch system mode to 'Maintenance', then open all blocks.
 3. Switch system mode to 'Normal'.
 4. From the Options panel disable 'Breakdowns'.
 5. Dispatch the first train by closing the gates and restraints.

### Add Trains to the Circuit:
 6. Switch to 'Maintenance' mode, and add a train to the circuit.
 7. Switch to 'Normal' mode, and dispatch the train newly added train.
 8. Repeat steps 6 & 7 one more time, for a total of four operating trains.
 9. Finally, open the restraints in the unload station, and dispatch said train to the loading station.
 10. Allow all trains to reach a resting state. Two trains present at the platforms, and two trains waiting outside the stations.

-------

## Ride Automation Set Up Instructions:

 1. Follow the Ride Set Up procedure (steps 1-10).
 2. Set the queue to 'Open' with the standby queue selected.
 3. Run the `ridesims` command in the terminal, then enter "everest" as the ride name you would like to start simulating.
 4. You will be prompted with a 10 second count down. Navigate to the simulator in your browser, and click in the active window to prepare before the automated sequence begins. (Optionally, you may also enter full screen mode.)


## Stopping Execution:

 To stop the execution of the automated script at anytime, navigate to the terminal and press Control + C twice (or until logging from the script ceases).

----

## Notes:

 This simulator requires that the trains be serviced periodically (typically every 2 hours or so). When this needs performed the MECH panel will begin to flash, and the train health bars will appear empty under the MECH panel.

 To resolve this, simply switch the ride to 'Maintenance' mode, and remove the trains from the circuit. Once in the mech bay the trains will slowly recover their health, and once full can be re-added to the ride circuit. (Remember: The circuit requires 4 trains total to operate properly.)

 Upon completion, the ride can re-enter 'Normal' system mode, and the automated sequence can be re-activated as described above.

----

## Keyboard Commands:

![keyboard commands screenshot](everest-keyboard-commands.png)

----
