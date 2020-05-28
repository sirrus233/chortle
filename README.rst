Chortle
=======
IoT based chore tracking dashboard  
We designed this to leverage AWS IoT buttons and display a chart of household chores.  

When you press a button it will mark a chore (for example clean the cat box) as done  
and set a timer for the next time this chore needs to be done.


## Chore Types: ##
=====================

**Toggle**
Chores which can either be in the 'needs attention' or 'completed' status. 
Ex. You start cooking and press the button to set the "Clean the kitchen" chore to 'needs attention'

**Timer**
This is for time based chores which need to be done regularlly, when the chore is completed it simply resets the timer.
Ex. Clean the Toilet, interval: every 2 weeks.

**Flow**
This is when a chore leads to another, which will them become due after a short timer
Ex. Do Laundry flow
tasks: do laundry, move laundry to dryer, fold laundry
Do laundry, interval: weekly
Move laundry to dryer, internal :1 hour
Fold Laundry, internal 1 hour.

Notes on Chore Buttons:
We have elected to use the Amazon IoT chore buttons which have three button press types (single, double and long press), You could of course elect to use any number of IoT buttons but currently this only suppose those running through AWS.
