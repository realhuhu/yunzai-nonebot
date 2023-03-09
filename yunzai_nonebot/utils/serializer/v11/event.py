from copy import deepcopy

from yunzai_nonebot.rpc.hola_pb2 import Event
from nonebot.adapters.onebot import v11
from .parser import message_parser, sender_parser, reply_parser, anonymous_parser


async def to_v11(event: Event) -> v11.event.Event:
    event_type = event.WhichOneof("event")
    if event_type == "friend_request":
        event = event.friend_request
        return v11.FriendRequestEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="request",
            request_type="friend",
            user_id=event.user_id,
            comment=event.comment,
            flag=event.flag
        )
    if event_type == "group_request":
        event = event.group_request
        return v11.GroupRequestEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="request",
            request_type="group",
            sub_type=event.sub_type,
            group_id=event.group_id,
            user_id=event.user_id,
            comment=event.comment,
            flag=event.flag
        )
    if event_type == "PrivateMessageEvent":
        event = event.private_message
        message = await message_parser(event.message)
        return v11.PrivateMessageEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="message",
            sub_type=event.sub_type,
            user_id=event.user_id,
            message_type="private",
            message_id=event.message_id,
            message=message,
            original_message=deepcopy(message),
            raw_message=event.raw_message,
            font=0,
            sender=await sender_parser(event.sender),
            to_me=event.to_me,
            reply=None if not event.reply.time else await reply_parser(event.reply)
        )
    if event_type == "GroupMessageEvent":
        event = event.group_message
        message = await message_parser(event.message)
        return v11.GroupMessageEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="message",
            sub_type=event.sub_type,
            user_id=event.user_id,
            message_type="group",
            message_id=event.message_id,
            message=message,
            original_message=deepcopy(message),
            raw_message=event.raw_message,
            font=0,
            sender=await sender_parser(event.sender),
            to_me=event.to_me,
            reply=None if not event.reply.time else await reply_parser(event.reply),
            group_id=event.group_id,
            anonymous=None if not event.anonymous.id else await anonymous_parser(event.anonymous),
        )
    if event_type == "friend_add_notice":
        event = event.friend_add_notice
        return v11.FriendAddNoticeEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="notice",
            notice_type="friend_add",
            user_id=event.user_id
        )
    if event_type == "friend_recall_notice":
        event = event.friend_recall_notice
        return v11.FriendRecallNoticeEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="notice",
            notice_type="friend_recall",
            user_id=event.user_id,
            message_id=event.message_id,
        )
    if event_type == "group_increase_notice":
        event = event.group_increase_notice
        return v11.GroupIncreaseNoticeEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="notice",
            notice_type="group_increase",
            sub_type=event.sub_type,
            user_id=event.user_id,
            group_id=event.group_id,
            operator_id=event.operator_id
        )
    if event_type == "group_decrease_notice":
        event = event.group_decrease_notice
        return v11.GroupDecreaseNoticeEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="notice",
            notice_type="group_decrease",
            sub_type=event.sub_type,
            user_id=event.user_id,
            group_id=event.group_id,
            operator_id=event.operator_id
        )
    if event_type == "group_recall_notice":
        event = event.group_recall_notice
        return v11.GroupRecallNoticeEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="notice",
            notice_type="group_recall",
            user_id=event.user_id,
            group_id=event.group_id,
            operator_id=event.operator_id,
            message_id=event.message_id,
        )
    if event_type == "group_ban_notice":
        event = event.group_ban_notice
        return v11.GroupBanNoticeEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="notice",
            notice_type="group_ban",
            sub_type=event.sub_type,
            user_id=event.user_id,
            group_id=event.group_id,
            operator_id=event.operator_id,
            duration=event.duration
        )
    if event_type == "group_admin_notice":
        event = event.group_admin_notice
        return v11.GroupAdminNoticeEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="notice",
            notice_type="group_admin",
            sub_type=event.sub_type,
            user_id=event.user_id,
            group_id=event.group_id,
        )
    if event_type == "poke_notify":
        event = event.poke_notify
        return v11.PokeNotifyEvent(
            time=event.time,
            self_id=event.self_id,
            post_type="notice",
            notice_type="notify",
            sub_type="poke",
            user_id=event.user_id,
            target_id=event.target_id,
            group_id=event.group_id,
        )
