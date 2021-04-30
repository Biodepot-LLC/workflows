#!/bin/sh

# verify compression type is supported, otherwise notify user
# this also sets a valid compression flag for the tar utility
check_compression_type() {
	case $archive_compression_type in
		gzip|gz)
			compression_flag='z'
			compression_extension='.gz'
			;;
		bzip2|bz2)
			compression_flag='j'
			compression_extension='.bz2'
			;;
		xz)
			compression_flag='J'
			compression_extension='.xz'
			;;
		*)
			local valid_types="gzip|gz|bzip2|bz2|xz"
			echo "Invalid compression type '$compression_type'"
			echo "Valid compression types are '$valid_types'"
			exit 1
			;;
	esac
}

# Bwb file list type input needs to be reformatted to work with tar and rm utilities
fix_file_list() {
	echo $* | sed 's|^\[||; s|\]$||; s|,| |g; s|"||g'
}

# archive all files listed in archive_files
if [ -n "$archive_files" ]; then
	[ -n "$archive_compression_type" ] && check_compression_type
	# set filename prefix
	if [ -z "$archive_prefix" ]; then
		archive_prefix='archive'
		echo "archive_prefix not set, defaulting to $archive_prefix"
	fi
	# directory to store archive
	if [ -z "$archive_location" ]; then
		archive_location='/data'
		echo "archive_location not set, defaulting to $archive_location"
	fi
	# construct archive command
	cmd="tar cv${compression_flag}f
		${archive_location}/${archive_prefix}.tar${compression_extension}
		$(fix_file_list $archive_files)"
	if [ -n "$archive_change_to_dir" ]; then
		dir=$PWD
		echo "Changeing to directory $archive_change_to_dir"
		cd $archive_change_to_dir
	fi
	echo $cmd
	$cmd || ret=1
	[ -n "$archive_change_to_dir" ] && cd $dir
fi

# remove all files and directories listed in delete_files
if [ -n "$delete_files" ]; then
	cmd="rm -fr $(fix_file_list $delete_files)"
	echo $cmd
	$cmd || ret=1
fi

exit $ret
