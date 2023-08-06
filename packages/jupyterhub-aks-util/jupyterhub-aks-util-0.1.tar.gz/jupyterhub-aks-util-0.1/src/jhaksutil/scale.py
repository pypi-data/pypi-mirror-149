import requests
from .auth import AzureBearerToken

class AKSScaler:
    def __init__(self,
        subscription_id: str,
        resource_group: str,
        cluster_name: str,
        token: AzureBearerToken,
    ):
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.cluster_name = cluster_name
        self.token = token


    def autoscale_enable(self, min_count: int, max_count: int) -> bool:
        """
        Enables cluster autoscaling and sets the min and max nodes.

        Parameters:
        min_count (int): Minimum number of nodes in the pool
        max_count (int): Maximum number of nodes in the pool

        Returns:
        bool: Success or failure
        """
        payload = {
            "properties": {
                "enableAutoScaling": True,
                "minCount": min_count,
                "maxCount": max_count,
                "type": "VirtualMachineScaleSets",
            }
        }
        resp = requests.put(
            url=f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.ContainerService/managedClusters/{self.cluster_name}/agentPools/userpods?api-version=2022-02-01",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"},
            json=payload,
        )
        print(resp.text)
        if resp.status_code == 200:
            return True
        return False

    def autoscale_disable(self, count: int) -> bool:
        """
        Disables cluster autoscaling and sets the node count.

        Parameters:
        count (int): Number of nodes in the pool

        Returns:
        bool: Success or failure
        """
        payload = {
            "properties": {
                "enableAutoScaling": False,
                "count": count,
            }
        }
        resp = requests.put(
            url=f"https://management.azure.com/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.ContainerService/managedClusters/{self.cluster_name}/agentPools/userpods?api-version=2022-02-01",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"},
            json=payload,
        )
        print(resp.text)
        if resp.status_code == 200:
            return True
        return False
