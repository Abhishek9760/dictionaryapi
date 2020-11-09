> ### GET ALL WORDS RELATED TO A CHATID _GET_
>
> - /api/word/?chatid=**chatid**
>
> ---
>
> ### GET SINGLE WORD RELATED TO A CHATID _GET_
>
> - /api/word/?chatid=**chatid**&word=**word**
>
> ---
>
> ### GET MEANINGFUL OR !MEANINGFUL WORD RELATED TO A CHATID _GET_
>
> - /api/word/?meaningful=**0 or 1**&chatid=**chatid**
>
> ---
>
> ### SAVE USER INFO TO CHATID DATABASE _POST_
>
> - /api/chatid/?name=**name**&username=**username**
> {
>    "chat_id":**chatid**
> }
>
> ---
>
> ### ADD WORD TO CHAT ID _POST_
>
> - /api/word/?chatid=**chatid**
>
>   {
>       "word": **word**
>   }
>
> ---
>
> ### DELETE A WORD RELATED TO A SPECIFIC CHATID _DELETE_
>
> - /api/word/**word**/?chatid=**chatid**
>
> ---
>
> ### DELETE WHOLE CHATID _DELETE_
>
> - /api/chatid/**chatid**
