from pony import orm

from database.db import db


class QuestObjectiveTemplate(db.Entity):
    """QuestObjectiveTemplate represents a single objective for a quest.

    Each template corresponds to one object for one quest.
    """
    base_quest_backlink = orm.Required('QuestTemplate')
    slot = orm.Required(int, min=0, max=3)

    objective_progress_backlink = orm.Set('ObjectiveProgress')

    orm.PrimaryKey(base_quest_backlink, slot)
