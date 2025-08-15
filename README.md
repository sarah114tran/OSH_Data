### 1. Description
A repository for developing scripts and working on classifiers for assembling OSH datasets

### 2. Repository Structure
```
├── Data
│   ├── Clean
│   │   ├── hackaday
│   │   │   └── hackaday_cleaned.csv
│   │   └── ohr
│   │       └── ohr_hardware_cleaned.csv
│   ├── Raw
│   │   ├── hackaday
│   │   │   └── hackaday_raw.csv
│   │   ├── kitspace
│   │   │   ├── kitspace_projects.json
│   │   │   └── kitspace_results.json
│   │   ├── ohr
│   │   │   └── ohr_raw.csv
│   │   ├── openhardware.io
│   │   │   └── hardwareIO_allProjects.json
│   │   ├── oshwa
│   │   │   └── oshwa_raw.csv
│   │   └── scientific_literature
│   │       ├── hardwareX
│   │       │   └── ohx_allPubs_extract.json
│   │       ├── joh
│   │       │   └── Journal of Open Hardware Papers.csv
│   │       ├── openalex_metadata.csv
│   │       └── openalex_metadata.json
│   └── Repo_Data
│       ├── git
│       │   └── place
│       ├── osf
│       │   ├── osf_comprehensive_metadata_dataset.json
│       │   ├── OSF_METADATA_README.md
│       │   ├── osf_ohx_links.txt
│       │   ├── osf_project_urls_validated.txt
│       │   └── place
│       └── zenodo
│           └── place
├── EDA
│   ├── hackaday
│   │   └── hackaday_analysis_report.txt
│   ├── ohr
│   │   └── ohr_analysis_report.txt
│   └── OSHWA
│       └── raw
│           ├── analysis_results.json
│           ├── certifications_by_year.png
│           ├── geographic_distribution.png
│           ├── oshwa_raw_analysis_report.txt
│           └── project_types.png
├── Prompt_Evaluation
│   ├── prompt
│   │   ├── prompt_1.md
│   │   └── prompt_2.md
│   └── results
│       ├── prompt_1
│       │   └── prompt_1_results_sarah.json
│       └── prompt_2
│           ├── place
│           ├── prompt_2_results_nic.json
│           └── prompt_2_sarah.json
└── SRC
    ├── data_collection
    │   ├── hardwareIO
    │   │   └── hardwareIO.py
    │   ├── metadata
    │   │   ├── github_metadata_collector.py
    │   │   ├── gitlab_metadata_extration.py
    │   │   ├── osf_comprehensive_metadata_collector.py
    │   │   └── OSF-metadata.py
    │   ├── ohr
    │   │   ├── ohr_raw.py
    │   │   └── ohr_wiki_extraction.py
    │   ├── oshwa
    │   │   └── oshwa_raw.py
    │   └── scientific_literature
    │       ├── hardwareX
    │       │   └── ohx.py
    │       └── openalex_metadata.py
    └── data_processing
        ├── classifiers
        │   └── ohr_repo_classifier.py
        ├── cleaners
        │   └── oshwa
        │       └── oshwa_clean.py
        └── prompt_gpt.py

```
