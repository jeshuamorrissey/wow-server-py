from pony import orm

from database.db import db


class QuestTemplate(db.Entity):
    """QuestTemplate represents quest information within the game.
    
    Each template corresponds to a unique quest.
    """
    id = orm.PrimaryKey(int, auto=True, min=10)

    title = orm.Required(str)
    description = orm.Required(str)
    objectives = orm.Set('QuestObjectiveTemplate')
    duration = orm.Optional(int)

    quest_backlink = orm.Set('Quest')
