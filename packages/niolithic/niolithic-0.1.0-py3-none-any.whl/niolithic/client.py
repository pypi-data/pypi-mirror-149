import asyncio
import getpass
import json
import os
import sys
import traceback

from rich import print
from pathlib import Path
from markdown import markdown

from nio import (
    AsyncClient,
    AsyncClientConfig,

    KeyVerificationCancel,
    KeyVerificationEvent,
    KeyVerificationKey,
    KeyVerificationMac,
    KeyVerificationStart,
    LocalProtocolError,
    LoginResponse,
    ToDeviceError,

    MatrixRoom,
    Event,
    RoomMessageText,
)


class SimpleClient:
    def __init__(self,
            homeserver:str = None,
            user_id: str = None,
            device_name: str = None,
            app_path: str = ".",
        ):

        # Configuration options for the client
        self.client_config = AsyncClientConfig(
            max_limit_exceeded=0,
            max_timeouts=0,
            store_sync_tokens=True,
            encryption_enabled=True,
        )

        # Where all data will be stored for your app
        self.app_path = Path(app_path)
        # Paths to everything within
        self.credentials_path = self.app_path / 'credentials.json'
        self.store_path = self.app_path / 'store'

        # Make sure the directories exist
        self.store_path.mkdir(exist_ok=True)


        # Initialise Matrix client from stored credentials if available

        if self.credentials_path.exists():
            with open(self.credentials_path, 'r') as f:
                config = json.load(f)
                
                self.client = AsyncClient(
                    config['homeserver'],
                    config['user_id'],
                    device_id=config['device_id'],
                    store_path=str(self.store_path),
                    config=self.client_config,
                )

                self.client.restore_login(
                    user_id=config['user_id'],
                    device_id=config['device_id'],
                    access_token=config['access_token'],
                )

            print('[green]Logged in using stored credentials.[/green]')


        # Set up credentials if they aren't already on disk
        
        else:
            self.client = asyncio.run(self._set_up_credentials(
                homeserver,
                user_id,
                device_name
            ))

            print(
                f'[green]Successfully logged in![/green] '
                f'Credentials have been saved to disk '
                f'and will be used in future attempts to log in.'
            )

        # Add event callbacks
        self.client.add_to_device_callback(self._on_device_callback, (KeyVerificationEvent,))
        self.client.add_event_callback(self.on_message, RoomMessageText)

    
    async def _set_up_credentials(self,
            homeserver:str = None,
            user_id: str = None,
            device_name: str = None,
        ):
        """Set up credentials and client by providing
        homeserver, user ID, device name, and password.
        """

        # HOMESERVER
        if homeserver is None:
            homeserver = input('Homeserver URL: [https://matrix.example.org] ')

        if not homeserver.startswith("https://") \
        and not homeserver.startswith("http://"):
            homeserver = "https://" + homeserver

        # USER ID
        if user_id is None:
            user_id = input('User ID: [@user:example.org] ')

        # DEVICE ID
        if device_name is None:
            device_name = input('Device name: [niolithic] ')


        # Initialise the Matrix client
        client = AsyncClient(
            homeserver,
            user_id,
            store_path=str(self.store_path),
            config=self.client_config,
        )

        # Enter password and log in
        response = await client.login(
            password=getpass.getpass('Password: '),
            device_name=device_name,
        )

        # Check if it was successfully logged in
        if isinstance(response, LoginResponse):
            self._store_credentials(response, homeserver)
            return client

        else:
            raise RuntimeError(f'Failed to log in as {user_id} at {homeserver}')

    def _store_credentials(self, response: LoginResponse, homeserver: str):
        """Store login details to disk."""

        with open(self.credentials_path, 'w') as f:
            json.dump({
                'homeserver': homeserver,
                'user_id': response.user_id,
                'device_id': response.device_id,
                'access_token': response.access_token,
            }, f)


    async def _on_device_callback(self, event: object):
        """Handle and redirect every device callback sent."""

        try:
            if isinstance(event, KeyVerificationStart):
                return await self._on_key_verification_start(event)

            if isinstance(event, KeyVerificationCancel):
                return await self._on_key_verification_cancel(event)

            if isinstance(event, KeyVerificationKey):
                return await self._on_key_verification_key(event)
                
            if isinstance(event, KeyVerificationMac):
                return await self._on_key_verification_mac(event)

            print(
                f'[yellow]Received unexpected event type {type(event)}. '
                f'Event is {event}. Event will be ignored.'
            )

        except BaseException:
            print(traceback.format_exc())

    async def _on_key_verification_start(self, event: KeyVerificationStart):
        if 'emoji' not in event.short_authentication_string:
            print(
                f'[red]Other device does not support emoji verification '
                f'{event.short_authentication_string}[/red]'
            )
            return

        response = await self.client.accept_key_verification(event.transaction_id)

        if isinstance(response, ToDeviceError):
            print(f'[red]accept_key_verification failed with {response}[/red]')

        
        sas = self.client.key_verifications[event.transaction_id]
        todevice_msg = sas.share_key()
        response = await self.client.to_device(todevice_msg)

        if isinstance(response, ToDeviceError):
            print(f'[red]to_device failed with {resp}[/red]')

    async def _on_key_verification_cancel(self, event: KeyVerificationCancel):
        print(f'Verification has been cancelled by {event.sender} for reason "{event.reason}"')

    async def _on_key_verification_key(self, event: KeyVerificationKey):
        sas = self.client.key_verifications[event.transaction_id]

        # Display emojis for verification
        print('┌─ Verification Emojis')
        for emoji, name in sas.get_emoji():
            print(f'│ {emoji} {name}')
        print('└─')
        
        # Ask if they match and act accordingly
        
        print('[b]Do the emojis match?')
        print('  [[b]Y[/b]] Yes  [[b]N[/b]] No')
        print('  [[b]C[/b]] Cancel verification')

        is_match = input('> ').lower()


        # Emojis match!
        if is_match == 'y':
            print('[green]The emojis match! The verification for this device will be accepted.[/green]')

            response = await self.client.confirm_short_auth_string(event.transaction_id)

            if isinstance(response, ToDeviceError):
                print(f'[red]confirm_short_auth_string failed with {resp}[/red]')

        # Emojis do NOT match!
        elif is_match == 'y':
            print('[red]Emojis do not match. Device will not be verified.')

            response = await self.client.cancel_key_verification(event.transaction_id, reject=True)

            if isinstance(response, ToDeviceError):
                print(f'[red]cancel_key_verification failed with {resp}[/red]')

        # Cancelling verification
        else:
            print('[yellow]Verification cancelled by user.[/yellow]')

            response = await self.client.cancel_key_verification(event.transaction_id, reject=False)

            if isinstance(response, ToDeviceError):
                print(f'[red]cancel_key_verification failed with {resp}[/red]')

    async def _on_key_verification_mac(self, event: KeyVerificationMac):
        sas = self.client.key_verifications[event.transaction_id]

        try:
            todevice_msg = sas.get_mac()

        except LocalProtocol as e:
            # It might have been cancelled by ourselves
            print(
                f'Canncelled or protocol error; Reason: {e}.\n'
                f'Verification with {event.sender} was not concluded. '
                f'Try again?'
            )

        else:
            response = await self.client.to_device(todevice_msg)

            if isinstance(response, ToDeviceError):
                print(f'[red]to_device failed with {resp}[/red]')

            print(
                f'sas.we_started_it = {sas.we_started_it}\n'
                f'sas.sas_accepted = {sas.sas_accepted}\n'
                f'sas.canceled = {sas.canceled}\n'
                f'sas.timed_out = {sas.timed_out}\n'
                f'sas.verified = {sas.verified}\n'
                f'sas.verified_devices = {sas.verified_devices}\n'
            )

            print('[green]Emoji verification was successful![/green]')


    async def on_ready(self): ...

    async def on_message(self, room: MatrixRoom, event: RoomMessageText): ...
    

    async def send_text(self,
            room_id: str, body: str,
            ignore_unverified_devices: bool = True,
            render_markdown: bool = True,
        ):
        """Send regular text message to room."""

        content = {
            'msgtype': 'm.text',
            'body': body,
        }

        if render_markdown:
            content['format'] = 'org.matrix.custom.html'
            content['formatted_body'] = markdown(body)

        await self.client.room_send(
            room_id=room_id,
            message_type='m.room.message',
            content=content,
            ignore_unverified_devices=ignore_unverified_devices,
        )

    async def redact_event(self, event: Event, reason: str = None):
        """Redact event from room."""

        await self.client.room_redact(
            room_id=event.source['room_id'],
            event_id=event.source['event_id'],
            reason=reason,
        )

    async def get_messages(self, 
            room_id: str, types: tuple[type] = None,
            start: str = None, limit: int = None,
            messages_per_request: int = 50,
        ):
        """Iterate over messages in a room."""
        
        start = start or self.client.next_batch
        
        i = 0
        while True:
            # Get another 50 messages
            response = await self.client.room_messages(
                room_id=room_id,
                start=start,
                limit=messages_per_request,
            )

            # Iterate over them and yield the once that match the types
            for message in response.chunk:
                if types is None or isinstance(message, types):
                    yield message
                    i += 1

                if limit is not None and i >= limit:
                    return

            start = response.end


    async def _run(self):
        # Synchronise encryption keys with the server
        if self.client.should_upload_keys:
            await self.client.keys_upload()
        print('[green]Keys are synchronised.[/green]')

        await self.on_ready()

        await self.client.sync_forever(timeout=30_000, full_state=True)

    def run(self):
        try:
            asyncio.get_event_loop().run_until_complete(self._run())
        except KeyboardInterrupt:
            sys.exit(0)