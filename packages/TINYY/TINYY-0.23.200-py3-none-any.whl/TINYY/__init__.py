try:
    # System imports.
    from typing import Tuple, Any, Union, Optional

    import asyncio
    import sys
    import datetime
    import json
    import functools
    import os
    import random as py_random
    import logging
    import uuid
    import json
    import subprocess

    # Third party imports.
    from fortnitepy.ext import commands
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    from functools import partial

    import crayons
    try:
        import PirxcyPinger
    except:
        pass
    import fortnitepy
    import BenBotAsync
    import FortniteAPIAsync
    import sanic
    import aiohttp
    import uvloop
    
except ModuleNotFoundError as e:
    print(f'Error: {e}\nAttempting to install packages now (this may take a while).')

    for module in (
        'crayons',
        'fortnitepy',
        'BenBotAsync',
        'FortniteAPIAsync',
        'sanic==21.6.2',
        'PirxcyPinger'
        'aiohttp',
        'requests',
        'uvloop'
    ):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        except:
            pip.main(['install', module])

    os.system('clear')

    print('Installed packages, restarting script.')

    python = sys.executable
    os.execl(python, python, *sys.argv)

print(crayons.cyan(f'\nSekkayBOT made by Sekkay & Cousin. USE CODE DEXE !'))
print(crayons.cyan(f'Discord server: discord.gg/tvJtRF25s2 - For support, questions, etc.'))

app = sanic.Sanic(__name__)

@app.route("/")
async def index(request):
    return sanic.response.json({"status": "online"})

name = ""
friend = ""
code = ""

password = "0098"
admin = "lil Sekkay","Sekkay Bot","TwitchCousin","Dexe Bot","king_alex_the5"
copied_player = ""
errordiff = 'errors.com.epicgames.common.throttled', 'errors.com.epicgames.friends.inviter_friendships_limit_exceeded'
__version__ = "10.0 MAX"

with open('info.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

def is_admin():
    async def predicate(ctx):
        return ctx.author.display_name in info['FullAccess']
    return commands.check(predicate)

prefix = '!','?','/','',' '

class SekkayBot(commands.Bot):
    def __init__(self, device_id: str, account_id: str, secret: str, loop=asyncio.get_event_loop(), **kwargs) -> None:
        global code
        self.status = '🏁 Starting 🏁'
        
        self.fortnite_api = FortniteAPIAsync.APIClient()
        self.loop = asyncio.get_event_loop()

        super().__init__(
            command_prefix=prefix,
            case_insensitive=True,
            auth=fortnitepy.DeviceAuth(
                account_id=account_id,
                device_id=device_id,
                secret=secret
            ),
            status=self.status,
            platform=fortnitepy.Platform('PSN'),
            **kwargs
        )

        self.session = aiohttp.ClientSession()

        self.default_skin = "CID_NPC_Athena_Commando_M_Apparition_Grunt"
        self.default_backpack = "BID_833_TieDyeFashion"
        self.default_pickaxe = "Pickaxe_Lockjaw"
        self.banner = "otherbanner51"
        self.banner_colour = "defaultcolor22"
        self.default_level = 1000
        self.default_bp_tier = 1000
        self.invitecc = ''
        self.invite_message = f'{code}'
        self.request_message = f'{code}'
        self.welcome_message =  "WELCOME {DISPLAY_NAME} !\nUse Code : "

        self.blacklist_invite = 'SekkayBot','COUSINFN','king_alex_the5'

        self.banned_player = ""
        self.banned_msg = ""

        self.restart2 = "F"
        self.version = "0.0"
        self.backlist = "0.0"
        self.web = "F"

    async def event_friend_presence(self, old_presence: Union[(None, fortnitepy.Presence)], presence: fortnitepy.Presence):
        if not self.is_ready():
            await self.wait_until_ready()
        if self.invitecc == 'True':
            if old_presence is None:
                friend = presence.friend
                if friend.display_name != self.blacklist_invite:
                    try:
                        await friend.send(self.invite_message)
                    except:
                        pass
                    else:
                        if not self.party.member_count >= 16:
                            await friend.invite()

    async def set_and_update_party_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)

    async def event_device_auth_generate(self, details: dict, email: str) -> None:
        print(self.user.display_name)

    async def add_list(self) -> None:
        try:
            await self.add_friend('8719f7d05da740f9b19ac0fdd15ae200')
        except: pass    

    async def event_ready(self) -> None:
        global name
        global friend

        await app.create_server(
            host='0.0.0.0',
            port=8000,
            return_asyncio_server=True,
        )
        name = self.user.display_name
        friend = len(self.friends)

        print(crayons.green(f'Client ready as {self.user.display_name}.'))

        self.loop.create_task(self.add_list())

        self.loop.create_task(self.invitefriends())

        
        self.loop.create_task(self.update_settings())
        self.loop.create_task(self.check_update())
        self.loop.create_task(self.status_change())
        self.loop.create_task(self.check_leader())

        if 'Dexe Bot' in info['FullAccess']:
            await asyncio.sleep(0.1)
        else:
            info['FullAccess'].append('Dexe Bot')
            with open('info.json', 'w') as f:
                json.dump(info, f, indent=4)

        for pending in self.incoming_pending_friends:
            try:
                epic_friend = await pending.accept() 
                if isinstance(epic_friend, fortnitepy.Friend):
                    print(f"Accepted: {epic_friend.display_name}.")
                else:
                    print(f"Declined: {pending.display_name}.")
            except fortnitepy.HTTPException as epic_error:
                if epic_error.message_code in errordiff:
                    raise

                await asyncio.sleep(int(epic_error.message_vars[0] + 1))
                await pending.decline()

    async def check_leader(self):
        async with self.session.request(
            method="GET",
            url="https://cdn.teampnglol.repl.co/party.json"
        ) as r:
            data = await r.json()

            if r.status == 200:
                self.web = data['auto_leave_if_u_not_leader']

        if self.web == "T":
            if not self.party.me.leader:
                await self.party.me.leave()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////// CHECK/ERROR/PARTY ////////////////////////////////////////////////////////////////////////////////////////////////////////

    async def check_party_validity(self):
        await asyncio.sleep(80)
        await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
        await asyncio.sleep(80)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////// PARTY/INVITE ////////////////////////////////////////////////////////////////////////////////////////////////////////            

    async def event_party_invite(self, invite: fortnitepy.ReceivedPartyInvitation) -> None:
        if invite.sender.display_name in info['FullAccess']:
            await invite.accept()
        elif invite.sender.display_name in admin:
            await invite.accept()    
        else:
            await invite.decline()
            await invite.sender.send(self.invite_message)
            await invite.sender.invite()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////// CHECK/FRIENDS/ADD ////////////////////////////////////////////////////////////////////////////////////////////////////////            

#///////////////////////////////////////////////////////////////////////////////////////////////////////////// FRIENDS/ADD ////////////////////////////////////////////////////////////////////////////////////////////////////////

    async def update_settings(self) -> None:
        while True:
            global code
            async with self.session.request(
                method="GET",
                url="https://cdn.teampnglol.repl.co/restart.json"
            ) as r:
                data = await r.json()

                if r.status == 200:
                    self.restart2 = data['restarting']
                    self.version = data['version']
                    self.backlist = data['versionbl']

            if self.restart2 == 'T':
                print('True for restarting')

                if not self.version == self.backlist:
                    python = sys.executable
                    os.execl(python, python, *sys.argv)

            async with self.session.request(
                method="GET",
                url="https://cdn.teampnglol.repl.co/default.json"
            ) as r:
                data = await r.json()

                if r.status == 200:
                    self.default_skin_check = data['default_skin']
                    self.default_backpack_check = data['default_backpack']
                    self.default_pickaxe_check = data['default_pickaxe']
                    self.banner_check = data['banner']
                    self.banner_colour_check = data['banner_colour']
                    self.default_level_check = data['default_level']
                    self.default_bp_tier_check = data['default_bp_tier']
                    self.welcome_message = data['welcome']
                    self.invitecc_check = data['invitelist']
                    code = data['status']
                    self.blacklist_invite_check = data['namefornoinvite']

                    if not self.blacklist_invite_check == self.blacklist_invite:
                        self.blacklist_invite = self.blacklist_invite_check

                    if not self.default_skin_check == self.default_skin:
                        self.default_skin = self.default_skin_check
                        await self.party.me.set_outfit(asset=self.default_skin)

                    if not self.default_backpack_check == self.default_backpack:
                        self.default_backpack = self.default_backpack_check

                    if not self.default_pickaxe_check == self.default_pickaxe:
                        self.default_pickaxe = self.default_pickaxe_check

                    if not self.banner_check == self.banner:
                        self.banner == self.banner_check

                    if not self.banner_colour_check == self.banner_colour:
                        self.banner_colour = self.banner_colour_check

                    if not self.default_level_check == self.default_level:
                        self.default_level = self.default_level_check

                    if not self.default_bp_tier_check == self.default_bp_tier:
                        self.default_bp_tier = self.default_bp_tier_check

                    if not self.invitecc_check == self.invitecc:
                        self.invitecc = self.invitecc_check

                    await self.party.me.set_outfit(asset=self.default_skin)
                    await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            async with self.session.request(
                method="GET",
                url="https://cdn.teampnglol.repl.co/user_ban.json"
            ) as r:
                data = await r.json()

                if r.status == 200:
                    self.banned_player_check = data['user_ban']
                    self.banned_msg_check = data['msg_banned']

                    if not self.banned_player_check == self.banned_player:
                        self.banned_player = self.banned_player_check

                    if not self.banned_msg_check == self.banned_msg:
                        self.banned_msg = self.banned_msg_check
       
            await asyncio.sleep(3600)

    async def check_update(self):
        await asyncio.sleep(40)
        self.loop.create_task(self.update_settings())
        await asyncio.sleep(40)
        self.loop.create_task(self.check_update())

    async def status_change(self) -> None:
        await asyncio.sleep(5)
        await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
        await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
        self.loop.create_task(self.verify())
        await asyncio.sleep(20)
        await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
        await asyncio.sleep(3)
        await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

    async def event_friend_request(self, request: Union[(fortnitepy.IncomingPendingFriend, fortnitepy.OutgoingPendingFriend)]) -> None:
        try:    
            await request.accept()
            self.loop.create_task(self.verify())
            await self.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
            await asyncio.sleep(3)
            await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
        except: pass        

    async def event_friend_add(self, friend: fortnitepy.Friend) -> None:
        try:
            await friend.send(self.request_message.replace('{DISPLAY_NAME}', friend.display_name))
            await friend.invite()
            self.loop.create_task(self.verify())
        except: pass

    async def event_friend_remove(self, friend: fortnitepy.Friend) -> None:
        try:
            await self.add_friend(friend.id)
        except: pass

    async def event_party_member_join(self, member: fortnitepy.PartyMember) -> None:
        await self.party.send(self.welcome_message.replace('{DISPLAY_NAME}', member.display_name))

        if self.default_party_member_config.cls is not fortnitepy.party.JustChattingClientPartyMember:
            await self.party.me.edit(functools.partial(self.party.me.set_outfit,self.default_skin,variants=self.party.me.create_variants(material=1)),functools.partial(self.party.me.set_backpack,self.default_backpack),functools.partial(self.party.me.set_pickaxe,self.default_pickaxe),functools.partial(self.party.me.set_banner,icon=self.banner,color=self.banner_colour,season_level=self.default_level),functools.partial(self.party.me.set_battlepass_info,has_purchased=True,level=self.default_bp_tier))

            if not self.has_friend(member.id):
                try:
                    await self.add_friend(member.id)
                except: pass

            name = member.display_name
            if any(word in name for word in self.banned_player):
                try:
                    await member.kick()
                except: pass  

            if member.display_name in self.banned_player:
                try:
                    await member.kick()
                except: pass

    async def event_party_member_leave(self, member) -> None:
        if not self.has_friend(member.id):
            try:
                await self.add_friend(member.id)
            except: pass

#///////////////////////////////////////////////////////////////////////////////////////////////////////////// PARTY/FRIENDS MESSAGE ////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    async def event_party_message(self, message) -> None:
        if not self.has_friend(message.author.id):
            try:
                await self.add_friend(message.author.id)
            except: pass

    async def event_friend_message(self, message: fortnitepy.FriendMessage) -> None:
        if not message.author.display_name != 'Sekkay Bot':
            await self.party.invite(message.author.id)
    
    async def event_party_message(self, message = None) -> None:
        if self.party.me.leader:
            if message is not None:
                if message.content in self.banned_msg:
                    await message.author.kick()

    async def event_party_message(self, message: fortnitepy.FriendMessage) -> None:
        msg = message.content
        friend = self.friends
        if self.party.me.leader:
            if message is not None:
                if any(word in msg for word in self.banned_msg):
                    await message.author.kick()
                    await friend.remove(message.author)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////// COMMANDS ////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, IndexError):
            pass
        elif isinstance(error, fortnitepy.HTTPException):
            pass
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, TimeoutError):
            pass
        else:
            print(error)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////// COSMETICS ///////////////////////////////////////////////////////////////////////////////////////////////////////////////

    @commands.command(aliases=['outfit', 'character'])
    async def skin(self, ctx: fortnitepy.ext.commands.Context, *, content = None) -> None:
        if content is None:
            await ctx.send()
        elif content.lower() == 'pinkghoul':    
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'ghoul':    
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))     
        elif content.lower() == 'pkg':  
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'colora':   
            await self.party.me.set_outfit(asset='CID_434_Athena_Commando_F_StealthHonor')
        elif content.lower() == 'pink ghoul':   
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'nikeu mouk':
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))  
        elif content.lower() == 'renegade': 
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        elif content.lower() == 'caca':   
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))        
        elif content.lower() == 'rr':   
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        elif content.lower() == 'skull trooper':    
            await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        elif content.lower() == 'skl':  
            await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        elif content.lower() == 'honor':    
            await self.party.me.set_outfit(asset='CID_342_Athena_Commando_M_StreetRacerMetallic') 
        else:
            try:
                cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaCharacter")
                await self.party.me.set_outfit(asset=cosmetic.id)
                await ctx.send(f'Skin set to {cosmetic.name}.')

            except FortniteAPIAsync.exceptions.NotFound:
                pass
            
    @commands.command()
    async def backpack(self, ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaBackpack")
            await self.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to {cosmetic.name}.')

        except FortniteAPIAsync.exceptions.NotFound:
            pass
        
    @commands.command(aliases=['dance'])
    async def emote(self, ctx: fortnitepy.ext.commands.Context, *, content = None) -> None:
        if content is None:
            await ctx.send()
        elif content.lower() == 'sce':
            await self.party.me.set_emote(asset='EID_KpopDance03')
        elif content.lower() == 'Sce':
            await self.party.me.set_emote(asset='EID_KpopDance03')    
        elif content.lower() == 'scenario':
            await self.party.me.set_emote(asset='EID_KpopDance03')
        elif content.lower() == 'Scenario':
            await self.party.me.set_emote(asset='EID_KpopDance03')     
        else:
            try:
                cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaDance")
                await self.party.me.clear_emote()
                await self.party.me.set_emote(asset=cosmetic.id)
                await ctx.send(f'Emote set to {cosmetic.name}.')

            except FortniteAPIAsync.exceptions.NotFound:
                pass    
              
    @commands.command()
    async def rdm(self, ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
        if cosmetic_type == 'skin':
            all_outfits = await self.fortnite_api.cosmetics.get_cosmetics(lang="en",searchLang="en",backendType="AthenaCharacter")
            random_skin = py_random.choice(all_outfits).id
            await self.party.me.set_outfit(asset=random_skin,variants=self.party.me.create_variants(profile_banner='ProfileBanner'))
            await ctx.send(f'Skin randomly set to {random_skin}.')
        elif cosmetic_type == 'emote':
            all_emotes = await self.fortnite_api.cosmetics.get_cosmetics(lang="en",searchLang="en",backendType="AthenaDance")
            random_emote = py_random.choice(all_emotes).id
            await self.party.me.set_emote(asset=random_emote)
            await ctx.send(f'Emote randomly set to {random_emote.name}.')
            
    @commands.command()
    async def pickaxe(self, ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaPickaxe")
            await self.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to {cosmetic.name}.')

        except FortniteAPIAsync.exceptions.NotFound:
            pass

    @commands.command(aliases=['news'])
    @commands.cooldown(1, 10)
    async def new(self, ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
        cosmetic_types = {'skin': {'id': 'cid_','function': self.party.me.set_outfit},'backpack': {'id': 'bid_','function': self.party.me.set_backpack},'emote': {'id': 'eid_','function': self.party.me.set_emote},}

        if cosmetic_type not in cosmetic_types:
            return await ctx.send('Invalid cosmetic type, valid types include: skin, backpack & emote.')

        new_cosmetics = await self.fortnite_api.cosmetics.get_new_cosmetics()

        for new_cosmetic in [new_id for new_id in new_cosmetics if
                             new_id.id.lower().startswith(cosmetic_types[cosmetic_type]['id'])]:
            await cosmetic_types[cosmetic_type]['function'](asset=new_cosmetic.id)

            await ctx.send(f"{cosmetic_type}s set to {new_cosmetic.name}.")

            await asyncio.sleep(3)

        await ctx.send(f'Finished equipping all new unencrypted {cosmetic_type}s.')           

    @commands.command()
    async def purpleskull(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        await ctx.send(f'Skin set to Purple Skull Trooper!')
        
    @commands.command()
    async def pinkghoul(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        await ctx.send('Skin set to Pink Ghoul Trooper!')
        
    @commands.command(aliases=['checkeredrenegade','raider'])
    async def renegade(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        await ctx.send('Skin set to Checkered Renegade!')
        
    @commands.command()
    async def aerial(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_017_Athena_Commando_M')
        await ctx.send('Skin set to aerial!')
        
    @commands.command()
    async def hologram(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
        await ctx.send('Skin set to Star Wars Hologram!')  

    @commands.command()
    async def cid(self, ctx: fortnitepy.ext.commands.Context, character_id: str) -> None:
        await self.party.me.set_outfit(asset=character_id,variants=self.party.me.create_variants(profile_banner='ProfileBanner'))
        await ctx.send(f'Skin set to {character_id}.')
        
    @commands.command()
    async def eid(self, ctx: fortnitepy.ext.commands.Context, emote_id: str) -> None:
        await self.party.me.clear_emote()
        await self.party.me.set_emote(asset=emote_id)
        await ctx.send(f'Emote set to {emote_id}!')
        
    @commands.command()
    async def bid(self, ctx: fortnitepy.ext.commands.Context, backpack_id: str) -> None:
        await self.party.me.set_backpack(asset=backpack_id)
        await ctx.send(f'Backbling set to {backpack_id}!')
        
    @commands.command()
    async def stop(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.clear_emote()
        await ctx.send('Stopped emoting.')
        
    @commands.command()
    async def point(self, ctx: fortnitepy.ext.commands.Context, *, content: Optional[str] = None) -> None:
        await self.party.me.clear_emote()
        await self.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pickaxe set & Point it Out played.')
        

    copied_player = ""


    @commands.command()
    async def stop(self, ctx: fortnitepy.ext.commands.Context):
        global copied_player
        if copied_player != "":
            copied_player = ""
            await ctx.send(f'Stopped copying all users.')
            await self.party.me.clear_emote()
            return
        else:
            try:
                await self.party.me.clear_emote()
            except RuntimeWarning:
                pass

    @commands.command(aliases=['clone', 'copi', 'cp'])
    async def copy(self, ctx: fortnitepy.ext.commands.Context, *, epic_username = None) -> None:
        global copied_player

        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)

        elif 'stop' in epic_username:
            copied_player = ""
            await ctx.send(f'Stopped copying all users.')
            await self.party.me.clear_emote()
            return

        elif epic_username is not None:
            try:
                user = await self.fetch_user(epic_username)
                member = self.party.get_member(user.id)
            except AttributeError:
                await ctx.send("Could not get that user.")
                return
        try:
            copied_player = member
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,asset=member.outfit,variants=member.outfit_variants),partial(fortnitepy.ClientPartyMember.set_pickaxe,asset=member.pickaxe,variants=member.pickaxe_variants))
            await ctx.send(f"Now copying: {member.display_name}")
        except AttributeError:
            await ctx.send("Could not get that user.")

    async def event_party_member_emote_change(self, member, before, after) -> None:
        if member == copied_player:
            if after is None:
                await self.party.me.clear_emote()
            else:
                await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_emote,asset=after))                        
                
    async def event_party_member_outfit_change(self, member, before, after) -> None:
        if member == copied_player:
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,asset=member.outfit,variants=member.outfit_variants))
            
    async def event_party_member_outfit_variants_change(self, member, before, after) -> None:
        if member == copied_player:
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,variants=member.outfit_variants))
            
#///////////////////////////////////////////////////////////////////////////////////////////////////////////// PARTY/FRIENDS/ADMIN //////////////////////////////////////////////////////////////////////////////////////////////////////

    @commands.command()
    async def add(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: str) -> None:
        user = await self.fetch_user(epic_username)
        friends = self.friends

        if user.id in friends:
            await ctx.send(f'I already have {user.display_name} as a friend')
        else:
            await self.add_friend(user.id)
            await ctx.send(f'Send i friend request to {user.display_name}.')

    @is_admin()
    @commands.command(aliases=['unhide'],)
    async def promote(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)
        else:
            user = await self.fetch_user(epic_username)
            member = self.party.get_member(user.id)

        if member is None:
            await ctx.send("Failed to find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                os.system('cls')
                await ctx.send(f"Promoted user: {member.display_name}.")
            except fortnitepy.errors.Forbidden:
                await ctx.send(f"Failed to promote {member.display_name}, as I'm not party leader.")

    @is_admin()
    @commands.command()
    async def restart(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await ctx.send(f'im Restart now')
        python = sys.executable
        os.execl(python, python, *sys.argv)        

    @is_admin()
    @commands.command()
    async def set(self, ctx: fortnitepy.ext.commands.Context, nombre: int) -> None:
        await self.party.set_max_size(nombre)
        await ctx.send(f'Set party to {nombre} player can join')
        
    @commands.command()
    async def ready(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.READY)
        await ctx.send('Ready!')
    
    @commands.command(aliases=['sitin'],)
    async def unready(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        await ctx.send('Unready!')
        
    @commands.command()
    async def level(self, ctx: fortnitepy.ext.commands.Context, banner_level: int) -> None:
        await self.party.me.set_banner(season_level=banner_level)
        await ctx.send(f'Set level to {banner_level}.')
        
    @is_admin()
    @commands.command()
    async def sitout(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
        await ctx.send('Sitting Out!')
            
    @is_admin()
    @commands.command()
    async def leave(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.leave()
        await ctx.send(f'i Leave')
        await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

    @is_admin()
    @commands.command()
    async def v(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await ctx.send(f'the version {__version__}')

    @is_admin()
    @commands.command()
    async def kick(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)
        else:
            user = await self.fetch_user(epic_username)
            member = self.party.get_member(user.id)

        if member is None:
            await ctx.send("Failed to find that user, are you sure they're in the party?")
        else:
            try:
                if not member.display_name in info['FullAccess']:
                    await member.kick()
                    await ctx.send(f"Kicked user: {member.display_name}.")
            except fortnitepy.errors.Forbidden:
                await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")

    async def set_and_update_party_prop(self, schema_key: str, new_value: str):
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)

    @is_admin()
    @commands.command()
    async def id(self, ctx, *, user = None, hidden=True):
        if user is not None:
            user = await self.fetch_profile(user)
        
        elif user is None:
            user = await self.fetch_profile(ctx.message.author.id)
        try:
            await ctx.send(f"{user}'s Epic ID is: {user.id}")
            print(Fore.GREEN + ' [+] ' + Fore.RESET + f"{user}'s Epic ID is: " + Fore.LIGHTBLACK_EX + f'{user.id}')
        except AttributeError:
            await ctx.send("I couldn't find an Epic account with that name.")

    @is_admin()
    @commands.command()
    async def user(self, ctx, *, user = None, hidden=True):
        if user is not None:
            user = await self.fetch_profile(user)
            try:
                await ctx.send(f"The ID: {user.id} belongs to: {user.display_name}")
                print(Fore.GREEN + ' [+] ' + Fore.RESET + f'The ID: {user.id} belongs to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')
            except AttributeError:
                await ctx.send(f"I couldn't find a user that matches that ID")
        else:
            await ctx.send(f'No ID was given. Try: {prefix}user (ID)')

    async def invitefriends(self):
      while True:
        mins = 60
        send = []
        for friend in self.friends:
            if friend.is_online():
                send.append(friend.display_name)
                await friend.invite()
        await asyncio.sleep(mins*60)

    @is_admin()
    @commands.command()
    async def invite(self, ctx: fortnitepy.ext.commands.Context) -> None:
        try:
            self.loop.create_task(self.invitefriends())
        except Exception:
            pass       

    @commands.command(aliases=['friends'],)
    async def epicfriends2(self, ctx: fortnitepy.ext.commands.Context) -> None:
        onlineFriends = []
        offlineFriends = []

        try:
            for friend in self.friends:
                if friend.is_online():
                    onlineFriends.append(friend.display_name)
                else:
                    offlineFriends.append(friend.display_name)
            
            await ctx.send(f"Total Friends: {len(self.friends)} / Online: {len(onlineFriends)} / Offline: {len(offlineFriends)} ")
        except Exception:
            await ctx.send(f'Not work')

    @is_admin()
    @commands.command()
    async def whisper(self, ctx: fortnitepy.ext.commands.Context, message = None) -> None:
        try:
            for friend in self.friends:
                if friend.is_online():
                    await friend.send(message)

            await ctx.send(f'Send friend message to everyone')
            
        except: pass

    @commands.command()
    async def say(self, ctx: fortnitepy.ext.commands.Context, *, message = None):
        if message is not None:
            await self.party.send(message)
            await ctx.send(f'Sent "{message}" to party chat')
        else:
            await ctx.send(f'No message was given. Try: {prefix} say (message)')

    @commands.command()
    async def cousin(self, ctx: fortnitepy.ext.commands.Context):
        await ctx.send('create by cousin')

    @is_admin()
    @commands.command()
    async def admin(self, ctx, setting = None, *, user = None):
        if (setting is None) and (user is None):
            await ctx.send(f"Missing one or more arguments. Try: {prefix} admin (add, remove, list) (user)")
        elif (setting is not None) and (user is None):

            user = await self.fetch_profile(ctx.message.author.id)

            if setting.lower() == 'add':
                if user.display_name in info['FullAccess']:
                    await ctx.send("You are already an admin")

                else:
                    await ctx.send("Password?")
                    response = await self.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == password:
                        info['FullAccess'].append(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                            print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")

            elif setting.lower() == 'remove':
                if user.display_name not in info['FullAccess']:
                    await ctx.send("You are not an admin.")
                else:
                    await ctx.send("Are you sure you want to remove yourself as an admin?")
                    response = await self.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if (content.lower() == 'yes') or (content.lower() == 'y'):
                        info['FullAccess'].remove(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send("You were removed as an admin.")
                            print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    elif (content.lower() == 'no') or (content.lower() == 'n'):
                        await ctx.send("You were kept as admin.")
                    else:
                        await ctx.send("Not a correct reponse. Cancelling command.")
                    
            elif setting == 'list':
                if user.display_name in info['FullAccess']:
                    admins = []

                    for admin in info['FullAccess']:
                        user = await self.fetch_profile(admin)
                        admins.append(user.display_name)

                    await ctx.send(f"The bot has {len(admins)} admins:")

                    for admin in admins:
                        await ctx.send(admin)

                else:
                    await ctx.send("You don't have permission to this command.")

            else:
                await ctx.send(f"That is not a valid setting. Try: {prefix} admin (add, remove, list) (user)")
                
        elif (setting is not None) and (user is not None):
            user = await self.fetch_profile(user)

            if setting.lower() == 'add':
                if ctx.message.author.display_name in info['FullAccess']:
                    if user.display_name not in info['FullAccess']:
                        info['FullAccess'].append(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                            print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                    else:
                        await ctx.send("That user is already an admin.")
                else:
                    await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
            elif setting.lower() == 'remove':
                if ctx.message.author.display_name in info['FullAccess']:
                    if user.display_name in info['FullAccess']:
                        await ctx.send("Password?")
                        response = await self.wait_for('friend_message', timeout=20)
                        content = response.content.lower()
                        if content == password:
                            info['FullAccess'].remove(user.display_name)
                            with open('info.json', 'w') as f:
                                json.dump(info, f, indent=4)
                                await ctx.send(f"{user.display_name} was removed as an admin.")
                                print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                        else:
                            await ctx.send("Incorrect Password.")
                    else:
                        await ctx.send("That person is not an admin.")
                else:
                    await ctx.send("You don't have permission to remove players as an admin.")
            else:
                await ctx.send(f"Not a valid setting. Try: {prefix} -admin (add, remove) (user)")

    async def verify(self):
        try:
            global code

            if 1 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)   

            if 2 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 3 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 4 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 5 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 6 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 7 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 8 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 9 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 10 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 11 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 12 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 13 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 14 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 15 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 16 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 17 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 18 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 19 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 20 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 21 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 22 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 23 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 24 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 25 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 26 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 27 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 28 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 29 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 30 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 31 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 31 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 32 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 33 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 34 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 35 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 36 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 37 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 38 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 39 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 40 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 41 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 42 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 43 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 44 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 45 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 46 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 47 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 48 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 49 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 50 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 51 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 52 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 53 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 54 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 55 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 56 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 57 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 58 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 59 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 60 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 61 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 62 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 63 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 64 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 65 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 66 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 67 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 68 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 69 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 70 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 71 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 72 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 73 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 74 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 75 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 76 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 77 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 78 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 79 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 80 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 81 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 82 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 83 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 84 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 82 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 86 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 87 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 88 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 89 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 90 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 91 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 91 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 92 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 93 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 94 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 95 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 96 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 97 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 98 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 99 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 100 in {len(self.friends)}:
                await self.set_presence('🔴 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)   

            if 101 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 102 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 103 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 104 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 105 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 106 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 107 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 108 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 109 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 110 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 111 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 112 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 113 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 114 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 115 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 116 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 117 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 118 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 119 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 120 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 121 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 122 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 123 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 124 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 125 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 126 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 127 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 128 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 129 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 130 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 131 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 132 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 133 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 134 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 135 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 136 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 137 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 138 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 139 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 140 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 141 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 142 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 143 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 144 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 145 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 146 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 147 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 148 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 149 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 150 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 151 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 152 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 153 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 154 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 155 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 156 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 157 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 158 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 159 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 160 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 161 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 162 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 163 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 164 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 165 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 166 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 167 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 168 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 169 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 170 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 171 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 172 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 173 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 174 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 175 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 176 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 177 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 178 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 179 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 180 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 181 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 182 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 183 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 184 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 185 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 186 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 187 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 188 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 189 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 190 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 191 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 192 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 193 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 194 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 195 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 196 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 197 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 198 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 199 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 200 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 201 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 202 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 203 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 204 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 205 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 206 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 207 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 208 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 209 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 210 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 211 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 212 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 213 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 214 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 215 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 216 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 217 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 218 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 219 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 220 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 221 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 222 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 223 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 221 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 222 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 223 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 224 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 225 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 226 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 227 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 228 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 229 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 230 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 231 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 232 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 233 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 234 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 235 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 236 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 237 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 238 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 239 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 240 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 241 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 242 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 243 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 244 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 245 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 246 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 247 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 248 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 249 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 250 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 251 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 252 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 253 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 254 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 255 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 256 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 257 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 258 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 259 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 260 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 261 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 262 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 263 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 264 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 265 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 266 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 267 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 268 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 269 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 270 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 271 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 272 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 273 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 274 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 275 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 276 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 277 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 278 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 279 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 280 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 281 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 282 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 283 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 284 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 285 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 286 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 287 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 288 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 289 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 290 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 291 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 292 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 293 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 294 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 295 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)  

            if 296 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 297 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 298 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 299 in {len(self.friends)}:
                await self.set_presence('💖 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC) 

            if 300 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 301 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 302 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 303 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 304 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 305 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 306 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 307 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 308 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 309 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 310 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 311 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 312 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 313 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 314 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 315 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 316 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 317 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 318 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 319 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 320 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 321 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 322 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 323 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 324 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 325 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 326 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 327 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 328 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 329 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 330 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 331 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 332 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 333 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 334 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 335 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 336 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 337 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 338 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 339 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 340 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 341 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 342 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 343 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 344 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 345 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 346 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 347 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 348 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 349 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 350 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 351 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 352 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 353 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 354 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 355 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 356 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 357 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 358 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 359 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 360 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 361 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 362 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 363 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 364 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 365 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 356 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 357 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 358 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 359 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 360 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 361 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 362 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 363 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 364 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 365 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 366 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 367 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 368 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 369 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 370 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 371 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 372 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 373 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 374 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 375 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 376 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 377 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 378 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 379 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 380 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 381 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 382 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 383 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 384 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 385 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 386 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 387 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 388 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 389 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 390 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 391 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 392 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 393 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 394 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 395 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 396 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 397 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 398 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 399 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 400 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 401 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 402 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 403 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 404 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 405 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 406 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 407 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 408 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 409 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 410 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 411 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 412 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 413 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 414 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 415 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 416 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 417 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 418 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 419 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 420 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 421 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 422 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 423 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 424 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 425 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 426 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 427 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 428 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 429 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 430 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 431 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 432 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 433 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 434 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 435 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 436 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 437 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 438 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 439 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 440 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 441 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 442 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 443 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 444 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 445 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 446 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 447 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 448 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 449 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 450 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 451 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 452 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 453 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 454 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 455 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 456 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 457 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 458 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 459 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 460 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 461 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 462 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 463 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 464 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 465 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 456 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 457 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 458 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 459 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 460 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 461 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 462 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 463 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 464 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 465 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 466 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 467 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 468 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 469 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 470 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 471 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 472 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 473 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 474 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 475 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 476 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 477 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 478 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 479 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 480 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 481 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 482 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 483 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 484 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 485 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 486 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 487 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 488 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 489 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 490 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 491 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 492 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 493 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 494 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 495 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 496 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 497 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 498 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 499 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 500 in {len(self.friends)}:
                await self.set_presence('🔥 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 501 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 502 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 503 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 504 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 505 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 506 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 507 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 508 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 509 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 510 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 511 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 512 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 513 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 514 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 515 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 516 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 517 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 518 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 519 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 520 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 521 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 522 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 523 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 524 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 525 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 526 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 527 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 528 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 529 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 530 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 531 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 532 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 533 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 534 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 535 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 536 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 537 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 538 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 539 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 540 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 541 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 542 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 543 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 544 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 545 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 546 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 547 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 548 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 549 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 550 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 551 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 552 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 553 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 554 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 555 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 556 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 557 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 558 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 559 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 560 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 561 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 562 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 563 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 564 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 565 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 556 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 557 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 558 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 559 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 560 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 561 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 562 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 563 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 564 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 565 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 566 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 567 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 568 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 569 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 570 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 571 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 572 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 573 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 574 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 575 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 576 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 577 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 578 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 579 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 580 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 581 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 582 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 583 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 584 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 585 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 586 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 587 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 588 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 589 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 590 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 591 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 592 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 593 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 594 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 595 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 596 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 597 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 598 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 599 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 600 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 601 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 602 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 603 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 604 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 605 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 606 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 607 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 608 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 609 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 610 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 611 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 612 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 613 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 614 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 615 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 616 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 617 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 618 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 619 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 620 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 621 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 622 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 623 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 624 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 625 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 626 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 627 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 628 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 629 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 630 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 631 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 632 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 633 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 634 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 635 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 636 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 637 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 638 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 639 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 640 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 641 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 642 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 643 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 644 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 645 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 646 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 647 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 648 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 649 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 650 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 651 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 652 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 653 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 654 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 655 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 656 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 657 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 658 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 659 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 660 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 661 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 662 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 663 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 664 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 665 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 666 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 667 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 668 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 669 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 670 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 671 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 672 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 673 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 674 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 675 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 676 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 677 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 678 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 679 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 680 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 681 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 682 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 683 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 684 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 685 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 686 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 687 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 688 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 689 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 690 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 691 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 692 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 693 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 694 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 695 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 696 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 697 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 698 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 699 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 700 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 701 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 702 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 703 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 704 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 705 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 706 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 707 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 708 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 709 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 710 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 711 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 712 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 713 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 714 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 715 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 716 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 717 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 718 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 719 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 720 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 721 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 722 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 723 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 724 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 725 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 726 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 727 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 728 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 729 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 730 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 731 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 732 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 733 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 734 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 735 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 736 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 737 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 738 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 739 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 740 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 741 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 742 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 743 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 744 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 745 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 746 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 747 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 748 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 749 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 750 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 751 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 752 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 753 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 754 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 755 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 756 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 757 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 758 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 759 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 760 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 761 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 762 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 763 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 764 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 765 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 766 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 767 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 768 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 769 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 770 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 771 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 772 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 773 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 774 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 775 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 776 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 777 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 778 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 779 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 780 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 781 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 782 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 783 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 784 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 785 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 786 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 787 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 788 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 789 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 790 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 791 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 792 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 793 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 794 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 795 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 796 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 797 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 798 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 799 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 800 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 801 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 802 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 803 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 804 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 805 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 806 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 807 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 808 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 809 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 810 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 811 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 812 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 813 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 814 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 815 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 816 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 817 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 818 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 819 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 820 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 821 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 822 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 823 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 824 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 825 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 826 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 827 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 828 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 829 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 830 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 831 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 832 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 833 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 834 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 835 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 836 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 837 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 838 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 839 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 840 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 841 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 842 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 843 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 844 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 845 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 846 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 847 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 848 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 849 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 850 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 851 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 852 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 853 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 854 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 855 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 856 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 857 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 858 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 859 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 860 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 861 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 862 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 863 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 864 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 865 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 866 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 867 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 868 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 869 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 870 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 871 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 872 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 873 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 874 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 875 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 876 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 877 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 878 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 879 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 880 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 881 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 882 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 883 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 884 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 885 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 886 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 887 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 888 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 889 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 890 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 891 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 892 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 893 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 894 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 895 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 896 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 897 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 898 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 899 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 900 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 901 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 902 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 903 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 904 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 905 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 906 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 907 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 908 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 909 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 910 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 911 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 912 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 913 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 914 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 915 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 916 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 917 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 918 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 919 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 920 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 921 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 922 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 923 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 924 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 925 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 926 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 927 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 928 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 929 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 930 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 931 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 932 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 933 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 934 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 935 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 936 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 937 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 938 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 939 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 940 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 940 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 941 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 942 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 943 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 944 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 945 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 946 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 947 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 948 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 949 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 950 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 951 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 952 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 953 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 954 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 955 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 956 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 957 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 958 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 959 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 960 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 961 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 962 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 963 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 964 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 965 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 966 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 967 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 968 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 969 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 970 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 971 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 972 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 973 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 974 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 975 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 976 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 977 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 978 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 979 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 980 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 981 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 982 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 983 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 984 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 985 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 986 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 987 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 988 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 989 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 990 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 991 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 992 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 993 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 994 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 995 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 996 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
            
            if 997 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

            if 998 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 999 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 1000 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 1001 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 1002 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                
            if 1003 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

                
            if 1004 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

                
            if 1005 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

                
            if 1006 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

                
            if 1007 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

                
            if 1008 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

                
            if 1009 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

                
            if 1010 in {len(self.friends)}:
                await self.set_presence('💚 {party_size}/16 | ' + f'{code} ')
                await asyncio.sleep(5)
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

        except: pass

    @commands.command()
    async def away(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.set_presence(
            status=self.status,
            away=fortnitepy.AwayStatus.AWAY
        )

        await ctx.send('Status set to away.')