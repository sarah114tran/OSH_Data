import requests
import os
import json
import sys
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
import os
import openai
from openai import OpenAI
import csv
from pathlib import Path
import pandas as pd

client = OpenAI(api_key="YOUR_API_KEY_HERE")

SYSTEM_PROMPT = """

"""

USER_PROMPT_TEMPLATE = """

"""


root = Path("/")
evaluation_results = []

for repo_folder in root.iterdir():
    if not repo_folder.is_dir():
        continue 

    project_name = repo_folder.name
    print(f"\n🔍 Processing project: {project_name}")

    try:
        combined_readme_file = repo_folder / "combined_readmes.md"
        combined_tree_file = repo_folder / "combined_repo_trees.txt"
        
        individual_readme_file = repo_folder / "01_readme.md"
        individual_tree_file = repo_folder / "01_repo_tree.txt"

        readme_content = ""
        directory_structure = ""

        # Some OSH project povide several links. We have combined the Readme files into one combined file and have combined the Repo Trees into another file
        # Therefore, apply the prompt to the combined file, rather than just the individual files
        # Try combined README, fallback to individual
        if combined_readme_file.exists():
            readme_content = combined_readme_file.read_text(encoding="utf-8")
            print(f"   ✅ Found combined README file")
        elif individual_readme_file.exists():
            readme_content = individual_readme_file.read_text(encoding="utf-8")
            print(f"   ✅ Found individual README file")
        else:
            print(f"   ⚠ No README file found - using empty content")
        
        # Try combined tree first, fallback to individual
        if combined_tree_file.exists():
            directory_structure = combined_tree_file.read_text(encoding="utf-8")
            print(f"   ✅ Found combined repo tree file")
        elif individual_tree_file.exists():
            directory_structure = individual_tree_file.read_text(encoding="utf-8")
            print(f"   ✅ Found individual repo tree file")
        else:
            print(f"   ⚠ No repo tree file found - using empty content")

        
        final_prompt = USER_PROMPT_TEMPLATE.format(
            readme_content=readme_content if readme_content else "[No README.md found]",
            directory_structure=directory_structure if directory_structure else "[No repo_tree.txt found]"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.strip()},
                {"role": "user", "content": final_prompt.strip()}
            ],
            temperature=0
        )

        result = response.choices[0].message.content
        print("\nLLM Response:\n")
        print(result)
        print("\n" + "=" * 50 + "\n")

        evaluation_results.append({
            "project": project_name,
            "readme_found": combined_readme_file.exists() or individual_readme_file.exists(),
            "tree_found": combined_tree_file.exists() or individual_tree_file.exists(),
            "output": result
        })

    except Exception as e:
        print(f"❗ Error processing project {project_name}: {e}")

    finally:
        print(f"✅ Finished processing project: {project_name}")

# Save all results as JSON
output_file = root / "revised_prompt_evaluation_results_rd1_nic.json"
try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(evaluation_results, f, indent=4, ensure_ascii=False)
    print(f"\n💾 All evaluation results saved to: {output_file}")
except Exception as e:
    print(f"❗ Error saving results to JSON: {e}")