import enum
from typing import Dict, Optional

from pony import orm

from database.db import db


class GuildMembership(db.Entity):
    player = orm.PrimaryKey('Player')
    guild = orm.Required('Guild')
    rank = orm.Required('GuildRank')


class GuildRank(db.Entity):
    guild = orm.Required('Guild')
    slot = orm.Required(int, min=0, max=9)

    name = orm.Required(str)

    orm.PrimaryKey(guild, slot)

    member_with_rank = orm.Set('GuildMembership')


class Guild(db.Entity):
    id = orm.PrimaryKey(int, auto=True)

    name = orm.Required(str)
    ranks = orm.Set('GuildRank')
    emblem_style = orm.Required(int)
    emblem_color = orm.Required(int)
    border_style = orm.Required(int)
    border_color = orm.Required(int)
    background_color = orm.Required(int)

    def get_ranks(self) -> Dict[int, Optional[GuildRank]]:
        rank_map = {i: None for i in range(10)}
        for rank in self.ranks:
            rank_map[rank.slot] = rank

        return rank_map

    members = orm.Set('GuildMembership')
