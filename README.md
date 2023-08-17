# PyAuger v0.0.1
An incomplete First-Principle Auger Computation Code using Python with VASP.

## Package requirements
• numpy
• scipy
• matplotlib, seaborn
• pymatgen
• pandas (optional)


1. PBE Bandstructure Calculation
Perform a regular PBE bandstructure calculation in VASP (for example using the pymatgen vasp input sets). You can find an example of this process in the provided link. Please note that some functionalities might differ in the updated pymatgen API.

2. Set Up Directory
Copy the non-SCF (self-consistent field) directory and place the k grid sample.sh script within it.

3. Adjust INCAR File and Run Non-SCF Calculations
Review the INCAR file tags and make any necessary adjustments. Once satisfied, execute the k grid sample.sh script. This script will initiate non-SCF calculations for various k-grids, which can be configured from within the script itself.
Please carefully examine the script’s content.

4. Post-Computation Analysis
After the calculations are converged, copy the parse output.py Python script from the directory. This script can be used to check convergence, parse Fermi energy, k-grid details, band energies, point weights, and more. You can customize the script according to your needs. Ensure that the directory contains KPOINTS, vasprun.xml, and EIGENVAL files as these are required by the script.
Subsequently, execute the get fermi cutoff.py script. This action will produce a text file named band info.txt, which will encompass details such as the fermi energy, as well as the minimum and maximum band indices necessary for running the parallel carlo.py or carlo auger.py code in the later stages. Generally, this step needs to be carried out only once, perhaps with a 20 × 20 × 20 or 50 × 50 × 50 kgrid configuration, since empirical tests have shown minimal variance in the band indices as the kgrid dimensions are increased.

5. File Naming
File names are self-explanatory. For instance, kw 10 47.npy is the k-point weight file resulting from a 10 × 10 × 10 k-grid computation with 47 irreducible k-points. I will call 10 as X and 47 as XX. So, for 20 × 20 × 20 grid, X = 20 and XX = 256 as there are 256 irreducible k-points. How do you get these numbers? parse output.py script will tell you these numbers when you run it.

6. Create a New Directory
Run the create oj dir.sh script. It will create a new directory called auger main and copy all .npy files in that directory.
Along with these, you need to copy parallel carlo.py or carlo auger.py and job submission script to the auger main directory.
The difference between parallel carlo.py and carlo auger.py is that one is parallel and one is serial. The difference and best practices have been explained in a later section.
7. Run Calculation
Execute the job script.sh script. Before each run, remember to modify the job name. Also, update the X and XX tags in the parallel carlo.py script as necessary.
8. Check Outputs
Upon completion of a computation, read the job-name.out file for results. For details of any errors, refer to the job-name.err file.
These steps guide you through the process of using the provided code for Auger computations. If you encounter any issues or need further assistance, please refer to this documentation or contact the relevant support channels.

Things to keep in mind

1. Model Hyperparameter
The hyperparameter σ plays a critical role within the model’s configuration. Currently, it has been predefined as 0.01, reflecting the existing setting. However, it’s worth noting that the code allows for flexible adjustment of this hyperparameter.
Should the need arise to fine-tune or optimize the σ value to align with specific requirements, such modifications can be made directly within the codebase. This level of adaptability ensures that the model’s performance can be effectively tailored to meet varying scenarios and objectives.

• Changing Temperature
The computations will be executed at a temperature of T = 300K. If you wish to modify the temperature, adjust the associated variable T within the fermi dirac function.

2. Optimal Computation Focus
For optimal efficiency and accuracy, it is recommended to restrict computations to bands situated close to the band edges. The provided code specifically targets transitions within the range of 30 bands around the Fermi energy. This approach ensures that the computational efforts are concentrated on relevant electronic transitions, enhancing the precision of the results while conserving computational resources. 0Although, this number can easily be changed.

Code Variants: Serial and Parallel
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
