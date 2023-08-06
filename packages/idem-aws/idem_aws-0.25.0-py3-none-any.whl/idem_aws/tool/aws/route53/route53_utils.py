from typing import Dict
from typing import List


def get_hosted_zone_with_filters(
    hub,
    ctx,
    raw_hosted_zones: Dict,
    hosted_zone_name: str = None,
    private_zone: bool = None,
    vpc_id: str = None,
    tags: List = None,
):
    """
    Returns the hosted_zone with the specified filters, if it is available.

    Args:
        raw_hosted_zones(Dict): Dict of all the described hosted_zones
        hosted_zone_name(string, optional): Domain name of hosted_zone to filter.
        private_zone(bool, optional): Bool argument to specify a private hosted_zone. One of the filter option for hosted_zone
        vpc_id(string, optional): The vpc_id associated with the hosted_zone. One of the filter option for hosted_zone
        tags(List, optional): Tags of the hosted_zone. One of the filter option for hosted_zone

    """
    result = dict(comment=(), result=True, ret=None)
    raw_hosted_zones = raw_hosted_zones.values()
    hosted_zones = []
    for hosted_zone in raw_hosted_zones:
        temp = hosted_zone["aws.route53.hosted_zone.present"]
        temp_hosted_zone = {}
        for sub_dict in temp:
            temp_hosted_zone.update(sub_dict)
        hosted_zones.append(temp_hosted_zone)

    # filter_hosted_zones() returns True if all the filters match for a hosted_zone, and it is added to the list
    filtered_hosted_zones = list(
        filter(
            lambda x: filter_hosted_zones(
                x, hosted_zone_name, private_zone, vpc_id, tags
            ),
            hosted_zones,
        )
    )
    if not filtered_hosted_zones:
        result["comment"] = (
            f"Unable to find aws.route53.hosted_zone resource with given filters",
        )
        return result
    if len(filtered_hosted_zones) > 1:
        result["comment"] = (
            f"More than one aws.route53.hosted_zone resource was found with given filters. Use resource {filtered_hosted_zones[0].get('resource_id')}",
        )
    else:
        result["comment"] = (
            f"Found this aws.route53.hosted_zone resource {filtered_hosted_zones[0].get('resource_id')} with given filters",
        )
    result["ret"] = filtered_hosted_zones[0]
    return result


def filter_hosted_zones(
    hosted_zone: Dict,
    hosted_zone_name: str = None,
    private_zone: bool = None,
    vpc_id: str = None,
    tags: List = None,
):
    """
    Returns True if the hosted_zone checks all the filters provided or return False

    Args:
        hosted_zone(Dict): The described hosted_zone
        hosted_zone_name(string, optional): Domain name of hosted_zone to filter.
        private_zone(bool, optional): Bool argument to specify a private hosted_zone. One of the filter option for hosted_zone
        vpc_id(string, optional): The vpc_id associated with the hosted_zone. One of the filter option for hosted_zone
        tags(List, optional): Tags of the hosted_zone. One of the filter option for hosted_zone

    """
    # Return True if all the provided filters match or return False.

    if hosted_zone_name:
        if hosted_zone["hosted_zone_name"] != hosted_zone_name:
            return False

    if private_zone is not None:
        if hosted_zone["config"]["PrivateZone"] != private_zone:
            return False

    if vpc_id:
        found = False
        if hosted_zone["vpcs"]:
            for vpc in hosted_zone["vpcs"]:
                if vpc["VPCId"] == vpc_id:
                    found = True
                    break
            if not found:
                return False

    # Checking if all the tags in the filter match with the tags present in the hosted_zone.If not we return False
    if tags:
        tags2 = hosted_zone.get("tags")
        if tags2 is None:
            return False
        tags2_map = {tag.get("Key"): tag for tag in tags2}
        for tag in tags:
            if tag["Key"] not in tags2_map or (
                tags2_map.get(tag["Key"]).get("Value") != tag["Value"]
            ):
                return False

    return True
