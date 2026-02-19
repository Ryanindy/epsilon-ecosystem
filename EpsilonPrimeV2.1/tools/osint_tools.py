import subprocess
import os
import sys
import json
from smolagents import tool

@tool
def run_sherlock(username: str) -> str:
    """
    Finds social media accounts for a given username using Sherlock.
    Args:
        username: The username to search for.
    """
    try:
        # Note: Sherlock can be slow. Using a timeout.
        result = subprocess.run(
            ["sherlock", "--timeout", "20", username],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except FileNotFoundError:
        return "Error: 'sherlock' command not found. Is it installed and in PATH?"
    except subprocess.CalledProcessError as e:
        return f"Sherlock Error: {e.stderr}"

@tool
def run_mr_holmes(module: str, query: str) -> str:
    """
    Executes a specific module from the Mr. Holmes OSINT framework.
    This tool automates the interactive menu of MrHolmes.py.
    Args:
        module: The module to run. Valid options are: 'username', 'phone', 'website', 'email', 'person'.
        query: The target for the module (e.g., a name, an email address).
    """
    holmes_path = "C:/Users/Media Server/Mr.Holmes"
    script_path = os.path.join(holmes_path, "MrHolmes.py")
    
    # Correct mapping based on Mr.Holmes/Core/Support/Menu.py
    module_map = {
        'username': '1',
        'phone': '2',
        'website': '3',
        'email': '8',
        'person': '10' 
    }
    
    selection = module_map.get(module.lower())
    if not selection:
        return f"Error: Invalid Mr. Holmes module. Choose from: {list(module_map.keys())}"

    # We provide the menu selection, then the query, then an exit command ('15' is exit).
    input_script = f"{selection}\n{query}\n15\n"

    try:
        # We must run from the Mr.Holmes directory for it to find its core files.
        result = subprocess.run(
            ["python", script_path],
            input=input_script,
            capture_output=True,
            text=True,
            check=True,
            cwd=holmes_path,
            timeout=180 # 3-minute timeout for potentially long OSINT scans.
        )
        # Clean up the verbose output a bit
        output_lines = result.stdout.splitlines()
        # Find where the actual results start (heuristic)
        start_index = next((i for i, line in enumerate(output_lines) if "------------" in line), 0)
        clean_output = "\n".join(output_lines[start_index:])
        
        return f"Mr. Holmes '{module}' report for '{query}':\n{clean_output}"
    except FileNotFoundError:
        return f"Error: '{script_path}' not found."
    except subprocess.TimeoutExpired:
        return f"Error: Mr. Holmes scan for '{query}' timed out after 180 seconds."
    except subprocess.CalledProcessError as e:
        return f"Mr. Holmes Execution Error: {e.stderr}"

@tool
def run_spiderfoot(target: str, modules: str = None) -> str:
    """
    Runs a Spiderfoot OSINT scan on a specified target.
    Args:
        target: The target of the scan (IP, domain, name, etc.).
        modules: Optional. Comma-separated list of modules to enable (e.g., 'sfp_whois,sfp_shodan').
    """
    sf_path = "C:/Users/Media Server/EpsilonPrimeV2.1/tools/osint/spiderfoot"
    script_path = os.path.join(sf_path, "sf.py")
    
    command = [sys.executable, script_path, "-s", target, "-o", "json"]
    if modules:
        command.extend(["-m", modules])
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=sf_path,
            timeout=300 # 5-minute timeout
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Spiderfoot Error: {e}"

@tool
def query_cylect(query: str) -> str:
    """
    Performs an OSINT search on Cylect.io for a given query.
    Args:
        query: The search term (e.g., name, phone, email).
    """
    # This is a placeholder for a browser-based tool or a direct API if available.
    # For now, we direct the agent to use the browser_operator skill.
    return f"Instruction: Use the 'browser_operator' skill to navigate to 'https://cylect.io' and search for '{query}'."

@tool
def run_theharvester(domain: str, limit: int = 500, source: str = "all") -> str:
    """
    Runs theHarvester to gather subdomains, emails, names, and more.
    Args:
        domain: The target domain to scan.
        limit: Limit of results to gather.
        source: Source to search (e.g., 'google', 'bing', 'hunter', 'all').
    """
    command = ["theHarvester", "-d", domain, "-l", str(limit), "-b", source]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"theHarvester Error: {e}"

@tool
def run_recon_cli(module: str, target: str) -> str:
    """
    Runs a recon-ng module via recon-cli.
    Args:
        module: The recon-ng module to run (e.g., 'recon/domains-hosts/google_site_web').
        target: The target for the module (e.g., a domain).
    """
    recon_path = "C:/Users/Media Server/EpsilonPrimeV2.1/tools/osint/recon-ng"
    script_path = os.path.join(recon_path, "recon-cli")
    
    command = [sys.executable, script_path, "-m", module, "-o", f"SOURCE={target}", "-x"]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=recon_path,
            timeout=300
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"recon-cli Error: {e}"

@tool
def generate_osint_report(target: str, findings_json: str) -> str:
    """
    Generates a comprehensive OSINT report from tool findings.
    Args:
        target: The name/domain of the target.
        findings_json: A JSON string containing 'summary', 'tools' (dict), and 'web' (dict) data.
    """
    import sys
    sys.path.append("C:/Users/Media Server/EpsilonPrimeV2.1/tools/osint")
    from generate_report import generate_report
    
    try:
        findings = json.loads(findings_json)
        report_path = generate_report(target, findings)
        return f"Success: Report generated at {report_path}"
    except Exception as e:
        return f"Error generating report: {e}"

OSINT_TOOLSET = [run_sherlock, run_mr_holmes, run_spiderfoot, query_cylect, run_theharvester, run_recon_cli, generate_osint_report]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="OSINT Tool Interface")
    subparsers = parser.add_subparsers(dest="command")

    # Sherlock
    parser_sherlock = subparsers.add_parser("run_sherlock")
    parser_sherlock.add_argument("username")

    # Mr. Holmes
    parser_holmes = subparsers.add_parser("run_mr_holmes")
    parser_holmes.add_argument("module", choices=['username', 'phone', 'website', 'email', 'person'])
    parser_holmes.add_argument("query")

    # Spiderfoot
    parser_sf = subparsers.add_parser("run_spiderfoot")
    parser_sf.add_argument("target")
    parser_sf.add_argument("--modules", help="Comma-separated modules")

    # Cylect
    parser_cylect = subparsers.add_parser("query_cylect")
    parser_cylect.add_argument("query")

    # theHarvester
    parser_th = subparsers.add_parser("run_theharvester")
    parser_th.add_argument("domain")
    parser_th.add_argument("--limit", type=int, default=500)
    parser_th.add_argument("--source", default="all")

    # recon-cli
    parser_recon = subparsers.add_parser("run_recon_cli")
    parser_recon.add_argument("module")
    parser_recon.add_argument("target")

    # Report Generator
    parser_report = subparsers.add_parser("generate_report")
    parser_report.add_argument("target")
    parser_report.add_argument("findings_source", help="JSON string or path to JSON file")

    args = parser.parse_args()

    if args.command == "run_sherlock":
        print(run_sherlock(args.username))
    elif args.command == "run_mr_holmes":
        print(run_mr_holmes(args.module, args.query))
    elif args.command == "run_spiderfoot":
        print(run_spiderfoot(args.target, args.modules))
    elif args.command == "query_cylect":
        print(query_cylect(args.query))
    elif args.command == "run_theharvester":
        print(run_theharvester(args.domain, args.limit, args.source))
    elif args.command == "run_recon_cli":
        print(run_recon_cli(args.module, args.target))
    elif args.command == "generate_report":
        source = args.findings_source
        if os.path.isfile(source):
            with open(source, 'r', encoding='utf-8') as f:
                source = f.read()
        print(generate_osint_report(args.target, source))
    else:
        parser.print_help()
