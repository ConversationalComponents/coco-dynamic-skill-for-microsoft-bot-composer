# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.schema import Activity, ActivityTypes, EndOfConversationCodes
from botbuilder.core import TurnContext


from coco_microsoft_bot_framework import CoCoActivityHandler


class CoCoBot(CoCoActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        print(turn_context.activity.conversation.id)
        if self.is_component_active():
            await self.call_active_component(turn_context)
            return
        else:
            self.conversation_state.active_component = turn_context.activity.value

        await self.activate_component(
            turn_context, self.conversation_state.active_component
        )

        if not self.conversation_state.active_component:
            end_of_conversation = Activity(type=ActivityTypes.end_of_conversation)
            end_of_conversation.code = EndOfConversationCodes.completed_successfully
            await turn_context.send_activity(end_of_conversation)

    async def on_end_of_conversation_activity(self, turn_context: TurnContext):
        # This will be called if the root bot is ending the conversation.  Sending additional messages should be
        # avoided as the conversation may have been deleted.
        # Perform cleanup of resources if needed.
        pass
