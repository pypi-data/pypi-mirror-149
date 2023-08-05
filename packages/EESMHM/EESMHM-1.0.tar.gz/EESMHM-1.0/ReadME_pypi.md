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
3. Download EvoEF (https://github.com/tommyhuangthu/EvoEF). Save and running the following bash script to easiy download and compile EvoEF  
```sh
	path=`python -c 'import site; print(site.getsitepackages()[0])'`
	path=${path}/EESMHM
	echo $path
	cd $path
	wget https://github.com/tommyhuangthu/EvoEF/archive/refs/heads/master.zip
	unzip master.zip
	rm master.zip
	cd EvoEF-master
	chmod +x build.sh
	./build.sh
```

4. Download foldx5 (https://foldxsuite.crg.eu/) and add executable to path.


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
* `-config`: config file path
* `-foldx`: use foldx
* `-evoef`: use EvoEF 
