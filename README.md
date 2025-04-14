# MLG Dashboard

## Description
MLG Dashboard is a lightweight, user-friendly GUI tool that leverages ProbML models to identify potential probiotic candidates directly from genomic data. In addition, the platform enables users to create personalized datasets and train custom machine learning models tailored to their specific research needs.

## Features
- **ProbML Module**: Classify genomes into probiotics or non-probiotics using in-house trained 12 XGB_LD3_IITMd models.
- **Kmers Module**: Generate a Kmer frequency matrix for training models.
- **Training Module**: Train various ML models using your dataset.
- **Prediction Module**: Classify genomes using the trained models.

## Requirements
- numpy
- pandas
- pillow
- scikit-learn
- scipy
- tkinter
- xgboost

## Installation and usage
1. Ensure you have Python version 3 or higher installed.
2. Install the required dependencies
3. **Clone the repository**:

    ```cmd
    git clone https://github.com/sysbio-iitmandi/MLG_Dashboard

    ```
4. Navigate to the directory

    ```cmd
    cd MLG_Dashboard-main/
    ```
5. Run the program

    ```cmd
    python probml_gui.py
    ```

## License

This project is licensed under the MIT License with a citation requirement. See the [LICENSE](LICENSE) file for details.

## Contact Information
  For support or questions, please contact the Systems Biology Lab, IIT Mandi at sysbio.iitmandi.gmail.com.

## Cite us
A. Orkkatteri Krishnan, L. N. Mudgal, V. Soni, T. Prakash, ProbML: A Machine Learning-Based Genome Classifier for Identifying Probiotic Organisms. Mol. Nutr. Food Res. 2025, e70025. [https://doi.org/10.1002/mnfr.70025](url)

