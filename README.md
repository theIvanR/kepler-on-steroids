


## Read before proceeding: 
- **NVFlash (Windows/Linux, full version)**  
  [Download here](https://www.techpowerup.com/download/nvidia-nvflash/)  

- **Kepler BIOS Tweaker**  
  [Download here](https://www.techpowerup.com/download/kepler-bios-tweaker/)  

- **Inforom Recovery (if needed)**  
  [HPE Recovery Guide](https://support.hpe.com/hpesc/public/docDisplay?docId=sf000073504en_us&docLocale=en_US)  


## Introduction to the Nvidia Tesla K40 GPU

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


### Clock domains explained — K40, stock P00 performance mode only {BC01,02,03,04}

| Clock | What it controls |  Fallback (BC01) -> 875mV | Boost (Max) (BC04) -> 925mV |
|---|---|---|---|
| **GPC** | Graphics Processing Cluster clock. Main shader/SMX execution domain; higher GPC = more CUDA core throughput. | 666.5 MHz | 875.5 MHz |
| **SYS** | System/chip-level clock. Tied to GPC on the K40; affects internal chip coordination. | 666.5 MHz | 875.5 MHz |
| **XBAR** | Crossbar interconnect. Moves data between GPCs, L2 cache, and memory controllers. | 599.5 MHz | 787.5 MHz |
| **L2C** | L2 cache clock. Controls the L2 cache slices. | 599.5 MHz | 787.5 MHz |
| **Memory** | GDDR5 effective data rate. | 3004 MHz | 3004 MHz |


## Custom BIOS: Install & Tuning

### Changes
- **P00 voltage:** +25 mV on all P00 states.
- **Power limit:** 275 W (was 235 W).

### Safety
- GPU must be **100% stable**. If `nvidia-smi` shows warnings or instability, **do not flash**.
- Lock to the lowest stable clocks while flashing (`BC00` in `P08`):  
  `nvidia-smi -i <index> -ac 324,324`
- Avoid **HP OEM BIOS files** — they can force PCIe Gen2 and alter the Inforom.
- Keep a **backup ROM**, a clean **Inforom template**, and a Linux-based recovery plan.
- Flashing can corrupt the Inforom. Proceed only if you understand the risks.

### Flash
1. Verify GPU stability.
2. Lock clocks (see above).
3. Disable NVFlash protections once per GPU, if needed:  
   `.\nvflash64.exe --protectoff --index=<index>`
4. Flash the ROM:  
   `.\nvflash64.exe -6 .\<your-bios.rom> --index=<index>`
   - NVFlash handles one GPU index at a time. Repeat for each GPU.
5. Reboot, verify the card posts correctly, then restore your clocks.

### Tuning
Use **MSI Afterburner** or a similar tool to find stable offsets.

**Recommended starting point:**
- Core: **+300 MHz**
- Memory: **+0 MHz**

Experiment from there and stress test after each change.
