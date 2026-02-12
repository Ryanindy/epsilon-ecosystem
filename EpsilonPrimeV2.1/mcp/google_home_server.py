import pychromecast
import threading
import time
from typing import List, Dict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Google Home Local")

# Global state for discovered devices
discovered_devices = {}
browser = None

def discover_loop():
    """
    Background thread to keep device list updated.
    """
    global browser
    def callback(chromecast):
        discovered_devices[chromecast.name] = chromecast
        print(f"[Google Home] Discovered: {chromecast.name} ({chromecast.model_name})")

    def stop_callback(chromecast):
        if chromecast.name in discovered_devices:
            del discovered_devices[chromecast.name]
            print(f"[Google Home] Lost: {chromecast.name}")

    browser = pychromecast.get_chromecasts(blocking=False, callback=callback, stop_callback=stop_callback)

# Start discovery immediately
threading.Thread(target=discover_loop, daemon=True).start()

@mcp.tool()
def list_devices() -> List[Dict[str, str]]:
    """
    Lists all discovered Google Home / Chromecast devices on the local network.
    Returns a list of dictionaries with 'name', 'model', and 'uuid'.
    """
    devices = []
    # Force a quick scan if empty (though the thread handles this)
    if not discovered_devices:
        cc_list, _ = pychromecast.get_chromecasts()
        for cc in cc_list:
            discovered_devices[cc.name] = cc

    for name, cc in discovered_devices.items():
        devices.append({
            "name": name,
            "model": cc.model_name,
            "uuid": str(cc.uuid),
            "ip_address": str(cc.host),
            "status": cc.status.status_text if cc.status else "unknown"
        })
    return devices

@mcp.tool()
def play_media(device_name: str, url: str, content_type: str = "audio/mp3") -> str:
    """
    Casts media (audio/video) to a specific Google Home device.
    Args:
        device_name: The name of the device (from list_devices).
        url: The HTTP URL of the media file.
        content_type: MIME type (e.g., 'audio/mp3', 'video/mp4').
    """
    cc = discovered_devices.get(device_name)
    if not cc:
        return f"Error: Device '{device_name}' not found."
    
    try:
        cc.wait()
        mc = cc.media_controller
        mc.play_media(url, content_type)
        mc.block_until_active()
        return f"Playing on {device_name}: {url}"
    except Exception as e:
        return f"Error playing media: {e}"

@mcp.tool()
def set_volume(device_name: str, level: float) -> str:
    """
    Sets the volume of a Google Home device.
    Args:
        device_name: The name of the device.
        level: Volume level between 0.0 and 1.0.
    """
    cc = discovered_devices.get(device_name)
    if not cc:
        return f"Error: Device '{device_name}' not found."
    
    try:
        cc.wait()
        cc.set_volume(level)
        return f"Volume set to {level} on {device_name}."
    except Exception as e:
        return f"Error setting volume: {e}"

@mcp.tool()
def speak_text(device_name: str, text: str) -> str:
    """
    Uses Google TTS to speak text on the device.
    Note: This uses the Google Translate internal API via pychromecast's media controller
    or requires a public URL for the TTS mp3.
    For this 'God Mode' implementation, we'll assume a lightweight TTS URL generator.
    """
    # Quick hack for TTS: Use a public TTS API (e.g., google-translate-proxy)
    # Ideally, we'd host a local TTS, but we want zero-dependency.
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text}&tl=en&client=tw-ob"
    return play_media(device_name, tts_url, "audio/mp3")

if __name__ == "__main__":
    print("[Google Home MCP] Server Running...")
    mcp.run()
