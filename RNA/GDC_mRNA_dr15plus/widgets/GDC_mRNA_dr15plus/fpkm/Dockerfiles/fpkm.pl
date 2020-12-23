#!/usr/bin/perl
#Ling-Hong Hung 2020
my ($gencodeFile,$sampleFile)=@ARGV;

print STDERR "Opening gene code summary $gencodeFile\n";
open (FIL, $gencodeFile) || die;
my $line=<FIL>;
my %pcLength;
my %geneLength;
my $basename=$sampleFile;
if (substr($sampleFile,-4,1) eq "."){
	$basename=substr($sampleFile,0,-4);
}
while (defined(my $line=<FIL>)){
	my @parts=split(/\t/,$line);
	my $name=$parts[0];
	my $len=$parts[10];
	$geneLength{$name}=$len;
	if ($parts[6] eq "protein_coding"){
	    $pcLength{$name}=$len;	
	} 
}

open (FIL, $sampleFile) || die;
my $header=<FIL>;
my @names;
my @pcSums;
my @uq75s;
my @counts;
my @parts=split(/\t/,"$header");
my $nfields=$#parts;
while (defined(my $line=<FIL>)){
	chomp($line);
	my @parts=split(/\t/,$line);
	my $name=$parts[0];
	my $length=$geneLength{$name};
	if($length){
		push(@names,$name);
		if($pcLength{$name}){
			foreach my $i (1..$nfields){
				push(@{$counts[$i-1]},$parts[$i]);
				$pcSums[$i-1]+=$parts[$i];
			}			
		}
		else{
			foreach my $i (1..$nfields){
				push(@{$counts[$i-1]},$parts[$i]);
			}
		}
	}
}
foreach my $i (0..$nfields-1){
 my(@sorted)=sort{$a <=> $b} @{$counts[$i]};
 my $uq75index=sprintf "%d",($#sorted+1)*.75;
 $uq75s[$i]=$sorted[$uq75index];
}
open (fpkmfp,">$basename\_fpkm.tsv") || die;
open (fpkmUQfp,">$basename\_fpkmUQ.tsv") || die;
open (countsfp,">$basename\_counts.tsv") || die;
print countsfp "$header";
print fpkmfp "$header";
print fpkmUQfp "$header";
foreach my $i (0..$#names){
	my $name=$names[$i];
	my $length=$geneLength{$name};
	print countsfp "$names[$i]";
	print fpkmfp "$names[$i]";
	print fpkmUQfp "$names[$i]";
	foreach my $j (0..$nfields-1){
		my $counts=$counts[$j][$i];
		my $fpkm=$counts*1000000000/($length*$pcSums[$j]);
		my $fpkmUQ=$counts*1000000000/($length*$uq75s[$j]);
		print countsfp "\t$counts";
		print fpkmfp "\t$fpkm";
		print fpkmUQfp "\t$fpkmUQ";
	}
	print countsfp "\n";
	print fpkmfp "\n";
	print fpkmUQfp "\n";
}
