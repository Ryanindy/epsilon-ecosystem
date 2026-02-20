from smolagents import tool
import json
import sys
import os
import subprocess
import logging

# --- PROJECT ROOT (Absolute path) ---
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(TOOLS_DIR))

# --- LOGGING ---
logger = logging.getLogger("WholesaleTools")

# Ensure the wholesale script path is available (using absolute path)
sys.path.insert(0, TOOLS_DIR)

# Lazy import to handle cases where execute_deal_analysis might not exist
WholesaleAISystem = None

def _get_wholesale_system():
    """Lazy loader for WholesaleAISystem to handle import errors gracefully."""
    global WholesaleAISystem
    if WholesaleAISystem is None:
        try:
            from execute_deal_analysis import WholesaleAISystem as WAS
            WholesaleAISystem = WAS
        except ImportError as e:
            logger.error(f"Could not import WholesaleAISystem: {e}")
            return None
    return WholesaleAISystem

@tool
def analyze_wholesale_deal(property_data_json: str) -> str:
    """
    Orchestrates the complete wholesale deal analysis workflow.
    Takes a JSON string representing the property data.
    Returns a JSON string of the final analysis and packet.
    Args:
        property_data_json: A JSON string containing the property details, e.g., '{"address": "123 Oak St", "list_price": 150000}'.
    """
    try:
        WAS = _get_wholesale_system()
        if WAS is None:
            return "Error: WholesaleAISystem module not available"

        property_data = json.loads(property_data_json)
        system = WAS(PROJECT_ROOT)
        result = system.analyze_property(property_data)

        return json.dumps(result, indent=2)

    except json.JSONDecodeError as e:
        return f"Error parsing property data JSON: {e}"
    except Exception as e:
        logger.error(f"Deal analysis failed: {e}")
        return f"Error executing deal analysis: {e}"

@tool
def find_real_estate_deals(max_deals: int = 5) -> str:
    """
    Runs the live property sourcing agent to find deals.
    This is a simulation and uses pre-canned data.
    Returns the file path of the generated JSON report.
    Args:
        max_deals: The maximum number of deals to return (ignored by current script, but good for future).
    """
    try:
        script_path = os.path.join(TOOLS_DIR, "live_property_sourcing.py")

        if not os.path.exists(script_path):
            return f"Error: Property sourcing script not found at {script_path}"

        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=PROJECT_ROOT  # Use absolute project root
        )

        # Find the output file path from the script's stdout
        output_file = None
        for line in result.stdout.splitlines():
            if "[OK] RESULTS SAVED TO:" in line:
                output_file = line.split(": ")[1].strip()

        if output_file and os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Script executed but no output file found. STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    except subprocess.TimeoutExpired:
        return "Error: Property sourcing agent timed out after 5 minutes"
    except subprocess.CalledProcessError as e:
        return f"Error running property sourcing agent: {e.stderr}"
    except Exception as e:
        logger.error(f"Property sourcing failed: {e}")
        return f"A general error occurred: {e}"

WHOLESALE_TOOLSET = [analyze_wholesale_deal, find_real_estate_deals]
