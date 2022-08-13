# Railway Management System

DEFAULT ADMIN USER = "admin" AND PASSWORD = "pass"
RUN testHelp(num of days, db) at the end of the file to fill the trainInfo table for testing purposes

After running the file u can:
1) Login - Login to an existing account
2) Sign Up - Create a new account
3) Exit - Exit the program

Each account has multiple passengers, you get presented with a table of all passengers linked to your account
You can either select a passenger to view their details, or add a new passenger by entering passenger id as -1

Each passenger can have multiple tickets, after choosing a passenger you can:
1) Ticket booking - Book a ticket for the passenger
2) Ticket checking - Check the status of a ticket
3) Ticket cancellation - Cancel a ticket
4) Delete account - Delete the account
5) Delete passenger - Delete the passenger
6) Logout - Go back to login screen
7) Exit - Exit the program

If you are to use login username as "admin" and password as "pass you get logged in as admin
Once logged in as admin you can:
1) Add train - Add a new train to the system
2) Delete train - Delete a train from the system
3) List trains - List all the trains in the system
4) Add admin - Add a new admin to the system
5) List users - List all the users in the system
6) Select user - Use the program as though logged in as the specified user, essentially sudo'ing in as that particular chosen user
7) Exit - Exit the program


-----------------------------------------------------------------------------------------------------------------------

[]: # Language: python
[]: # Path: main.py