# NVIDIA Tesla K40c "Ultra" BIOS Mod

The **NVIDIA Tesla K40** remains a formidable GPU for compute workloads, featuring **2880 CUDA cores**, dual-issue pipelines (2 IPC), and robust memory bandwidth. Out of the box, its FP32 and FP64 throughput is limited by conservative BIOS settings.  

This repository provides a modified **"Ultra" BIOS** that unlocks additional voltage, power, and clock headroom, enabling the GPU to reach **up to 1124 MHz on SYS and GPC clocks**, with proportional increases for memory, Xbar, and L2c clocks. The result is a **theoretical FP32 performance of ~6.47 TFLOPS** and **FP64 performance of ~2.16 TFLOPS**, all while maintaining stability.  

Unlike standard overclocking tools like MSI Afterburner, this BIOS **optimizes internal clocks such as Xbar and L2c**, unlocking performance that cannot be reached through software-only tuning.  

Whether for scientific computation, deep learning research, or hardware experimentation, this BIOS allows you to explore the K40’s full potential beyond factory constraints.
---

## Features of the "Ultra" BIOS
- **Unlocked TDP range**: 150W – 235w -> 150w - 300w (adjustable with Afterburner or nvidia-smi)  
- **Unlocked voltage Ceiling**: 925mV in P0 -> 950 mV in P0 top range.
- **Unlocked fan control**: 25% – 100% range (instead of fixed blower profiles)  
- **Unlocked clock limits**: up to 1124 MHz SYS and GPC, 1050MHz Xbar and L2c, 3500 MHz memory effective 
- **Full support for MSI Afterburner and nvidia-smi adjustments**  
- **Stable under load**: tested for in FurMark without crashes  

---

## Tools & References
- **NVFlash (Windows/Linux, full version)**  
  [Download here](https://www.techpowerup.com/download/nvidia-nvflash/)  

- **Kepler BIOS Tweaker**  
  [Download here](https://www.techpowerup.com/download/kepler-bios-tweaker/)  

- **Inforom Recovery (if needed)**  
  [HPE Recovery Guide](https://support.hpe.com/hpesc/public/docDisplay?docId=sf000073504en_us&docLocale=en_US)  

---

## Important Notes
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
