# Security Policy

Thanks for helping keep this project safe.

##  Supported Versions

This repo doesn’t publish formal releases yet. Support is:
- **`main` branch** – ✅ actively supported
- **Tagged commits older than 6 months** – ❌ not supported

If/when versioned releases start (e.g., `v1.x`), this section will switch to a proper table.

---

##  Reporting a Vulnerability

Please report vulnerabilities **privately**:

- **Preferred:** GitHub Security Advisory (Go to: “Security” tab → “Report a vulnerability”)  
  <https://github.com/<ginesthoii>/<your-repo>/security/advisories/new>
- **Fallback:** Email: **oliviagriffindev@gmail.com** 

**Please include:**
- A clear description of the issue and impact
- Steps/PoC to reproduce (minimal code/inputs)
- Affected file(s) and commit/tag if known
- Any suggested fixes or mitigations

**Do not** open a public issue for vulnerabilities.

---

##  Response & Disclosure Timeline

- **Acknowledgement:** within **3 business days**
- **Triage/assessment:** within **7 business days**
- **Fix & release/patch:** typical target **≤ 30 days**, severity-dependent
- **Coordinated disclosure:** we’ll agree on a public disclosure date once a fix/mitigation is available (default **90 days** max unless higher risk warrants faster disclosure)

We’re happy to **credit you** in release notes/advisory unless you prefer to remain anonymous.

---

##  In Scope

- Code execution, injection, or sandbox escapes in scripts
- Path traversal or unsafe file writes in utilities (e.g., file organizer)
- Credential/API key leakage through code or logs
- Logic flaws that bypass intended security checks
- Dependency issues **introduced by this repo’s configuration** (e.g., unsafe defaults)

##  Out of Scope

- Social engineering, phishing, or attacks on individuals
- Denial of Service that requires unreasonable inputs or hostile local environments
- Vulnerabilities that require local admin/root access already
- Issues in **third-party services** (e.g., OpenWeather) or libraries (e.g., `qrcode`) that aren’t caused by our usage
- Missing security headers on GitHub Pages or non-existent web endpoints
- Typos or minor non-security bugs (open a normal issue instead)

---

##  Handling Secrets

- Never include real API keys in issues, PoCs, or PRs
- This repo ignores `.env` via `.gitignore`; please keep it that way
- If you accidentally committed a secret, rotate it immediately and let us know privately

---

##  Dependencies

- Runtime deps (e.g., `requests`, `qrcode[pil]`) are listed in `requirements.txt`
- If you find a vulnerability in a dependency **that affects this project’s usage**, report it to us and also to the upstream project if appropriate

---

##  Safe Harbor

We will not pursue or support legal action against you for **good-faith** security research that:
- Respects privacy and data (use local clones, not real user data)
- Avoids service disruption
- Follows responsible disclosure above

Thank you for helping improve security ❤!
