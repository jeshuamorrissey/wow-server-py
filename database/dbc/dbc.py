from pony import orm

from database.db import db


# Special DBC types: LangStringRef vs. StringRef
class SingleString(str):
    pass


class SingleEnumString(SingleString):
    pass


class MultiString(str):
    pass


class MultiEnumString(MultiString):
    pass


class FixedIntArray(orm.IntArray):

    def __init__(self, size: int):
        self.size = size


class AnimationData(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(SingleEnumString)
    weapon_flags = orm.Required(int)
    body_flags = orm.Required(int)
    flags = orm.Required(int)
    fallback = orm.Optional('AnimationData', reverse='fallback_backlink')
    previous = orm.Optional('AnimationData', reverse='previous_backlink')

    fallback_backlink = orm.Set('AnimationData', reverse='fallback')
    previous_backlink = orm.Set('AnimationData', reverse='previous')


class AreaPOI(db.Entity):
    id = orm.PrimaryKey(int)
    importance = orm.Required(int)
    icon = orm.Required(int)
    faction_id = orm.Required(int)
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    continent_id = orm.Required(int)
    flags = orm.Required(int, unsigned=True)
    area_id = orm.Required(int, unsigned=True)
    name = orm.Required(MultiString)
    description = orm.Optional(MultiString)
    world_state_id = orm.Required(int)


class AreaTrigger(db.Entity):
    id = orm.PrimaryKey(int)
    continent_id = orm.Required(int)
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    radius = orm.Required(float)
    box_length = orm.Required(float)
    box_width = orm.Required(float)
    box_height = orm.Required(float)
    box_yaw = orm.Required(float)


class AttackAnimKits(db.Entity):
    id = orm.PrimaryKey(int)
    item_subclass_id = orm.Required(int)
    anim_type = orm.Required('AttackAnimTypes', reverse='attack_anim_kits_backlink')
    anim_frequency = orm.Required(int)
    which_hand = orm.Required(int)


class AttackAnimTypes(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(SingleString)

    attack_anim_kits_backlink = orm.Set('AttackAnimKits', reverse='anim_type')


class AuctionHouse(db.Entity):
    id = orm.PrimaryKey(int)
    faction = orm.Required('Faction', reverse='auction_house_backlink')
    deposit_rate = orm.Required(int)
    consignment_rate = orm.Required(int)
    name = orm.Required(MultiEnumString)


class BankBagSlotPrices(db.Entity):
    id = orm.PrimaryKey(int)
    cost = orm.Required(int)


class Faction(db.Entity):
    id = orm.PrimaryKey(int)
    reputation_index = orm.Required(int, unsigned=True)
    reputation_race_mask1 = orm.Required(int, unsigned=True)
    reputation_race_mask2 = orm.Required(int, unsigned=True)
    reputation_race_mask3 = orm.Required(int, unsigned=True)
    reputation_race_mask4 = orm.Required(int, unsigned=True)
    reputation_class_mask1 = orm.Required(int, unsigned=True)
    reputation_class_mask2 = orm.Required(int, unsigned=True)
    reputation_class_mask3 = orm.Required(int, unsigned=True)
    reputation_class_mask4 = orm.Required(int, unsigned=True)
    reputation_base1 = orm.Required(int, unsigned=True)
    reputation_base2 = orm.Required(int, unsigned=True)
    reputation_base3 = orm.Required(int, unsigned=True)
    reputation_base4 = orm.Required(int, unsigned=True)
    reputation_flags1 = orm.Required(int, unsigned=True)
    reputation_flags2 = orm.Required(int, unsigned=True)
    reputation_flags3 = orm.Required(int, unsigned=True)
    reputation_flags4 = orm.Required(int, unsigned=True)
    parent_faction = orm.Optional('Faction', reverse='parent_faction_backlink')
    name = orm.Required(MultiEnumString)
    description = orm.Optional(MultiString)

    parent_faction_backlink = orm.Set('Faction', reverse='parent_faction')
    auction_house_backlink = orm.Set('AuctionHouse', reverse='faction')
    chr_races_backlink = orm.Set('ChrRaces', reverse='faction')


class Languages(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(MultiEnumString)

    chr_races_backlink = orm.Set('ChrRaces', reverse='base_language')


class CreatureType(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(MultiEnumString)
    flags = orm.Required(int)

    chr_races_backlink = orm.Set('ChrRaces', reverse='creature_type')


class Spell(db.Entity):
    id = orm.PrimaryKey(int)
    school_mask = orm.Required(int, unsigned=True)
    category = orm.Required(int, unsigned=True)
    cast_ui = orm.Required(int)
    dispel = orm.Required(int, unsigned=True)
    mechanic = orm.Required(int, unsigned=True)
    attributes = orm.Required(int, unsigned=True)
    attributes_ex = orm.Required(int, unsigned=True)
    attributes_ex2 = orm.Required(int, unsigned=True)
    attributes_ex3 = orm.Required(int, unsigned=True)
    attributes_ex4 = orm.Required(int, unsigned=True)
    shapeshift_mask = orm.Required(int, unsigned=True)
    shapeshift_exclude = orm.Required(int, unsigned=True)
    targets = orm.Required(int, unsigned=True)
    target_creature_type = orm.Required(int, unsigned=True)
    requires_spell_focus = orm.Required(int, unsigned=True)
    caster_aura_state = orm.Required(int, unsigned=True)
    target_aura_state = orm.Required(int, unsigned=True)
    casting_time_index = orm.Required(int, unsigned=True)
    recovery_time = orm.Required(int, unsigned=True)
    category_recovery_time = orm.Required(int, unsigned=True)
    interrupt_flags = orm.Required(int, unsigned=True)
    aura_interrupt_flags = orm.Required(int, unsigned=True)
    channel_interrupt_flags = orm.Required(int, unsigned=True)
    proc_flags = orm.Required(int, unsigned=True)
    proc_chance = orm.Required(int, unsigned=True)
    proc_charges = orm.Required(int, unsigned=True)
    maximum_level = orm.Required(int, unsigned=True)
    base_level = orm.Required(int, unsigned=True)
    spell_level = orm.Required(int, unsigned=True)
    duration_index = orm.Required(int, unsigned=True)
    power_type = orm.Required(int, unsigned=True)
    mana_cost = orm.Required(int, unsigned=True)
    mana_cost_per_level = orm.Required(int, unsigned=True)
    mana_per_second = orm.Required(int, unsigned=True)
    mana_per_second_per_level = orm.Required(int, unsigned=True)
    range_index = orm.Required(int, unsigned=True)
    speed = orm.Required(int, unsigned=True)
    modal_next_spell = orm.Required(int, unsigned=True)
    stack_amount = orm.Required(int, unsigned=True)
    totem1 = orm.Required(int, unsigned=True)
    totem2 = orm.Required(int, unsigned=True)
    reagent1 = orm.Required(int)
    reagent2 = orm.Required(int)
    reagent3 = orm.Required(int)
    reagent4 = orm.Required(int)
    reagent5 = orm.Required(int)
    reagent6 = orm.Required(int)
    reagent7 = orm.Required(int)
    reagent8 = orm.Required(int)
    reagent_count1 = orm.Required(int, unsigned=True)
    reagent_count2 = orm.Required(int, unsigned=True)
    reagent_count3 = orm.Required(int, unsigned=True)
    reagent_count4 = orm.Required(int, unsigned=True)
    reagent_count5 = orm.Required(int, unsigned=True)
    reagent_count6 = orm.Required(int, unsigned=True)
    reagent_count7 = orm.Required(int, unsigned=True)
    reagent_count8 = orm.Required(int, unsigned=True)
    equipped_item_class = orm.Required(int, unsigned=True)
    equipped_item_sub_class_mask = orm.Required(int, unsigned=True)
    equipped_item_inventory_type_mask = orm.Required(int, unsigned=True)
    effect1 = orm.Required(int, unsigned=True)
    effect2 = orm.Required(int, unsigned=True)
    effect3 = orm.Required(int, unsigned=True)
    effect_die_sides1 = orm.Required(int, unsigned=True)
    effect_die_sides2 = orm.Required(int, unsigned=True)
    effect_die_sides3 = orm.Required(int, unsigned=True)
    effect_base_dice1 = orm.Required(int)
    effect_base_dice2 = orm.Required(int)
    effect_base_dice3 = orm.Required(int)
    effect_dice_per_level1 = orm.Required(int)
    effect_dice_per_level2 = orm.Required(int)
    effect_dice_per_level3 = orm.Required(int)
    effect_real_points_per_level1 = orm.Required(int, unsigned=True)
    effect_real_points_per_level2 = orm.Required(int, unsigned=True)
    effect_real_points_per_level3 = orm.Required(int, unsigned=True)
    effect_base_points1 = orm.Required(int, unsigned=True)
    effect_base_points2 = orm.Required(int, unsigned=True)
    effect_base_points3 = orm.Required(int, unsigned=True)
    effect_mechanic1 = orm.Required(int, unsigned=True)
    effect_mechanic2 = orm.Required(int, unsigned=True)
    effect_mechanic3 = orm.Required(int, unsigned=True)
    effect_implicit_target_a1 = orm.Required(int, unsigned=True)
    effect_implicit_target_a2 = orm.Required(int, unsigned=True)
    effect_implicit_target_a3 = orm.Required(int, unsigned=True)
    effect_implicit_target_b1 = orm.Required(int, unsigned=True)
    effect_implicit_target_b2 = orm.Required(int, unsigned=True)
    effect_implicit_target_b3 = orm.Required(int, unsigned=True)
    effect_radius_index1 = orm.Required(int, unsigned=True)
    effect_radius_index2 = orm.Required(int, unsigned=True)
    effect_radius_index3 = orm.Required(int, unsigned=True)
    effect_apply_aura_name1 = orm.Required(int, unsigned=True)
    effect_apply_aura_name2 = orm.Required(int, unsigned=True)
    effect_apply_aura_name3 = orm.Required(int, unsigned=True)
    effect_amplitude1 = orm.Required(int, unsigned=True)
    effect_amplitude2 = orm.Required(int, unsigned=True)
    effect_amplitude3 = orm.Required(int, unsigned=True)
    effect_multiple_value1 = orm.Required(float)
    effect_multiple_value2 = orm.Required(float)
    effect_multiple_value3 = orm.Required(float)
    effect_chain_target1 = orm.Required(int, unsigned=True)
    effect_chain_target2 = orm.Required(int, unsigned=True)
    effect_chain_target3 = orm.Required(int, unsigned=True)
    effect_item_type1 = orm.Required(int, unsigned=True)
    effect_item_type2 = orm.Required(int, unsigned=True)
    effect_item_type3 = orm.Required(int, unsigned=True)
    effect_misc_value1 = orm.Required(int, unsigned=True)
    effect_misc_value2 = orm.Required(int, unsigned=True)
    effect_misc_value3 = orm.Required(int, unsigned=True)
    effect_trigger_spell1 = orm.Required(int, unsigned=True)
    effect_trigger_spell2 = orm.Required(int, unsigned=True)
    effect_trigger_spell3 = orm.Required(int, unsigned=True)
    effect_points_per_combo_point1 = orm.Required(float)
    effect_points_per_combo_point2 = orm.Required(float)
    effect_points_per_combo_point3 = orm.Required(float)
    spell_visual1 = orm.Required(int, unsigned=True)
    spell_visual2 = orm.Required(int, unsigned=True)
    spell_icon_id = orm.Required(int, unsigned=True)
    active_icon_id = orm.Required(int, unsigned=True)
    spell_priority = orm.Required(int, unsigned=True)
    spell_name = orm.Required(MultiEnumString)
    spell_rank = orm.Optional(MultiString)
    spell_description = orm.Optional(MultiString)
    spell_tool_tip = orm.Optional(MultiString)
    mana_cost_percentage = orm.Required(int, unsigned=True)
    start_recovery_category = orm.Required(int, unsigned=True)
    start_recovery_time = orm.Required(int, unsigned=True)
    maximum_target_level = orm.Required(int, unsigned=True)
    spell_class_set = orm.Required(int, unsigned=True)
    spell_class_mask1 = orm.Required(int, unsigned=True)
    spell_class_mask2 = orm.Required(int, unsigned=True)
    maximum_affected_targets = orm.Required(int, unsigned=True)
    damage_class = orm.Required(int, unsigned=True)
    prevention_type = orm.Required(int, unsigned=True)
    stance_bar_order = orm.Required(int, unsigned=True)
    effect_damage_multiplier1 = orm.Required(float)
    effect_damage_multiplier2 = orm.Required(float)
    effect_damage_multiplier3 = orm.Required(float)
    minimum_faction_id = orm.Required(int, unsigned=True)
    minimum_reputation = orm.Required(int, unsigned=True)
    required_aura_vision = orm.Required(int, unsigned=True)

    chr_races_login_effect_backlink = orm.Set('ChrRaces', reverse='login_effect')
    chr_races_combat_stun_backlink = orm.Set('ChrRaces', reverse='combat_stun')
    chr_races_res_sickness_backlink = orm.Set('ChrRaces', reverse='res_sickness')


class CinematicCamera(db.Entity):
    id = orm.PrimaryKey(int)
    model = orm.Required(SingleString)
    sound_id = orm.Required(int)
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    o = orm.Required(float)

    cinematic_sequences_camera1_backlink = orm.Set('CinematicSequences', reverse='camera1')
    cinematic_sequences_camera2_backlink = orm.Set('CinematicSequences', reverse='camera2')
    cinematic_sequences_camera3_backlink = orm.Set('CinematicSequences', reverse='camera3')
    cinematic_sequences_camera4_backlink = orm.Set('CinematicSequences', reverse='camera4')
    cinematic_sequences_camera5_backlink = orm.Set('CinematicSequences', reverse='camera5')
    cinematic_sequences_camera6_backlink = orm.Set('CinematicSequences', reverse='camera6')
    cinematic_sequences_camera7_backlink = orm.Set('CinematicSequences', reverse='camera7')
    cinematic_sequences_camera8_backlink = orm.Set('CinematicSequences', reverse='camera8')


class CinematicSequences(db.Entity):
    id = orm.PrimaryKey(int)
    sound_id = orm.Required(int)
    camera1 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera1_backlink')
    camera2 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera2_backlink')
    camera3 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera3_backlink')
    camera4 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera4_backlink')
    camera5 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera5_backlink')
    camera6 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera6_backlink')
    camera7 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera7_backlink')
    camera8 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera8_backlink')

    chr_races_backlink = orm.Set('ChrRaces', reverse='cinematic_sequence')


class ChrRaces(db.Entity):
    id = orm.PrimaryKey(int)
    flags = orm.Required(int)
    faction = orm.Required('Faction', reverse='chr_races_backlink')
    exploration_sound_id = orm.Required(int)
    male_display_id = orm.Required(int)
    female_display_id = orm.Required(int)
    client_prefix = orm.Required(SingleString)
    mount_scale = orm.Required(float)
    base_language = orm.Required('Languages', reverse='chr_races_backlink')
    creature_type = orm.Required('CreatureType', reverse='chr_races_backlink')
    login_effect = orm.Required('Spell', reverse='chr_races_login_effect_backlink')
    combat_stun = orm.Required('Spell', reverse='chr_races_combat_stun_backlink')
    res_sickness = orm.Required('Spell', reverse='chr_races_res_sickness_backlink')
    splash_sound_id = orm.Required(int)
    starting_taxi_nodes = orm.Required(int)
    client_file_string = orm.Required(SingleString)
    cinematic_sequence = orm.Optional('CinematicSequences', reverse='chr_races_backlink')
    name = orm.Required(MultiEnumString)
    facial_hair_customization_male = orm.Required(SingleString)
    facial_hair_customization_female = orm.Required(SingleString)
    hair_customization = orm.Required(SingleString)
