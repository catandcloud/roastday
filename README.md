Yo!

This is a Python project that automatically tells the roaster how many
pounds of each coffee to roast based on the contents of the orders in 
Shipstation.

Sick.

[ Note: DON'T erase the "Roast Day Template New" file!!! ]
[ Note: This code will work on MacOSX only :-( ]

Here's how to get started using this software...

1) Install the Project
* In Finder, go to the "roastdayapp" folder
* Double click on the "setup.sh" file to run the installation script
* Once the installation script finishes running, proceed to the next step

2) Run the Application
* In Finder, go to the "roastdayapp" folder
* Double click on the "run.sh" file to run the application

3) Understand the Spreadsheet
This spreadsheet is made up of coffees and quantities. Coffees make up the rows, and various quantities make up the columns.

Here is a breakdown of the columns:
* SKU: The unique identifier for each coffee, pulled from Shipstation
* Coffee: The name of the coffee
* 10oz: The number of 10oz bags of this coffee that have been ordered (pulled from Shipstation)
* 1lb: See above...
* KILO: See above...
* 5lb: See above...
* IN STOCK: The number of pounds of this coffee currently in stock (auto-filled based on the previous day's "EOD STOCK", 			 but you can also change this on the fly if necessary)
* ROASTED LBS: The number of roasted pounds of the coffee that we need to be able to fulfill all of the orders
* GREEN LBS: How many green pounds of the coffee we need to end up with the right number of roasted pounds
* BATCHES: The number of batches that need to be roasted to end up with the right number of roasted pounds
* EOD STOCK: The total number of pounds of each coffee that we physically weigh ourselves at the end of fulfillment day (			  or before the next roast day)

The Python application works as follows:
* Pull current unfulfilled orders from the Shipstation API
* Parse each order and build a data structure of each coffee and the number of bags in the orders
* Use the previous roast file's "EOD STOCK" as the current file's "IN STOCK"
* Create a csv file of each coffee and number of bags based on "Roast Day Template New" file
* Archive the previous roast day file

In order to make sure we end up with the right amount of coffee to roast, we need to use this software in a particular way:
* At the beginning of roast day, run the app using the instructions in "2) Run the Application"
* Refer to the "Batches" column to determine how many batches of each coffee you will need to roast
* At the end of fulfillment day, weigh the total pounds of each coffee and input the "EOD STOCK" – this will become the next roast day's "IN STOCK"
* Never delete anything in the Roasting directory before asking Alex :-)
