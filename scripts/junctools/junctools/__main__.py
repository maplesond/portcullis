
import argparse
import sys

from . import compare
from . import convert
from . import gtf
from . import markup
from . import set
from . import split

version = "1.X.X"
try:
	from . import __version__
	version = __version__
except:
	pass


def main():
	call_args = sys.argv[1:]

	parser = argparse.ArgumentParser(
		"""This script contains a number of tools for manipulating junction files.""",
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-V", "--version", action='store_true', default=False,
						help="Output the version of junctools")

	subparsers = parser.add_subparsers(
		title="Junction tools")

	compare_parser = subparsers.add_parser("compare",
										   help="Compares junction files.")
	compare.add_options(compare_parser)
	compare_parser.set_defaults(func=compare.compare)

	convert_parser = subparsers.add_parser("convert",
										   help="Converts junction files between various formats.",
										   description='''Supported file formats:

# Widely used file formats
bed        = (Input only) BED format - we automatically determine if this is
             BED 6 or 12 format, as well as if it is intron, exon or tophat style).
ebed       = (Output only) Portcullis style exon-based BED12 format (Thick-start
             and end represent splice sites).
tbed       = (Output only) Tophat style exon-based BED12 format (splice sites
             derived from blocks).
ibed       = (Output only) Intron-based BED12 format.
bed6       = (Output only) BED6 format (BED6 files are intron-based).
gtf        = (Input only) Transcript assembly or gene model containing transcript
             and exon features.  NOTE: output will only contain junctions derived
             from this GTF.
gff        = (Input only) Transcript assembly or gene model containing introns to
             extract. NOTE: input must contain \"intron\" features, and output will
             only contain these introns represented as junctions.
egff       = (Output only) Exon-based junctions in GFF3 format, uses partial
             matches to indicate exon anchors.
igff       = (Output only) Intron-based junctions in GFF3 format

# Application specific tab delimited file formats
portcullis = Portcullis style tab delimited output.
hisat      = HISAT style tab delimited format.
star       = STAR style tab delimited format.
finesplice = Finesplice style tab delimited format.
soapslice  = Soapsplice style tab delimited format.
spanki     = SPANKI style tab delimited format.
truesight  = Truesight style tab delimited format.''')

	convert.add_options(convert_parser)
	convert_parser.set_defaults(func=convert.convert)

	gtf_parser = subparsers.add_parser("gtf",
										   help="Filter or markup GTF files based on provided junctions",
									   	description='''GTF modes:
filter   = Filters out transcripts from GTF file that are not supported by the provided
           junction file.
markup   = Marks transcripts from GTF file with \'portcullis\' attribute, which indicates
           if transcript has a fully supported set of junctions, or if not, which ones are
           not supported.
compare  = For each GTF provided in the input. compare mode creates statistics describing
		   how many transcripts contain introns that are supported by a junction file.''')
	gtf.add_options(gtf_parser)
	gtf_parser.set_defaults(func=gtf.gtf)

	markup_parser = subparsers.add_parser("markup",
										  help="Marks whether each junction in the input can be found in the reference or not.")
	markup.add_options(markup_parser)
	markup_parser.set_defaults(func=markup.markup)

	set_parser = subparsers.add_parser("set",
									   description='''Supported set operations:

# These modes support 2 or more input files.
# The output contains junctions with extended anchors representing the most
# extreme extents found across all inputs
# Note: Any duplicates within a single input are removed from the output, only
# the first entry is retained
intersection = Produces the intersection of junctions from multiple input files
union        = Produces the union of junctions from multiple input files
consensus    = If there are 3 or more input files, the consensus operation produces
               a merged set of junctions where those junctions are found across
               a user-defined number of input files

# These modes only support 2 input files and produce an output file
# The output file may retain any duplicated junctions passing the set operation
subtract     = Produces an output set of junctions containing all junctions present
               in the first input file that also are not found in the second file
filter       = Produces an output set of junctions containing all junctions present
               in the first input file that are also found in the second file.  This
               is similar to an intersection on two files except that duplicates and
               additional content assigned to junctions in the first file are retained
symmetric_difference =
               Produces an output set containing junctions from both input files
               that are not present in the intersection of both

# These modes also only support 2 input files and return True or False
# depending on the test requested
is_subset    = Returns True if all junctions in the first file are present in the
               second
is_superset  = Returns True if all junctions in the second file are present in the
               first
is_disjoint  = Returns True if there is a null intersection between both files''',
									   help="Apply set operations to two or more junction files.")
	set.add_options(set_parser)
	set_parser.set_defaults(func=set.setops)

	split_parser = subparsers.add_parser("split",
										 help="Splits portcullis pass and fail juncs into 4 sets (TP, TN, FP, FN) based on whether or not the junctions are found in the reference or not.")
	split.add_options(split_parser)
	split_parser.set_defaults(func=split.split)

	args = parser.parse_args(call_args)
	if hasattr(args, "func"):
		args.func(args)
	elif args.version:
		print(version)
	else:
		parser.print_help()


if __name__ == '__main__':
	# __spec__ = "junctools"
	main()