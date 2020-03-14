from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import raid_instance_info, request_raid_info


@router.Handler(op_code.Client.REQUEST_RAID_INFO)
@orm.db_session
def handler(pkt: request_raid_info.ClientRequestRaidInfo,
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    # TODO: implement this when there are instances
    return [(
        op_code.Server.RAID_INSTANCE_INFO,
        raid_instance_info.ServerRaidInstanceInfo.build(dict(instances=[])),
    )]
