#!/usr/bin/env perl
use v5.40;

sub parse($tok) {
    $tok =~ /mul\((\d{1,3}),(\d{1,3})\)/;
    return $1 * $2;
}

my @lines = <<>>;

my $part1 = 0;
for (@lines) {
    while (/(mul\(\d{1,3},\d{1,3}\))/g) {
	$part1 += parse($1);
    }
}
say "Part 1: $part1";

my $part2 = 0;
my $do = 1;
for (@lines) {
    while (m/(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))/g) {
	if ($1 eq "do()") {
	    $do = 1;
	} elsif ($1 eq "don't()") {
	    $do = 0;
	} elsif ($do) {
	    $part2 += parse($1);
	}
    }
}
say "Part 2: $part2";
