## Table of Contents
- [Introduction](#introduction)
	- [Contributors](#contributors)
	- [Dependencies](#dependencies)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
	- [Modes](#modes)
		- [RAxML](#raxml)
		- [File Converter](#file-converter)
		- [MS Comparison](#ms-comparison)
		- [D Statistic](#d-statistic)

## Introduction
PhyloVis is a python-based application that provides an intuitive user interface for phylogenetic analyses and data visualization. It has four distinct modes that are useful for different types of phylogenetic analysis: RAxML, File Converter, MS Comparison and D-Statistic.

RAxML mode gives users a front-end to interact with RAxML (STAMATAKIS 2014a) for Maximum Likelihood based inference of large phylogenetic trees. PhyloVis’s RAxML mode allows one to use RAxML to automatically perform sliding window analysis over an inputted alignment. Users are able to select from a plethora of options in performing their analysis, including: window size, window offset, and number of bootstraps. In this mode, users are able to produce a variety of graphs to help understand their genomic alignment and interpret the trees outputted by RAxML. These graph options include: visualization of the top topologies, scatter plot of windows to their topologies, frequency of top topologies, genome atlas, and a heat map of the informative sites. RAxML mode also provides support for calculating two statistics based on the trees produced within each window as compared to an overall species tree; Robinson-Foulds distance and probability of gene tree given species tree, p(gt\|st).

The file converter in PhyloVis provides a user interface for a Biopython AlignIO file converter function. It allows users to convert between 12 different popular genome alignment file types. RAxML mode only accepts phylip-sequential format.

MS Comparison mode allows users to perform an accuracy comparison between a “truth file” and one or more files in MS format or the results of RAxML mode.

With D-Statistic mode users can compute Patterson’s D-Statistic for determining introgression in a four taxa alignment. D-Statistic mode can produce graphs for the value of the D-Statistic across sliding windows as well as the value of the D-Statistic across the entire alignment.
### Contributors
- [Chabrielle Allen](https://github.com/chaballen)
- [Travis Benedict](https://github.com/travisbenedict)
- [Peter Dulworth](https://github.com/PeterDulworth)
- [Chill Leo]()
- [Luay]()

### Dependencies
- [BioPython](http://biopython.org/wiki/Documentation)
- [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/)
- [DendroPy](https://www.dendropy.org/)
- [MatPlotLib](https://matplotlib.org/)
- [ETE](http://etetoolkit.org/)

## Installation
Install it. How? We don't know.

## Basic Usage

### RAxML
#### Standard
#### Advanced
### File Converter
### MS Comparison
### D Statistic

## More Examples

## Detailed Input Documentation


```python
p = subprocess.Popen("raxmlHPC -f a -x12345 -p 12345 -# 2 -m GTRGAMMA -s {0} -n txt".format(phylip), shell=True)
```