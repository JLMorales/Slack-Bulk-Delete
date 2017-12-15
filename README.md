# Slack-Bulk-Delete
Deletes files from slack using provided user access tokens and the web api.


## What you have to do first...

*Create your _tokens.py file.* This file contains access tokens belonging to your slack users in a dictionary like the following example:

```
_tokens = [
	"xoxp-1234567890-1234567890-1234567890-123abc456q",
	"xoxp-1234567890-1234567890-1234567890-987rvd456a"
]
```

That is all you have to do. 


You might get an error with the clear screen command I am pulling from the os module. I am running windows, so I use `cls`, but you might want to change it to `clear` if you run this on linux or mac. I am unsure if there is a need to use the os package to get that screen cleared on linux or mac, like I said, I did not develop this on linux or mac, so I have not tested it on those platforms yet.

## So.... How do I use it?

Hit your command line and go to the location with these files. Type bulkdelete.py and it should work its way through the access tokens you gave it and delete up to 100 files at a time from each access token in the \_tokens dict. Slack gives us 100 items per page and I am not paginating the results to keep this as simple as possible pecause my python knowledge is beginner at most and my lack of time is advanced at best. 