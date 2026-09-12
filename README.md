


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
- **Stock memory:** 3000 MHz effective
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



# 1: Comparison of Bioses
If starting out or unsure of workload, I recommend to test the bios A first, and if the gpu is not thermally constrained switch to bios B and if more performance is desired experiment with bios C.

```
# Stock BIOS: (ratio 0.9)
SYS / GPC Clocks      : 875 MHz
Xbar / L2c Clocks     : 787.5 MHz
Memory Effective      : 3000 MHz
Voltage (P0)          : 925 mV
TDP Range             : 150 – 235W
```

```
# A: CUDA BIOS (stable under extreme CUDA + FurMark workloads)
SYS / GPC Clocks      : 1084.5 MHz
Xbar / L2c Clocks       : 875.5 MHz
Memory Effective      : 3004 MHz
Voltage (P0)          : 937.5 mV
TDP Range             : 150 – 300W
```



# 4 Setting Custom Clocks within Provided Bios: 
- Use MSI afterburner or similar, set clock ranges (ex +13 Mhz cores, +150Mhz Memory)
- use nvidia-smi to set new clock range (ex 3450,1084)
- enjoy

# 5: Making a custom BIOS yourself
(coming later)


---
