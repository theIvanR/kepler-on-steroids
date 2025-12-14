# 0: NVIDIA Tesla K40c "Ultra" BIOS Mod

The **NVIDIA Tesla K40** remains a formidable GPU for compute workloads, featuring **2880 CUDA cores**, dual-issue pipelines (2 IPC), and robust memory bandwidth. This repository provides modified BIOS files that unlock additional voltage, power, and clock headroom beyond factory constraints.

# 1: Comparison of Bioses
If starting out or unsure of workload, I recommend to test the bios A first, and if the gpu is not thermally constrained switch to bios B and if more performance is desired experiment with bios C.

```
# Stock BIOS:
SYS / GPC Clocks      : 875 MHz
Xbar / L2c Clocks     : 787.5 MHz
Memory Effective      : 3000 MHz
Voltage (P0)          : 925 mV
TDP Range             : 150W – 235W
```

```
# A: CUDA BIOS (stable under extreme CUDA + FurMark) -> one currently provided
SYS / GPC Clocks      : 1071.5 MHz  # +196.5 MHz over stock, ~26 MHz headroom
SYS / GPC Clocks      : 1025 MHz    # +237.5 MHz over stock, ~26 MHz headroom
Memory Effective      : 3300 MHz    # +300 MHz over stock, ~150MHz headroom
Voltage (P0)          : 925 mV      # +0 mV over stock
TDP Range             : 150W – 300W
```

```
# B: High Performance "normal work" BIOS
SYS / GPC Clocks      : 1150 MHz  # +275 MHz over stock, ~? MHz headroom
SYS / GPC Clocks      : 1097.5 MHz  # +310 MHz over stock, ~? MHz headroom
Memory Effective      : 3300 MHz    # +300 MHz over stock, ~150MHz headroom
Voltage (P0)          : 937.5 mV      # +12.5 mV over stock
TDP Range             : 150W – 300W
```

```
# C: Extreme BIOS (maximum theoretical performance, some instability)
(will be overvolted for maximum OC performance, power limit boosted further)
```
---

#2: Tools & References to read before proceeding
- **NVFlash (Windows/Linux, full version)**  
  [Download here](https://www.techpowerup.com/download/nvidia-nvflash/)  

- **Kepler BIOS Tweaker**  
  [Download here](https://www.techpowerup.com/download/kepler-bios-tweaker/)  

- **Inforom Recovery (if needed)**  
  [HPE Recovery Guide](https://support.hpe.com/hpesc/public/docDisplay?docId=sf000073504en_us&docLocale=en_US)  

---

## 3 — Flashing your BIOS — **IMPORTANT**

> ⚠️ **Do NOT flash if the GPU is unstable.**  
> If `nvidia-smi` reports any warnings or instability, **do not flash**. Flashing an unstable card can corrupt the **Inforom** and may require a Linux-based recovery! Set instead to lowest clocks where it is stable. 

### Overview / Safety checklist
- ✅ Ensure the GPU is **100% stable** before attempting any flash.
- ✅ Use `nvidia-smi` to lock the GPU to the lowest stable clocks while flashing.
- ⚠️ **Avoid HP OEM BIOS files.** They may force PCIe Gen2 and alter Inforom configuration.
- 🧰 A **clean Inforom template** is included in this repo for recovery purposes.
- 💾 Always have **backups**: a backup ROM and a recovery plan before proceeding.
- ⚠️ Flashing carries inherent risk — proceed only if you understand the consequences.

---

### Recommended step-by-step procedure

1. **Verify stability**
   - Monitor the GPU with `nvidia-smi` and other stress / diagnostic tools.
   - If you see any warnings, errors, or abnormal behavior → **STOP**.

2. **Set the GPU to the lowest safe clocks**
   - Lock clocks to a low, stable level with `nvidia-smi` (example below).

3. **Disable NVFlash protections**
   - Run NVFlash to turn off protections prior to flashing.

4. **Flash the ROM**
   - Use NVFlash to write the ROM to your target index.

5. **Reboot and verify**
   - Reboot the system, verify the card posts correctly, and restore clocks.

---

### Windows command templates (example)

> Replace `<index>` and `<your-bios.rom>` with your values. Use `bios.rom` if NVFlash complains about filename length.

```batch
:: 1) Set the GPU to safe, minimum clocks (example values)
nvidia-smi -i <index> -ac 324,324

:: 2) Disable NVFlash protections
.\nvflash64.exe --protectoff --index=<index>

:: 3) Flash the BIOS (use bios.rom if needed)
.\nvflash64.exe -6 .\<your-bios.rom> --index=<index>

:: 4) Reboot the machine (manual step)
:: After reboot, restore clocks to normal operation (example values)
nvidia-smi -i <index> -ac <memory,gpc/sys>
```

# 4 Setting Custom Clocks within Provided Bios: 
- Use MSI afterburner or similar, set clock ranges (ex +13 Mhz cores, +150Mhz Memory)
- use nvidia-smi to set new clock range (ex 3450,1084)
- enjoy

# 5: Making a custom BIOS yourself
(coming later)

---
## Disclaimer
This repository serves as a reference for:
- Computer architecture research
- Hardware modification education
- Preservation of legacy computing techniques

This BIOS and inforom is provided **as-is** with no warranty.  
While this bios is stable in good faith on my silicon (5 hours Furmark), the flashing is at your own risk. Act accordingly and proceed with caution.

NVIDIA, Tesla, and related logos are trademarks or registered trademarks of NVIDIA Corporation. This project is not affiliated with or endorsed by NVIDIA.

# LICENSE (MIT)

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---
