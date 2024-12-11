#!/usr/bin/env perl
use v5.40;
use autodie;
use List::Util qw(sum);

my @stones;
open my $fh, '<', $ARGV[0];
while (<$fh>) {
    chomp;
    @stones = split ' ';
}

my %cnts;
for my $stone (@stones) {
    $cnts{$stone}++;
}

for my $i (1..$ARGV[1]) {
    my %new_cnts;
    while (my ($k, $v) = each %cnts) {
        if ($k == 0) {
            $new_cnts{1} += $v;
        } elsif ((my $len = length($k)) % 2 == 0) {
            $new_cnts{0 + substr $k, 0, $len/2} += $v;
            $new_cnts{0 + substr $k, $len/2} += $v;
        } else {
            $new_cnts{$k * 2024} += $v;
        }
    }
    %cnts = %new_cnts;
    printf "i = %d sum = %d\n", $i, sum values %cnts;
}
