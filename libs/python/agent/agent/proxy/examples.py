"""
Example usage of the proxy server and client requests.
"""
import dotenv
dotenv.load_dotenv()

import asyncio
import json
import os
import aiohttp
from typing import Dict, Any

def print_agent_response(result: dict):
    # Pretty-print AgentResponse per your schema
    output = result.get("output", []) or []
    usage = result.get("usage") or {}

    for msg in output:
        t = msg.get("type")
        if t == "message":
            role = msg.get("role")
            if role == "assistant":
                for c in msg.get("content", []):
                    if c.get("type") == "output_text":
                        print(f"assistant> {c.get('text','')}")
        elif t == "reasoning":
            for s in msg.get("summary", []):
                if s.get("type") == "summary_text":
                    print(f"(thought) {s.get('text','')}")
        elif t == "computer_call":
            action = msg.get("action", {})
            a_type = action.get("type", "action")
            # Compact action preview (omit bulky fields)
            preview = {k: v for k, v in action.items() if k not in ("type", "path", "image")}
            print(f"🛠 computer_call {a_type} {preview} (id={msg.get('call_id')})")
        elif t == "computer_call_output":
            print(f"🖼 screenshot (id={msg.get('call_id')})")
        elif t == "function_call":
            print(f"🔧 fn {msg.get('name')}({msg.get('arguments')}) (id={msg.get('call_id')})")
        elif t == "function_call_output":
            print(f"🔧 fn result: {msg.get('output')} (id={msg.get('call_id')})")

    if usage:
        print(
            f"[usage] prompt={usage.get('prompt_tokens',0)} "
            f"completion={usage.get('completion_tokens',0)} "
            f"total={usage.get('total_tokens',0)} "
            f"cost=${usage.get('response_cost',0)}"
        )


async def test_http_endpoint():
    """Test the HTTP /responses endpoint."""
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert isinstance(openai_api_key, str), "OPENAI_API_KEY environment variable must be set"
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    assert isinstance(anthropic_api_key, str), "ANTHROPIC_API_KEY environment variable must be set"

    # Test requests
    base_url = "https://m-linux-96lcxd2c2k.containers.cloud.trycua.com:8443"
    # base_url = "http://localhost:8000"
    api_key = os.getenv("CUA_API_KEY")
    assert isinstance(api_key, str), "CUA_API_KEY environment variable must be set"
    
    async with aiohttp.ClientSession() as session:
        for i, request_data in enumerate([
            # ==== Request Body Examples ====

            # Simple text request
            {
                "model": "anthropic/claude-3-5-sonnet-20241022",
                "input": "Hello!",
                "env": {
                    "ANTHROPIC_API_KEY": anthropic_api_key
                }
            },

            # {
            #     "model": "openai/computer-use-preview",
            #     "input": "Hello!",
            #     "env": {
            #         "OPENAI_API_KEY": openai_api_key
            #     }
            # },

            # Multimodal request with image
            # {
            #     "model": "anthropic/claude-3-5-sonnet-20241022",
            #     "input": [
            #         {
            #             "role": "user",
            #             "content": [
            #                 {"type": "input_text", "text": "what is in this image?"},
            #                 {
            #                     "type": "input_image",
            #                     "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            #                 }
            #             ]
            #         }
            #     ],
            #     "env": {
            #         "ANTHROPIC_API_KEY": anthropic_api_key
            #     }
            # }

        ], 1):
            print(f"\n--- Test {i} ---")
            print(f"Request: {json.dumps(request_data, indent=2)}")
            
            try:
                print(f"Sending request to {base_url}/responses")
                async with session.post(
                    f"{base_url}/responses",
                    json=request_data,
                    headers={"Content-Type": "application/json", "X-API-Key": api_key}
                ) as response:
                    text_result = await response.text()
                    print(f"Response Text: {text_result}")
                    
                    result = json.loads(text_result)
                    print(f"Status: {response.status}")
                    print(f"Response: {json.dumps(result, indent=2)}")
                    print(f"Response Headers:")
                    for header in response.headers:
                        print(f"- {header}: {response.headers[header]}")
                    
            except Exception as e:
                print(f"Error: {e}")

async def simple_repl():
    base_url = "https://m-linux-96lcxd2c2k.containers.cloud.trycua.com:8443"
    api_key = os.getenv("CUA_API_KEY", "")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    model = "openai/computer-use-preview"

    messages = []
    async with aiohttp.ClientSession() as session:
        while True:
            if not messages or messages[-1].get("type") == "message":
                user_text = input("you> ").strip()
                if user_text == "exit":
                    break
                if user_text:
                    messages += [{"role": "user", "content": user_text}]  # loop

            payload = {
                "model": model,
                "input": messages,
                "env": {
                    "ANTHROPIC_API_KEY": anthropic_api_key,
                    "OPENAI_API_KEY": openai_api_key
                }
            }
            async with session.post(f"{base_url}/responses",
                                    json=payload,
                                    headers={"Content-Type": "application/json", "X-API-Key": api_key}) as resp:
                result = json.loads(await resp.text())
                print_agent_response(result)

            messages += result.get("output", [])  # request

async def test_p2p_client():
    """Example P2P client using peerjs-python."""
    try:
        from peerjs import Peer, PeerOptions, ConnectionEventType
        from aiortc import RTCConfiguration, RTCIceServer
        
        # Set up client peer
        options = PeerOptions(
            host="0.peerjs.com",
            port=443,
            secure=True,
            config=RTCConfiguration(
                iceServers=[RTCIceServer(urls="stun:stun.l.google.com:19302")]
            )
        )
        
        client_peer = Peer(id="test-client", peer_options=options)
        await client_peer.start()
        
        # Connect to proxy server
        connection = client_peer.connect("computer-agent-proxy")
        
        @connection.on(ConnectionEventType.Open)
        async def connection_open():
            print("Connected to proxy server")
            
            # Send a test request
            request = {
                "model": "anthropic/claude-3-5-sonnet-20241022",
                "input": "Hello from P2P client!"
            }
            await connection.send(json.dumps(request))
        
        @connection.on(ConnectionEventType.Data)
        async def connection_data(data):
            print(f"Received response: {data}")
            await client_peer.destroy()
        
        # Wait for connection
        await asyncio.sleep(10)
        
    except ImportError:
        print("P2P dependencies not available. Install peerjs-python for P2P testing.")
    except Exception as e:
        print(f"P2P test error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "p2p":
        asyncio.run(test_p2p_client())
    elif len(sys.argv) > 1 and sys.argv[1] == "repl":
        asyncio.run(simple_repl())
    else:
        asyncio.run(test_http_endpoint())
