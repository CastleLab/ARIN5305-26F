A simple way to run **Codex powered by `deepseek-v4-flash`** on Windows and macOS without installing heavy developer toolchains or building Node.js environments is through the **ChatGPT Desktop App** using DeepSeek's automated setup script. On Linux, the same DeepSeek configuration can be used in a graphical user interface with the **Codex IDE extension for VS Code**; the official ChatGPT Desktop App is currently available on Windows and macOS, not Linux.

Codex shares its backend system configuration (`~/.codex/config.toml`) across all clients. On Windows, this file is under your user profile (for example, `%USERPROFILE%\.codex\config.toml`); on macOS/Linux, it is `~/.codex/config.toml`. Setting it up once instantly makes **DeepSeek-V4-Flash** available across supported Codex clients.

---

### Prerequisites (1 Minute Setup)

1. **Get a DeepSeek API Key:** Log in to [platform.deepseek.com](https://platform.deepseek.com) and copy an API key starting with `sk-`.
2. **Install and launch a Codex client once:** This allows Codex to generate its configuration folder (`.codex`).
   - **Windows:** Install and launch the official **ChatGPT Desktop App**, which includes Codex.
   - **macOS:** Install and launch the official **ChatGPT Desktop App**, which includes Codex.
   - **Linux:** Install and launch the **Codex IDE extension for VS Code** once. The official ChatGPT Desktop App is not currently available for Linux.

---

1. **Run the 1-Line Setup:** Executes DeepSeek's official automated configuration.

   **Windows**

   1. Open **PowerShell** on your Windows PC (Press `Win + X` and select **PowerShell** or **Terminal**).
   2. Paste and run DeepSeek's official PowerShell configuration command:

   ```powershell
   irm https://cdn.deepseek.com/api-docs/codex-deepseek-setup-en.ps1 | iex
   ```

   **macOS / Linux**

   1. Open **Terminal**.
   2. Paste and run DeepSeek's official shell configuration command:

   ```bash
   bash <(curl -fsSL https://cdn.deepseek.com/api-docs/codex-deepseek-setup-en.sh)
   ```
2. **Configure the Model Provider:** Select DeepSeek-V4-Flash and enter API credential.

   1. When prompted by the script, paste your **DeepSeek API Key** (`sk-...`).
   2. Select **Option 1** (`deepseek-v4-flash`).
   3. The script will automatically write the necessary `models.json` metadata and register `[model_providers.deepseek]` in your system configuration.
3. **Launch the App / Client:** Start using Codex with DeepSeek-V4-Flash.

   **Windows**

   1. Open the **ChatGPT Desktop / Codex** application.
   2. Under the model selection dropdown, the model may appear as **`DeepSeek-V4-Flash`** or **`Custom`**. When `Custom` is shown after this configuration, Codex is using the DeepSeek model selected by the setup script.
   3. Open any workspace directory or project folder and start prompting your agent.

   **macOS**

   1. Open the **ChatGPT Desktop / Codex** application.
   2. Under the model selection dropdown, the configured DeepSeek model is typically shown as **`Custom`**.
   3. Open any workspace directory or project folder and start prompting your agent.

   **Linux**

   1. Open the project in **VS Code** and use the **Codex IDE extension**; it reads the same `~/.codex/config.toml` configuration.
      If the startup banner shows `model: deepseek-v4-flash`, the configuration is active.

---

### Advantages

* **Zero per-client model configuration:** You configure DeepSeek once in the shared Codex configuration instead of setting up each Codex client separately.
* **No local Node.js build environment required for the DeepSeek configuration:** The automated setup script writes the required Codex configuration directly.
* **Graphical User Interface (GUI):** You interact with the agent through the ChatGPT Desktop App (Windows & macOS) and the Codex VS Code extension (Linux) with workspace and visual diff support.
