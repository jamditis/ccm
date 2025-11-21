# Repository structure

All project code and assets now live under the `tools` directory. Each tool or application has its own subfolder:

- `tools/ccm-app/`: primary application that previously lived at the repository root. All original source, configuration, and documentation files are now contained here.
- `tools/llm-advisor/`: existing `LLM-advisor` artifact moved into its dedicated tool folder.

To run the main app, change into `tools/ccm-app/` and use the usual Node scripts (e.g., `npm install`, `npm run dev`).
