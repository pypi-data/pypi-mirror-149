from typing import Dict
from typing import List


def compare_and_get_notification_payload(
    hub, new_notifications: Dict[str, List], old_state: Dict[str, List]
) -> Dict[str, List]:
    """
    This functions helps in comparing two dicts.
    It compares each key value in both the dicts and return merged notifications configuration

    Returns:
        {Resultant notifications dictionary}

    """
    if "notifications" in old_state:
        existing_notifications = old_state["notifications"]
        notifications_result = {}
        for key in new_notifications:
            if not hub.tool.aws.state_comparison_utils.are_lists_identical(
                existing_notifications[key], new_notifications[key]
            ):
                notifications_result[key] = new_notifications[key]

        return notifications_result
    else:
        return new_notifications
