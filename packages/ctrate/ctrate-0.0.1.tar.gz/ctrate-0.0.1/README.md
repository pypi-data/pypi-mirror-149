# CTrate
Version 0.1.beta


![CTrate_white_bg](https://user-images.githubusercontent.com/60097047/164969088-94b6cf0c-4027-4f15-bab7-4c66d9968fc1.png)


About 

Rate calculation for models and molecular dynamics trajectories based on an assorted of rate theories.

List of Theories :

Fermi Golden Rule

Marcus Theory

Transient Localization Theory

Second Order Cumulant


Usage: 

In NYUSH HPC 
module use /xspace/sungroup/modules/

module load ctrate

then you can simply call 

ctrate <input file> <options>

For development:

Set the following command to your ~/.bashrc: (assuming The CTRate is in home directory, ~/)

module load gcc/7.3 cuda/11.2

export CTRATE=~/CTrate

export PATH=$PATH:$CTRATE/bin


Copyright, Sun Group, NYUSH, 2022.  
