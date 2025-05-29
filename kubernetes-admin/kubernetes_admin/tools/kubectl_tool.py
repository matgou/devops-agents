# In kubernetes_admin/kubernetes_admin/tools/kubectl_tool.py
"""Tool for executing kubectl get commands."""

import subprocess # For actual kubectl calls
from google.adk.tools import FunctionTool

def run_kubectl(verbs: str = "get", resource_type: str = "pods", resource_name: str = "", namespace: str = "default") -> str:
    """
    Runs a kubectl command with the specified verb, resource type, optional resource name, and namespace.
    Exemples:
        To get configuration of a specific pod use verbs: "describe", namespace: "all", resource_type: "pods", resource_name: "<custom pod name>"
        To get logs of a specific pod use verbs: "logs", namespace: "<namespace>", resource_type: "", resource_name: "<custom pod name>"
        To list pods in all namespace use verbs: "get", namespace: "all", resource_type: "pods", resource_name: ""
        
    Args:
        verbs: The kubectl verb to use (e.g., 'get', 'describe', 'logs', 'top').
        resource_type: The type of Kubernetes resource (e.g., 'pods', 'nodes', 'services', 'deployments').
        resource_name: Optional. The specific name of the resource. If None, lists all resources of the type.
        namespace: Optional. The Kubernetes namespace. Defaults to 'default'.

    Returns:
        A string containing the output of the kubectl command or an error message.
    """
    try:
        command = ["kubectl", verbs]
        if resource_name != "":
            command.append(f'{resource_type}/{resource_name}')
        else:
            command.append(f'{resource_type}')
        if namespace != "all":
            command.extend(["-n", namespace])
        else:
            command.extend(["--all-namespaces"])
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=30)
        return result.stdout
    except FileNotFoundError:
        return "Error: kubectl command not found. Please ensure kubectl is installed and in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error executing kubectl command: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: kubectl command timed out."
    except Exception as e:
         return f"An unexpected error occurred: {str(e)}"

kubectl_tool = FunctionTool(
    func=run_kubectl)
