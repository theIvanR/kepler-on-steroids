# NVIDIA Tesla K40c Ultra BIOS Mod

This repository contains a modified "Ultra" BIOS for the **NVIDIA Tesla K40** GPU.  
The BIOS unlocks additional power and clock controls, allowing the card to reach much higher performance than stock settings.

---

## Features of the "Ultra" BIOS
- **Unlocked TDP range**: 150W – 300W (adjustable with Afterburner or nvidia-smi)  
- **Unlocked voltage control**: extra +75 mV at top range of P0 to 1000mv (vs 925mV) 
- **Unlocked fan control**: 25% – 100% range (instead of fixed blower profiles)  
- **Unlocked clock limits**: up to 1150 MHz SYS and GPC, 1025MHz Xbar and L2c, 3504 MHz memory effective 
- **Full support for MSI Afterburner and nvidia-smi adjustments**  
- **Stable under load**: tested for 5 hours in FurMark without crashes  

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
- Avoid using HP bioses, these limit to pcie gen2 and mess with inforom configuration.
- The modded BIOS is provided in the description of this repository.  
- The original recovery **Inforom** is also included in case you need to restore.  
- Flashing a GPU BIOS always carries risk – make sure you have a backup and recovery method before proceeding.  
- Recommended command for flashing (run from elevated terminal / shell):

  **Windows**:
  ```
  nvflash64 --protectoff
  nvflash64 -6 k40_ultra.rom
  ```

  **Linux**:
  ```
  sudo nvflash --protectoff
  sudo nvflash -6 k40_ultra.rom
  ```

---

## Disclaimer
This BIOS is provided **as-is** with no warranty.  
Flashing is at your own risk. Neither the author nor contributors are responsible for any damage caused to hardware, software, or data.  

Use only if you are comfortable with BIOS flashing and GPU recovery methods.

---
