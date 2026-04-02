"""ComfyUI workflow execution service"""
import httpx
import json
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path
from app.core.config import settings


class ComfyUIService:
    """Service for executing ComfyUI workflows"""

    def __init__(self):
        self.base_url = settings.comfyui_url
        self.timeout = 300  # 5 minutes default timeout

    async def execute_workflow(
        self,
        workflow_json: Dict[str, Any],
        client_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a ComfyUI workflow

        Args:
            workflow_json: ComfyUI workflow JSON structure
            client_id: Unique client ID for WebSocket tracking

        Returns:
            Dict with execution results including output URLs
        """
        if not client_id:
            client_id = "manjuflow_" + str(asyncio.get_event_loop().time())

        # Load the workflow template
        workflow = self._load_workflow(workflow_json)

        # Get server info
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Get prompt ID
            response = await client.post(
                f"{self.base_url}/prompt",
                json={
                    "prompt": workflow,
                    "client_id": client_id
                }
            )
            response.raise_for_status()
            prompt_data = response.json()

            prompt_id = prompt_data["prompt_id"]

            # Wait for completion (polling approach)
            result = await self._wait_for_completion(client, client_id, prompt_id)

            return result

    async def _wait_for_completion(
        self,
        client: httpx.AsyncClient,
        client_id: str,
        prompt_id: str,
        poll_interval: float = 1.0
    ) -> Dict[str, Any]:
        """Poll for workflow completion"""
        max_attempts = int(self.timeout / poll_interval)

        for _ in range(max_attempts):
            response = await client.get(
                f"{self.base_url}/history/{prompt_id}"
            )
            response.raise_for_status()
            history = response.json()

            if prompt_id in history:
                # Get output data
                history_data = history[prompt_id]
                outputs = history_data.get("outputs", {})

                # Extract image URLs
                result = {
                    "prompt_id": prompt_id,
                    "status": "completed",
                    "outputs": outputs
                }

                # Build image URLs
                for node_id, node_output in outputs.items():
                    if "images" in node_output:
                        images = []
                        for img in node_output["images"]:
                            img_url = f"{self.base_url}/view?filename={img['filename']}&subfolder={img.get('subfolder', '')}&type={img.get('type', 'output')}"
                            images.append({
                                "filename": img["filename"],
                                "subfolder": img.get("subfolder", ""),
                                "type": img.get("type", "output"),
                                "url": img_url
                            })
                        result["images"] = images

                return result

            await asyncio.sleep(poll_interval)

        raise TimeoutError(f"Workflow execution timed out after {self.timeout} seconds")

    def _load_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load workflow from JSON or template

        Args:
            workflow_data: Either raw workflow JSON or dict with 'template' and 'params'

        Returns:
            Complete ComfyUI workflow JSON
        """
        if "template" in workflow_data:
            # Load template file
            template_name = workflow_data["template"]
            template_path = Path(settings.comfyui_workflows_dir) / f"{template_name}.json"

            if not template_path.exists():
                raise FileNotFoundError(f"Workflow template not found: {template_path}")

            with open(template_path, "r") as f:
                workflow = json.load(f)

            # Apply parameter substitutions
            params = workflow_data.get("params", {})
            workflow = self._apply_params(workflow, params)

            return workflow
        else:
            # Direct workflow JSON
            return workflow_data

    def _apply_params(self, workflow: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply parameter substitutions to workflow"""
        for node_id, node_data in workflow.items():
            if "inputs" in node_data:
                for input_name, input_value in node_data["inputs"].items():
                    if isinstance(input_value, str) and input_value.startswith("${"):
                        param_name = input_value[2:-1]  # Remove ${ and }
                        if param_name in params:
                            workflow[node_id]["inputs"][input_name] = params[param_name]

        return workflow

    async def get_queue_info(self) -> Dict[str, Any]:
        """Get current queue information"""
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{self.base_url}/queue")
            response.raise_for_status()
            return response.json()

    async def get_server_info(self) -> Dict[str, Any]:
        """Get ComfyUI server information"""
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{self.base_url}/system_stats")
            response.raise_for_status()
            return response.json()


# Singleton instance
comfy_service = ComfyUIService()
