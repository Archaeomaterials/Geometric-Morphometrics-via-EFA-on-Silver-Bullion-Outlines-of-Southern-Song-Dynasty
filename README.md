
## Geometric Morphometric Analysis Sheds New Light on Silver Bullion Production Systems of the Southern Song Period ##
This study analyzes the orthoimages of 113 Southern Song silver bullions to investigate potential correlations between their shapes and the production systems of the time. By employing a quantitative analysis of silver bullion outlines using two-dimensional geometric morphometric methods (2D-GMM) based on Elliptic Fourier Analysis and multivariate statistical techniques, the research reveals that the shapes of silver bullions vary with their weights and production locales.For detailed information, please refer to the paper "Geometric Morphometric Analysis Sheds New Light on Silver Bullion Production Systems of the Southern Song Period."

**Dataset**
-------
The dataset for this study comprises 113 orthoimages of Southern Song silver bullions, sourced from archaeological excavation reports and museum collection catalogues. 

----------
The code for this study is divided into two main parts:

1. Part 1: Outline Extraction Using `OpenCV` in `python`
   - This part utilizes Python's `OpenCV` to extract the outlines of images and their coordinates.
   - The output includes both the extracted outlines and their coordinates.

2. Part 2: Elliptical Fourier Analysis and Multivariate Statistical Analysis Using `Momocs` in `Rstudio`
   - This part primarily uses the `Momocs` package in R to perform Elliptical Fourier Analysis (EFA) on the extracted contour coordinates.
   - Additionally, multivariate statistical analysis is conducted.

Next, I will introduce methods for using the code: 
## **PART1** ##
## 1.Anaconda ##

 1. Setting up the environment
 
- Create the virtual environment required by the project
    ```python
  conda create -n extraction python=3.8
    ```
-  Activate the virtual environment:
    ```python
    conda activate extraction
    ```    
- Install the required packages:
    ```python
    python -m pip install -r requirements.txt 
    ```    
2. extract outlines and coordinates

-  Command line

    Navigate to the directory containing the `extract_outlines_and_coordinates.py` file and run the code with the following command:
    ```  
    python extract_outlines_and_coordinates.py
    ```
    Then, you can find all the  results in the `coordinates` folder.
    The results folder contains: all images outline.png and a coordinates_txt containing all coordinates.

## 2.Docker ##

 1. Setting up the environment
*   Ensure you have Docker installed on your system. 
*   Dockerfile:
 
      ```
     FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.10-slim

    WORKDIR /app

    RUN echo "deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list

    RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsm6 libxext6 libxrender-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

    ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
    ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn


    COPY requirements.txt ./

    RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

    COPY ./ ./

    CMD ["python", "extract_outlines_and_coordinates.py"]
* bulid the docker image (Windows)
 
  After preparing the dockerfile and placing it in your project directory, build the Docker image using the following command:

      docker build -t silver-gmm .

2. Run the code

   Using command line: Navigate to the whole directory. Prepare your data in the `./OpenCV--get_coordinates/data`, then use the following command to start training:
   ```
   docker run --rm -v "%cd%\OpenCV--get_coordinates\data":/app/OpenCV--get_coordinates/data silver-gmm
3. Output

   After running the script, the `coordinates` folder will be generated. You can then access the `coordinates` folder on your host machine at `./coordinates`.
   
## **PART 2** ##
## 1.Elliptical Fourier Analysis by Momocs in R 4.4.2
- All scripts are designed to be executed within the RStudio Project structure (`.Rproj`) and output figures are saved in the `figures/` folder. Execute the `01-EFA.R` script first, followed by the `02-cluster_and_cluster_bootstrap.R` script, and finally the `03-variance_boot.R` script.
- Install packages
    ```
    "Momocs", "dplyr", "ggplot2", "ggExtra", "hrbrthemes", "viridis","RColorBrewer", "colorspace", "dendextend",             "tidyverse", "cluster", "fpc", "here", "scales"
    ```
- **01-EFA.R** 

    1.Loads outline coordinate files from `OpenCV--get_coordinates/coordinates/coordinates_txt/`

    2.Loads metadata labels from `Momocs--EFA/label1.txt`

    3.Performs EFA and PCA

    4.Outputs Figures 7–9 to the figures/ folder
    
    5.get the EFA results 
    
    - `silver.f` contains the efourier results
    - `silver.p`contains PCA results
    
## 2.Multivariate Statistical Analysis: Combining data with Production Location and Bullion Weights

- **02-cluster_and_cluster_bootstrap.R**

    1.Loads label file `Momocs--EFA/label2.txt`

    2.Applies K-means clustering with bootstrap

    3.Generates cluster visualizations (e.g., Figure 10, 11, 13, 14)
- **03-variance_boot.R**

    1.Performs bootstrap analysis based on rarefaction on selected groups

    2.Outputs Figure 16   

---

## **PART 3: Academic Review Article Writing Assistant** ##

This repository now includes a comprehensive tool for writing high-quality academic review articles suitable for submission to top-tier journals.

### Overview

The **Academic Review Article Writing Assistant** (`review_article_assistant.py`) is a professional tool designed to help researchers write review articles with:

- **Critical analysis** rather than simple literature listing
- **Systematic organization** of literature by theme
- **Structured writing** with proper academic formatting
- **Multiple citation formats** (APA, IEEE, Vancouver)

### Quick Start

#### Interactive Mode (Recommended)

```bash
python review_article_assistant.py --interactive
```

This launches an interactive interface where you can:
1. Create and manage review article outlines
2. Add and organize literature entries
3. Draft sections with templates
4. Export complete manuscripts

#### Demo Mode

```bash
python review_article_assistant.py
```

This creates a demonstration project showing the tool's capabilities.

### Key Features

1. **Outline Generation**: Create structured outlines for comprehensive reviews, systematic reviews, or meta-analyses
2. **Literature Management**: Organize papers by theme, year, and methodology with automatic bibliography generation
3. **Critical Writing Support**: Avoid literature listing with guided synthesis and critical analysis
4. **Section Drafting**: Templates for introduction, main body, and conclusion sections
5. **Manuscript Export**: Generate complete manuscripts in Markdown format

### Documentation

- **Chinese Guide**: See `REVIEW_ARTICLE_GUIDE_CN.md` for detailed Chinese documentation (中文指南)
- **English Guide**: See `REVIEW_ARTICLE_GUIDE_EN.md` for comprehensive English documentation

### Use Cases

This tool is particularly useful for:
- Writing review articles about geometric morphometrics methodologies
- Synthesizing archaeological research findings
- Creating comprehensive reviews of quantitative analysis methods
- Any academic review article for top-tier journals

### Example: Creating a Review Project

```python
from review_article_assistant import ReviewArticleAssistant, Literature

# Initialize project
assistant = ReviewArticleAssistant("gmm_review")

# Create outline
outline = assistant.create_outline(
    title="Geometric Morphometrics in Archaeological Research",
    target_journal="Journal of Archaeological Science",
    scope="2D and 3D GMM methods for artifact analysis",
    time_range="2010-2024"
)

# Add literature
lit = Literature(
    authors="Smith, J., Jones, A.",
    year=2023,
    title="Advances in Elliptic Fourier Analysis",
    journal="J. Archaeol. Method Theory",
    key_findings="EFA provides robust shape quantification",
    methods="2D-GMM, EFA, PCA",
    limitations="Limited to 2D analysis"
)
assistant.literature_manager.add_literature(lit)

# Export manuscript
assistant.export_manuscript()
```

For detailed instructions and best practices, please refer to the documentation files.
  
