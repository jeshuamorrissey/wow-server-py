import enum

from pony import orm

from database.db import db


class Objective(db.Entity):
    base_quest = orm.Required('QuestTemplate')
    slot = orm.Required(int, min=0, max=3)

    instances = orm.Set('ObjectiveProgress')

    orm.PrimaryKey(base_quest, slot)


class QuestTemplate(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=10)

    title = orm.Required(str)
    description = orm.Required(str)
    objectives = orm.Set(Objective)
    duration = orm.Optional(int)

    instances = orm.Set('Quest')
