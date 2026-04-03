# TUFF-OS Isolation Mode: Recovery Procedures

Isolation Mode is the final defense mechanism of TUFF-OS.
Once triggered, **all standard logins and commands are completely rejected**, and the system enters a disconnected state at both the physical and network layers. Recovery is **strictly limited**, by design, to prevent accidental release or deactivation by an attacker.

### Conditions for Recovery (The Sole Authorized Path)

Recovery is possible **only if all of the following conditions are met**:

1. The user has administrative privileges (root or admin rights granted).
2. The correct Recovery PIN (12+ digits, generated and encrypted during installation).
3. The system is in a physically secure state (no tampering detected).

**Standard users**, **individuals who do not know the PIN**, and **attackers who have not compromised the PIN** can **never recover the system**.

### Recovery Procedure (Step-by-Step)

#### Step 1: Verify the Current State (Optional but Highly Recommended)

- Confirm that the lockout screen displays "System Isolated" or "TUFF-OS Isolation Mode Active."
- If possible, check witness.log from another terminal (e.g., via USB).
  - There should be a final record stating: "Isolation mode triggered by ..."

#### Step 2: Prepare the Recovery PIN

- Open the **TUFFkey.json** file generated during installation (USB drive recommended).
  - Locate the field `"recovery_pin": "XXXXXXXXXXXX"`.
- To avoid input errors, **write the PIN on paper** or keep it in a secure offline location.

**If the PIN is lost:**
- Reinstallation (total data wipe) is the only option.
- If restoring from a backup, a **restore from external storage** will be required.

#### Step 3: Execute the Recovery Command

Run the following command from **CUI mode** (VGA text screen) or via **SSH/Serial Console**:

```bash
tuffutl sys isolation recover --pin XXXXXXXXXXXX
```

- Enter the 12-digit PIN after the `--pin` argument.
- If the PIN is correct, processing begins immediately (Duration: approx. 2–5 seconds).

**Example Output on Success:**
```
Recovery PIN accepted.
Zeroizing remaining session data... OK
Clearing Isolation Persistent flag... OK
Reinitializing I/O Gatekeeper... OK
Network defense rules restored... OK
System recovered from Isolation mode.
Please login again.
```

**Common Error Examples:**

| Error Message | Cause | Action |
|:---|:---|:---|
| Invalid Recovery PIN | Incorrect PIN | Re-enter the correct PIN (Temporarily locked after 3 failures). |
| Isolation not active | Already released | Normal login should be possible. |
| Consensus Failure | 3N Mismatch (Tampering?) | Replace disk then run `fsck --repair`. |
| Hardware ID mismatch | Disk removal/tampering | Full reinstallation required. |

#### Step 4: Mandatory Post-Recovery Actions

1. **Immediate Login**
   ```bash
   tuffutl sys login <your_id> --password <your_pw>
   ```

2. **Verify State**
   ```bash
   tuffutl sys status --detail
   ```
   - Confirm that "Isolation: Inactive" is displayed.

3. **Check Audit Trail**
   ```bash
   tuffutl log tail --lines 50
   ```
   - Verify the record: "Isolation recovered at ..." (PQC signed).

4. **Preventative Measures** (Highly Recommended)
   - Identify the trigger cause (inspect witness.log).
   - Change your password (`tuffutl user password`).
   - Review network policies (`tuffutl nw blacklist` / `aiserverlist`).
   - Strengthen physical access controls.

---

### Summary of Key Rules

- **Never leak the PIN.**
  - Loss results in mandatory total data reconstruction (Backup is essential).
- **Do not trust the system immediately after recovery.**
  - Run `fs fsck` and `nw status` immediately to ensure no lingering anomalies.
- **Training Recommended.**
  - Periodically conduct drills: `tuffutl sys isolation trigger` → `recover`.

### Operational Tips

- **PIN Management**: Store on paper in a safe, or in an encrypted offline-only password manager.
- **Prohibit Automatic Recovery**: Manually requiring human intervention prevents automated attacks.
- **Enhanced Monitoring**: Use a separate terminal to monitor `tuffutl log tail | grep Isolation`.

Isolation Mode embodies the ultimate TUFF-OS philosophy: "**Once triggered, only a trusted administrator can bring it back.**"
