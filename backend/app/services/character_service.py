"""Character training and consistency service"""
from typing import List, Optional, Dict, Any
from pathlib import Path
from app.core.config import settings
from app.services.comfy_service import comfy_service


class CharacterService:
    """Service for character LoRA training and consistency management"""

    def __init__(self):
        self.output_dir = Path(settings.lora_output_dir)

    async def train_lora(
        self,
        character_id: int,
        reference_images: List[str],
        training_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Train character LoRA for consistency

        Args:
            character_id: Character database ID
            reference_images: List of reference image URLs
            training_config: Training parameters (epochs, learning_rate, etc.)

        Returns:
            Dict with training job info and LoRA model path
        """
        default_config = {
            "training_epochs": 100,
            "learning_rate": 0.0001,
            "batch_size": 1,
            "resolution": 512
        }

        config = {**default_config, **(training_config or {})}

        # Build ComfyUI workflow for LoRA training
        workflow = {
            "template": "character_lora",
            "params": {
                "reference_images": reference_images,
                "output_name": f"character_{character_id}",
                "epochs": config["training_epochs"],
                "learning_rate": config["learning_rate"],
                "resolution": config["resolution"]
            }
        }

        # Execute workflow
        result = await comfy_service.execute_workflow(workflow)

        # Extract LoRA model path
        lora_path = self._extract_lora_path(result)

        return {
            "character_id": character_id,
            "lora_model_path": lora_path,
            "training_config": config,
            "status": "completed"
        }

    async def generate_consistent_image(
        self,
        character_id: int,
        prompt: str,
        lora_path: str,
        generation_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate image with character consistency using trained LoRA

        Args:
            character_id: Character ID
            prompt: Generation prompt
            lora_path: Path to character LoRA model
            generation_config: Image generation parameters

        Returns:
            Dict with generated image URLs
        """
        default_config = {
            "width": 1024,
            "height": 1024,
            "steps": 30,
            "cfg_scale": 7.5,
            "lora_strength": 0.8
        }

        config = {**default_config, **(generation_config or {})}

        # Build ComfyUI workflow for consistent generation
        workflow = {
            "template": "image_generation",
            "params": {
                "prompt": prompt,
                "negative_prompt": "(worst quality, low quality:1.4), blurry, deformed",
                "width": config["width"],
                "height": config["height"],
                "steps": config["steps"],
                "cfg_scale": config["cfg_scale"],
                "lora_path": lora_path,
                "lora_strength": config["lora_strength"]
            }
        }

        # Execute workflow
        result = await comfy_service.execute_workflow(workflow)

        # Extract image URLs
        image_urls = self._extract_image_urls(result)

        return {
            "character_id": character_id,
            "images": image_urls,
            "generation_config": config
        }

    def _extract_lora_path(self, result: Dict[str, Any]) -> str:
        """Extract LoRA model path from workflow result"""
        # TODO: Implement based on actual ComfyUI output structure
        # This would typically come from a SaveLoRA node
        return f"lora/character_model.safetensors"

    def _extract_image_urls(self, result: Dict[str, Any]) -> List[str]:
        """Extract image URLs from workflow result"""
        urls = []
        for img in result.get("images", []):
            urls.append(img["url"])
        return urls

    def prepare_reference_images(self, image_paths: List[str]) -> List[str]:
        """
        Prepare and validate reference images for training

        Args:
            image_paths: List of image URLs or file paths

        Returns:
            List of processed image URLs
        """
        # TODO: Implement image validation and preprocessing
        # - Check image quality
        - Extract faces using face detection
        - Crop and normalize
        return image_paths


# Singleton instance
character_service = CharacterService()
