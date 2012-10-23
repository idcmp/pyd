A long time ago I started to keep track of my daily activities in a text file.  Eventually I broke this text
file down week-by-week.  Then I wrote a tiny shell script to launch the correct file to edit. It was called d.

Then, that shell script supported a super simple "todo" tracking system.  I would enter:

 - todo: take out the trash

 ..and after exiting the editor, the shell script would give it a unique # based on other numbers it could find

 - todo(#42): take out the trash

 ..then I wrote another shell script that would show me all the todo's in a week.  I was able to mark a todo done by:

 - done: #42 trash is gone

 .. the other shell script became smart enough to show me only todo items that weren't done.

Slowly it started to gain a few other features, such as tracking what time I unlocked my screensaver in the morning and
what time I locked it at night.  It would use this as my "in" and "out" times. A gentle reminder of how long I was at
work for.

Then, I switched jobs.  Time passed and tried different variants of the shell script.  Writing in Java, using an IRC
bot, a Jabber bot, etc, etc.  All of them were too sluggish to be usable.  If I had to wait too long, I'd start to
swap out the mental context I was in..

So, then comes Python.  It's fast enough and more structured than a shell script.

$ din <- sets the time you came in today as "now".  Will not overwrite if run more than once a day.
$ dout <- sets the time you left, *will* overwrite each time it's run
$ d <- launch the diary week text file in an editor
$ dtodo <- show all the undone things currently tracked
$ dscrum <- show all the public items you did yesterday

First, and foremost, the file this works on is a text file.  While it has some syntax, it's designed so that you
have enough wiggle room to just put whatever you want in there.

Second, the format it follows is defined in diarymodel.py.  Basically it's:

** 29-Jul (in 09:42 out 18:08)
- This is a single line activity.
+ This is a *public* single line activity.
--
This is a multilined activity.
I can write multiple lines.
Lines are cool. I write in lines now.
--
- todo: This is a todo item, which after saving, will have a # associated with it
- done: #nn   <- mark todo # nn as done
+++carriedforward <- used internally to say that information from this week has been carried into the next

We don't do timesheets at my current dayjob (we did at my last), but there is room so that carrying forward
could copy over all the in/out times in a timesheet format for whatever timesheet tool.

See the TODO for various ideas.

