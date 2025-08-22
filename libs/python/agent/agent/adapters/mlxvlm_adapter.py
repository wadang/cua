import asyncio
import functools
import warnings
from concurrent.futures import ThreadPoolExecutor
from typing import Iterator, AsyncIterator, Dict, List, Any, Optional
from litellm.types.utils import GenericStreamingChunk, ModelResponse
from litellm.llms.custom_llm import CustomLLM
from litellm import completion, acompletion
import base64
from io import BytesIO
from PIL import Image

# Try to import MLX-VLM dependencies
try:
    import mlx.core as mx
    from mlx_vlm import load
    from mlx_vlm.utils import generate
    MLX_VLM_AVAILABLE = True
except ImportError:
    MLX_VLM_AVAILABLE = False


class MLXVLMAdapter(CustomLLM):
    """MLX-VLM Adapter for running vision-language models locally using Apple's MLX framework."""
    
    def __init__(self, **kwargs):
        """Initialize the adapter.
        
        Args:
            **kwargs: Additional arguments
        """
        super().__init__()
        self.models = {}  # Cache for loaded models
        self.processors = {}  # Cache for loaded processors
        self._executor = ThreadPoolExecutor(max_workers=1)  # Single thread pool
        
        if not MLX_VLM_AVAILABLE:
            raise ImportError("MLX-VLM dependencies not available. Please install mlx-vlm.")
        
    def _load_model_and_processor(self, model_name: str):
        """Load model and processor if not already cached.
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            Tuple of (model, processor)
        """
        if model_name not in self.models:
            # Load model and processor using mlx-vlm
            model, processor = load(
                model_name,
                processor_kwargs={
                    "min_pixels": 256 * 28 * 28,
                    "max_pixels": 1512 * 982
                }
            )
            
            # Cache them
            self.models[model_name] = model
            self.processors[model_name] = processor
            
        return self.models[model_name], self.processors[model_name]
    
    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert OpenAI format messages to MLX-VLM format.
        
        Args:
            messages: Messages in OpenAI format
            
        Returns:
            Messages in MLX-VLM format
        """
        converted_messages = []
        
        for message in messages:
            converted_message = {
                "role": message["role"],
                "content": []
            }
            
            content = message.get("content", [])
            if isinstance(content, str):
                # Simple text content
                converted_message["content"].append({
                    "type": "text",
                    "text": content
                })
            elif isinstance(content, list):
                # Multi-modal content
                for item in content:
                    if item.get("type") == "text":
                        converted_message["content"].append({
                            "type": "text",
                            "text": item.get("text", "")
                        })
                    elif item.get("type") == "image_url":
                        # Convert image_url format to image format
                        image_url = item.get("image_url", {}).get("url", "")
                        converted_message["content"].append({
                            "type": "image",
                            "image": image_url
                        })
                    elif item.get("type") == "image":
                        # Direct image format - pass through
                        converted_message["content"].append(item)
            
            converted_messages.append(converted_message)
            
        return converted_messages
    
    def _process_image_from_url(self, image_url: str) -> Image.Image:
        """Process image from URL (base64 or file path).
        
        Args:
            image_url: Image URL (data:image/... or file path)
            
        Returns:
            PIL Image object
        """
        if image_url.startswith("data:image/"):
            # Base64 encoded image
            header, data = image_url.split(",", 1)
            image_data = base64.b64decode(data)
            return Image.open(BytesIO(image_data))
        else:
            # File path or URL
            return Image.open(image_url)
    
    def _extract_image_from_messages(self, messages: List[Dict[str, Any]]) -> Optional[Image.Image]:
        """Extract the first image from messages.
        
        Args:
            messages: List of messages
            
        Returns:
            PIL Image object or None
        """
        for message in messages:
            content = message.get("content", [])
            if isinstance(content, list):
                for item in content:
                    if item.get("type") == "image":
                        image_url = item.get("image", "")
                        if image_url:
                            return self._process_image_from_url(image_url)
                    elif item.get("type") == "image_url":
                        image_url = item.get("image_url", {}).get("url", "")
                        if image_url:
                            return self._process_image_from_url(image_url)
        return None
    
    def _generate(self, **kwargs) -> str:
        """Generate response using the local MLX-VLM model.
        
        Args:
            **kwargs: Keyword arguments containing messages and model info
            
        Returns:
            Generated text response
        """
        messages = kwargs.get('messages', [])
        model_name = kwargs.get('model', 'mlx-community/Qwen2.5-VL-7B-Instruct-4bit')
        max_tokens = kwargs.get('max_tokens', 1000)
        temperature = kwargs.get('temperature', 0.1)
        
        # Warn about ignored kwargs
        ignored_kwargs = set(kwargs.keys()) - {'messages', 'model', 'max_tokens', 'temperature'}
        if ignored_kwargs:
            warnings.warn(f"Ignoring unsupported kwargs: {ignored_kwargs}")
        
        # Load model and processor
        model, processor = self._load_model_and_processor(model_name)
        
        # Convert messages to MLX-VLM format
        mlx_messages = self._convert_messages(messages)
        
        # Extract image from messages
        image = self._extract_image_from_messages(mlx_messages)
        
        # Apply chat template
        prompt = processor.apply_chat_template(
            mlx_messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        
        # Generate response using mlx-vlm
        try:
            response = generate(
                model,
                processor,
                prompt,
                image,  # type: ignore
                temperature=temperature,
                max_tokens=max_tokens,
                verbose=False,
            )
            
            # Clear MLX cache to free memory
            mx.metal.clear_cache()
            
            return response
            
        except Exception as e:
            # Clear cache on error too
            mx.metal.clear_cache()
            raise e
    
    def completion(self, *args, **kwargs) -> ModelResponse:
        """Synchronous completion method.
        
        Returns:
            ModelResponse with generated text
        """
        generated_text = self._generate(**kwargs)
        
        response = completion(
            model=f"mlx/{kwargs.get('model', 'default')}",
            mock_response=generated_text,
        )
        return response  # type: ignore
    
    async def acompletion(self, *args, **kwargs) -> ModelResponse:
        """Asynchronous completion method.
        
        Returns:
            ModelResponse with generated text
        """
        # Run _generate in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        generated_text = await loop.run_in_executor(
            self._executor, 
            functools.partial(self._generate, **kwargs)
        )
        
        response = await acompletion(
            model=f"mlx/{kwargs.get('model', 'default')}",
            mock_response=generated_text,
        )
        return response  # type: ignore
    
    def streaming(self, *args, **kwargs) -> Iterator[GenericStreamingChunk]:
        """Synchronous streaming method.
        
        Returns:
            Iterator of GenericStreamingChunk
        """
        generated_text = self._generate(**kwargs)
        
        generic_streaming_chunk: GenericStreamingChunk = {
            "finish_reason": "stop",
            "index": 0,
            "is_finished": True,
            "text": generated_text,
            "tool_use": None,
            "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0},
        }
        
        yield generic_streaming_chunk
    
    async def astreaming(self, *args, **kwargs) -> AsyncIterator[GenericStreamingChunk]:
        """Asynchronous streaming method.
        
        Returns:
            AsyncIterator of GenericStreamingChunk
        """
        # Run _generate in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        generated_text = await loop.run_in_executor(
            self._executor, 
            functools.partial(self._generate, **kwargs)
        )
        
        generic_streaming_chunk: GenericStreamingChunk = {
            "finish_reason": "stop",
            "index": 0,
            "is_finished": True,
            "text": generated_text,
            "tool_use": None,
            "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0},
        }
        
        yield generic_streaming_chunk
