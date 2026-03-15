# dragon_bot - The Personal Assistant Bot

## Installation
The dragonbot can be installed using pip.
```bash
pip install dragon-bot
```

## Description
The Personal Assistant Bot can:
1. Save contacts with names, addresses, phone numbers, emails and birthdays to the contact book.
2. Display a list of contacts whose birthday is a specified number of days from the current date.
3. Check the correctness of the entered phone number and email when creating or editing an entry and notify the user in case of incorrect entry.
4. Search for contacts among the book's contacts.
5. Edit and delete entries from the contact book.
6. Save notes with text information.
7. Search for notes
8. Edit and delete notes.
9. Add "tags" to your notes, keywords that describe the topic and subject of the entry.
10. Search and sort notes by keywords (tags).

## Usage
Start using the assistant by simply entering a console command
```bash
dragon-bot
```
You will see a prompt
```
Enter command:
```
The following commands will be available to you:

1. Add a contact    

    ```add-contact <name> <phone>```

1. Edit the name in the contact    

    ```edit-name <old_name> <new_name>```

3. Add another phone number to the contact

    ```add-phone <name> <phone>```

4. Add or change email to the contact

    ```set-email <name> <email>```

5. Add or change birthday to the contact

    ```set-birthday <name> <DD.MM.YYYY>```

6. Display the contact list on the screen

    ```all-contacts```

7. Find a contact by name

    ```find-contact <name>```

8. Display a list of contacts whose birthday is a specified number of days away from the current date

    ```birthdays <number_of_days>```

9. Delete contact's phone

    ```del-phone <name> <phone>```

10. Delete contact's email

    ```del-email <name>```

11. Delete contact's birthday

    ```del-birthday <name>```

12. Delete a contact

    ```del-contact <name>```

13. Add or change address to the contact

    ```set-address <name> <address```

14. Delete an address from the contact

    ```del-address <name>```

15. Add a note

    ```add-note <Any_note_in_quotation_marks>```

16. Edit a note

    ```edit-note <note_id> <Any_note_in_quotation_marks>```

17. Display the note list on the screen

    ```all-notes```

18. Add another a tag to the note 

    ```add-tag <note_id> <tag>```

19. Delete a tag from the note

    ```del_tag <note_id> <tag>```

20. Display the sorted note list by tags

    ```sort-notes```

21. Delete a note

    ```del-note <note_id>```

22. Display the note list on the screen by a tag

    ```find-notes-by-tag <tag>```

23. Display the note list on the screen by a keyword

    ```find-notes-by-keyword <keyword>```

24. Get help about the bot commands

    ```help```

25. Exit from program

    ```exit```
    ```quit```

## Demo Contacts

The project includes sample contacts that allow you to immediately test the bot's functionality.

The example data is located in:

```example/dragon_bot_data/*.pkl```

How to use:

Clone the repository:

```git clone```

Navigate to the project folder

Copy the folder dragon_bot_data from the example directory to your home directory.

You can do it in two ways:

Option 1 — manually

Copy the folder dragon_bot_data from example and paste it into your home directory.

Option 2 — using a command

```cp -r example/dragon_bot_data ~/```

After copying, the structure in your home folder should look like this:

~/dragon_bot_data/*.pkl

Run the bot:

```python main.py```

After starting the bot, the sample contacts from contacts.pkl and notes from notes.pkl will be loaded automatically, so you can immediately test contact and note management commands.