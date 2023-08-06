from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

"""
Util functions to convert raw resource state from AWS ECR to present input format.
"""


def convert_raw_repository_to_present(
    hub, raw_resource: Dict[str, Any], tags: List = None, idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("repositoryName")
    resource_parameters = OrderedDict(
        {
            "repositoryArn": "repository_arn",
            "registryId": "registry_id",
            "repositoryName": "repository_name",
            "repositoryUri": "repository_uri",
            "imageTagMutability": "image_tag_mutability",
            "imageScanningConfiguration": "image_scanning_configuration",
            "encryptionConfiguration": "encryption_configuration",
        }
    )

    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    if tags:
        resource_translated["tags"] = tags

    return resource_translated
