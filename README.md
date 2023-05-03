# Discord Birthday Bot

A simple Discord Bot which can be used to ping you and your friend's birthdays.

## Setup

1. Clone the repository
2. Paste the bot token in the `token.txt` file
3. Put the channel ID in which the bot will ping in the `owner_ch.txt` file
4. Put your Discord user ID in the `owner_id.txt` file
5. Add the birthdays in the `birthdays.json` file in the format `{"MM-DD" : "Name"}`

## Commands

- `!add <words_in_name> <full_name>` - This command adds a birthday to the dictionary. Note: The `<words_in_name>` must be a numeric value. Only administrators have the right to use this command.

    Example: `!add 02 Test Subject 06-24`

- `!remove <words_in_name> <full_name>` - This command removes a birthday from the dictionary. Note: The `<words_in_name>` must be a numeric value. Only administrators have the right to use this command.

    Example: `!remove 02 Test Subject 06-24`

- `!list` - This command lists all the birthdays in the dictionary.

- `!today` - This command tells us whose birthday is it today.
