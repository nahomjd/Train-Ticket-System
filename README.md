# Train-Ticket-System

Relational Schema:
![ticketsRS](https://user-images.githubusercontent.com/27834881/78067511-d8d54200-7364-11ea-916f-547d44d3d0cc.PNG)

Login:

![image](https://user-images.githubusercontent.com/27834881/80921759-43074b00-8d46-11ea-8635-528fa45ca8e6.png)

Narrative:

  This project will be a flask application for a Railway System. The main application for this project for passenger booking. You will also be able to check all supporting aspects that are related to a particular trip. 
  
  A passenger will be able to input information so as to be offered tickets for train rides using the flask application. There will be three types of users: customers/passengers, booking agents, and administrators. Passengers will only be able to input information about themselves and the required info to buy a ticket. Booking agents will be able to enter information for an existing customer to book them a train ride; they will also be able to see all data in order to help passengers with potential problems. Administrators are there to create, update, and delete the Trip, Train, and TrainStations as they need to.

  This project was a challenge blending python, HTML, and SQL into working seamlessly with each other. While doing this project I learned a lot about using classes to make this project successful. Passengers, Agents, and Admins all live seamlessly in this application. Admin pages can only be accessed by Admins. Agent pages only deny passengers from accessing them. There is no access checking for passenger pages. This is because there is no reason to try and keep Admins and Agents off the pages. Also, you need to be logged in to be on any page other than login.
  
   Error handling is pretty extensive in this ticket purchasing system. It is not possible to use any IDs for any tables that do not exist. Dates are also checked, a train can not arrive before it departs. When it comes to text inputs those are checked for being blank. Also, the session is checked for inactivity to log out users that are not active. Finally, there are some other minor errors checking to make sure pages work correctly throughout the application.
  
  For the most part, this flask application came together with the majority of the functionality working correctly. However, there are a few shortfalls I will highlight in advance. Update and deleting trips, trains, and Train stations for the administrator did not come to fruition. Update trip does have a page however it does not update the database correctly, though the error checking on it works correctly. So update trip does have partial functionality. Another shortfall is that when purchasing a ticket and purchase a ticket is submitted without selecting a ticket the page is reloaded. However, once reloaded tickets won’t appear due to not being able to access the original searched information. The final shortfall is if no information is found in a search a blank table is made. With more time I would implement a “Nothing found” message. 


