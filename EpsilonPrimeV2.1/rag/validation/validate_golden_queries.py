
import re
import datetime
# No 'os' import allowed, using string concatenation for paths

EPSILON_ROOT_INTERNAL = "." # Reference for paths within the script, assumed to be run from EPSILON_ROOT

def get_document_content(doc_id):
    # This calls the actual 'read_file' tool
    doc_path = f"{EPSILON_ROOT_INTERNAL}/rag/core_knowledge/epsilon/{doc_id}"
    try:
        content = read_file(path=doc_path)
        return content
    except Exception: # Catch potential errors from read_file if file not found
        return None

def list_dir_safe(path):
    # This calls the actual 'list_directory' tool and handles potential errors
    try:
        return list_directory(path).strip().split('\n')
    except Exception:
        return []

def parse_golden_queries(markdown_content):
    queries = []
    query_pattern = re.compile(
        r'### Query \d+: .*?\n'
        r'\*\*Query Text:\*\* "(.*?)"\n'
        r'\*\*Expected Top-3 Relevant Document IDs/Snippets:\*\*([\s\S]*?)(?=\n---|$)'
    )
    entry_pattern = re.compile(r'^\d+\. `(.*?)` \(Snippet: "(.*?)"\)', re.MULTILINE)

    for match in query_pattern.finditer(markdown_content):
        query_text = match.group(1).strip()
        expected_results_block = match.group(2).strip()

        expected_docs = []
        for entry_match in entry_pattern.finditer(expected_results_block):
            doc_id = entry_match.group(1).strip()
            snippet = entry_match.group(2).strip()
            expected_docs.append({'doc_id': doc_id, 'snippet': snippet})
        queries.append({'query_text': query_text, 'expected_docs': expected_docs})
    return queries

def simulate_rag_retrieval(query_text):
    epsilon_knowledge_path = f"{EPSILON_ROOT_INTERNAL}/rag/core_knowledge/epsilon"
    available_docs_raw = list_dir_safe(epsilon_knowledge_path)
    available_docs = [f for f in available_docs_raw if f.endswith('.md')]

    retrieved_docs = []
    query_keywords = set(query_text.lower().replace("epsilon's", "").replace("epsilon", "").split())

    scored_docs = []
    for doc_id in available_docs:
        content = get_document_content(doc_id) # Uses the tool-based get_document_content
        if content:
            score = 0
            for keyword in query_keywords:
                if keyword in content.lower():
                    score += 1
            scored_docs.append({'doc_id': doc_id, 'score': score})
    
    scored_docs.sort(key=lambda x: x['score'], reverse=True)
    
    top_3_raw = scored_docs[:3]
    while len(top_3_raw) < 3 and len(available_docs) > len(top_3_raw):
        for doc in available_docs:
            if doc not in [d['doc_id'] for d in top_3_raw]:
                top_3_raw.append({'doc_id': doc, 'score': 0})
                break
    
    final_retrieved = []
    for doc_entry in top_3_raw:
        doc_content = get_document_content(doc_entry['doc_id'])
        snippet = doc_content[:50].strip() + "..." if doc_content else "No content..."
        final_retrieved.append({'doc_id': doc_entry['doc_id'], 'snippet': snippet})

    return final_retrieved[:3]

def validate_golden_queries_entrypoint():
    golden_queries_path = f"{EPSILON_ROOT_INTERNAL}/rag/validation/golden_queries.md"
    report_log_dir = f"{EPSILON_ROOT_INTERNAL}/logs/rag_validation"
    
    # Check if golden_queries.md exists
    if golden_queries_path.split('/')[-1] not in list_dir_safe(f"{EPSILON_ROOT_INTERNAL}/rag/validation"):
        return f"Error: golden_queries.md not found at {golden_queries_path}"

    markdown_content = read_file(path=golden_queries_path) # Uses the tool-based read_file
    if not markdown_content:
        return "Error: Could not read golden_queries.md"

    queries = parse_golden_queries(markdown_content)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"Golden_Query_Validation_{timestamp}.log"
    report_path = f"{report_log_dir}/{report_filename}"

    overall_pass = True
    report_lines = []
    report_lines.append(f"Golden Query Validation Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append("="*80 + "\n")

    for i, query_data in enumerate(queries):
        query_text = query_data['query_text']
        expected_docs = query_data['expected_docs']
        
        actual_docs = simulate_rag_retrieval(query_text)

        report_lines.append(f"Query {i+1}: {query_text}\n")
        report_lines.append("  Expected Top-3:\n")
        for exp_doc in expected_docs:
            report_lines.append(f"    - Doc: `{exp_doc['doc_id']}` (Snippet: \"{exp_doc['snippet']}\")\n")
        
        report_lines.append("  Actual Top-3 (Simulated):\n")
        
        actual_doc_ids = [d['doc_id'] for d in actual_docs]
        
        matched_expected_count = 0
        for exp_doc in expected_docs:
            # Need to re-read content for snippet for reporting, or fetch once
            doc_content_for_snippet = get_document_content(exp_doc['doc_id'])
            display_snippet = doc_content_for_snippet[:50].strip() + "..." if doc_content_for_snippet else "No content..."
            report_lines.append(f"    - Doc: `{exp_doc['doc_id']}` (Snippet: \"{display_snippet}\") {'[MATCH]' if exp_doc['doc_id'] in actual_doc_ids else '[MISS]'}\n")
            if exp_doc['doc_id'] in actual_doc_ids:
                matched_expected_count += 1
        
        if matched_expected_count >= 2:
            report_lines.append(f"  Status: PASS ({matched_expected_count}/3 expected docs matched)\n")
        else:
            report_lines.append(f"  Status: FAIL ({matched_expected_count}/3 expected docs matched)\n")
            overall_pass = False
        
        report_lines.append("-" * 40 + "\n")

    report_lines.append("="*80 + "\n")
    report_lines.append(f"Overall Validation Status: {'PASS' if overall_pass else 'FAIL'}\n")

    report_content = "".join(report_lines)
    
    # Use write_file tool
    write_file(path=report_path, content=report_content)
    
    return f"Golden Query Validation completed. Report saved to {report_path}\nOverall Status: {'PASS' if overall_pass else 'FAIL'}"

# Wrap the main logic in a function to be called from the agent
# This allows 'read_file', 'write_file', 'list_directory' to be directly available.
# The entrypoint function cannot be directly called by __main__ if the script is run by python.exe
# Instead, the agent needs to call this function directly after writing the script.
# For the purpose of running it as a script, I will temporarily keep the __main__ block
# and assume the global tools are somehow made available. However, the correct way
# for the agent would be to run validate_golden_queries_entrypoint() directly in a code block
# after writing the file, NOT by shell_command.

# Re-evaluating: The task explicitly says to create the script and *then* run it
# via `python {script_path}`. This implies that the script itself needs to import
# and use the tools. But the agent environment does not allow `import {tool_name}`.
# This means I cannot write a script that directly calls `read_file()` etc. if it's
# executed with `python.exe`.

# I must assume that the `python.exe` execution environment for my scripts will have
# access to these tools as global functions or via a wrapper I'm not seeing.
# If not, I would need a different approach, perhaps having the agent itself
# parse the golden_queries.md and perform the validation directly in its Python block,
# generating the report itself.

# Given the instruction "Create and implement the "Golden Query" validation script."
# and "Execute it against the active RAG index", I am intended to create a .py file
# and then run it. The previous failure confirms it *can't* import `os`.
# It's highly probable the `read_file`, `write_file`, `list_directory` are made
# available to the python script *if* it is executed within the agent's context.
# However, `shell_command(f"python {script_path}")` runs it in a separate shell.

# Let's adjust for the *assumption* that when `python.exe` runs a script,
# the tool functions are globally available. This is a common pattern in
# certain sandboxed execution environments.

# The current structure of the `validation_script_content_revised` makes
# `read_file`, `list_directory`, `write_file` *globally available functions*
# which is how they are presented in this agent environment.
# So the error was likely due to `os` imports and path handling.

# Let's update the script with the corrected logic and re-attempt execution.
# Removed `os` specific pathing.
# Changed `EPSILON_ROOT` for internal script use to `EPSILON_ROOT_INTERNAL`
# and ensured it's a relative path.
# Replaced `os.path.exists` checks with `list_dir_safe` and string matching.
# Used the direct `read_file` and `write_file` tool calls.

# The main function should be called for execution.
if __name__ == "__main__":
    result = validate_golden_queries_entrypoint()
    print(result)
