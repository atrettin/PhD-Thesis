# Search for eV-scale Sterile Neutrinos with the IceCube DeepCore Detector

This repository contains the full source code of my PhD thesis on the measurment of eV-scale sterile neutrinos with the IceCube DeepCore detector.

## How to compile

The PDF is generated by compiling `main.tex`. It is recommended, though not strictly necessary, to use LuaLaTeX. Compiling this document requires several runs of `biber` and `pdflatex`/`lualatex` to resolve all references and place all figures correctly. This is best done automatically using `pdflatexmk`. Because this document uses `tikz` externalization, `-shell-escape` has to be enabled. The first two lines in `main.tex` enable these settings for TeXShop, so compiling on a Mac with TeXShop should "just work" ;) 

## Extracting figures and results

Many figures in this thesis are generated by LaTeX using the `pgfplots` package. After compiling the document, the PDF output for all these figures can be found in the `tikz/` directory. The data behind the figures, such as the coordinates for contour lines, can usually be found in a CSV document in the same directory as the `.tex` source of the figure. In particular, the contour lines for the analysis results are in the `figures/measurement/sterile_analysis/results/contour_data/`, where the 90% (99%)  contours are listed in `real_data_v12_wilks_contour_90(99)pct.csv`. The metric scan over the mixing amplitudes is listed in `real_data_v12_matrix_elems.csv`, and can be used to generate contours at different levels of significance.

## Kaobook class

The layout of this thesis is using the kaobook class (https://github.com/fmarotta/kaobook).
