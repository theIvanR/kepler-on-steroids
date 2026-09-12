


# ⚠️ Work in Progress

## NVIDIA Tesla K40 — Introduction

The NVIDIA Tesla K40 / K40c is a Kepler-generation compute GPU that still has a following for legacy CUDA workloads, cheap FP64 compute, and hardware tinkering. It is based on the **GK110B** core and packs **2880 CUDA cores** across 15 SMX units, with dual-issue SM pipelines and a 384-bit GDDR5 memory interface. Factory clocks are conservative, so modified BIOS files can unlock more voltage, power, and clock headroom than the stock firmware allows.

### Architecture at a glance

- **GPU:** NVIDIA Kepler GK110B
- **CUDA cores:** 2880
- **SMX units:** 15
- **Issue capability:** dual-issue SM pipelines, up to 2 IPC in ideal cases
- **Compute capability:** 3.5
- **Memory:** 12 GB GDDR5, 384-bit
- **Stock boost clock:** 875 MHz (GPC/SYS)
- **Stock memory:** 3004 MHz effective
- **Stock TDP:** 235 W

Kepler’s SMX design can dual-issue instructions to help keep the CUDA cores fed. The K40 also exposes several separate clock domains, which is important when tuning or comparing BIOS profiles.

### Clock domains explained

| Clock | What it controls | Stock |
|---|---|---|
| **GPC** | Graphics Processing Cluster clock. This is the main shader/SMX execution domain; higher GPC clock means more CUDA core throughput. | 875 MHz |
| **SYS** | System/chip-level clock. On the K40 it is usually tied to GPC; it affects internal chip coordination. | 875 MHz |
| **XBAR** | Crossbar interconnect clock. Moves data between GPCs, L2 cache, and memory controllers. | 787.5 MHz |
| **L2C** | L2 cache clock. Controls the L2 cache slices. | 787.5 MHz |
| **Memory** | GDDR5 effective memory data rate. | 3004 MHz |

## Tools & References to read before proceeding
- **NVFlash (Windows/Linux, full version)**  
  [Download here](https://www.techpowerup.com/download/nvidia-nvflash/)  

- **Kepler BIOS Tweaker**  
  [Download here](https://www.techpowerup.com/download/kepler-bios-tweaker/)  

- **Inforom Recovery (if needed)**  
  [HPE Recovery Guide](https://support.hpe.com/hpesc/public/docDisplay?docId=sf000073504en_us&docLocale=en_US)  

## Why and How to Use Custom BIOS

### Why?
Custom BIOS files unlock higher power limits, voltage, and clock speeds than the stock firmware allows, letting you squeeze more compute performance out of the Tesla K40.

### How?
By flashing a modified BIOS ROM to the GPU using NVFlash.

> ⚠️ **Do NOT flash if the GPU is unstable.**
> If `nvidia-smi` reports any warnings or instability, **do not flash**. Flashing an unstable card can corrupt the **Inforom** and may require a Linux-based recovery. Instead, set the GPU to the lowest clocks where it is stable.

### Safety checklist (condensed)
- ✅ Ensure the GPU is **100% stable** before flashing.
- ✅ Lock the GPU to the lowest stable clocks with `nvidia-smi` while flashing.
- ⚠️ **Avoid HP OEM BIOS files** — they may force PCIe Gen2 and alter Inforom configuration.
- 🧰 A **clean Inforom template** is included in this repo for recovery.
- 💾 Always have **backups**: a backup ROM and a recovery plan.
- ⚠️ Flashing carries inherent risk — proceed only if you understand the consequences.

### Recommended step-by-step procedure

1. **Verify stability**
   - Monitor the GPU with `nvidia-smi` and stress/diagnostic tools.
   - If you see warnings, errors, or abnormal behavior → **STOP**.

2. **Set the GPU to the lowest safe clocks**
   - Lock clocks to a low, stable level:
     ```
     nvidia-smi -i <index> -ac 324,324
     ```

3. **Disable NVFlash protections** (only needed once per GPU, if not already done)
   - Run NVFlash to turn off protections:
     ```
     .\nvflash64.exe --protectoff --index=<index>
     ```
   - **Note:** NVFlash only accepts one GPU index at a time. For multiple GPUs, run it for each index (0, 1, 2, …).
   - If protections are already disabled, skip to step 4.

4. **Flash the ROM**
   - Write the modified BIOS to the target GPU:
     ```
     .\nvflash64.exe -6 .\<your-bios.rom> --index=<index>
     ```
   - **Note:** This also only flashes one GPU at a time. Run it separately for each GPU index.

5. **Reboot and verify**
   - Reboot the system, verify the card posts correctly, and restore clocks.
   - Example for multiple GPUs:
     ```
     nvidia-smi -i 0,1,2,3 -ac 3004,1084
     ```

## Comparison of BIOS Profiles

If you are just starting out or are unsure which workload you will run, test **BIOS A** first. If the GPU is not thermally constrained, you can switch to **BIOS B**. If you want even more performance and are willing to trade some stability, experiment with **BIOS C**.

| Profile | SYS / GPC Clocks | Xbar / L2c Clocks | Memory Effective | Voltage (P0) | TDP Range |
|---|---|---|---|---|---|
| **Stock** (ratio 0.9) | 875 MHz | 787.5 MHz | 3000 MHz | 925 mV | 150 – 235 W |
| **A: CUDA BIOS** (stable under extreme CUDA + FurMark) | 1084.5 MHz | 875.5 MHz | 3004 MHz | 937.5 mV | 150 – 300 W |

> **Note:** BIOS B and C are higher-performance profiles with increased clocks, voltage, and power limits. They may introduce occasional instability. See the repository for their exact specifications and use them only if you understand the risks.

---

## 4. Setting Custom Clocks within Provided BIOS

Once a modified BIOS is flashed, you can fine-tune clocks further without reflashing:

- Use **MSI Afterburner** or a similar tool to set clock offsets (for example: +13 MHz core, +150 MHz memory).
- Use **`nvidia-smi`** to set a new clock range (for example: `nvidia-smi -i <index> -ac 3450,1084`).
- Enjoy the extra performance.

> **Tip:** Always verify stability after changing clocks. If you see artifacts, crashes, or `nvidia-smi` warnings, reduce the clocks until stable.

## Making custom bioses with Kepler Bios Tweaker
- work in progress, coming soon. 
