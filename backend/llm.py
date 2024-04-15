from typing import Awaitable, Callable, List
from openai import AsyncOpenAI, AsyncAzureOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionChunk

from api_types import ApiProviderInfo
import requests

MODEL_GPT_4_VISION = "gpt-4-vision-preview"


async def stream_openai_response(
    messages: List[ChatCompletionMessageParam],
    api_provider_info: ApiProviderInfo,
    callback: Callable[[str], Awaitable[None]],
) -> str:
    azure_endpoint = ""
    headers = ""
    # params = ""
    if api_provider_info.name == "openai":
        client = AsyncOpenAI(
            api_key=api_provider_info.api_key, base_url=api_provider_info.base_url
        )
    elif api_provider_info.name == "azure":
        # client = AsyncAzureOpenAI(
        #     api_version=api_provider_info.api_version,
        #     api_key=api_provider_info.api_key,
        #     azure_endpoint=f"https://{api_provider_info.resource_name}.openai.azure.com/openai/deployments/ebdc-vision/chat/completions?api-version=2023-07-01-preview",
        #     azure_deployment=api_provider_info.deployment_name,
        # )
        azure_endpoint=f"https://{api_provider_info.resource_name}.openai.azure.com/openai/deployments/ebdc-vision/chat/completions?api-version=2023-07-01-preview"

        headers = {
            "Content-Type": "application/json",
            "api-key": api_provider_info.api_key
        }
    else:
        raise Exception("Invalid api_provider_info")

    model = MODEL_GPT_4_VISION

    # Base parameters
    # params = {"model": model, "messages": messages, "stream": True}
    params = {"messages": messages}

    # Add 'max_tokens' only if the model is a GPT4 vision model
    if model == MODEL_GPT_4_VISION:
        params["max_tokens"] = 4096
        params["temperature"] = 0
        params["top_p"] = 0.95
    # print(api_provider_info,"api_provider_info")
    # print(headers,"headers")
    # print(params,"params")

    # response = client.chat.completions.create(**params)  # type: ignore
    # full_response = response.choices[0].message.content
    # full_response = ""
    # async for chunk in stream:  # type: ignore
    #     assert isinstance(chunk, ChatCompletionChunk)
    #     print(chunk,"chunk")
    #     content = chunk.choices[0].delta.content or ""
    #     full_response += content
    #     await callback(content)

    try:
        response = requests.post(azure_endpoint, headers=headers, json=params)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"]
        # print(result,"result")
        return result
    except requests.RequestException as e:
        print("ask_azureai_img exception: ", str(e))
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # await client.close()

    return full_response
