# API Sender

Sends messages to various APIs for email or discord

``` python
from apisender import Apisender
```
```
Supported APIs:

- Discord
- Mailjet
- SMTP2GO

Todo:
- Mailgun
- Twillo (sms)
- Telnyx (sms)
```
``` python
Examples:

    fromname = "fromname"
    fromid = "from@test.com"
    subject = "test subject"
    toid = "to@test.com"
    toname = "toname"
    bodytext = "test text"
    bodyhtml = "<h1>test html</h1>"
    subject = "test subject"

    print(Apisender(fromname=fromname,
                    bodytext=bodytext).discord().text)

    print(Apisender(fromname=fromname,
                    fromid=fromid,
                    toname=toname,
                    toid=toid,
                    subject=subject,
                    bodytext=bodytext,
                    bodyhtml=bodyhtml).mailjet().text)

    print(Apisender(fromid=fromid,
                    toid=toid,
                    subject=subject,
                    bodytext=bodytext).smtp2go().text)
```

```
Notes:
    - No except checks are done for failed sending.
    - Check is done if password file is missing.
    - Requires requests to work.
    - Returns requests responses.
    - apisender.json is where you keep your passwords
```

