from upswingutil.resource import decrypt, http_retry
from loguru import logger
from upswingutil.schema import Token
from upswingutil.db import Firestore


def get_key(org_id: str, app: str = None) -> Token:
    db = Firestore(app) if app else Firestore()
    client = db.get_collection(f"{db.org_collection}/{org_id}/tokens").document("doorlock").get().to_dict()
    url = client["url"]
    body = {
        "client_id": decrypt(client['client_id']),
        "client_pw": decrypt(client["client_pw"])
    }
    try:
        http = http_retry()
        resp = http.post(f"http://{url}/mst/enc/auth/auth", json=body)
        if resp.status_code != 200:
            logger.error('POST /authToken {}'.format(resp.status_code))
            logger.error(resp.__str__())
            logger.error(resp.reason)
        else:
            return Token(
                key=resp.json()['value'],
                validity='',
                hostName=url
            )
    except Exception as e:
        logger.error('Exception generating auth token for Messerschmitt')
        logger.error(e)
