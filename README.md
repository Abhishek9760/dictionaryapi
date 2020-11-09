# GET ALL WORDS RELATED TO A CHATID             [GET]

/api/word/?chatid=<chatid>

# GET SINGLE WORD RELATED TO A CHATID           [GET]

/api/word/?chatid=<chatid>&word=<word>

# GET MEANINGFUL OR !MEANINGFUL WORD RELATED    [GET]
# TO A CHATID
/api/word/?meaningful=<0 or 1>&chatid=<chatid>

# SAVE USER INFO TO CHATID DATABASE                   [POST]
/api/chatid/?name=<name>&username=<username>
{
    "chat_id":<int:chatid>
}

# ADD WORD TO CHAT ID                           [POST]

/api/word/?chatid=<chatid>
{
    "word": <str:word>
}

# DELETE A WORD RELATED TO A SPECIFIC CHATID    [DELETE]

/api/word/<word>/?chatid=<chatid>

# DELETE WHOLE CHATID                           [DELETE]

/api/chatid/<chatid>

