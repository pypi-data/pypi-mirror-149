from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions to convert raw resource state from AWS Config rule to present input format.
"""


async def convert_raw_config_rule_to_present(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str
) -> Dict[str, Any]:
    # ConfigRuleName is the unique identifier for Config so it is set as resource_id
    resource_id = raw_resource.get("ConfigRuleName")
    config_rule_arn = raw_resource.get("ConfigRuleArn")
    tag_ret = await hub.exec.boto3.client.config.list_tags_for_resource(
        ctx, ResourceArn=config_rule_arn
    )

    resource_parameters = OrderedDict(
        {
            "ConfigRuleName": "config_rule_name",
            "ConfigRuleArn": "config_rule_arn",
            "ConfigRuleId": "config_rule_id",
            "Scope": "scope",
            "Source": "source",
            "ConfigRuleState": "config_rule_state",
            "MaximumExecutionFrequency": "max_execution_frequency",
            "InputParameters": "input_parameters",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    if tag_ret:
        resource_translated["tags"] = tag_ret["ret"]["Tags"]
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    return resource_translated
