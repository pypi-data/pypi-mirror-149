### Energy Evaluation of Single Mutant Homology Models:

### Installation and Dependencies:
1. Install:
```sh
   pip install EESMHM
```
2. Download Modeller: https://salilab.org/modeller/download_installation.html
    * for Conda enviroment:
```sh 
        conda config --add channels salilab
        conda install modeller
```
3. Download EVoEF (https://github.com/tommyhuangthu/EvoEF).

4. Download foldx (https://foldxsuite.crg.eu/).

5. Add Evoef and foldx executable to $PATH.

### Configuration File:
The config.txt is used to guide the mutagensis and is organzied in three columns:
1) `1 letter amino acid` 
2) `residue number`
3) `comma seprated list of amino acids to mutate to or * for all`

If config.txt is empty all interface positions will be mutated.  

### Command line Arguments:
* `-pdb`: RCSB PDB id, if not provided you will be prompted to select one. If it is is in the current working directory it will be used. Otherwise it will be downloaded from the RCSB.
* `-qc`: Query chain to mutate.
* `-ic`: Partner chain.
