from pyrogram import Client , Message , Filters
from db import r
import time


# Auto Seen 
@Client.on_message(Filters.incoming & Filters.private, group=40)
def autoseen(app : Client ,msg : Message):
    chatid = str(msg.chat.id)
    if chatid in r.smembers("mark"):
        app.read_history(
            chatid
        )

@Client.on_message(Filters.me & Filters.private & Filters.regex("^[Mm]ark$") , group=41)
def addmark(app : Client ,msg : Message):
    chatid = str(msg.chat.id)
    if chatid in r.smembers("mark"):
        r.srem("mark", chatid)
        text = "This Chat Deleted from MarkList"
    else:
        r.sadd("mark", chatid)
        text = "This Chat Added to MarkList\nMark Anyway"
    send =app.edit_message_text(text=text,
            chat_id=msg.chat.id,
            message_id=msg.message_id,)     
    if r.get("autodel") == "on":
        time.sleep(float(r.get("autodeltime")))
        app.delete_messages(msg.chat.id,[send.message_id])


@Client.on_message(Filters.me & Filters.regex("^[Mm]arklist$") , group=42)
def marklist(app : Client ,msg : Message):
    marklist = r.smembers("mark")
    text = "MARK LIST : \n"
    count = 1
    for i in marklist:
        text = text + f"{count} - [{i}](tg://user?id={i})\n"
        count+=1
    app.edit_message_text(
        msg.chat.id,
        msg.message_id,
        text 
    )