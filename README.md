`mutt-to-things.py` is a short python script to create 
a [Things](https://culturedcode.com/things/) task from an e-mail.  As the name 
suggests, the primary use case is to offload e-mails from 
[http://mutt.org/](mutt) into Things, although it accepts any RFC 5322-compliant 
message on STDIN that python's 
[email.parser](https://docs.python.org/3/library/email.parser.html) module can 
handle.  It is the Things equivalent of 
[mutt-to-omnifocus.py](https://github.com/andrewlkho/mutt-to-omnifocus).


## Usage

Place the script somewhere in `$PATH` and then use the following in `muttrc`:

    macro index,pager \cL "<pipe-message>mutt-to-things.py<enter>" \
        "Create Things task from message"

The task is placed in the Inbox with the e-mail Subject as the task title and 
some useful headers to identify the e-mail by are in the note.  I tend to use 
the `Message-Id` header to pull up the e-mail later in mutt.

If you want to use the Quick Entry window instead (in which case the task title 
is not pre-populated) then pass `-q`.
