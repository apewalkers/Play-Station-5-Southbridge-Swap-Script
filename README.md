# Swap_emc — PS5 NOR Southbridge Firmware Patcher

patching **PlayStation 5 NOR flash firmware** `.BIN` files, specifically to swap the embedded **EMC / Southbridge (CXD90061GG)** & **EMC / Southbridge (CXD90069GG)** firmware region. Useful when replacing a PS5 southbridge IC and needing to match the NOR firmware to the correct southbridge revision.
---
⚠️ NOTE: The 61.bin is the EMC Firmware for 1.0.4 (Exploitable with Symbrkrs/ PS5-uart https://github.com/symbrkrs/ps5-uart)

## Background

The PS5 NOR flash contains the EMC firmware used by the **CXD90061GG Southbridge** (also referred to as the EMC/Syscon). Two hardware revisions of this chip exist, commonly referred to as **61** and **69** (matching their board-level identifiers). When replacing a southbridge, the NOR firmware region must match the installed chip revision — this tool automates that swap.
---

## Features

- Scans the `IN/` folder for valid PS5 NOR `.BIN` files using the Sony header signature
- Supports patching for both southbridge variants: **61** and **69**
- Writes patch data across two NOR regions: `0x4000–0x82000` and `0x82000–0x100000`
- Extracts the mainboard serial and model strings from the NOR to auto-name output folders
- Saves a copy of the original alongside the patched file
- Optional cleanup — delete the source file from `IN/` after patching
---

## Requirements

- Python 3.6+
---

## Directory Structure
Swap_emc.py
├── IN/ # Place your PS5 NOR .BIN dumps here
├── OUT/ # Patched output written here (auto-created)
├── 61/
│ └── 61.bin # EMC firmware for southbridge revision 61 (must be exactly 0x7E000 bytes)
└── 69/
└── 69.bin # EMC firmware for southbridge revision 69 (must be exactly 0x7E000 bytes)


---

## Usage

1. Place your PS5 NOR dump `.BIN` file(s) into the `IN/` folder.
2. Ensure the correct patch binary (`61.bin` or `69.bin`) is present in its subfolder.
3. Run the script:

```bash
python Swap_emc.py
```

4. When prompted, enter `61` or `69` to match your replacement southbridge revision.
5. Output is written to `OUT/<ModelString_VersionString>/`:
   - `<original_filename>.bin` — unmodified NOR dump
   - `patched_<original_filename>.bin` — NOR with swapped EMC firmware
6. Optionally confirm deletion of the source dump from `IN/`.

---

## Patch Details

| Parameter            | Value                                        |
|----------------------|----------------------------------------------|
| Header Signature     | `SONY COMPUTER ENTERTAINMENT INC.` (ASCII)   |
| Required NOR size    | `0x100000` (1 MB)                            |
| Patch (EMC FW) size  | `0x7E000` bytes                              |
| Patch region 1       | `0x4000` – `0x82000`                         |
| Patch region 2       | `0x82000` – `0x100000`                       |
| Mainboard S/N offset | `0x1C7210`, 18 bytes                         |
| Serial No. offset    | `0x1C7230`, 32 bytes                         |

---

## Notes

- If the source NOR dump is smaller than `0x100000` bytes, it will be zero-padded before patching.
- Files that do not match the Sony header signature are silently skipped.
- Patch binaries must be **exactly** `0x7E000` bytes — the script will reject mismatched files.
- This tool does **not** modify console-unique data (serial numbers, MAC addresses). Those fields remain intact from the original dump.

---

## ⚠️ Disclaimer — Read Before Use

> **USE AT YOUR OWN RISK.**
>
> Patching PS5 NOR firmware is a **destructive, hardware-level operation**. Flashing an incorrect or corrupted firmware image to your console's NOR flash can result in a **permanently bricked device** that may be unrecoverable.
>
> **Before using this tool, you MUST:**
> - Have a **verified, full backup of your original NOR dump** stored safely before making any changes
> - Confirm the southbridge revision (**61** or **69**) of your replacement IC before selecting a patch variant
> - Verify the integrity of your NOR dump (file size, header signature) prior to patching
>
> The author(s) of this tool accept **no responsibility** for damaged, bricked, or otherwise unusable hardware resulting from use of this software. This tool is provided as-is, with no warranty expressed or implied.
>
> This tool is intended for **board repair and educational purposes only**. Use only with hardware and firmware you own or have explicit authorisation to modify.
