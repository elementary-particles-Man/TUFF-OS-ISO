# Backup and Restore Procedures (Step-by-Step)

The following describes the detailed procedures for **restoring from a backup** in **TUFF-OS**.

This procedure is required in any of the following situations:
- Reinstallation after losing the Recovery PIN.
- Total loss or replacement of physical disks.
- Intentional data reset.
- Migration from a test environment to production.

### CRITICAL WARNING (Read First)

- **ALL EXISTING DATA ON THE TARGET WILL BE OVERWRITTEN.**
  - **Perform a full backup of current data** to another location before starting the restore.
- The backup source must be on **secure storage outside of TUFF-OS** (e.g., external HDD, NAS, or encrypted cloud storage).
- **DO NOT POWER OFF** during the restore. While the system is designed with automatic rollback, using a **UPS** is highly recommended.

---

### Restore Procedure (Step-by-Step)

#### Step 1: Verify Backup Data Readiness

1. **Confirm the Backup Source**
   - Recommended formats: **TUFF-FS compatible RAW image** (via `dd`) or **Logical Backup** (via `tuffutl export`).
   - Example filenames:
     - `tuff_backup_20260322.tar.zst` (Logical backup)
     - `jbod_backup.img` (Physical JBOD full image)

2. **Check Backup Integrity**
   ```bash
   # For logical backups
   tuffutl backup verify --file tuff_backup_20260322.tar.zst

   # For physical images
   sha256sum jbod_backup.img
   # Ensure it matches the previously recorded hash.
   ```

3. Copy the backup to your **restore-ready storage** (e.g., external HDD).

#### Step 2: TUFF-OS Reinstallation (If PIN is lost or disks dead)

1. Boot from the USB installer.
   - Set USB as the top priority in BIOS/UEFI.
2. Select "**Complete Reinstallation (Total Data Wipe)**."
   - Confirm the two warning dialogs.
3. Select target disks:
   - SSD (System area).
   - HDDs (JBOD Pool: Minimum 3, recommended 5).
4. A new Recovery PIN is generated.
   - **Record it on paper** + **Save it encrypted to the USB drive**. (Crucial!)
5. Reboot and allow Genesis re-initialization on first boot.

#### Step 3: Execute Restore

**Method A: Restore from Logical Backup (Recommended, Fast)**

```bash
# 1. Copy the backup file into TUFF-OS
# (Mount the USB/HDD and copy the file)

# 2. Run the restore command
tuffutl backup restore \
  --file /mnt/external/tuff_backup_20260322.tar.zst \
  --target /data \
  --commit auto \
  --verify

# Option breakdown
--file        Path to backup file (Required)
--target      Destination root path (e.g., /data) (Required)
--commit auto Automatic commit after restore (Recommended)
--verify      Integrity check after restore (Recommended)
--dry-run     Pre-execution simulation (Safety check)
```

**Method B: Restore from Physical Image (Full Disk Reconstruction)**

```bash
# 1. Write the image file to all HDDs using dd
# WARNING: All data on target HDDs will be erased!

dd if=jbod_backup.img of=/dev/sdb bs=4M status=progress conv=fsync
dd if=jbod_backup.img of=/dev/sdc bs=4M status=progress conv=fsync
# ... repeat for all HDDs in the pool

# 2. After rebooting TUFF-OS, run integrity check
tuffutl sys fsck --repair

# 3. Verify status
tuffutl sys status
```

#### Step 4: Post-Restore Verification & Final Tuning

1. **Verify System State**
   - Run `tuffutl sys status --detail`.
   - Confirm Genesis is Valid, 3N is Healthy, and Isolation is Inactive.
2. **Re-create Users & Login**
   - `tuffutl user add admin --password "NewStrongPass123!"`
   - `tuffutl sys login admin ...`
3. **Re-apply TagGroupMask**
   - Re-assign tags to confidential folders: `tuffutl fs tag add /data/secret "Confidential" "Finance"`.
4. **Re-apply Network Settings**
   - `tuffutl nw blacklist refresh`
   - `tuffutl nw aiserverlist add https://trusted.ai ...`
5. **Final Commit**
   - `tuffutl fs commit --target /`
6. **Final Audit**
   - Verify file lists/contents and check `tuffutl log tail` for anomalies.

---

### Summary of Risks and Notes

| Caution | Risk | Prevention |
|:---|:---|:---|
| Destination disk error | Overwriting the wrong drive | Triple-check device names. |
| Backup file corruption | Failed restore → Total loss | Run `tuffutl backup verify` before restore. |
| Power loss during restore | Inconsistency from partial restore | Mandatory UPS + rely on auto-rollback. |
| Loss of new Recovery PIN | Reinstall required next failure | Store PIN in multiple safe locations. |

**The Golden Rule**: "**Restore is the last resort.**" Preventing PIN loss is your top priority. **Manage your PIN as if your life depends on it.**
