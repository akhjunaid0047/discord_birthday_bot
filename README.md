# Discord birthday bot

A simple Discord Bot which can be used to ping you your friend's birthday

The owner_ch.txt file which will have the channel id in which the bot will ping

The owner_id.txt file which will have your discord user id

The birthdays.json file which will have the birthdays in the dictionary format {"MM-DD" : "Name"}

# COMMANDS

!add <words_in_name> <full_name> <date>
        
This Command adds a birthday to the dictionary
Note:   The <words_in_name> must be a numeric value
        Only Administrators have the right to use this command.
        
Example : !add 02 Test Subject 06-24

!remove <words_in_name> <full_name> <date>

This Command removes a birthday from the dictionary     
Note:   The <words_in_name> must be a numeric value
        Only Administrators have the right to use this command.
        
Example : !remove 02 Test Subject 06-24

!list
        
This Command lists all the birthdays in the dictionary

!today

Tells us whose birthday is it today.

