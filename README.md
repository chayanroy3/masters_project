
# LLZO Deep Potential Modeling Project

This repository contains the code, data, and documentation for developing a deep neural potential model to simulate and study Lithium Lanthanum Zirconium Oxide (LLZO) as a solid-state electrolyte. The project leverages advanced techniques in deep potential molecular dynamics (DPMD) and active learning to accurately reproduce density functional theory (DFT) results while enabling efficient simulations of large systems, including grain boundaries.

---

## Overview

All-solid-state lithium-ion batteries are emerging as a promising technology for next-generation energy storage. LLZO, a garnet-type solid-state electrolyte, offers advantages such as low electronic conductivity, excellent chemical and thermal stability, and a wide electrochemical window. However, simulating its ionic transport properties—especially at grain boundaries—poses significant computational challenges. This project employs a deep potential model, trained on DFT data, to predict key properties including lattice constants, radial distribution functions (RDFs), and diffusion constants in both bulk and grain boundary regions.

---

## Methodology

### Deep Potential Molecular Dynamics (DPMD)
- **DeePMD-kit Integration:**  
  Utilizes a deep neural network to construct force fields from local atomic environments. Each atom is assigned a unique local reference frame, preserving translational, rotational, and permutational symmetries.
- **Neural Network Architecture:**  
  Features an embedding network for extracting descriptors from local atomic environments and a fitting network to map these descriptors to atomic energies. The training process minimizes a loss function balancing errors in energy, force, and virial predictions.

### Initial Data Generation
- **AIMD Simulations:**  
  Initial training data is generated using ab initio molecular dynamics (AIMD) with VASP. This involves structure relaxation, random lattice perturbations, and short AIMD trajectories at various temperatures to ensure a diverse set of configurations.
- **Random Perturbation:**  
  Structures are scaled and atoms are randomly perturbed to produce a robust dataset for model training.

### Model Training & Active Learning
- **Multiple Model Training:**  
  Four initial models are trained with different random seeds on the initial dataset.
- **Exploration with LAMMPS:**  
  Classical MD simulations are conducted to identify candidate configurations based on deviations in energy and force predictions.
- **Labeling with DFT:**  
  Selected candidate configurations are re-evaluated with VASP for accurate energy and force labels, which are then incorporated into the training set in an iterative active learning loop.

### Grain Boundary Construction
- **Algorithmic Approach:**  
  A Python package (e.g., [aimsgb]) is used to construct periodic grain boundary models from the cubic LLZO structure.
- **Grain Boundary Types:**  
  Both sigma3[112] and sigma5[310] grain boundaries are generated to study the influence of microstructural features on ionic transport.

### Molecular Dynamics Simulations
- **Bulk and GB Simulations:**  
  MD simulations are performed on both bulk LLZO and regions containing grain boundaries.
- **Diffusion Analysis:**  
  Mean squared displacement (MSD) analysis is applied to compute diffusion constants and assess the transport properties of lithium ions.

---

## Results and Discussion

- **Model Validation:**  
  The deep potential model is validated by comparing its energy and force predictions against DFT calculations, achieving a high correlation for energy and acceptable errors for forces.
- **Structural Properties:**  
  Lattice constants and radial distribution functions (RDFs) are calculated to confirm the accuracy of the LLZO structure.
- **Transport Properties:**  
  Diffusion constants are determined for both bulk and grain boundary regions, highlighting the impact of microstructural features on ion mobility.

---

## Getting Started

### Requirements
- **Programming Language:** Python 3.8+
- **Software & Tools:**
  - DeePMD-kit
  - VASP (for DFT and AIMD simulations)
  - LAMMPS (for classical MD simulations)
  - aimsgb (for grain boundary construction)
- **Dependencies:**  
  Install required Python packages via `pip` (see [requirements.txt](requirements.txt)).

### Installation

Clone the repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/username/llzo-deep-potential.git
cd llzo-deep-potential

# Install required Python packages
pip install -r requirements.txt
```

### Running the Simulations

1. **Data Generation:**  
   Run AIMD simulations using VASP to generate the initial training dataset.
2. **Model Training:**  
   Execute the provided training scripts in the `scripts/` directory to train the deep potential model.
3. **Active Learning Cycle:**  
   Perform exploratory MD simulations with LAMMPS, label candidate configurations with VASP, and iteratively update the training dataset.
4. **Grain Boundary Construction:**  
   Generate grain boundary models using the provided scripts, then run MD simulations on these systems.
5. **Analysis:**  
   Use analysis scripts to calculate diffusion constants (via MSD analysis) and visualize simulation results. Outputs are stored in the `results/` directory.

---

## Project Structure

```
llzo-deep-potential/
├── data/              # Input datasets and simulation data
├── docs/              # Documentation and presentation materials
├── models/            # Trained models and checkpoints
├── results/           # Simulation outputs, figures, and logs
├── scripts/           # Python scripts for simulations and analysis
├── requirements.txt   # Python dependencies
└── README.md          # Project overview and instructions
```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests with enhancements or bug fixes. Follow the established coding guidelines and include tests for new features.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

We acknowledge the contributions of the communities behind DeePMD-kit, VASP, LAMMPS, and aimsgb. Their tools and methodologies have been instrumental in the development of this project.

For more detailed information, please refer to the [documentation](docs/).
