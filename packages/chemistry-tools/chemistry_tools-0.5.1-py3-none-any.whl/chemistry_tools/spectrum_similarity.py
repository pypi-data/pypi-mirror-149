#!/usr/bin/env python3
#
#  spectrum_similarity.py
"""
Mass spectrum similarity calculations.
"""
#
#  Copyright (c) 2019-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Adapted from SpectrumSimilarity.R
#  Part of OrgMassSpecR
#  |  Copyright (c) 2011-2017 Nathan Dodder <nathand@sccwrp.org>
#  |  Available under the BSD 2-Clause License
#  |
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |    Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |    Redistributions in binary form must reproduce the above copyright notice, this
#  |    list of conditions and the following disclaimer in the documentation and/or
#  |    other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
#  |  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  |  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  |  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from typing import Mapping, Optional, Sequence, Tuple, Union

# 3rd party
import numpy
import pandas  # type: ignore

__all__ = ["spectrum_similarity", "normalize", "create_array"]


def spectrum_similarity(
		spec_top: numpy.ndarray,
		spec_bottom: numpy.ndarray,
		t: float = 0.25,
		b: float = 10,
		top_label: Optional[str] = None,
		bottom_label: Optional[str] = None,
		xlim: Tuple[int, int] = (50, 1200),
		x_threshold: float = 0,
		print_alignment: bool = False,
		print_graphic: bool = True,
		output_list: bool = False,
		) -> Union[Tuple[float, float], Tuple[float, float, pandas.DataFrame]]:
	"""
	Calculate the similarity score for two mass spectra.

	:param spec_top: Array containing the experimental spectrum's peak list with the m/z values in the
		first column and corresponding intensities in the second
	:param spec_bottom: Array containing the reference spectrum's peak list with the m/z values in the
		first column and corresponding intensities in the second
	:param t: numeric value specifying the tolerance used to align the m/z values of the two spectra.
	:param b: numeric value specifying the baseline threshold for peak identification.
		Expressed as a percent of the maximum intensity.
	:param top_label: string to label the top spectrum.
	:param bottom_label: string to label the bottom spectrum.
	:param xlim: tuple of length 2, defining the beginning and ending values of the x-axis.
	:param x_threshold: numeric value specifying
	:param print_alignment:  whether the intensities should be printed
	:param print_graphic:
	:param output_list: whether the intensities should be returned as a third element of the tuple.
	"""

	# format spectra and normalize intensitites
	top_tmp = pandas.DataFrame(data=spec_top, columns=["mz", "intensity"])
	top_tmp["normalized"] = top_tmp.apply(normalize, args=(max(top_tmp["intensity"]), ), axis=1)
	top_tmp = top_tmp[top_tmp["mz"].between(xlim[0], xlim[1])]
	top_plot = top_tmp[["mz", "normalized"]].copy()  # data frame for plotting spectrum
	top_plot.columns = ["mz", "intensity"]
	top = top_plot[top_plot["intensity"] >= b]  # data frame for similarity score calculation

	bottom_tmp = pandas.DataFrame(data=spec_bottom, columns=["mz", "intensity"])
	bottom_tmp["normalized"] = bottom_tmp.apply(normalize, args=(max(bottom_tmp["intensity"]), ), axis=1)
	bottom_tmp = bottom_tmp[bottom_tmp["mz"].between(xlim[0], xlim[1])]
	bottom_plot = bottom_tmp[["mz", "normalized"]].copy()  # data frame for plotting spectrum
	bottom_plot.columns = ["mz", "intensity"]
	bottom = bottom_plot[bottom_plot["intensity"] >= b]  # data frame for similarity score calculation

	# align the m/z axis of the two spectra, the bottom spectrum is used as the reference

	# Unimplemented R code
	#   for(i in 1:nrow(bottom))
	# 	top["mz"][bottom["mz"][i] >= top["mz"] - t & bottom["mz"][i] <= top["mz"] + t] = bottom["mz"][i]
	# 	top[,1][bottom[,1][i] >= top[,1] - t & bottom[,1][i] <= top[,1] + t] <- bottom[,1][i]
	#   alignment <- merge(top, bottom, by = 1, all = TRUE)
	#   if(length(unique(alignment[,1])) != length(alignment[,1])) warning("the m/z tolerance is set too high")
	# alignment[,c(2,3)][is.na(alignment[,c(2,3)])] <- 0   # convert NAs to zero (R-Help, Sept. 15, 2004, John Fox)
	# names(alignment) <- c("mz", "intensity.top", "intensity.bottom")
	#
	alignment = pandas.merge(top, bottom, on="mz", how="outer")
	alignment.fillna(value=0, inplace=True)  # Convert NaN to 0
	alignment.columns = ["mz", "intensity_top", "intensity_bottom"]
	if print_alignment:
		with pandas.option_context("display.max_rows", None, "display.max_columns", None):
			print(alignment)

	# similarity score calculation

	if x_threshold < 0:
		raise ValueError("x_threshold argument must be zero or a positive number")

	# Unimplemented R code
	# alignment <- alignment[alignment[,1] >= x.threshold, ]

	u = numpy.array(alignment.iloc[:, 1])
	v = numpy.array(alignment.iloc[:, 2])

	similarity_score = numpy.dot(u, v) / (
			numpy.sqrt(numpy.sum(numpy.square(u))) * numpy.sqrt(numpy.sum(numpy.square(v)))
			)

	# Reverse Match
	reverse_alignment = pandas.merge(top, bottom, on="mz", how="right")
	reverse_alignment = reverse_alignment.dropna()  # Remove rows containing NaN
	reverse_alignment.columns = ["mz", "intensity_top", "intensity_bottom"]
	u = numpy.array(reverse_alignment.iloc[:, 1])
	v = numpy.array(reverse_alignment.iloc[:, 2])

	reverse_similarity_score = numpy.dot(u, v) / (
			numpy.sqrt(numpy.sum(numpy.square(u))) * numpy.sqrt(numpy.sum(numpy.square(v)))
			)

	# generate plot

	if print_graphic:
		# 3rd party
		import matplotlib.pyplot as plt  # type: ignore  # nodep

		fig, ax = plt.subplots()
		# fig.scatter(top_plot["mz"],top_plot["intensity"], s=0)
		ax.vlines(top_plot["mz"], 0, top_plot["intensity"], color="blue")
		ax.vlines(bottom["mz"], 0, -bottom["intensity"], color="red")
		ax.set_ylim(-125, 125)
		ax.set_xlim(xlim[0], xlim[1])
		ax.axhline(color="black", linewidth=0.5)
		ax.set_ylabel("Intensity (%)")
		ax.set_xlabel("m/z", style="italic", family="serif")

		h_centre = xlim[0] + (xlim[1] - xlim[0]) // 2

		ax.text(h_centre, 110, top_label, horizontalalignment="center", verticalalignment="center")
		ax.text(h_centre, -110, bottom_label, horizontalalignment="center", verticalalignment="center")
		plt.show()

	# Unimplemented R code
	# 	ticks <- c(-100, -50, 0, 50, 100)
	# 	plot.window(xlim = c(0, 20), ylim = c(-10, 10))
	#
	#
	#   if(output.list == TRUE) {
	#
	# 	# Grid graphics head to tail plot
	#
	# 	headTailPlot <- function() {
	#
	# 	  pushViewport(plotViewport(c(5, 5, 2, 2)))
	# 	  pushViewport(dataViewport(xscale = xlim, yscale = c(-125, 125)))
	#
	# 	  grid.rect()
	# 	  tmp <- pretty(xlim)
	# 	  xlabels <- tmp[tmp >= xlim[1] & tmp <= xlim[2]]
	# 	  grid.xaxis(at = xlabels)
	# 	  grid.yaxis(at = c(-100, -50, 0, 50, 100))
	#
	# 	  grid.segments(top_plot$mz,
	# 					top_plot$intensity,
	# 					top_plot$mz,
	# 					rep(0, length(top_plot$intensity)),
	# 					default.units = "native",
	# 					gp = gpar(lwd = 0.75, col = "blue"))
	#
	# 	  grid.segments(bottom_plot$mz,
	# 					-bottom_plot$intensity,
	# 					bottom_plot$mz,
	# 					rep(0, length(bottom_plot$intensity)),
	# 					default.units = "native",
	# 					gp = gpar(lwd = 0.75, col = "red"))
	#
	# 	  grid.abline(intercept = 0, slope = 0)
	#
	# 	  grid.text("intensity (%)", x = unit(-3.5, "lines"), rot = 90)
	# 	  grid.text("m/z", y = unit(-3.5, "lines"))
	#
	# 	  popViewport(1)
	# 	  pushViewport(dataViewport(xscale = c(0, 20), yscale = c(-10, 10)))
	# 	  grid.text(top.label, unit(10, "native"), unit(9, "native"))
	# 	  grid.text(bottom.label, unit(10, "native"), unit(-9, "native"))
	#
	# 	  popViewport(2)
	#
	# 	}
	#
	# 	p <- grid.grabExpr(headTailPlot())
	#
	#   }
	#
	# with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
	# 	print(similarity_score)

	if output_list:
		return similarity_score, reverse_similarity_score, alignment
	# Unimplemented R code
	#
	# return(list(similarity.score = similarity_score,
	# 	alignment = alignment,
	# 	plot = p))
	#
	else:
		return similarity_score, reverse_similarity_score


# simscore <- as.vector((u %*% v)^2 / (sum(u^2) * sum(v^2)))   # cos squared

SpectrumSimilarity = spectrum_similarity


def normalize(row: Union[Mapping, pandas.Series], max_val: Union[float, str]) -> float:
	"""
	Returns the normalised intensity for each rows of a :class:`pandas.DataFrame`.

	:param row:
	:param max_val:
	"""

	# http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/
	return (row["intensity"] / float(max_val)) * 100.0


def create_array(intensities: Sequence[float], mz: Sequence[float]) -> numpy.ndarray:
	"""
	Create a :class:`numpy.ndarray`, in a format appropriate for :func:`~.spectrum_similarity`,
	from a list of intensities and a list of *m/z* values.

	:param intensities: List of intensities
	:param mz: List of *m/z* values.
	"""  # noqa: D400

	return numpy.column_stack((mz, intensities))
