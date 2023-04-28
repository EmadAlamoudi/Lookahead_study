
-   **Codes** Contains all files and scripts required to run the models, 

    -   **M1\_Tumor** Everything required to run and evaluate the tests
        of the tumor growth model (M1). The inference is performed in
        the python programs *TumorAdaptiveEps.py* an adaptive epsilon. 
        Executing these files returns detailed information about each
        run in a database file, and some additional statistics about the
        effect of the look-ahead scheduling is written into .csv file.

    -   **M2\_HIV** The python programs used to perform parameter
        inference for the HIV model (M2) and the results of the 8 runs
        (.csv files, and for the LA, adaptive epsilon run on 256 workers
        also the database). Also, the notebook used to visualize these
        results, creating Figures 25, 26. Model and posterior plots
        (Figure 24) provided by Nils Bundgaard.

    -   **T1\_UnbModes** Files used to run model (T1) on an HPC. The 
		inference is performed multiple times by executing the python
		program *run_bimodal.py*. The scipt was run on different 
		configrations producing database file, some additional 
		statistics about the effect of the look-ahead scheduling for the
		 run in .csv file.

    -   **T2\_ODE** Everything required to run and evaluate the tests of
        the ODE model (T2). The inference is performed multiple times by
        executing the python program *ODEWLogfiles.py*. Executing this
        file returns detailed information about each repetition in a
        separate database file, some additional statistics about the
        effect of the look-ahead scheduling for each run in different
        .csv files and additionally a .txt file containing summarized
        wall time statistics.

-   **Concept_figures** Contains all some illustrations that are 
	independent of the models, 

-   **Notebooks** Contains all notebooks for different models that was 
	used to generate the figures used in the paper, 
	
	-   **{MODEL_ID}_figures** contaning the produced figure from the 
	notebooks for the differents models.

-   **Data** a file that containes all the result of the fitting process
	that was presented on the paper. there are sub folder for each 
	models.	Using the notebooks, one can directly plot all needed 
	figures from these data files. <span style="color:blue">some *blue* 
	Important note: Due to size limit, this folder was not uploaded to
	Github. Instead the folder can be found on the Zenodo link 
	here: TODO</span>


-   **pyABC** Version 0.12.07 which was used for testing and a run different models.

-   **FitMultiCell** Version 0.0.08 which was used for model M2..

-   **Morpheus** Version 2.2.0 which was used for model M2..


-   **tumor2d** Version 1.0.0 of the tumor2d package required to run the
    tumor model (M1).


