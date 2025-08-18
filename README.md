# NVIDIA Tesla K40c Ultra BIOS Mod

This repository contains a modified "Ultra" BIOS for the **NVIDIA Tesla K40** GPU.  
The BIOS unlocks additional power and clock controls, allowing the card to reach much higher performance than stock settings.

---

## Features of the "Ultra" BIOS
- **Unlocked TDP range**: 150W – 235w -> 150w - 300w (adjustable with Afterburner or nvidia-smi)  
- **Unlocked voltage Ceiling**: 925mV in P0 -> 1000mV in P0 top range.
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
- A clean INFOROM template is provided for recovery purposes
- Flashing a GPU BIOS always carries risk – make sure you have a backup and recovery method before proceeding.  
- Recommended command for flashing (run from elevated terminal / shell):

  **Windows**:
  ```
  nvflash64 --protectoff
  nvflash64 -6 ultra_bios.rom
  ```

  **Linux**:
  ```
  sudo nvflash --protectoff
  sudo nvflash -6 ultra_bios.rom
  ```

  **WARNING**
  - if you get a pcie error in --protectoff command, this means that your overclock or something else is unstable, meaning DO NOT FLASH! Set to lowest clock and try again. Otherwise you may not only corrupt the bios rom but also the inforom and you will need to recover it with HPE recovery guide
    ```
    nvidia-smi -i 0 -ac 324,324
    ```

Once done, set clocks
```
nvidia-smi -i 0 -ac 3504,1150
```

---

## Disclaimer
This repository serves as a reference for:
- Computer architecture research
- Hardware modification education
- Preservation of legacy computing techniques

This BIOS and inforom is provided **as-is** with no warranty.  
While this bios is stable in good faith on my silicon (5 hours Furmark), the flashing is at your own risk. Act accordingly and proceed with caution/  

---
