from typing import List, Tuple

from pony import orm

from database import enums, world
from world_server import op_code, router, session
from world_server.packets import guild_command_result, guild_query


@router.Handler(op_code.Client.GUILD_QUERY)
@orm.db_session
def handle_guild_query(pkt: guild_query.ClientGuildQuery,
                       session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    try:
        guild = world.Guild[pkt.id]

        rank_names = [gr.name for gr in guild.ranks]
        rank_names += [''] * (10 - len(rank_names))

        return [(
            op_code.Server.GUILD_QUERY_RESPONSE,
            guild_query.ServerGuildQuery.build(
                dict(
                    id=guild.id,
                    name=guild.name,
                    rank_names=rank_names,
                    emblem_style=guild.emblem_style,
                    emblem_color=guild.emblem_color,
                    border_style=guild.border_style,
                    border_color=guild.border_color,
                    background_color=guild.background_color,
                )),
        )]
    except orm.ObjectNotFound:
        return [(
            op_code.Server.GUILD_COMMAND_RESULT,
            guild_command_result.ServerGuildCommandResult.build(
                dict(
                    cmd=enums.GuildCommandType.CREATE,
                    str='',
                    result=enums.GuildCommandError.PLAYER_NOT_IN_GUILD,
                )),
        )]
