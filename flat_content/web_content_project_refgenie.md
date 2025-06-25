Reference genome assemblies are essential for high-throughput sequencing analysis projects. Typically, genome assemblies are stored on disk alongside related resources; e.g., many sequence aligners require the assembly to be indexed. The resulting indexes are broadly applicable for downstream analysis, so it makes sense to share them. However, there is no simple tool to do this.

Refgenie is a reference genome assembly asset manager. Refgenie makes it easier to organize, retrieve, and share genome analysis resources. In addition to genome indexes, refgenie can manage any files related to reference genomes, including sequences and annotation files. Refgenie includes a command line interface and a server application that provides a RESTful API, so it is useful for both tool development and analysis.

RC staff supported this project through its design phase, underlying infrastructure and final deployment of a Refgenie server within containers, which are attached to reference data in high performance storage.

<http://refgenie.databio.org/>

**PI: Nathan Sheffield ([Center for Public Health Genomics](https://med.virginia.edu/cphg/))**
