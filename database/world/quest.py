import enum
import time

from pony import orm

from database import game
from database.db import db

from .player import Player


class ObjectiveProgress(db.Entity):
    quest = orm.Required('Quest')
    objective = orm.Required('QuestObjectiveTemplate')
    slot = orm.Required(int, min=0, max=3)
    progress = orm.Required(int)

    orm.PrimaryKey(quest, slot)


class Quest(db.Entity):
    player = orm.Required('Player')
    base_quest = orm.Required('QuestTemplate')

    progress = orm.Set(ObjectiveProgress)
    due = orm.Optional(int)
    status = orm.Required(game.QuestStatus, default=game.QuestStatus.NONE)

    orm.PrimaryKey(player, base_quest)

    @classmethod
    def New(cls, player: Player, base_quest: game.QuestTemplate, **kwargs) -> 'Quest':
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

        if self.status == game.QuestStatus.COMPLETE:
            objective_bytes |= (1 << 24)
        elif self.status == game.QuestStatus.FAILED:
            objective_bytes |= (2 << 24)

        return objective_bytes
