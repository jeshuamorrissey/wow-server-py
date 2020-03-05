import enum

from pony import orm
import time

from database.db import db
from database.dbc import constants as c

from database.dbc.quest_template import QuestTemplate
from database.world.game_object.player import Player


class ObjectiveProgress(db.Entity):
    quest = orm.Required('Quest')
    objective = orm.Required('Objective')
    slot = orm.Required(int, min=0, max=3)
    progress = orm.Required(int)

    orm.PrimaryKey(quest, slot)


class Quest(db.Entity):
    player = orm.Required('Player')
    base_quest = orm.Required('QuestTemplate')

    progress = orm.Set(ObjectiveProgress)
    due = orm.Optional(int)
    status = orm.Required(c.QuestStatus, default=c.QuestStatus.NONE)

    orm.PrimaryKey(player, base_quest)

    @classmethod
    def New(cls, player: Player, base_quest: QuestTemplate, **kwargs) -> 'Quest':
        quest = Quest(
            player=player,
            base_quest=base_quest,
            due=int(time.time()) + base_quest.duration if base_quest.duration else None,
            **kwargs,
        )

        for objective in base_quest.objectives:
            ObjectiveProgress(
                quest=quest,
                objective=objective,
                slot=objective.slot,
                progress=0,
            )

        return quest

    def flags(self) -> int:
        objective_bytes = 0
        for objective in self.progress:
            objective_bytes |= (objective.slot << (objective.progress * 6))

        if self.status == c.QuestStatus.COMPLETE:
            objective_bytes |= (1 << 24)
        elif self.status == c.QuestStatus.FAILED:
            objective_bytes |= (2 << 24)

        return objective_bytes
