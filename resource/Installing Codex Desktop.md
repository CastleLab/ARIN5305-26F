A simple way to run **Codex powered by `deepseek-flash`** on Windows and macOS without installing heavy developer toolchains or building Node.js environments is through the **ChatGPT Desktop App** using DeepSeek's automated setup script. On Linux, the same DeepSeek configuration can be used in a graphical user interface with the **Codex IDE extension for VS Code**; the official ChatGPT Desktop App is currently available on Windows and macOS, not Linux.

Codex shares its backend system configuration (`~/.codex/config.toml`) across all clients. On Windows, this file is under your user profile (for example, `%USERPROFILE%\.codex\config.toml`); on macOS/Linux, it is `~/.codex/config.toml`. Setting it up once instantly makes **DeepSeek-Flash** available across supported Codex clients.

---

### Prerequisites (1 Minute Setup)

1. **Get a DeepSeek API Key:** 
 We provide each student with a private API key with some free quota to use DeepSeek-Flash for assignments. Please check the comment for the assignment named **DeepSeek-Flash API Key** on [this Canvas page](https://canvas.ust.hk/courses/71922/grades).
2. **Install and launch a Codex client once:** This allows Codex to generate its configuration folder (`.codex`).
   - **Windows:** Install the official **ChatGPT Desktop App** from the Microsoft Store or [this link](https://get.microsoft.com/installer/download/9PLM9XGG6VKS?cid=website_cta_psi) and launch the installed App once, which includes Codex.
   - **macOS:** Install the official **ChatGPT Desktop App** from [this link](https://persistent.oaistatic.com/codex-app-prod/ChatGPTInstaller.dmg) and launch the installed App once, which includes Codex.
   - **Linux:** Install and launch the **Codex IDE extension for VS Code** once. The official ChatGPT Desktop App is not currently available for Linux.

---

### Setup Steps

1. **Run the 1-Line Setup:** Executes DeepSeek's official automated configuration.

   **Windows**

   1. Open **PowerShell** on your Windows PC (Press `Win + X` and select **PowerShell** or **Terminal**).
   2. Paste and run DeepSeek's official PowerShell configuration command with the API endpoint replaced to point to our relay server:

 ```powershell
 (irm https://cdn.deepseek.com/api-docs/codex-deepseek-setup-en.ps1).Replace('https://api.deepseek.com/', 'http://sccpu6.cse.ust.hk/v1/') | iex
 ```

   **macOS / Linux**

   1. Open **Terminal**.
   2. Paste and run DeepSeek's official shell configuration command with the API endpoint replaced to point to our relay server:

 ```bash
   bash <(curl -fsSL https://cdn.deepseek.com/api-docs/codex-deepseek-setup-en.sh | sed 's|https://api\.deepseek\.com/|http://sccpu6.cse.ust.hk/v1/|g')
 ```

2. **Configure the Model Provider:** Select DeepSeek-Flash and enter the API credential.

   1. When prompted by the script, paste your **DeepSeek API Key** (`sk-...`) provided by us (available in the comment for the assignment named **DeepSeek-Flash API Key** on [this Canvas page](https://canvas.ust.hk/courses/71922/grades)).
   2. Select **Option 1** (`deepseek-flash`).
   3. The script will automatically write the necessary `models.json` metadata and register `[model_providers.deepseek]` in your system configuration.

3. **Launch the App / Client:** Start using Codex with DeepSeek-Flash.

   **Windows/macOS**

   1. Open the **ChatGPT Desktop / Codex** application.
   2. Under the model selection dropdown, the model may appear as **`DeepSeek-Flash`** or **`Custom`**. When `Custom` is shown after this configuration, Codex is using the DeepSeek model selected by the setup script.
   3. Open any workspace directory or project folder and start prompting your agent.

   **Linux**

   1. Open the project in **VS Code** and use the **Codex IDE extension**; it reads the same `~/.codex/config.toml` configuration.
 If the startup banner shows `model: deepseek-flash`, the configuration is active.

---

### Advantages

* **Zero per-client model configuration:** You configure DeepSeek once in the shared Codex configuration instead of setting up each Codex client separately.
* **No local Node.js build environment required for the DeepSeek configuration:** The automated setup script writes the required Codex configuration directly.
* **Graphical User Interface (GUI):** You interact with the agent through the ChatGPT Desktop App (Windows & macOS) and the Codex VS Code extension (Linux) with workspace and visual diff support.

---

### Notes

1. Upon using the API key provided by us, you have agreed to use the key only for the programming assignments of the course, and to keep the key to yourself. Violation of these agreements will result in revocation of the key immediately.

2. The relay server `http://sccpu6.cse.ust.hk/v1/` is only accessible within the campus network of HKUST. If you are off-campus, please install [HKUST VPN](https://itso.hkust.edu.hk/services/cyber-security/vpn) to connect to the campus network before using Codex connected to our relay server.

3. You can check the remaining quota of the API key provided by us by visiting [http://sccpu6.cse.ust.hk/](http://sccpu6.cse.ust.hk/) and entering your API key in the input box. Note that the website is also only accessible within the campus network of HKUST or through the HKUST VPN.

4. When your quota given by us is used up and you want to use your own DeepSeek API official key quota purchased by yourself, please run the original DeepSeek setup script **without the relay server replacement** (command listed below) twice to remove the relay server configuration (using option 9) and set your own DeepSeek API key (using option 1 with your own key), respectively. The original DeepSeek setup script is:
```powershell
# Windows
irm https://cdn.deepseek.com/api-docs/codex-deepseek-setup-en.ps1 | iex
```
```bash
# macOS / Linux
bash <(curl -fsSL https://cdn.deepseek.com/api-docs/codex-deepseek-setup-en.sh)
```
You may need to purchase quota and create your own DeepSeek API key at [DeepSeek official platform](https://platform.deepseek.com/api_keys).

5. In addition to the ChatGPT Desktop App, you can also use the OpenAI Codex CLI, which provides a terminal interface to interact with Codex. The installation instructions for Codex CLI are available at the [Codex official repository](https://github.com/openai/codex). Upon installation, please follow the same setup steps to configure Codex to use the DeepSeek-Flash model through our relay server. Note that the Codex CLI shares the same configuration file as the ChatGPT Desktop App, so you don't need to configure it separately if you have already set up the DeepSeek-Flash model in the ChatGPT Desktop App.
