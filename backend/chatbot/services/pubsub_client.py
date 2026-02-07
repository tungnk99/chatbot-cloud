"""
Client Pub/Sub: publish tin nhắn chat vào topic để xử lý bất đồng bộ.
"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def publish_chat_request(topic_path: str, payload: dict[str, Any]) -> bool:
    """
    Publish message lên Pub/Sub topic.
    payload: {"session_id": str, "message": str, "user_msg_id": str}
    Trả về True nếu thành công.
    """
    if not topic_path:
        logger.warning("PUBSUB_TOPIC not set, skip publish")
        return False
    try:
        from google.cloud import pubsub_v1

        publisher = pubsub_v1.PublisherClient()
        data = json.dumps(payload).encode("utf-8")
        future = publisher.publish(topic_path, data)
        future.result(timeout=10)
        logger.info("Published chat request to Pub/Sub: session_id=%s", payload.get("session_id"))
        return True
    except Exception as e:
        logger.exception("Pub/Sub publish failed: %s", e)
        return False
