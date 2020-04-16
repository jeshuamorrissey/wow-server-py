from typing import List, Tuple

from pony import orm

from database import game
from world_server import op_code, router, session
from world_server.packets import item_query_single


@router.Handler(op_code.Client.ITEM_QUERY_SINGLE)
@orm.db_session
def handle_item_query_single(pkt: item_query_single.ClientItemQuerySingle,
                session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    item = game.ItemTemplate[pkt.entry]

    return [(
        op_code.Server.ITEM_QUERY_SINGLE_RESPONSE,
        item_query_single.ServerItemQuerySingle.build(
            dict(
                entry=item.entry,
                class_=item.class_,
                subclass=item.subclass,
                name=item.name,
                name_2='',
                name_3='',
                name_4='',
                display_info_id=item.displayid,
                quality=item.Quality,
                flags=item.Flags,
                buy_price=item.BuyPrice,
                sell_price=item.SellPrice,
                inventory_type=item.InventoryType,
                allowable_class=item.AllowableClass,
                allowable_race=item.AllowableRace,
                item_level=item.ItemLevel,
                required_level=item.RequiredLevel,
                required_skill=item.RequiredSkill,
                required_skill_rank=item.RequiredSkillRank,
                required_spell=item.requiredspell,
                required_honor_rank=item.requiredhonorrank,
                required_city_rank=item.RequiredCityRank,
                required_reputation_faction=item.RequiredReputationFaction,
                required_reputation_faction_2=item.RequiredReputationRank,
                max_count=item.maxcount,
                stackable=item.stackable,
                container_slots=item.ContainerSlots,
                stats=[
                    dict(
                        type=getattr(item, f'stat_type{i}'),
                        value=getattr(item, f'stat_type{i}'),
                    ) for i in range(1, 10 + 1)
                ],
                damages=[
                    dict(
                        min=getattr(item, f'dmg_min{i}'),
                        max=getattr(item, f'dmg_max{i}'),
                        type=getattr(item, f'dmg_type{i}'),
                    ) for i in range(1, 5 + 1)
                ],
                armor=item.armor,
                holy_res=item.holy_res,
                fire_res=item.fire_res,
                nature_res=item.nature_res,
                frost_res=item.frost_res,
                shadow_res=item.shadow_res,
                arcane_res=item.arcane_res,
                delay=item.delay,
                ammo_type=item.ammo_type,
                ranged_mod_range=item.RangedModRange,
                spells=[
                    dict(
                        id=getattr(item, f'spellid_{i}'),
                        trigger=getattr(item, f'spelltrigger_{i}'),
                        charges=getattr(item, f'spellcharges_{i}'),
                        cooldown=getattr(item, f'spellcooldown_{i}'),
                        category=getattr(item, f'spellcategory_{i}'),
                        category_cooldown=getattr(item, f'spellcategorycooldown_{i}'),
                    ) for i in range(1, 5 + 1)
                ],
                bonding=item.bonding,
                description=item.description,
                page_text=item.PageText,
                language_id=item.LanguageID,
                page_material=item.PageMaterial,
                start_quest=item.startquest,
                lock_id=item.lockid,
                material=item.Material,
                sheath=item.sheath,
                random_property=item.RandomProperty,
                block=item.block,
                item_set=item.itemset,
                max_durability=item.MaxDurability,
                area=item.area,
                map=item.Map,
                bag_family=item.BagFamily,
            )),
    )]
