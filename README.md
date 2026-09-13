


# ⚠️ Work in Progress

## Tools & References to read before proceeding
- **NVFlash (Windows/Linux, full version)**  
  [Download here](https://www.techpowerup.com/download/nvidia-nvflash/)  

- **Kepler BIOS Tweaker**  
  [Download here](https://www.techpowerup.com/download/kepler-bios-tweaker/)  

- **Inforom Recovery (if needed)**  
  [HPE Recovery Guide](https://support.hpe.com/hpesc/public/docDisplay?docId=sf000073504en_us&docLocale=en_US)  


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

### Clock domains explained — K40, stock P00 performance mode only

**P00 voltage range:** 875.0 – 925.0 mV

| Clock | What it controls | Min (BC01) | Max (BC04) |
|---|---|---|---|
| **GPC** | Graphics Processing Cluster clock. Main shader/SMX execution domain; higher GPC = more CUDA core throughput. | 666.5 MHz | 875.5 MHz |
| **SYS** | System/chip-level clock. Tied to GPC on the K40; affects internal chip coordination. | 666.5 MHz | 875.5 MHz |
| **XBAR** | Crossbar interconnect. Moves data between GPCs, L2 cache, and memory controllers. | 599.5 MHz | 787.5 MHz |
| **L2C** | L2 cache clock. Controls the L2 cache slices. | 599.5 MHz | 787.5 MHz |
| **Memory** | GDDR5 effective data rate. | 3004 MHz | 3004 MHz |

### P00 boost clock ladder

Boost clock 04 is the top of the range (the "max" column). Clocks 03 and 02 each sit **13 MHz below the previous step**. Boost clock 01 is a **fixed default fallback** — it cannot be set directly, it's just where the card drops to.

| Boost state | Voltage | GPC / SYS | XBAR / L2C | Notes |
|---|---|---|---|---|
| **BC04** (max) | 925.0 mV | 875.5 MHz | 787.5 MHz | top of P00 range |
| **BC03** | — | 862.5 MHz | 774.5 MHz | −13 MHz from BC04 |
| **BC02** | — | 849.5 MHz | 761.5 MHz | −13 MHz from BC03 |
| **BC01** (min) | 875.0 mV | 666.5 MHz | 599.5 MHz | fixed fallback, not directly settable |

**Key points:**

- Everything above is **P00 stock only** — voltage lives between 875.0 and 925.0 mV.
- GPC and SYS move together; XBAR and L2C move together.
- Only BC04 (max) and the intermediate steps below it are user-adjustable; BC01 is hardwired as the safe fallback.
- Memory stays at 3004 MHz effective regardless of the boost state.

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

### Clock domains explained — K40, modded BIOS

**P00 voltage range:** 887.5 – 937.5 mV *(stock + 12.5 mV offset)*

| Clock | What it controls | Min (BC01) | Max (BC04) |
|---|---|---|---|
| **GPC** | Graphics Processing Cluster clock. Main shader/SMX execution domain; higher GPC = more CUDA core throughput. | 666.5 MHz | 1071.5 MHz |
| **SYS** | System/chip-level clock. Tied to GPC on the K40; affects internal chip coordination. | 666.5 MHz | 1071.5 MHz |
| **XBAR** | Crossbar interconnect. Moves data between GPCs, L2 cache, and memory controllers. | 599.5 MHz | 875.5 MHz |
| **L2C** | L2 cache clock. Controls the L2 cache slices. | 599.5 MHz | 875.5 MHz |
| **Memory** | GDDR5 effective data rate. | 3004 MHz | 3004 MHz |

### What was changed vs. stock

| Setting | Stock | Modded | Delta |
|---|---|---|---|
| P00 voltage offset | — | +12.5 mV | +12.5 mV |
| GPC / SYS (BC02–BC04) | 849.5 – 875.5 MHz | 1045.5 – 1071.5 MHz | +196 MHz |
| XBAR / L2C (BC02–BC04) | 761.5 – 787.5 MHz | 836.5 – 875.5 MHz | +75 – 88 MHz |
| Power limit | 235 W | 300 W | +65 W |

### P00 boost clock ladder (modded)

Boost clock 04 is the top of the range (the "max" column). Clocks 03 and 02 each sit **13 MHz below the previous step**. Boost clock 01 is a **fixed default fallback** — it cannot be set directly, it's just where the card drops to.

| Boost state | Voltage | GPC / SYS | XBAR / L2C | Notes |
|---|---|---|---|---|
| **BC04** (max) | 937.5 mV | 1071.5 MHz | 875.5 MHz | top of P00 range |
| **BC03** | — | 1058.5 MHz | 862.5 MHz | −13 MHz from BC04 |
| **BC02** | — | 1045.5 MHz | 849.5 MHz | −13 MHz from BC03 |
| **BC01** (min) | 887.5 mV | 666.5 MHz | 599.5 MHz | fixed fallback, not directly settable |

### Why these specific settings?

**1) Why not a 0.9 ratio (GPC : XBAR)?**

Under testing, bus utilization peaked at only ~50% with the stress test, and closer to ~15% for LLM workloads. Raising XBAR/L2C further than necessary just produces waste heat with no throughput benefit, so the crossbar is kept proportionally lower than the GPC clock.

**2) Why not higher GPC / SYS clocks?**

Thermal limits. See below for how to tune them in situ with MSI Afterburner.

**3) Why not boost memory?**

Instability. See below for how to tune it in situ with MSI Afterburner.

### Comparison of BIOS profiles

| Profile | Voltage (P00) | GPC / SYS (max) | XBAR / L2C (max) | Power limit |
|---|---|---|---|---|
| **Stock** | 875.0 – 925.0 mV | 875.5 MHz | 787.5 MHz | 235 W |
| **Modded** | 887.5 – 937.5 mV | 1071.5 MHz | 875.5 MHz | 300 W |

## Setting custom clocks within the provided BIOS

Once a modified BIOS is flashed, you can fine-tune clocks further without reflashing:

- Use **MSI Afterburner** or a similar tool to set clock offsets (for example: +13 MHz core, +150 MHz memory).
- Use **`nvidia-smi`** to set a new clock range (for example: `nvidia-smi -i <index> -ac 3450,1084`).
- Enjoy the extra performance.

> **Tip:** Always verify stability after changing clocks. If you see artifacts, crashes, or `nvidia-smi` warnings, reduce the clocks until stable.
## Making custom bioses with Kepler Bios Tweaker
- work in progress, coming soon. 
