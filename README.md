# EHR summarization

## Overview

This is a repo for Coronary artery disease (CAD) electronic health record (EHR) summarization. It contains a pipeline for processing the xml data and NLP model for extracting information. 
A GUI is also integrated to visulize the result

`Pipeline.ipynb` 
A jupyter notebook format final pipeline. It contains data preprocessing, creating input files to the algorithms, and evaluation

`GUI` 
The integrated GUI is created using Streamlit and is located in a public Github repo (https://github.com/lyz9928/EHR). The GUI can also be direcctly accessed with the link: https://ehr-summary.streamlit.app/

## Usage

1. Request data access at i2b2 2014 website (https://portal.dbmi.hms.harvard.edu/projects/n2c2-2014/)
2. Go to script folder and access the pipeline
3. Further instruction please see details within the pipeline

## References

1. Uzuner Ö, Stubbs A. Practical applications for natural language processing in clinical research: The 2014 i2b2/UTHealth shared tasks. J Biomed Inform. 2015 Dec;58 Suppl(Suppl):S1-S5. doi: 10.1016/j.jbi.2015.10.007. Epub 2015 Oct 24. PMID: 26515500; PMCID: PMC4978169.

