Chortle
=======
IoT based chore tracking dashboard  
We designed this to leverage AWS IoT buttons and display a chart of household chores.  

Chores are managed using one of three strategies:
**Modal:** this chore is either complete or open
**Periodic:** This type of chore needs to be done regularly but should not appear open until the timer is 50% complete
Ex. When you press a button it will mark a chore (for example clean the cat box) as done  
and set a timer for the next time this chore needs to be done.
**Phased** This type of chore begins a flow of necessary chores, when one is complete it opens the next chore in the series.
Ex. Do laundry  interval: 1 hour
Move Laundry to Dryer, Interval 1 hour,
Fold Laundry, Interval 2 hours.


Installation
------------
1. Download Poetry_ and NodeJS_
2. Clone the repository
3. Inside the repository top level, run :code:`poetry install`
4. Inside the app directory, run :code:`npm install`

Usage
-----
1. Start the application by running :code:`node app.js` inside the app directory.
2. Navigate to http://localhost:5000/chortle.html in a web browser.

.. _Poetry: https://python-poetry.org/ 
.. _NodeJS: https://nodejs.org/en/
