# CAA_SBB_2023
 ## Semester project for the Cloud Advanced Analytics class, 
 ### 2023 HEC Lausanne
 
 #### Huynh Nguyen
 #### Michaela Píchová
 #### Stergios Konstantinidis

## Project Goals:
Establish a system that evalates the alcohol level in someones body. 
By relating it to their alcohol consumption preference (None, be able to drive or no limit) and their departure time, we can make sone drink recommendations.

## How it works:
We are utilizing two m5 Stacks with an RFID reader and a TV0C reader.
The RFID reader allows us to identify the user on our database (through their student card, or any RFID capable card) and the TV0C reader allows us to evaluate their current alcohol level.

We are also using a computer that runs a PyQT page where users can update their informations such as their consumption preference (None, be able to drive or no limit) or weight (usefull in order to evaluate the amount of liters of blood per individual and then the Alcohol mg/L).

Finaly we have a Colaboratory page runing an infinite loop with the function running the user identification; evaluates their alcohol level and finaly recommends drinks.

## Analytics:
1. Current alcohol level 1: We have a standard function that evaluates the alcohol level based on the TVOC sensor (through a Linear Regression fit from data where we had both the TVOC value and the true value
2. Current alcohol level 2: We have a function that evaluates the alcohol level the user should have according to the drink he drank from our system. 
3. Ultimately the maximal value between the current alcohol level 1 and the current alcohol level 2 is kept. That is not as much as for analytics as to ensure that no one would get overly affected by alcohol due to one of the metrics being wrong.
4. Reccomendation #Mifa could you write this part?
5. Post event analytics for the bar #Michaela could you write this part? We can then make the analytics or if you have time you can dig into it


## Final result:

[![Watch the video](https://img.youtube.com/vi/NsvXTMALeLc/default.jpg)](https://www.youtube.com/watch?v=NsvXTMALeLc)

## How to set it up on your own device:
1st step:
Recreate the following SQL tables on your Big querry in a project called "SBB-Project-2023" and a dataset named "projetalcohol".

2nd step:
Follow the instructions available on this video:


## Step by step code review:
### M5 stacks device:


### Jupyter notebook:

### PyQt interface:

### SQL tables:

