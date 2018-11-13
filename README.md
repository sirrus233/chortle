Chortle
=======
A IoT based chore tracking dashboard.
Chortle is a chore management system to help households manage their regular chores using both software and hardware.
The reason we decided to use hardware is because we wanted the user experience to be as seamless as possible, you don't have to pull out your phone and open an application, you simply press a button after completing a chore.
 
After you press the button (we used the Amazon IoT button) it sends a signal to a Lambda which then resets an appropriate length timer to remind you to do another chore. We have two types of chores which can be tracked, periodic (such as water the plants once a week) or modal ( load the dishwasher, wait 1 hour then unload the dishwasher).
 
We suggest setting up a monitory, tablet, or dashboard somewhere highly visible in the household which displays the chortle website to help remind people of chores that are growing close to their due date. (it also renders nicely on mobile which means you can open it on your phone without downloading an app).
 
 Next Steps
Possible v2 iterations include adding SMS push notifications of past due chores and leveraging multiclick modes of the button to identify who completed the chore and keep metrics on household chores.
