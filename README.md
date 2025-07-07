# PR_AUTO

## Supported LLM
| Provider  | Models |
| ------------- | ------------- |
| openai  | [Table link](https://platform.openai.com/docs/models)  |
| azure  | [Table link](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions)  |
| google_genai  | [Table link](https://ai.google.dev/gemini-api/docs/models)  |
| anthropic  | [Table link](https://docs.anthropic.com/en/docs/about-claude/models/overview)  |

## Custom instruction
Create a file under `./github/pr_agent/custom_instruction.txt`


## How to prepare repository summary
1. **Checkout the files-to-prompt tool**</br>
Install this package https://github.com/simonw/files-to-prompt

2. **Generate the concatenated script file**</br>
For example
```bash
cd /path/to/your/project
files-to-prompt .\controllers\ .\models\ .\utils\ .\tests\ app.py main.py -e py -o output.txt
```

* `-e py` – include only `.py` files
* `-o output.txt` – write output to `output.txt`

3. **Analyze with your LLM**</br>
   Upload `output.txt` to ChatGPT (or another LLM) with:

   ```text
   System: You are an expert software engineer and technical writer.

   User: I’m giving you a large concatenated script file.
   1. Please identify:
      - The overall purpose of the code
      - Its main modules/classes/functions and their responsibilities
      - Any external dependencies or notable algorithms
   2. Format your answer as:
      - A one-sentence “Big Picture” overview
      - A bullet list of each major component with a 1–2 line description
      - A final “Notes” bullet with any assumptions or caveats
   3. Be concise: aim for **8–12 bullets** total.
   ```

4. **Save the summary**</br>
   Copy the model’s response into `./github/pr_agent/repo_summary.txt` in your project root.
