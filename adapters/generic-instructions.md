# TheBrief outside an Agent Skills environment

Use this adapter for a ChatGPT or Claude project, custom assistant, or ordinary chat that cannot install a `SKILL.md` bundle.

## Project setup

Add the contents of `SKILL.md` as project or assistant instructions. Add the `references/` directory as project knowledge. Keep the relative filenames visible so the model can retrieve the format-specific guidance.

Use this short invocation when needed:

> Используй методику TheBrief. Определи операцию и формат, сохрани смысловой контракт, загрузи только нужные справочные правила и верни результат в установленном формате.

If the environment cannot retrieve individual reference files reliably, combine `methodology.md`, `semantic-preservation.md`, and the single relevant format reference with the request. Avoid loading all format modules into every chat.

The source book is study material, not required runtime context. The distilled references are the operational source of truth.

