"""
i18n for language localization of the discord bot interface .
"""

from typing import Any, Callable, Dict, Optional, Union
from discord.types.snowflake import Snowflake
from googletrans import LANGCODES
from discord.enums import ComponentType
from discord.abc import Messageable

Messegable_send = Messageable.send

from discord.message import Message

Message_edit = Message.edit

from discord.http import HTTPClient

HTTPClient_send_message = HTTPClient.send_message
HTTPClient_edit_message = HTTPClient.edit_message

from discord.interactions import InteractionResponse

InteractionResponse_send_message = InteractionResponse.send_message
InteractionResponse_edit_message = InteractionResponse.edit_message

from discord.webhook.async_ import AsyncWebhookAdapter, WebhookMessage

AsyncWebhookAdapter_create_interaction_response = (
    AsyncWebhookAdapter.create_interaction_response
)
WebhookMessage_edit = WebhookMessage.edit


"""
TODO: Improper translations when dealing with send_message requests
      Specific string caching is not working properly
      Components are being translated twice
"""

from .preprocess import DetectionAgent, TranslationAgent


def i18n_localizer(lang_id: str, kwds: Dict[str, Any], content: Optional[str]):
    """
    Translates all necessary given content and UI keyword arguments with the local
    or preferential language settings.
    """
    if lang_id != LANGCODES["english"]:
        agent = TranslationAgent(lang_id)
        if content:
            content = agent.translate(content)

        if "embeds" in kwds and kwds["embeds"]:
            embeds = kwds["embeds"]
        else:
            embeds = []

        if "embed" in kwds:
            embeds.append(kwds["embed"])

        for i, template_embed in enumerate(embeds):
            if template_embed:
                embed = template_embed.copy()
                if "fields" in embed:
                    for field in embed["fields"]:
                        if field["name"].strip() and field["name"] != "\u200b":
                            field["name"] = agent.translate(field["name"])
                        if field["value"].strip() and field["value"] != "\u200b":
                            field["value"] = agent.translate(field["value"])

                if (
                    "author" in embed
                    and "name" in embed["author"]
                    and embed["author"]["name"].strip()
                ):
                    embed["author"]["name"] = agent.translate(embed["author"]["name"])

                if (
                    "footer" in embed
                    and "text" in embed["footer"]
                    and embed["footer"]["text"].strip()
                ):
                    embed["footer"]["text"] = agent.translate(embed["footer"]["text"])

                if "description" in embed and embed["description"].strip():
                    embed["description"] = agent.translate(embed["description"])

                if "title" in embed and embed["title"].strip():
                    embed["title"] = agent.translate(embed["title"])
                embeds[i] = embed

        if "components" in kwds and kwds["components"]:
            for i, template_row in enumerate(kwds["components"]):
                if template_row:
                    row = template_row.copy()
                    for item in row["components"]:
                        if item["type"] is ComponentType.button.value:
                            if item["label"]:
                                item["label"] = agent.translate(item["label"])
                    kwds["components"][i] = row
    return kwds, content


def predicate_i18n_edit(overriden: Callable):
    """
    Creates the i18n_send method for the method that is being overriden.

    The i18n_Message_edit method appends language data through the `content` field.
    The language data is intercepted and extracted in the low-level methods where
    translation occurs.

    The method is injected into `Message.edit`.

    Language detection is processed on different levels; `user`, `channel` and
    finally `guild`. For instance, if `DetectionAgent.language_of` called on a
    user id snowflake returns a valid language setting, it will proceed.
    """

    async def wrapped_i18n_edit(
        self: Union[Message, InteractionResponse], **kwds
    ) -> Message:
        dest_lang = await DetectionAgent.first_language_of(self)
        if dest_lang:
            kwds["content"] = DetectionAgent.encode_lang_str(
                kwds.get("content", None) or "", dest_lang
            )
        return await overriden(self, **kwds)

    return wrapped_i18n_edit


def i18n_HTTPClient_edit_message(
    self: HTTPClient, channel_id: Snowflake, message_id: Snowflake, **fields: Any
):
    """
    An override for `HTTPClient.edit_message` whereas it extracts extra language data
    if exists and translates accordingly.

    Language data is only appended when the recieving channel has affiliations
    with a guild.
    """
    if fields["content"]:
        content, lang_id = DetectionAgent.decode_lang_str(fields["content"])
        if lang_id:
            fields, fields["content"] = i18n_localizer(
                lang_id, fields, "".join(content)
            )
    return HTTPClient_edit_message(self, channel_id, message_id, **fields)


def predicate_i18n_send(overriden: Callable):
    """
    Creates the i18n_send method for the method that is being overriden.

    The i18n_send method appends language data through the `content` field.
    The language data is intercepted and extracted in the low-level methods where
    translation occurs.

    The method created can be injected into any high level message sending method.
    In other words, it does not affect or care at all what goes on inside the send
    function.
    """

    async def wrapped_i18n_send(
        self: Union[Messageable, InteractionResponse], content=None, *_, **kwds
    ):
        dest_lang = await DetectionAgent.first_language_of(self)
        if dest_lang:
            content = DetectionAgent.encode_lang_str(content, dest_lang)
        return await overriden(self, content, **kwds)

    return wrapped_i18n_send


def i18n_HTTPClient_send_message(
    self: HTTPClient,
    channel_id: Snowflake,
    content: Optional[str],
    *_,
    **kwds,
):
    """
    An override for `HTTPClient.send_message` whereas it extracts extra language data
    if exists and translates accordingly.

    Language data is only appended when the recieving channel has affiliations
    with a guild.
    """
    if content:
        payload, lang_id = DetectionAgent.decode_lang_str(content)
        if lang_id:
            kwds, content = i18n_localizer(lang_id, kwds, "".join(payload))
    return HTTPClient_send_message(self, channel_id, content, **kwds)


def i18n_Adapter_create_interaction_response(self: AsyncWebhookAdapter, *args, **kwds):
    """
    An override for `AsyncWebhookAdapter.create_interaction_response` whereas it
    extracts extra language data if exists and translates accordingly.

    Language data is only appended when the recieving channel has affiliations
    with a guild.
    """
    if kwds["data"] and "content" in kwds["data"]:
        content, lang_id = DetectionAgent.decode_lang_str(kwds["data"]["content"])
        if lang_id:
            kwds["data"], kwds["data"]["content"] = i18n_localizer(
                lang_id, kwds["data"], "".join(content)
            )
    return AsyncWebhookAdapter_create_interaction_response(self, *args, **kwds)


def init():
    """
    Sets initialized injectors to override any necessary high and low level methods
    that pertains to the guild based bot UI elements. Guild based bot UI elements
    includes any message sending and editing methods, views and button components (no selects).

    ### Injections
    Various high level and low level methods are overriden to realize language
    preferences and when needed, text is automatically translated.

    UI method -> `Realizes Guild Language` + `Translation` -> Discord API

    Surround your text with `\\u200b` to prevent being translated.
    This is a zero-width character and it will not affect your message output
    in any way even if you removed i18n.

    E.g. `\\u200b`report`\\u200b` can be used to avoid reperations!
    The affected methods are:
        Messegable.send

        HTTPClient.send_message
    """
    setattr(
        AsyncWebhookAdapter,
        "create_interaction_response",
        i18n_Adapter_create_interaction_response,
    )

    setattr(Messageable, "send", predicate_i18n_send(Messegable_send))
    setattr(
        InteractionResponse,
        "send_message",
        predicate_i18n_send(InteractionResponse_send_message),
    )
    setattr(HTTPClient, "send_message", i18n_HTTPClient_send_message)

    setattr(Message, "edit", predicate_i18n_edit(Message_edit))
    setattr(
        InteractionResponse,
        "edit_message",
        predicate_i18n_edit(InteractionResponse_edit_message),
    )
    setattr(WebhookMessage, "edit", predicate_i18n_edit(WebhookMessage_edit))
    setattr(HTTPClient, "edit_message", i18n_HTTPClient_edit_message)
