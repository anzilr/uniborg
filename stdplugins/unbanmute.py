"""Restrict Users
Available Commands: .ban, .unban, .mute """
from telethon import events
import asyncio
from datetime import datetime
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

unbanned_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None
)
muted_rights = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)
banned_rights = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)



@borg.on(events.NewMessage(pattern=r"\.(ban|unban|mute) ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "ban":
        rights = banned_rights
    elif input_cmd == "unban":
        rights = unbanned_rights
    elif input_cmd == "mute":
        rights = muted_rights
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.message.id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.sender_id
    elif input_str:
        to_ban_id = input_str
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"{input_cmd}ed Successfully")
