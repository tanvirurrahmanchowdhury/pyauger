# PyAuger v0.0.1
An incomplete First-Principle Auger Computation Code in Python with VASP.

## Requirements
* python >= 3.9
* numpy
* scipy
* matplotlib, seaborn
* pymatgen
* pandas *(optional)*
---
* * *
## Background
In the pursuit of quantifying the temporal evolution of carrier states, we resort to the application of the Fermi Golden Rule derived from the principles of time-dependent perturbation theory. This approach empowers us to accurately evaluate the probability of transition between states, facilitating a comprehensive understanding of the dynamic behavior of carriers over time.
$$C_{auger}=\text{constant}\times\sum_{\mathbf{1234}}\mathbf{P_{1234}}|\mathbf{M_{1234}}|^2\delta(E_1+E_2-E_3-E_4)$$
where, $P_{1234}=f_1f_2(1-f_3)(1-f_4)$, $f_n$ is the Fermi-Dirac distribution \footnote{$f(E) = \left[ e^{(E-E_F)/k_BT}+1 \right] ^{-1}$}. The $\delta(E_1+E_2-E_3-E_4)$ function is modeled in terms of a Gaussian function.
 $$\delta(E_1+E_2-E_3-E_4) \approx e^{-(E_1+E_2-E_3-E_4)^2/2\sigma^2}$$
## Running a Computation: A Step-by-Step Guide
---
* * *
1. PBE Bandstructure Calculation
Perform a regular PBE bandstructure calculation using the *pymatgen* package. You can find an example of this process in the provided [Link](http://matgenb.materialsvirtuallab.org/2017/04/14/Inputs-and-Analysis-of-VASP-runs.html).  Please note that some functionalities might differ in the updated *pymatgen* API.

2. Set Up Directory
Copy the non-SCF (self-consistent field) directory and place the *k_grid_sample.sh* script within it.

3. Adjust INCAR File and Run Non-SCF Calculations
Review the INCAR file tags and make any necessary adjustments. Once satisfied, execute the *k_grid_sample.sh* script. This script will initiate non-SCF calculations for various k-grids, which can be configured from within the script itself. Please carefully examine the script's content.

4. Post-Computation Analysis
After the calculations are converged, copy the *parse_output.py* Python script from the directory. This script can be used to check convergence, parse Fermi energy, k-grid details, band energies, point weights, and more. You can customize the script according to your needs. Ensure that the directory contains *KPOINTS, vasprun.xml,* and *EIGENVAL* files as these are required by the script.  Subsequently, execute the *get_fermi_cutoff.py* script. This action will produce a text file named *band_info.txt*, which will encompass details such as the fermi energy, as well as the minimum and maximum band indices necessary for running the *parallel*_carlo.py* or *carlo_auger.py* code in the later stages. Generally, this step needs to be carried out only once, perhaps with a $20\times20\times20$ or $50\times50\times50$ kgrid configuration, since empirical tests have shown minimal variance in the band indices as the kgrid dimensions are increased.

5. File Naming
File names are self-explanatory. For instance, *kw_10_47.npy* is the k-point weight file resulting from a $10\times10\times10$ k-grid computation with 47 irreducible k-points. I will call $10$ as $X$ and $47$ as $XX$. So, for $20\times20\times20$ grid, $X=20$ and $XX=256$ as there are $256$ irreducible k-points. \\How do you get these numbers? *parse_output.py* script will tell you these numbers when you run it.

6. Create a New Directory
Run the *create_oj_dir.sh* script. It will create a new directory called *auger_main* and copy all *.npy* files in that directory.  Along with these, you need to copy \texttt{parallel\_carlo.py} or *carlo_auger.py* and job submission script to the *auger_main* directory.  The difference between *parallel_carlo.py* and *carlo_auger.py* is that one is parallel and one is serial. The difference and best practices have been explained in a later section.

7. Run Calculation
Execute the *job_script.sh* script. Before each run, remember to modify the job name. Also, update the $X$ and $XX$ tags in the *parallel_carlo.py* script as necessary.

8. Check Outputs
Upon completion of a computation, read the *job-name.out* file for results. For details of any errors, refer to the *job-name.err* file.  These steps guide you through the process of using the provided code for Auger computations. If you encounter any issues or need further assistance, please refer to this documentation or contact the relevant support channels.

---
* * *

## Things to keep in mind

1. Model Hyperparameter
The hyperparameter $\sigma$ plays a critical role within the model’s configuration. Currently, it has been predefined as 0.01, reflecting the existing setting. However, it’s worth noting that the code allows for flexible adjustment of this hyperparameter.
Should the need arise to fine-tune or optimize the σ value to align with specific requirements, such modifications can be made directly within the codebase. This level of adaptability ensures that the model’s performance can be effectively tailored to meet varying scenarios and objectives.
2. Changing Temperature
The computations will be executed at a temperature of $T = 300K$. If you wish to modify the temperature, adjust the associated variable $T$ within the fermi dirac function.
3. Optimal Computation Focus
For optimal efficiency and accuracy, it is recommended to restrict computations to bands situated close to the band edges. The provided code specifically targets transitions within the range of 30 bands around the Fermi energy. This approach ensures that the computational efforts are concentrated on relevant electronic transitions, enhancing the precision of the results while conserving computational resources. 0Although, this number can easily be changed.

## Code Variants: Serial and Parallel
This documentation outlines the differences between the serial and parallel versions of the code, focusing on their performance and considerations for optimal execution.

1. Serial Version vs. Parallel Version
The code is available in both serial and parallel versions, each with distinct performance characteristics. The parallel version is designed to enhance execution speed by utilizing multiple processing units (using joblib library).

2. Performance Comparison
While the parallel version offers faster execution times, it is important to note that the computational gains might not be substantial in all scenarios. Initial test runs indicate that the performance improvement might not be significant.

3. Optimization Factors
To achieve the best performance for your specific use case, consider the following optimization factors:

a) Total Monte Carlo Samples: Experiment with varying the number of total Monte Carlo samples. Adjusting this parameter could impact the execution speed and accuracy of results.

b) Number of Parallel Blocks: Modify the number of parallel blocks used during execution. Finding the optimal balance between parallelization and computational efficiency is key.

c) Performance Evaluation: Conduct thorough performance evaluations by testing different configurations and measuring their impact on both serial and parallel versions.

4. Experiment and Refine
To determine the most effective configuration for your computational needs, it is recommended to experiment with different combinations of parameters. This process involves adjusting the total Monte Carlo samples, number of parallel blocks, and other relevant parameters to find the optimal balance between execution time and results accuracy.

Keep in mind that the choice between the serial and parallel versions should be driven by the specific requirements of your task and the available hardware resources.
For further assistance or guidance on optimizing the code’s performance, feel free to refer to this documentation or reach out to the designated support channels.
