# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.schema import Activity
from botframework.connector.auth import AuthenticationConfiguration

from bots import CoCoBot
from config import DefaultConfig
from authentication import AllowedCallersClaimsValidator
from adapter_with_error_handler import AdapterWithErrorHandler

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    MemoryStorage,
    ConversationState,
)

CONFIG = DefaultConfig()
CLAIMS_VALIDATOR = AllowedCallersClaimsValidator(CONFIG)
AUTH_CONFIG = AuthenticationConfiguration(
    claims_validator=CLAIMS_VALIDATOR.claims_validator
)
# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(
    app_id=CONFIG.APP_ID,
    app_password=CONFIG.APP_PASSWORD,
    auth_configuration=AUTH_CONFIG,
)
ADAPTER = AdapterWithErrorHandler(SETTINGS)

# Create the Bot
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
# Create the Bot
BOT = CoCoBot(CONVERSATION_STATE)


# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    try:
        await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        return Response(status=201)
    except Exception as exception:
        raise exception


async def manifest(req: Request) -> Response:
    return Response(body=open("""./wwwroot/manifest/echoskillbot-manifest-1.0.json""", "r+").read())


APP = web.Application()
APP.router.add_post("/api/messages", messages)
APP.router.add_get("/api/manifest", manifest)


if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
