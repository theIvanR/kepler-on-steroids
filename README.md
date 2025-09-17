# NVIDIA Tesla K40c "Ultra" BIOS Mod

The **NVIDIA Tesla K40** remains a formidable GPU for compute workloads, featuring **2880 CUDA cores**, dual-issue pipelines (2 IPC), and robust memory bandwidth. This repository provides modified BIOS files that unlock additional voltage, power, and clock headroom beyond factory constraints.

---

## BIOS Variants

### A. CUDA BIOS (Recommended)
- **Stability**: Stable under extreme CUDA workloads and FurMark
- **Clocks**: 
  - SYS/GPC: 1124 MHz
  - Xbar/L2c: 1050 MHz
  - Memory: 3500 MHz effective
- **Power Limit**: 300W
- **Voltage**: 950 mV

### B. Casual Use BIOS
- **Stability**: Stable under FurMark and general compute
- **Clocks**:
  - SYS/GPC: 1100 MHz
  - Xbar/L2c: 1000 MHz
  - Memory: 3400 MHz effective
- **Power Limit**: 280W
- **Voltage**: 940 mV

### C. Extreme BIOS (Experimental)
- **Stability**: May require manual tuning in Afterburner
- **Clocks**:
  - Base: 1150 MHz (can reach 1200-1300 MHz with manual OC)
  - Xbar/L2c: 1100 MHz
  - Memory: 3600 MHz effective
- **Power Limit**: 320W
- **Voltage**: 975 mV

---

## Tools & References
- **NVFlash (Windows/Linux, full version)**  
  [Download here](https://www.techpowerup.com/download/nvidia-nvflash/)  

- **Kepler BIOS Tweaker**  
  [Download here](https://www.techpowerup.com/download/kepler-bios-tweaker/)  

- **Inforom Recovery (if needed)**  
  [HPE Recovery Guide](https://support.hpe.com/hpesc/public/docDisplay?docId=sf000073504en_us&docLocale=en_US)  

---

## Flashing your Bios and Important Notes
- Make sure the card is STABLE, set to lowest clock with nvidia-smi. IF THERE IS A WARNING DO NOT UNDER ANY CIRCUMSTANCES FLASH, this will corrupt inforom and require recovery under linux
- Avoid using HP bioses, these limit to pcie gen2 and mess with inforom configuration.
- A clean INFOROM template is provided for recovery purposes
- Flashing a GPU BIOS always carries risk – make sure you have a backup and recovery method before proceeding.  

  **Window Commands Template**:
  ```
  nvidia-smi -i <your index here> -ac 324,324
  & ".\nvflash64.exe" --protectoff --index=<your index here>
  & ".\nvflash64.exe" -6 ".\<bios name goes here>.rom" --index=<your index here>
  ```

  **After Reboot**
  ```
  nvidia-smi -i <your index here> -ac 3500,1124
  ```
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
