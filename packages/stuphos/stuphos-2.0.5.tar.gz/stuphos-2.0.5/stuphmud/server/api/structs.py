'''
Contains all of the Circle/StuphMUD structures.

'''
 #-
 # Copyright (c) 2008 Clint Banis (hereby known as "The Author")
 # All rights reserved.
 #
 # Redistribution and use in source and binary forms, with or without
 # modification, are permitted provided that the following conditions
 # are met:
 # 1. Redistributions of source code must retain the above copyright
 #    notice, this list of conditions and the following disclaimer.
 # 2. Redistributions in binary form must reproduce the above copyright
 #    notice, this list of conditions and the following disclaimer in the
 #    documentation and/or other materials provided with the distribution.
 # 3. All advertising materials mentioning features or use of this software
 #    must display the following acknowledgement:
 #        This product includes software developed by The Author, Clint Banis.
 # 4. The name of The Author may not be used to endorse or promote products
 #    derived from this software without specific prior written permission.
 #
 # THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS
 # ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 # TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 # PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS
 # BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 # CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 # SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 # INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 # CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 # ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 # POSSIBILITY OF SUCH DAMAGE.
 #

from ctypes import c_int, c_char_p, c_char, c_byte, c_ubyte, c_float
from ctypes import c_void_p, c_short, c_ushort, c_long, c_ulong
from ctypes import Structure, cast, _Pointer as PointerType
from ctypes import POINTER, CFUNCTYPE, _CFuncPtr, _FUNCFLAG_CDECL

# C Typedefs
c_time_t = c_int
c_bool = c_byte
c_size_t = c_int
c_socket_t = c_int

c_int_p = POINTER(c_int)
c_int_pp = POINTER(c_int_p)

c_char_pp = POINTER(c_char_p)

FILE_P = c_void_p

#
# This is intended for use as a void return type for cdecl convention,
# assuming that void equates to a c_int on the stack.  It seems perfectly
# reasonable to use `None` in this capacity, but that only crashes the
# interpreter.
#
# XXX `None` *should* be a valid restype!  (according to examples)
# c_void = None
#
c_void = c_int

# Standard library types
FILE = c_void_p

class TimeValue(Structure):
    _fields_ = []

TimeValue.P = POINTER(TimeValue)
c_timeval = TimeValue

# Return Value Conversion Facility
    #
    #  Is this true?
    #   [There seems to be a matter of POINTER types, even to simple
    #    ctypes data types, being invalid result types (???)]
    #

_c_default_retval = c_int
_conversion_functype_cache = {}
def AUTOFUNCTYPE(data_type, *argtypes):
    'Automatically install conversion function for pointer data type.'
    try:
        return _conversion_functype_cache[(data_type, argtypes)]
    except:
        class ConversionFunctionType(_CFuncPtr):
            _data_type_ = data_type

            _argtypes_ = argtypes
            _restype_ = _c_default_retval
            _flags_ = _FUNCFLAG_CDECL

            def __init__(self, *args, **kwd):
                _CFuncPtr.__init__(self, *args, **kwd)

                # Override the restype on the instance.
                self.restype = self.__cast_data__

                # I can't decide whether or not to implement this:
                # self.data_type = self._data_type_

            def __cast_data__(self, address):
                # The conversion routine expects an integer address.
                return cast(address, self._data_type_)

        _conversion_functype_cache[(data_type, argtypes)] = ConversionFunctionType
        return ConversionFunctionType

# MUD Typedefs
RealNumber = c_int
VirtualNumber = c_int

generic_rnum = RealNumber
generic_vnum = VirtualNumber

room_rnum = RealNumber
room_vnum = VirtualNumber

obj_rnum = RealNumber
obj_vnum = VirtualNumber

mob_rnum = RealNumber
mob_vnum = VirtualNumber

zone_rnum = RealNumber
zone_vnum = VirtualNumber

# Should we support these?
# sh_int = c_short

# Constants
MAX_INPUT_LENGTH = 256
MAX_RAW_INPUT_LENGTH = 512
SMALL_BUFSIZE = 4096
MAX_NAME_LENGTH = 20
MAX_EMAIL_LENGTH = 80

# Todo: re-cast all types that are unsigned.  I forgot that `ctypes`
# offered unsigned varities of the primitives.

# MUD Entities
class DescriptorData(Structure):
    'descriptor_data'
    HOST_LENGTH = 40

    class TxtBlock(Structure):
        'txt_block'

    TxtBlock.P = POINTER(TxtBlock)
    TxtBlock._fields_ = \
        [('text', c_char_p),
         ('aliased', c_int),
         ('next', TxtBlock.P)]

    class TxtQueue(Structure):
        'txt_q'

    TxtQueue.P = POINTER(TxtQueue)

DescriptorData.P = POINTER(DescriptorData)

DescriptorData.TxtQueue._fields_ = \
    [('head', DescriptorData.TxtBlock.P),
     ('tail', DescriptorData.TxtBlock.P)]

class TimeData(Structure):
    'time_data'

    _fields_ = \
        [('birth', c_time_t),
         ('logon', c_time_t),
         ('played', c_int)]

class CharacterData(Structure):
    'char_data'

    NUM_WEARS = 10
    MAX_COLOR_SET = 10
    MAX_PWD_LENGTH = 10

    class PlayerData(Structure):
        'char_player_data'

    class AbilityData(Structure):
        'char_ability_data'

        _fields_ = [('str', c_byte),
                    ('str_add', c_byte),
                    ('intel', c_byte),
                    ('wis', c_byte),
                    ('dex', c_byte),
                    ('con', c_byte),
                    ('cha', c_byte)]

    class PointData(Structure):
        'char_point_data'
        POINT_TYPE = c_short

        _fields_ = [('mana', POINT_TYPE),
                    ('max_mana', POINT_TYPE),
                    ('hit', POINT_TYPE),
                    ('max_hit', POINT_TYPE),
                    ('move', POINT_TYPE),
                    ('max_move', POINT_TYPE),
                    ('deaths', POINT_TYPE),
                    ('mkills', POINT_TYPE),
                    ('pkills', POINT_TYPE),
                    ('dts', POINT_TYPE),
                    ('qpoints', POINT_TYPE),
                    ('armor', POINT_TYPE),
                    ('gold', c_int),
                    ('bank_gold', c_int),
                    ('exp', c_int),
                    ('hitroll', c_byte),
                    ('damroll', c_byte)]

    class CharSpecialData(Structure):
        'char_special_data'

        class Saved(Structure):
            'char_special_data_saved'

    CharSpecialData.P = POINTER(CharSpecialData)

    class PlayerSpecialData(Structure):
        'player_special_data_saved'

        class Saved(Structure):
            'player_special_data'

            MAX_SKILLS = 200
            MAX_TONGUE = 3

        class AliasData(Structure):
            'alias_data'

        AliasData.P = POINTER(AliasData)

    PlayerSpecialData.P = POINTER(PlayerSpecialData)

    class NpcSpecialData(Structure):
        'mob_special_data'
        DICE_TYPE = c_byte

        class NpcMemoryRecord(Structure):
            'memory_rec_struct'

        class NpcActionList(Structure):
            'action_list'

    class FollowType(Structure):
        'follow_type'

    class GroupType(Structure):
        'group_type'

    class AffectedType(Structure):
        'affected_type'

    AffectedType.P = POINTER(AffectedType)

    class FileU(Structure):
        'char_file_u'

        MAX_PWD_LENGTH = 10
        MAX_AFFECT = 32
        MAX_COLOR_SET = 32

    FileU.P = POINTER(FileU)

CharacterData.P = POINTER(CharacterData)
CharacterData.PP = POINTER(CharacterData.P)

SPECIAL_TYPE = CFUNCTYPE(c_int, CharacterData.P, c_void_p, c_int, c_char_p)

class ExtraDescrData(Structure):
    'extra_descr_data'

ExtraDescrData.P = POINTER(ExtraDescrData)

ExtraDescrData._fields_ = \
    [('keyword', c_char_p),
     ('description', c_char_p),
     ('next', ExtraDescrData.P)]

class ItemData(Structure):
    'obj_data'

    class FlagData(Structure):
        'obj_flag_data'

        _fields_ = \
            [('value', c_int),
             ('type_flag', c_byte),
             ('wear_flags', c_int),
             ('extra_flags', c_int),
             ('anti_flags', c_int),
             ('weight', c_int),
             ('cost', c_int),
             ('cost_per_day', c_int),
             ('timer', c_int),
             ('trap', c_int),
             ('bitvector', c_long)]

    class AffectedType(Structure):
        'obj_affected_type'

        _fields_ = \
            [('location', c_byte),
             ('modifier', c_byte)]

    AffectedType.P = POINTER(AffectedType)

ItemData.P = POINTER(ItemData)
ItemData.PP = POINTER(ItemData.P)

class ItemRentData(Structure):
    'obj_file_elem'
    MAX_OBJ_AFFECT = 6

    _fields_ = \
        [('item_number', obj_vnum),
         ('name', c_char_p * 128),
         ('description', c_char_p * 256),
         ('short_description', c_char_p * 128),
         ('locate', c_short),
         ('value', c_int * 4),
         ('item_type', c_int),
         ('extra_flags', c_int),
         ('anti_flags', c_int),
         ('wear_flags', c_int),
         ('weight', c_int),
         ('timer', c_int),
         ('bitvector', c_long),
         ('affected', ItemData.AffectedType * MAX_OBJ_AFFECT)]

ItemRentData.P = POINTER(ItemRentData)

class RentInfo(Structure):
    'rent_info'

    _fields_ = \
        [('time', c_int),
         ('rentcode', c_int),
         ('net_cost_per_diem', c_int),
         ('gold', c_int),
         ('account', c_int),
         ('nitems', c_int),
         ('spare0', c_int),
         ('spare1', c_int),
         ('spare2', c_int),
         ('spare3', c_int),
         ('spare4', c_int),
         ('spare5', c_int),
         ('spare6', c_int),
         ('spare7', c_int)]

ItemData._fields_ = \
    [('item_number', obj_vnum),
     ('in_room', room_rnum),
     ('obj_flags', ItemData.FlagData),
     ('affected', ItemData.AffectedType),
     ('name', c_char_p),
     ('description', c_char_p),
     ('short_description', c_char_p),
     ('action_description', c_char_p),
     ('ex_description', ExtraDescrData.P),
     ('affected_by', CharacterData.AffectedType.P),
     ('carried_by', CharacterData.P),
     ('worn_by', CharacterData.P),
     ('worn_on', c_short),
     ('was_worn_on', c_short),
     ('in_obj', ItemData.P),
     ('contains', ItemData.P),
     ('next_content', ItemData.P),
     ('next', ItemData.P),
     ('tried_wear', c_bool),
     ('py_handle', c_void_p)]

CharacterData.CharSpecialData.Saved._fields_ = \
    [('alignment', c_int),
     ('idnum', c_long),
     ('act', c_long),
     ('affected_by', c_long),
     ('apply_saving_throw', c_short * 5)]

CharacterData.CharSpecialData._fields_ = \
    [('afk_message', c_char_p),
     ('fighting', CharacterData.P),
     ('hunting', CharacterData.P),
     ('wielded_by', CharacterData.P),
     ('position', c_byte),
     ('carry_weight', c_int),
     ('carry_items', c_byte),
     ('timer', c_int),
     ('arena', c_int),
     ('tracking', c_int),
     ('track_timer', c_int),
     ('saved', CharacterData.CharSpecialData.Saved)]

CharacterData.PlayerData._fields_ = \
    [('passwd', c_byte * (CharacterData.MAX_PWD_LENGTH+1)),
     ('name', c_char_p),
     ('short_descr', c_char_p),
     ('long_descr', c_char_p),
     ('description', c_char_p),
     ('title', c_char_p),
     ('nickname', c_char_p),
     ('prename', c_char_p),
     ('wizname', c_char_p),
     ('plan', c_char_p),
     ('email', c_char_p),
     ('remort', c_int),
     ('race', c_int),
     ('clan', c_int),
     ('clanrank', c_int),
     ('save_room', c_int),
     ('page_length', c_int),
     ('breath', c_int),
     ('sex', c_byte),
     ('chclass', c_byte),
     ('level', c_byte),
     ('hometown', c_int),
     ('time', TimeData),
     ('weight', c_ubyte),
     ('height', c_ubyte),
     ('login_time', c_time_t)]

class LastBuffer(Structure):
    'last_buffer'
    CHANNEL_BUFSIZE = 10

    _fields_ = \
        [('message', c_char_p),
         ('name', c_char_p),
         ('invis', c_int),
         ('when', c_time_t)]

LastBuffer.P  = POINTER(LastBuffer)
LastBuffer.PP = POINTER(LastBuffer.P)

CharacterData.PlayerSpecialData.Saved._fields_ = \
    [('skills', c_byte * (CharacterData.PlayerSpecialData.Saved.MAX_SKILLS+1)),
     ('PADDING0', c_byte),
     ('talks', c_bool * CharacterData.PlayerSpecialData.Saved.MAX_TONGUE),
     ('wimp_level', c_int),
     ('freeze_level', c_byte),
     ('invis_level', c_short),
     ('load_room', room_vnum),
     ('pref', c_long),
     ('pref2', c_long),
     ('disp', c_long),
     ('bad_pws', c_byte),
     ('conditions', c_byte * 3),
     ('spells_to_learn', c_int),
     ('marital_status', c_int),
     ('num_marriages', c_int),
     ('married_to', c_long),
     ('spell_attack', c_int * 2),
     ('remort_points', c_int)]

CharacterData.PlayerSpecialData.AliasData._fields_ = \
    [('alias', c_char_p),
     ('replacement', c_char_p),
     ('type', c_int),
     ('next', CharacterData.PlayerSpecialData.AliasData.P)]

CharacterData.PlayerSpecialData._fields_ = \
    [('saved', CharacterData.PlayerSpecialData.Saved),
     ('poofin', c_char_p),
     ('poofout', c_char_p),
     ('aliases', CharacterData.PlayerSpecialData.AliasData.P),
     ('last_tell', c_long),
     ('last_olc_targ', c_void_p),
     ('last_olc_mode', c_int),
     ('tell_buf', LastBuffer * LastBuffer.CHANNEL_BUFSIZE),
     ('ctell_buf', LastBuffer * LastBuffer.CHANNEL_BUFSIZE),
     ('wiznet_buf', LastBuffer * LastBuffer.CHANNEL_BUFSIZE),
     ('cmdlock', c_int)]

CharacterData.NpcSpecialData.NpcMemoryRecord._fields_ = \
    [('id', c_long),
     ('next', POINTER(CharacterData.NpcSpecialData.NpcMemoryRecord))]

CharacterData.NpcSpecialData.NpcActionList._fields_ = \
    [('type', c_byte),
     ('chance', c_int),
     ('spell', c_int),
     ('self', c_byte),
     ('cmd', c_char_p),
     ('next', POINTER(CharacterData.NpcSpecialData.NpcActionList))]

CharacterData.NpcSpecialData._fields_ = \
    [('last_direction', c_byte),
     ('memory', POINTER(CharacterData.NpcSpecialData.NpcMemoryRecord)),
     ('attack_type', c_int),
     ('walk_type', c_int),
     ('default_pos', c_byte),
     ('damnodice', CharacterData.NpcSpecialData.DICE_TYPE),
     ('damsizedice', CharacterData.NpcSpecialData.DICE_TYPE),
     ('gen_spec_act', POINTER(CharacterData.NpcSpecialData.NpcActionList)),
     ('timer', c_int)]

CharacterData.FollowType._fields_ = \
    [('follower', CharacterData.P),
     ('next', POINTER(CharacterData.FollowType))]

CharacterData.GroupType._fields_ = \
    [('member', CharacterData.P * 9),
     ('formation', c_int * 9)]

CharacterData.AffectedType._field_ = \
    [('type', c_short),
     ('duration', c_short),
     ('modifier', c_byte),
     ('location', c_byte),
     ('bitvector', c_long),
     ('next', CharacterData.AffectedType.P)]

CharacterData._fields_ = \
    [('pfilepos', c_int),
     ('nr', mob_rnum),
     ('in_room', room_rnum),
     ('was_in_room', room_rnum),
     ('wait', c_int),
     ('player', CharacterData.PlayerData),
     ('real_abils', CharacterData.AbilityData),
     ('aff_abils', CharacterData.AbilityData),
     ('points', CharacterData.PointData),
     ('char_specials', CharacterData.CharSpecialData),
     ('player_specials', CharacterData.PlayerSpecialData.P),
     ('mob_specials', CharacterData.NpcSpecialData),
     ('affected', POINTER(CharacterData.AffectedType)),
     ('equipment', POINTER(ItemData) * CharacterData.NUM_WEARS),
     ('color', c_int * CharacterData.MAX_COLOR_SET),
     ('carrying', POINTER(ItemData)),
     ('desc', POINTER(DescriptorData)),
     ('next_in_room', POINTER(CharacterData)),
     ('next', POINTER(CharacterData)),
     ('next_fighting', POINTER(CharacterData)),
     ('followers', POINTER(CharacterData.FollowType)),
     ('master', POINTER(CharacterData)),
     ('group', CharacterData.GroupType),
     ('holding', POINTER(CharacterData)),
     ('held_by', POINTER(CharacterData)),
     ('mount', POINTER(CharacterData)),
     ('mounted_by', POINTER(CharacterData)),
     ('py_handle', c_void_p)]

CharacterData.FileU._fields_ = \
    [('name', c_char * (MAX_NAME_LENGTH + 1)),
     ('email', c_char * (MAX_EMAIL_LENGTH + 1)),
     ('remort', c_int),
     ('race', c_int),
     ('clan', c_int),
     ('clanrank', c_int),
     ('page_length', c_int),
     ('save_room', c_int),
     ('sex', c_byte),
     ('chclass', c_byte),
     ('level', c_byte),
     ('hometown', c_short),
     ('birth', c_time_t),
     ('played', c_int),
     ('weight', c_ubyte),
     ('height', c_ubyte),
     ('pwd', c_char * (CharacterData.FileU.MAX_PWD_LENGTH + 1)),
     ('char_specials_saved', CharacterData.CharSpecialData.Saved),
     ('player_specials_saved', CharacterData.PlayerSpecialData.Saved),
     ('abilities', CharacterData.AbilityData),
     ('points', CharacterData.PointData),
     ('affected', CharacterData.AffectedType * CharacterData.FileU.MAX_AFFECT),
     ('color', c_int * CharacterData.FileU.MAX_COLOR_SET),
     ('last_login', c_time_t),
     ('last_logon', c_time_t),
     ('host', c_char * (DescriptorData.HOST_LENGTH + 1))]

class RoomData(Structure):
    'room_data'

    NUM_OF_DIRS = 6

    class DirectionData(Structure):
        'room_direction_data'

        _fields_ = \
            [('general_description', c_char_p),
             ('keyword', c_char_p),
             ('exit_info', c_long),
             ('key', obj_vnum),
             ('to_room', room_rnum)]

    DirectionData.P = POINTER(DirectionData)

RoomData.P = POINTER(RoomData)
RoomData._fields_ = \
    [('number', room_vnum),
     ('zone', zone_rnum),
     ('sector_type', c_int),
     ('name', c_char_p),
     ('description', c_char_p),
     ('ex_description', ExtraDescrData.P),
     ('dir_option', RoomData.DirectionData.P * RoomData.NUM_OF_DIRS),
     ('room_flags', c_int),
     ('affected_by', CharacterData.AffectedType.P),
     ('light', c_byte),
     ('func', SPECIAL_TYPE),
     ('contents', ItemData.P),
     ('people', CharacterData.P),
     ('py_handle', c_void_p)]

class TrustCommandInfo(Structure):
    'trust_cmd_info'

TrustCommandInfo.P = POINTER(TrustCommandInfo)
TrustCommandInfo._fields_ = \
    [('command', c_int),
     ('next', TrustCommandInfo.P)]

class AttackHitType(Structure):
    'attack_hit_type'

    _fields_ = \
        [('singular', c_char_p),
         ('plural', c_char_p)]

AttackHitType.P = POINTER(AttackHitType)

class AuctionData(Structure):
    'auction_data'

AuctionData.P = POINTER(AuctionData)
AuctionData._fields_ = \
    [('obj', ItemData.P),
     ('seller', CharacterData.P),
     ('bidder', CharacterData.P),
     ('min_bid', c_int),
     ('current_bid', c_int),
     ('timer', c_int)]

class BanListElement(Structure):
    'ban_list_element'

BanListElement.P = POINTER(BanListElement)
BanListElement._fields_ = \
    [('start_ip', c_long),
     ('end_ip', c_long),
     ('when', c_time_t),
     ('type', c_byte),
     ('by', c_byte * (MAX_NAME_LENGTH+1)),
     ('next', BanListElement.P)]

class BoardInfoType(Structure):
    'board_info_type'

    _fields_ = \
         [('vnum', obj_vnum),
          ('read_lvl', c_int),
          ('write_lvl', c_int),
          ('remove_lvl', c_int),
          ('filename', c_byte * 128),
          ('cleanup', c_int),
          ('rnum', obj_rnum)]

    class MessageInfo(Structure):
        'board_msginfo'

        _fields_ = \
             [('slot_num', c_int),
              ('heading', c_char_p),
              ('level', c_int),
              ('heading_len', c_int),
              ('message_len', c_int),
              ('birth', c_time_t)]

    MessageInfo.PP = POINTER(POINTER(MessageInfo))

BoardInfoType.P = POINTER(BoardInfoType)

class ClassInfoType(Structure):
    'class_info_type'

    _fields_ = \
        [('name', c_char_p),
         ('abbrev_color', c_char_p),
         ('abbrev_no_color', c_char_p),
         ('anti', c_long)]

ClassInfoType.P = POINTER(ClassInfoType)

class CommandInfo(Structure):
    'command_info'

    _fields_ = \
        [('command', c_char_p),
         ('minimum_position', c_byte),
         ('command_pointer', CFUNCTYPE(c_void, CharacterData.P, c_char_p, c_int, c_int)),
         ('minimum_level', c_short),
         ('subcmd', c_int)]

CommandInfo.P = POINTER(CommandInfo)

class FightMessageList(Structure):
    'message_list'

    class MessageType(Structure):
        'message_type'

        class Message(Structure):
            'msg_type'

            _fields_ = \
                [('attacker_msg', c_char_p),
                 ('victim_msg', c_char_p),
                 ('room_msg', c_char_p)]

    MessageType.P = POINTER(MessageType)
    MessageType._fields_ = \
        [('die_msg', MessageType.Message),
         ('miss_msg', MessageType.Message),
         ('hit_msg', MessageType.Message),
         ('god_msg', MessageType.Message),
         ('next', MessageType.P)]

FightMessageList.P = POINTER(FightMessageList)
FightMessageList._fields_ = \
    [('a_type', c_int),
     ('number_of_attacks', c_int),
     ('msg', FightMessageList.MessageType.P)]

class HelpEntry(Structure):
    'help_entry'

    _fields_= \
        [('keywords', c_char_p),
         ('text', c_char_p),
         ('minlevel', c_int),
         ('savefile', c_char_p)]

HelpEntry.P = POINTER(HelpEntry)

class HometownData(Structure):
    'hometown_data'

    _fields_= \
        [('name', c_char_p),
         ('start_room', c_int),
         ('low', c_int),
         ('high', c_int)]

HometownData.P = POINTER(HometownData)

class HouseControlRecord(Structure):
    'house_control_rec'
    MAX_GUESTS = 10

    _fields_= \
        [('vnum', room_vnum),
         ('atrium', room_vnum),
         ('exit_num', c_short),
         ('built_on', c_time_t),
         ('mode', c_int),
         ('owner', c_long),
         ('num_of_guests', c_int),
         ('guests', c_long * MAX_GUESTS),
         ('last_payment', c_time_t),
         ('max_item_save', c_long),
         ('spare1', c_long),
         ('spare2', c_long),
         ('spare3', c_long),
         ('spare4', c_long),
         ('spare5', c_long),
         ('spare6', c_long),
         ('spare7', c_long)]

HouseControlRecord.P = POINTER(HouseControlRecord)

class IndexData(Structure):
    'index_data'

    _fields_ = \
        [('vnum', VirtualNumber),
         ('number', c_int),
         ('func', SPECIAL_TYPE)]

IndexData.P = POINTER(IndexData)

class RaceInfoType(Structure):
    'race_info_type'

    _fields_ = \
        [('name', c_char_p),
         ('color_name', c_char_p),
         ('abbrev_color', c_char_p),
         ('abbrev_no_color', c_char_p),
         ('max_str', c_int),
         ('max_int', c_int),
         ('max_wis', c_int),
         ('max_dex', c_int),
         ('max_con', c_int),
         ('max_cha', c_int),
         ('min_remort_level', c_int),
         ('innates', c_int_p)]

RaceInfoType.P = POINTER(RaceInfoType)

class ResetQType(Structure):
    'reset_q_type'

    class Element(Structure):
        'reset_q_element'

    Element.P = POINTER(Element)
    Element._fields_ = \
        [('zone_to_reset', zone_rnum),
         ('next', POINTER(Element))]

ResetQType._fields_ = \
    [('head', ResetQType.Element.P),
     ('tail', ResetQType.Element.P)]

class ShopData(Structure):
    'shop_data'

    class BuyData(Structure):
        'shop_buy_data'

        _fields_ = \
            [('type', c_int),
             ('keywords', c_char_p)]

    BuyData.P = POINTER(BuyData)

    _fields_ = \
        [('zone', zone_vnum),
         ('vnum', room_vnum),
         ('producing', POINTER(obj_vnum)),
         ('profit_buy', c_float),
         ('profit_sell', c_float),
         ('type', BuyData.P),
         ('no_such_item1', c_char_p),
         ('no_such_item2', c_char_p),
         ('missing_cash1', c_char_p),
         ('missing_cash2', c_char_p),
         ('do_not_buy', c_char_p),
         ('message_buy', c_char_p),
         ('message_sell', c_char_p),
         ('temper1', c_int),
         ('bitvector', c_int),
         ('keeper', mob_rnum),
         ('with_who', c_int),
         ('in_room', POINTER(room_vnum)),
         ('open1', c_int),
         ('open2', c_int),
         ('close1', c_int),
         ('close2', c_int),
         ('bankAccount', c_int),
         ('goldOnHand', c_int),
         ('lastsort', c_int),
         ('func', SPECIAL_TYPE)]

ShopData.P = POINTER(ShopData)

class SocialListData(Structure):
    'social_list_data'

    class SocialData(Structure):
        'social_data'

    SocialData.P = POINTER(SocialData)
    SocialData._fields_ = \
        [('char_no_args', c_char_p),
         ('others_no_args', c_char_p),
         ('char_found', c_char_p),
         ('others_found', c_char_p),
         ('vict_found', c_char_p),
         ('not_found', c_char_p),
         ('char_auto', c_char_p),
         ('others_auto', c_char_p),
         ('next', SocialData.P)]

SocialListData.P = POINTER(SocialListData)
SocialListData._fields_ = \
    [('cmd', c_int),
     ('position', c_int),
     ('hide', c_int),
     ('socials', SocialListData.SocialData.P),
     ('next', SocialListData.P)]

class TimeInfoData(Structure):
    'time_info_data'

    _fields_ = \
        [('hours', c_int),
         ('day', c_int),
         ('month', c_int),
         ('year', c_short)]

TimeInfoData.P = POINTER(TimeInfoData)

class TitleType(Structure):
    'title_type'

    _fields_ = \
        [('title_m', c_char_p),
         ('title_f', c_char_p),
         ('exp', c_int)]

TitleType.P  = POINTER(TitleType  )
TitleType.PP = POINTER(TitleType.P)

class WeatherData(Structure):
    'weather_data'

    _fields_ = \
        [('pressure', c_int),
         ('change', c_int),
         ('sky', c_int),
         ('sunlight', c_int)]

WeatherData.P = POINTER(WeatherData)

class OlcIndexData(Structure):
    'olc_index_data'

    class OlcListData(Structure):
        'olc_list_data'

    OlcListData.P = POINTER(OlcListData)
    OlcListData._fields_ = \
        [('idnum', c_long),
         ('next', OlcListData.P)]

OlcIndexData.P = POINTER(OlcIndexData)
OlcIndexData._fields_ = [('list', OlcIndexData.OlcListData.P)]

class PlayerIndexElement(Structure):
    'player_index_element'

    _fields_ = \
        [('lvl', c_int),
         ('rname', c_char_p),
         ('name', c_char_p),
         ('id', c_long),
         ('commands', TrustCommandInfo.P)]

PlayerIndexElement.P = POINTER(PlayerIndexElement)

class MailData(Structure):
    'mail_data'

    class Recipient(Structure):
        'mail_to_data'

MailData.Recipient.P = POINTER(MailData.Recipient)
MailData.Recipient._fields_ = \
    [('idnum', c_long),
     ('next', POINTER(MailData.Recipient))]

MailData.P = POINTER(MailData)
MailData._fields_ = \
    [('from', c_char_p),
     ('subject', c_char_p),
     ('body', c_char_p),
     ('to', MailData.Recipient.P),
     ('next', MailData.P)]

class ClanInfoType(Structure):
    'clan_info_type'

    class ClanRankType(Structure):
        'clan_rank_type'
        NUM_CLAN_RANKS = 10

        _fields_ = \
            [('male', c_char_p),
             ('female', c_char_p)]

ClanInfoType.P = POINTER(ClanInfoType)
ClanInfoType._fields_= \
    [('vnum', c_int),
     ('alias', c_char_p),
     ('name', c_char_p),
     ('color_name', c_char_p),
     ('filename', c_char_p),
     ('donate_room', c_int),
     ('entrance_room', c_int),
     ('recall_room', c_int),
     ('range_low_room', c_int),
     ('range_high_room', c_int),
     ('store_object', c_int),
     ('last_updated', c_time_t),
     ('updated_by', c_long),
     ('ranks', ClanInfoType.ClanRankType * ClanInfoType.ClanRankType.NUM_CLAN_RANKS),
     ('next', ClanInfoType.P)]

class ZoneData(Structure):
    'zone_data'

    class ZCmdData(Structure):
        'reset_com'

        _fields_ = \
            [('command', c_byte),
             ('if_flag', c_bool),
             ('arg1', c_int),
             ('arg2', c_int),
             ('arg3', c_int),
             ('line', c_int)]

ZoneData.P = POINTER(ZoneData)
ZoneData._fields_ = \
    [('name', c_char_p),
     ('lifespan', c_int),
     ('age', c_int),
     ('bot', room_vnum),
     ('top', room_vnum),
     ('zone_flags', c_long),
     ('reset_mode', c_int),
     ('number', zone_vnum),
     ('cmd', POINTER(ZoneData.ZCmdData)),
     ('continent', c_int),
     ('func', SPECIAL_TYPE),
     ('py_handle', c_void_p)]

class RemortEdit(Structure):
    'RemortEdit'
    # C++ class.  Prototyped here for compatability.
    # The field data here is expressed arbitrarily
    # because the ctypes FFI code requires a sizable
    # structure on certain platforms (I think).

RemortEdit.P = POINTER(RemortEdit)

class OLCZCmdData(Structure):
    'zcmd_data'
    # Note that this is different from reset_com,
    # which is defined as a ctype in the ZoneData class.

    _fields_ = \
        [('command', c_byte),
         ('if_flag', c_bool),
         ('arg1', c_int),
         ('arg2', c_int),
         ('arg3', c_int)]

DescriptorData._fields_ = \
    [('remort', RemortEdit.P),
     ('descriptor', c_socket_t),
     ('ident_sock', c_socket_t),
     ('peer_port', c_short),
     ('network_mode', c_int),
     ('host', c_byte * (DescriptorData.HOST_LENGTH+1)),
     ('ip', c_long),
     ('port', c_short),
     ('login', c_time_t),
     ('last_host', c_byte * (DescriptorData.HOST_LENGTH+1)),
     ('bad_pws', c_byte),
     ('idle_tics', c_byte),
     ('connected', c_int),
     ('desc_num', c_int),
     ('login_time', c_time_t),
     ('command_time', c_time_t),
     ('showstr_head', c_char_p),
     ('showstr_vector', c_char_pp),
     ('showstr_count', c_int),
     ('showstr_page', c_int),
     ('showstr_point', c_char_p),
     ('showstr_start', c_char_p),
     ('str', c_char_pp),
     ('email', c_char_p),
     ('max_str', c_size_t),
     ('mail_to', c_long),
     ('mail_mode', c_int),
     ('mail', MailData.P),
     ('report', c_char_p),
     ('has_prompt', c_int),
     ('color_mode', c_int),
     ('medit_mode', c_int),
     ('oedit_mode', c_int),
     ('sedit_mode', c_int),
     ('zedit_mode', c_int),
     ('zedit_page', c_int),
     ('zedit_index', c_int),
     ('hedit_mode', c_int),
     ('cedit_mode', c_int),
     ('cedit_clan', ClanInfoType.P),
     ('olc_save_type', c_int),
     ('vt_bar_on', c_int),
     ('saved', c_int),
     ('affect_index', c_int),
     ('edit_vnum', c_int),
     ('edit_room', c_int),
     ('edit_zone', c_int),
     ('edit_clan', c_int),
     ('help_entry', c_int),
     ('redit_dir', c_int),
     ('redit_mode', c_int),
     ('exdesc', ExtraDescrData.P),
     ('prev_exdesc', ExtraDescrData.P),
     ('edit_obj', ItemData.P),
     ('edit_mob', CharacterData.P),
     ('edit_shop', ShopData.P),
     ('cmd', OLCZCmdData),
     ('olc_string', c_byte * MAX_INPUT_LENGTH),
     ('olc_int', c_int),
     ('gen_spec_act', POINTER(CharacterData.NpcSpecialData.NpcActionList)),
     ('inbuf', c_byte * MAX_RAW_INPUT_LENGTH),
     ('last_input', c_byte * MAX_INPUT_LENGTH),
     ('small_outbuf', c_byte * SMALL_BUFSIZE),
     ('history', c_char_pp),
     ('history_pos', c_int),
     ('bufptr', c_size_t),
     ('bufspace', c_size_t),
     ('large_outbuf', POINTER(DescriptorData.TxtBlock)),
     ('input', DescriptorData.TxtQueue),
     ('character', CharacterData.P),
     ('original', CharacterData.P),
     ('snooping', DescriptorData.P),
     ('snoop_by', DescriptorData.P),
     ('next', DescriptorData.P),
     ('bandwidth_in', c_long),
     ('bandwidth_out', c_long),
     ('py_handle', c_void_p),
     ('telnetOption', CFUNCTYPE(c_void, DescriptorData.P, c_byte, c_byte, c_char_p))]

class EventOperations(Structure):
    'EventOperations'
    _fields_ = \
        [('boot_start', CFUNCTYPE(c_void)),
         ('boot_complete', CFUNCTYPE(TimeValue.P)),
         ('world_reset_start', CFUNCTYPE(c_void)),
         ('world_reset_complete', CFUNCTYPE(c_void)),
         ('heartbeat_pulse', CFUNCTYPE(c_char_p, c_int)),
         ('heartbeat_timeout', CFUNCTYPE(TimeValue.P)),
         ('do_python', CFUNCTYPE(CharacterData.P, c_char_p, c_int, c_int))]
        # Unfinished

EventOperations.P = POINTER(EventOperations)

# Todo: reconfigure getvalues to use the autofunc.
class MUDOperations(Structure):
    'MUDOperations'

    _fields_ = \
       [('BankAccess'                  , CFUNCTYPE(c_int, c_int, c_int, c_int)),
        ('CAP'                         , CFUNCTYPE(c_char_p, c_char_p)),
        ('Crash_load'                  , CFUNCTYPE(c_int, CharacterData.P)),
        ('Crash_rentsave'              , CFUNCTYPE(c_int, CharacterData.P, c_int)),
        ('Crash_save_all'              , CFUNCTYPE(c_int)),
        ('FindBanTypeDesc'             , CFUNCTYPE(c_int, c_int)),
        ('House_can_enter'             , CFUNCTYPE(c_int, CharacterData.P, c_int)),
        ('House_crashsave'             , CFUNCTYPE(c_int, c_int)),
        ('House_delete_file'           , CFUNCTYPE(c_int, c_int)),
        ('House_get_filename'          , CFUNCTYPE(c_int, c_int, c_char_p, c_ulong)),
        ('House_load'                  , CFUNCTYPE(c_int, c_int)),
        ('House_save_all'              , CFUNCTYPE(c_int)),
        ('InstallStuphEventBridge'     , CFUNCTYPE(c_void, EventOperations)),
        ('IsBanned'                    , CFUNCTYPE(c_int, c_ulong)),
        ('IsBannedByHost'              , CFUNCTYPE(c_int, c_char_p)),
        ('LoadBanned'                  , CFUNCTYPE(c_int)),
        ('Obj_from_store_to'           , AUTOFUNCTYPE(ItemData.P, ItemRentData.P, c_int_p)),
        ('Obj_to_store_temp'           , CFUNCTYPE(c_int, ItemData.P, ItemRentData.P, c_int)),
        ('PyAcquireControl'            , CFUNCTYPE(c_int)),
        ('PyExecuteFile'               , CFUNCTYPE(c_int, c_char_p)),
        ('PyReleaseControl'            , CFUNCTYPE(c_int)),
        ('Py_IsInteractive'            , CFUNCTYPE(c_int)),
        ('StuphItemPrototype_Created'  , CFUNCTYPE(c_int, c_int)),
        ('StuphMobile_Extraction'      , CFUNCTYPE(c_int, CharacterData.P)),
        ('StuphPeer_QuitGame'          , CFUNCTYPE(c_int, DescriptorData.P)),
        ('StuphWorld_ResetComplete'    , CFUNCTYPE(c_int)),
        ('StuphWorld_ResetStart'       , CFUNCTYPE(c_int)),
        ('Valid_Name'                  , CFUNCTYPE(c_int, c_char_p)),
        ('add_to_dns_cache'            , CFUNCTYPE(c_int, c_ulong, c_char_p)),
        ('add_to_olc_index'            , CFUNCTYPE(c_int, c_int, c_long)),
        ('announce'                    , CFUNCTYPE(c_void, CharacterData.P, c_bool, c_char_p, c_char_p)),
        ('apply_ac'                    , CFUNCTYPE(c_int, CharacterData.P, c_int)),
        ('asciiflag_conv'              , CFUNCTYPE(c_int, c_char_p)),
        ('auction_update'              , CFUNCTYPE(c_int)),
        ('backup'                      , CFUNCTYPE(c_int)),
        ('backup_filename'             , CFUNCTYPE(c_char_p)),
        ('backup_freq'                 , CFUNCTYPE(c_int)),
        ('bad_help_entry'              , CFUNCTYPE(c_int, c_int)),
        ('basic_mud_log'               , CFUNCTYPE(c_void, c_char_p, c_char_p)),
        ('blank_profanity'             , CFUNCTYPE(c_int, c_char_p, c_char_pp)),
        ('bufcat'                      , CFUNCTYPE(c_int, c_long, c_char_p)),
        ('bufcpy'                      , CFUNCTYPE(c_int, c_long, c_char_p)),
        ('buflen'                      , CFUNCTYPE(c_int, c_long)),
        ('buildWorldPathDEBUG'         , CFUNCTYPE(c_char_p, c_char_p, c_int, c_char_p, c_char_p)),
        ('build_olc_index'             , CFUNCTYPE(c_int)),
        ('can_create_zone'             , CFUNCTYPE(c_int, c_int)),
        ('change_alignment'            , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('char_from_room'              , CFUNCTYPE(c_int, CharacterData.P)),
        ('char_to_room'                , CFUNCTYPE(c_int, CharacterData.P, c_int)),
        ('char_to_store'               , CFUNCTYPE(c_void, CharacterData.P, CharacterData.FileU.P)),
        ('check_autoassist'            , CFUNCTYPE(c_int, CharacterData.P)),
        ('check_idle_passwords'        , CFUNCTYPE(c_int)),
        ('check_subdue'                , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('cir_record_usage'            , CFUNCTYPE(c_int)),
        ('clear_char'                  , CFUNCTYPE(c_void, CharacterData.P)),
        ('command_interpreter'         , CFUNCTYPE(c_void, CharacterData.P, c_char_p)),
        ('compute_armor_class'         , CFUNCTYPE(c_int, CharacterData.P)),
        ('compute_thaco'               , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('count_hash_records'          , CFUNCTYPE(c_int, FILE_P)),
        ('create_char'                 , AUTOFUNCTYPE(CharacterData.P)),
        ('create_money'                , AUTOFUNCTYPE(ItemData.P, c_int)),
        ('damage'                      , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P, c_int, c_int)),
        ('death_cry'                   , CFUNCTYPE(c_int, CharacterData.P)),
        ('die'                         , CFUNCTYPE(c_int, CharacterData.P)),
        ('dns_cache_lookup'            , CFUNCTYPE(c_char_p, c_ulong)),
        ('do_action'                   , CFUNCTYPE(c_void, CharacterData.P, c_char_p, c_int, c_int)),
        ('do_auto_exits'               , CFUNCTYPE(c_int, CharacterData.P)),
        ('do_insult'                   , CFUNCTYPE(c_void, CharacterData.P, c_char_p, c_int, c_int)),
        ('do_start'                    , CFUNCTYPE(c_int, CharacterData.P, c_int)),
        ('drop_norents'                , CFUNCTYPE(c_int, CharacterData.P, ItemData.P)),
        ('echo_off'                    , CFUNCTYPE(c_int, DescriptorData.P)),
        ('echo_on'                     , CFUNCTYPE(c_int, DescriptorData.P)),
        ('equip_char'                  , AUTOFUNCTYPE(ItemData.P, CharacterData.P, ItemData.P, c_int, c_int)),
        ('extract_char'                , CFUNCTYPE(c_int, CharacterData.P)),
        ('extract_obj'                 , CFUNCTYPE(c_int, ItemData.P)),
        ('extract_pending_chars'       , CFUNCTYPE(c_void)),
        ('fcopy'                       , CFUNCTYPE(c_int, c_char_p, c_char_p)),
        ('find_all_dots'               , CFUNCTYPE(c_int, c_char_p)),
        ('find_exdesc'                 , CFUNCTYPE(c_char_p, c_char_p, ExtraDescrData.P)),
        ('find_first_step'             , CFUNCTYPE(c_int, c_int, c_int, c_int_p)),
        ('find_help_entry'             , CFUNCTYPE(c_int, c_char_p, c_int)),
        ('find_house'                  , CFUNCTYPE(c_int, c_int)),
        ('find_room_insert_position'   , CFUNCTYPE(c_int, c_int)),
        ('find_zone'                   , CFUNCTYPE(c_int, c_int)),
        ('find_zone_insert_position'   , CFUNCTYPE(c_int, c_int)),
        ('flush_queues'                , CFUNCTYPE(c_int, DescriptorData.P)),
        ('fname'                       , CFUNCTYPE(c_char_p, c_char_p)),
        ('fread_string'                , CFUNCTYPE(c_char_p, FILE_P, c_char_p)),
        ('free_char'                   , CFUNCTYPE(c_void, CharacterData.P)),
        ('freebuf'                     , CFUNCTYPE(c_int, c_long)),
        ('generic_find'                , CFUNCTYPE(c_int, c_char_p, c_ulong, CharacterData.P, CharacterData.PP, ItemData.PP)),
        ('gettimeofday'                , CFUNCTYPE(c_int, c_timeval.P, c_void_p)),
        ('get_bufstr'                  , CFUNCTYPE(c_char_p, c_long)),
        ('get_char_num'                , AUTOFUNCTYPE(CharacterData.P, c_int)),
        ('get_char_room_vis'           , AUTOFUNCTYPE(CharacterData.P, CharacterData.P, c_char_p, c_int_p)),
        ('get_char_world_vis'          , AUTOFUNCTYPE(CharacterData.P, CharacterData.P, c_char_p, c_int_p)),
        ('get_commands_by_id'          , AUTOFUNCTYPE(TrustCommandInfo.P, c_long)),
        ('get_filename'                , CFUNCTYPE(c_int, c_char_p, c_ulong, c_int, c_char_p)),
        ('get_from_q'                  , CFUNCTYPE(c_int, DescriptorData.TxtQueue.P, c_char_p, c_int_p)),
        ('get_hometown_by_room'        , CFUNCTYPE(c_int, c_int)),
        ('get_hostname'                , CFUNCTYPE(c_char_p, c_ulong)),
        ('get_id_by_name'              , CFUNCTYPE(c_long, c_char_p)),
        ('get_last_backup'             , CFUNCTYPE(c_int)),
        ('get_level_by_id'             , CFUNCTYPE(c_int, c_long)),
        ('get_line'                    , CFUNCTYPE(c_int, FILE_P, c_char_p)),
        ('get_mail_count'              , CFUNCTYPE(c_int, c_long, c_int)),
        ('get_name_by_id'              , CFUNCTYPE(c_char_p, c_long)),
        ('get_number'                  , CFUNCTYPE(c_int, c_char_pp)),
        ('get_obj_in_list_vis'         , AUTOFUNCTYPE(ItemData.P, CharacterData.P, c_char_p, c_int_p, ItemData.P)),
        ('get_obj_num'                 , AUTOFUNCTYPE(ItemData.P, c_int)),
        ('get_player_vis'              , AUTOFUNCTYPE(CharacterData.P, CharacterData.P, c_char_p, c_int_p, c_int, c_int)),
        ('get_ptable_by_id'            , CFUNCTYPE(c_long, c_int)),
        ('get_ptable_by_name'          , CFUNCTYPE(c_long, c_char_p)),
        ('getvalue_AGE_NOTICE'         , CFUNCTYPE(c_char_p)),
        ('getvalue_DFLT_PORT'          , CFUNCTYPE(c_int)),
        ('getvalue_EMAIL_NOTICE'       , CFUNCTYPE(c_char_p)),
        ('getvalue_MENU'               , CFUNCTYPE(c_char_p)),
        ('getvalue_PEACEFUL_MSG'       , CFUNCTYPE(c_char_p)),
        ('getvalue_START_MESSG'        , CFUNCTYPE(c_char_p)),
        ('getvalue_WELC_MESSG'         , CFUNCTYPE(c_char_p)),
        ('getvalue_WIZLOCK_MSG'        , CFUNCTYPE(c_char_p)),
        ('getvalue_player_bits'        , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_preference_bits'    , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_preference_bits2'   , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_action_bits'        , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_room_bits'          , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_extra_bits'         , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_wear_bits'          , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_affected_bits'      , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_all_start_equip'    , AUTOFUNCTYPE(c_int_p)),
        ('getvalue_apply_types'        , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_attack_hit_text'    , AUTOFUNCTYPE(AttackHitType.P)),
        ('getvalue_attack_mode_names'  , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_attack_mode_order'  , AUTOFUNCTYPE(c_int_p)),
        ('getvalue_auction'            , AUTOFUNCTYPE(AuctionData.P)),
        ('getvalue_auto_save'          , CFUNCTYPE(c_int)),
        ('getvalue_autosave_time'      , CFUNCTYPE(c_int)),
        ('getvalue_background'         , CFUNCTYPE(c_char_p)),
        ('getvalue_backups_disabled'   , CFUNCTYPE(c_int)),
        ('getvalue_ban_list'           , AUTOFUNCTYPE(BanListElement.P)),
        ('getvalue_board_info'         , AUTOFUNCTYPE(BoardInfoType.P)),
        ('getvalue_boot_time'          , CFUNCTYPE(c_int)),
        ('getvalue_buf_largecount'     , CFUNCTYPE(c_int)),
        ('getvalue_buf_overflows'      , CFUNCTYPE(c_int)),
        ('getvalue_buf_switches'       , CFUNCTYPE(c_int)),
        ('getvalue_bufpool'            , AUTOFUNCTYPE(DescriptorData.TxtBlock.P)),
        ('getvalue_bugs'               , CFUNCTYPE(c_char_p)),
        ('getvalue_channel_buffer'     , AUTOFUNCTYPE(LastBuffer.P)),
        ('getvalue_channel_buffer_names', AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_character_list'     , AUTOFUNCTYPE(CharacterData.P)),
        ('getvalue_circle_reboot'      , CFUNCTYPE(c_int)),
        ('getvalue_circle_restrict'    , CFUNCTYPE(c_int)),
        ('getvalue_circle_shutdown'    , CFUNCTYPE(c_int)),
        ('getvalue_circlemud_version'  , CFUNCTYPE(c_char_p)),
        ('getvalue_clan_help'          , CFUNCTYPE(c_char_p)),
        ('getvalue_class_count'        , AUTOFUNCTYPE(c_int_p)),
        ('getvalue_class_info'         , AUTOFUNCTYPE(ClassInfoType.P)),
        ('getvalue_class_names'        , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_cmd_info'           , AUTOFUNCTYPE(CommandInfo.P)),
        ('getvalue_cmd_sort_info'      , AUTOFUNCTYPE(c_int_p)),
        ('getvalue_combat_list'        , AUTOFUNCTYPE(CharacterData.P)),
        ('getvalue_connected_types'    , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_crash_file_timeout' , CFUNCTYPE(c_int)),
        ('getvalue_credits'            , CFUNCTYPE(c_char_p)),
        ('getvalue_dirs'               , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_donation_room_1'    , CFUNCTYPE(c_int)),
        ('getvalue_donation_room_2'    , CFUNCTYPE(c_int)),
        ('getvalue_donation_room_3'    , CFUNCTYPE(c_int)),
        ('getvalue_dts_are_dumps'      , CFUNCTYPE(c_int)),
        ('getvalue_efficiency'         , CFUNCTYPE(c_int)),
        ('getvalue_emergency_unban'    , CFUNCTYPE(c_int)),
        ('getvalue_exit_bits'          , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_fight_messages'     , AUTOFUNCTYPE(FightMessageList.P)),
        ('getvalue_free_rent'          , CFUNCTYPE(c_int)),
        ('getvalue_frozen_start_room'  , CFUNCTYPE(c_int)),
        ('getvalue_genders'            , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_generic_trash_vnum' , CFUNCTYPE(c_int)),
        ('getvalue_handbook'           , CFUNCTYPE(c_char_p)),
        ('getvalue_help'               , CFUNCTYPE(c_char_p)),
        ('getvalue_help_rename'        , CFUNCTYPE(c_char_p)),
        ('getvalue_help_table'         , AUTOFUNCTYPE(HelpEntry.P)),
        ('getvalue_holler_move_cost'   , CFUNCTYPE(c_int)),
        ('getvalue_hometown_count'     , AUTOFUNCTYPE(c_int_p)),
        ('getvalue_hometowns'          , AUTOFUNCTYPE(HometownData.P)),
        ('getvalue_house_control'      , AUTOFUNCTYPE(HouseControlRecord.P)),
        ('getvalue_ideas'              , CFUNCTYPE(c_char_p)),
        ('getvalue_idle_max_level'     , CFUNCTYPE(c_int)),
        ('getvalue_idle_rent_time'     , CFUNCTYPE(c_int)),
        ('getvalue_idle_timeout_check' , CFUNCTYPE(c_int)),
        ('getvalue_idle_void'          , CFUNCTYPE(c_int)),
        ('getvalue_immlist'            , CFUNCTYPE(c_char_p)),
        ('getvalue_immort_level_ok'    , CFUNCTYPE(c_int)),
        ('getvalue_immort_start_room'  , CFUNCTYPE(c_int)),
        ('getvalue_imotd'              , CFUNCTYPE(c_char_p)),
        ('getvalue_improve_menu'       , CFUNCTYPE(c_char_p)),
        ('getvalue_info'               , CFUNCTYPE(c_char_p)),
        ('getvalue_item_types'         , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_level_can_shout'    , CFUNCTYPE(c_int)),
        ('getvalue_loadIntoObjectIndex', CFUNCTYPE(obj_rnum)),
        ('getvalue_loadIntoZoneIndex'  , CFUNCTYPE(zone_rnum)),
        ('getvalue_load_into_inventory', CFUNCTYPE(c_int)),
        ('getvalue_log_last_cmd'       , CFUNCTYPE(c_int)),
        ('getvalue_max_aliases'        , CFUNCTYPE(c_int)),
        ('getvalue_max_bad_pws'        , CFUNCTYPE(c_int)),
        ('getvalue_max_breath_time'    , CFUNCTYPE(c_int)),
        ('getvalue_max_exp_gain'       , CFUNCTYPE(c_int)),
        ('getvalue_max_exp_loss'       , CFUNCTYPE(c_int)),
        ('getvalue_max_filesize'       , CFUNCTYPE(c_int)),
        ('getvalue_max_gold_decay_timer', CFUNCTYPE(c_int)),
        ('getvalue_max_house_save'     , CFUNCTYPE(c_int)),
        ('getvalue_max_key_time'       , CFUNCTYPE(c_int)),
        ('getvalue_max_npc_corpse_time', CFUNCTYPE(c_int)),
        ('getvalue_max_obj_save'       , CFUNCTYPE(c_int)),
        ('getvalue_max_object_decay_timer', CFUNCTYPE(c_int)),
        ('getvalue_max_pc_corpse_time' , CFUNCTYPE(c_int)),
        ('getvalue_max_pfile_boots'    , CFUNCTYPE(c_int)),
        ('getvalue_max_players'        , CFUNCTYPE(c_int)),
        ('getvalue_max_playing'        , CFUNCTYPE(c_int)),
        ('getvalue_max_spell_attacks'  , CFUNCTYPE(c_int)),
        ('getvalue_min_passwd_length'  , CFUNCTYPE(c_int)),
        ('getvalue_min_rent_cost'      , CFUNCTYPE(c_int)),
        ('getvalue_min_wizlist_lev'    , CFUNCTYPE(c_int)),
        ('getvalue_mini_mud'           , CFUNCTYPE(c_int)),
        ('getvalue_mob_index'          , AUTOFUNCTYPE(IndexData.P)),
        ('getvalue_mob_proto'          , AUTOFUNCTYPE(CharacterData.P)),
        ('getvalue_mortal_start_room'  , CFUNCTYPE(room_vnum)),
        ('getvalue_motd'               , CFUNCTYPE(c_char_p)),
        ('getvalue_msg_index'          , AUTOFUNCTYPE(BoardInfoType.MessageInfo.PP)),
        ('getvalue_msg_storage'        , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_mudlog_types'       , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_nameserver_is_slow' , CFUNCTYPE(c_int)),
        ('getvalue_newbie_ban'         , CFUNCTYPE(c_char_p)),
        ('getvalue_newbie_level'       , CFUNCTYPE(c_int)),
        ('getvalue_newbie_start_room'  , CFUNCTYPE(c_int)),
        ('getvalue_news'               , CFUNCTYPE(c_char_p)),
        ('getvalue_no_rent_check'      , CFUNCTYPE(c_int)),
        ('getvalue_no_specials'        , CFUNCTYPE(c_int)),
        ('getvalue_num_invalid'        , CFUNCTYPE(c_int)),
        ('getvalue_num_of_msgs'        , AUTOFUNCTYPE(c_int_p)),
        ('getvalue_obj_index'          , AUTOFUNCTYPE(IndexData.P)),
        ('getvalue_obj_proto'          , AUTOFUNCTYPE(ItemData.P)),
        ('getvalue_object_list'        , AUTOFUNCTYPE(ItemData.P)),
        ('getvalue_olc_index'          , AUTOFUNCTYPE(OlcIndexData.P)),
        ('getvalue_pk_allowed'         , CFUNCTYPE(c_int)),
        ('getvalue_pkok_in_peaceful_rooms', CFUNCTYPE(c_int)),
        ('getvalue_player_fl'          , CFUNCTYPE(FILE_P)),
        ('getvalue_player_table'       , AUTOFUNCTYPE(PlayerIndexElement.P)),
        ('getvalue_policies'           , CFUNCTYPE(c_char_p)),
        ('getvalue_port'               , CFUNCTYPE(c_int)),
        ('getvalue_position_types'     , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_pt_allowed'         , CFUNCTYPE(c_int)),
        ('getvalue_r_frozen_start_room', CFUNCTYPE(room_rnum)),
        ('getvalue_r_immort_start_room', CFUNCTYPE(room_rnum)),
        ('getvalue_r_mortal_start_room', CFUNCTYPE(room_rnum)),
        ('getvalue_r_newbie_start_room', CFUNCTYPE(room_rnum)),
        ('getvalue_race_desc'          , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_race_info'          , AUTOFUNCTYPE(RaceInfoType.P)),
        ('getvalue_race_names'         , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_rent_file_timeout'  , CFUNCTYPE(c_int)),
        ('getvalue_reread_wizlist'     , CFUNCTYPE(c_int)),
        ('getvalue_reset_q'            , AUTOFUNCTYPE(ResetQType)),
        ('getvalue_scheck'             , CFUNCTYPE(c_int)),
        ('getvalue_sector_types'       , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_select_ban'         , CFUNCTYPE(c_char_p)),
        ('getvalue_shop_index'         , AUTOFUNCTYPE(ShopData.P)),
        ('getvalue_shutdown_by'        , CFUNCTYPE(c_long)),
        ('getvalue_shutdown_mode'      , CFUNCTYPE(c_int)),
        ('getvalue_shutdown_modes'     , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_shutdown_timer'     , CFUNCTYPE(c_int)),
        ('getvalue_siteok_everyone'    , CFUNCTYPE(c_int)),
        ('getvalue_sky_types'          , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_social_list'        , AUTOFUNCTYPE(SocialListData.P)),
        ('getvalue_start_equip'        , AUTOFUNCTYPE(c_int_p)),
        ('getvalue_sun_types'          , AUTOFUNCTYPE(c_char_pp)),
        ('getvalue_tics'               , CFUNCTYPE(c_int)),
        ('getvalue_time_info'          , AUTOFUNCTYPE(TimeInfoData)),
        ('getvalue_title_screen'       , CFUNCTYPE(c_char_p)),
        ('getvalue_titles'             , AUTOFUNCTYPE(TitleType.PP)),
        ('getvalue_top_of_mobt'        , CFUNCTYPE(c_int)),
        ('getvalue_top_of_objt'        , CFUNCTYPE(c_int)),
        ('getvalue_top_of_p_table'     , CFUNCTYPE(c_int)),
        ('getvalue_top_of_world'       , CFUNCTYPE(c_int)),
        ('getvalue_top_of_zone_table'  , CFUNCTYPE(c_int)),
        ('getvalue_top_shop'           , CFUNCTYPE(c_int)),
        ('getvalue_total_ban'          , CFUNCTYPE(c_char_p)),
        ('getvalue_track_through_doors', CFUNCTYPE(c_int)),
        ('getvalue_tunnel_size'        , CFUNCTYPE(c_int)),
        ('getvalue_typos'              , CFUNCTYPE(c_char_p)),
        ('getvalue_use_autowiz'        , CFUNCTYPE(c_int)),
        ('getvalue_use_dns_cache'      , CFUNCTYPE(c_int)),
        ('getvalue_usec_spent_per_sec' , CFUNCTYPE(c_int)),
        ('getvalue_wear_sort_pos'      , AUTOFUNCTYPE(c_int_p)),
        ('getvalue_weather_info'       , AUTOFUNCTYPE(WeatherData.P)),
        ('getvalue_wizlist'            , CFUNCTYPE(c_char_p)),
        ('getvalue_wiznames'           , CFUNCTYPE(c_int)),
        ('getvalue_world'              , AUTOFUNCTYPE(RoomData.P)),
        ('getvalue_zone_table'         , AUTOFUNCTYPE(ZoneData.P)),
        ('hit'                         , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P, c_int)),
        ('idle_dns_cache'              , CFUNCTYPE(c_int)),
        ('initworld'                   , CFUNCTYPE(c_int)),
        ('init_char'                   , CFUNCTYPE(c_void, CharacterData.P)),
        ('internalMakePrompt'          , CFUNCTYPE(c_char_p, DescriptorData.P)),
        ('invalid_align'               , CFUNCTYPE(c_int, CharacterData.P, ItemData.P)),
        ('is_empty'                    , CFUNCTYPE(c_int, c_int)),
        ('is_speedwalk_string'         , CFUNCTYPE(c_int, c_char_p)),
        ('isname'                      , CFUNCTYPE(c_int, c_char_p, c_char_p)),
        ('lightning'                   , CFUNCTYPE(c_int, CharacterData.P)),
        ('list_char_to_char'           , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('list_obj_to_char'            , CFUNCTYPE(c_int, ItemData.P, CharacterData.P, c_int, c_int)),
        ('load_char'                   , CFUNCTYPE(c_int, c_char_p, CharacterData.FileU.P)),
        ('load_dns_cache'              , CFUNCTYPE(c_int)),
        ('load_zones'                  , CFUNCTYPE(c_int, FILE_P, c_char_p)),
        ('lockMUD'                     , CFUNCTYPE(c_int, c_char_p)),
        ('log_zone_error'              , CFUNCTYPE(c_int, c_int, c_int, c_char_p)),
        ('mainDescriptorList'          , AUTOFUNCTYPE(DescriptorData.P)),
        ('make_corpse'                 , CFUNCTYPE(c_int, CharacterData.P)),
        ('mobiles_same'                , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('money_desc'                  , CFUNCTYPE(c_char_p, c_int)),
        ('mudlog'                      , CFUNCTYPE(c_void, c_int, c_int, c_int, c_char_p, c_char_p)),
        ('newbuf'                      , CFUNCTYPE(c_int)),
        ('num_of_zcmds'                , CFUNCTYPE(c_int, c_int)),
        ('obj_from_char'               , CFUNCTYPE(c_int, ItemData.P)),
        ('obj_from_obj'                , CFUNCTYPE(c_int, ItemData.P)),
        ('obj_from_room'               , CFUNCTYPE(c_int, ItemData.P)),
        ('obj_to_char'                 , CFUNCTYPE(c_int, ItemData.P, CharacterData.P)),
        ('obj_to_obj'                  , CFUNCTYPE(c_int, ItemData.P, ItemData.P)),
        ('obj_to_room'                 , CFUNCTYPE(c_int, ItemData.P, c_int)),
        ('open_logfile'                , CFUNCTYPE(c_int, c_char_p, FILE_P)),
        ('page_string'                 , CFUNCTYPE(c_int, DescriptorData.P, c_char_p, c_int)),
        ('parse_object'                , CFUNCTYPE(c_char_p, FILE_P, c_int)),
        ('perform_attack'              , CFUNCTYPE(c_int, CharacterData.P, c_int, c_int)),
        ('perform_backup'              , CFUNCTYPE(c_int)),
        ('perform_complex_alias'       , CFUNCTYPE(c_int, DescriptorData.TxtQueue.P, c_char_p, CharacterData.PlayerSpecialData.AliasData.P)),
        ('perform_subdue'              , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('power_rating'                , CFUNCTYPE(c_int, CharacterData.P)),
        ('process_speedwalk'           , CFUNCTYPE(c_int, DescriptorData.TxtQueue.P, c_char_p)),
        ('python_mobile'               , CFUNCTYPE(c_int, CharacterData.P, c_void_p, c_int, c_char_p)),
        ('python_object'               , CFUNCTYPE(c_int, CharacterData.P, c_void_p, c_int, c_char_p)),
        ('python_room'                 , CFUNCTYPE(c_int, CharacterData.P, c_void_p, c_int, c_char_p)),
        ('raw_kill'                    , CFUNCTYPE(c_int, CharacterData.P)),
        ('read_aliases'                , CFUNCTYPE(c_int, CharacterData.P)),
        ('read_config'                 , CFUNCTYPE(c_int, c_char_p)),
        ('read_last_backup'            , CFUNCTYPE(c_int)),
        ('read_mobile'                 , AUTOFUNCTYPE(CharacterData.P, c_int, c_int)),
        ('read_object'                 , AUTOFUNCTYPE(ItemData.P, c_int, c_int)),
        ('real_mobile'                 , CFUNCTYPE(mob_rnum, c_int)),
        ('real_object'                 , CFUNCTYPE(obj_rnum, c_int)),
        ('real_room'                   , CFUNCTYPE(room_rnum, c_int)),
        ('real_zone'                   , CFUNCTYPE(zone_rnum, c_int)),
        ('reboot_wizlists'             , CFUNCTYPE(c_int)),
        ('remove_from_olc_index'       , CFUNCTYPE(c_int, c_int, c_long)),
        ('report_dns'                  , CFUNCTYPE(c_int, c_char_p)),
        ('reset_time'                  , CFUNCTYPE(c_int)),
        ('reset_zone'                  , CFUNCTYPE(c_int, c_int)),
        ('saveZone'                    , CFUNCTYPE(c_int, c_int)),
        ('save_char'                   , CFUNCTYPE(c_void, CharacterData.P)),
        ('save_dns_cache'              , CFUNCTYPE(c_int)),
        ('save_load_rooms'             , CFUNCTYPE(c_int)),
        ('save_mud_time'               , CFUNCTYPE(c_void, TimeInfoData.P)),
        ('save_player_file'            , CFUNCTYPE(c_int, CharacterData.P, c_char_p, c_char_p)),
        ('saving_throws'               , CFUNCTYPE(c_int, c_int, c_int, c_int)),
        ('search_block'                , CFUNCTYPE(c_int, c_char_p, c_char_pp, c_int)),
        ('search_positions'            , CFUNCTYPE(c_int, c_char_p)),
        ('send_to_all'                 , CFUNCTYPE(c_int, c_char_p, c_char_p)),
        ('send_to_auction'             , CFUNCTYPE(c_int, c_char_p)),
        ('send_to_char'                , CFUNCTYPE(c_int, CharacterData.P, c_char_p, c_char_p)),
        ('send_to_outdoor'             , CFUNCTYPE(c_int, c_char_p, c_char_p)),
        ('set_fighting'                , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('setvalue_bufpool'            , CFUNCTYPE(c_int, DescriptorData.TxtBlock.P)),
        ('setvalue_character_list'     , CFUNCTYPE(c_int, CharacterData.P)),
        ('setvalue_loadIntoObjectIndex', CFUNCTYPE(c_int, obj_rnum)),
        ('setvalue_loadIntoZoneIndex'  , CFUNCTYPE(c_int, zone_rnum)),
        ('setvalue_mini_mud'           , CFUNCTYPE(c_int, c_int)),
        ('setvalue_obj_proto'          , CFUNCTYPE(c_int, ItemData.P)),
        ('setvalue_obj_index'          , CFUNCTYPE(c_int, IndexData.P)),
        ('setvalue_top_of_objt'        , CFUNCTYPE(c_int, obj_rnum)),
        ('setvalue_player_fl'          , CFUNCTYPE(c_int, FILE_P)),
        ('setvalue_r_frozen_start_room', CFUNCTYPE(c_int, room_rnum)),
        ('setvalue_r_immort_start_room', CFUNCTYPE(c_int, room_rnum)),
        ('setvalue_r_newbie_start_room', CFUNCTYPE(c_int, room_rnum)),
        ('setvalue_r_mortal_start_room', CFUNCTYPE(c_int, room_rnum)),
        ('setvalue_shutdown_by'        , CFUNCTYPE(c_void, c_long)),
        ('setvalue_shutdown_mode'      , CFUNCTYPE(c_void, c_int)),
        ('setvalue_shutdown_modes'     , CFUNCTYPE(c_int, c_int)),
        ('setvalue_shutdown_timer'     , CFUNCTYPE(c_void, c_int)),
        ('setvalue_olc_index'          , CFUNCTYPE(c_int, OlcIndexData.P)),
        ('setvalue_top_of_world'       , CFUNCTYPE(c_int, room_rnum)),
        ('setvalue_top_of_zone_table'  , CFUNCTYPE(c_int, zone_rnum)),
        ('setvalue_world'              , CFUNCTYPE(c_int, RoomData.P)),
        ('setvalue_zone_table'         , CFUNCTYPE(c_int, ZoneData.P)),
        ('sever_limb'                  , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('show_obj_modifiers'          , CFUNCTYPE(c_int, ItemData.P, CharacterData.P)),
        ('show_obj_to_char'            , CFUNCTYPE(c_int, ItemData.P, CharacterData.P, c_int)),
        ('shutdownMother'              , CFUNCTYPE(c_int)),
        ('shutdown_message'            , CFUNCTYPE(c_int)),
        ('spec_proc_func'              , AUTOFUNCTYPE(SPECIAL_TYPE, c_char_p, c_int)),
        ('special'                     , CFUNCTYPE(c_int, CharacterData.P, c_int, c_char_p)),
        ('spell_name'                  , CFUNCTYPE(c_char_p, c_int)),
        ('sprintbit'                   , CFUNCTYPE(c_size_t, c_ulong, c_char_pp, c_char_p, c_ulong)),
        ('sprinttype'                  , CFUNCTYPE(c_size_t, c_int, c_char_pp, c_char_p, c_ulong)),
        ('stop_fighting'               , CFUNCTYPE(c_int, CharacterData.P)),
        ('stop_hunting'                , CFUNCTYPE(c_int, CharacterData.P, CharacterData.P)),
        ('store_to_char'               , CFUNCTYPE(c_void, CharacterData.FileU.P, CharacterData.P, c_int)),
        ('string_write'                , CFUNCTYPE(c_int, DescriptorData.P, c_char_pp, c_ulong, c_long, c_void_p)),
        ('timediff'                    , CFUNCTYPE(c_int, c_timeval.P, c_timeval.P, c_timeval.P)),
        ('toggle_underworld_bridge'    , CFUNCTYPE(c_int)),
        ('unequip_char'                , AUTOFUNCTYPE(ItemData.P, CharacterData.P, c_int, c_int, c_int)),
        ('unload_dns_cache'            , CFUNCTYPE(c_int)),
        ('unlockMUD'                   , CFUNCTYPE(c_int, c_char_p)),
        ('update_index'                , CFUNCTYPE(c_int, c_char_p, c_int)),
        ('update_pos'                  , CFUNCTYPE(c_void, CharacterData.P)),
        ('update_shutdown'             , CFUNCTYPE(c_int)),
        ('valid_email'                 , CFUNCTYPE(c_int, c_char_p)),
        ('write_ban_list'              , CFUNCTYPE(c_int)),
        ('write_last_backup'           , CFUNCTYPE(c_int)),
        ('write_olc_file'              , CFUNCTYPE(c_int)),
        ('write_to_output'             , CFUNCTYPE(c_int, DescriptorData.P, c_char_p, c_char_p)),
        ('write_to_q'                  , CFUNCTYPE(c_int, c_char_p, DescriptorData.TxtQueue.P, c_int))]

MUDOperations.P = POINTER(MUDOperations)
