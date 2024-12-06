#!/usr/bin/env perl
use v5.40;

my $part1 = 0;
my $part2 = 0;
my $in_rules = 1;
my %rules;

while (<<>>) {
    chomp;
    if (!$_) {
        $in_rules = 0;
    } elsif ($in_rules) {
        $rules{$_} = 1;
    } else {
        my @pages = split ',';
        my $ok = 1;
        for my $i (0..$#pages-1) {
            for my $j ($i+1..$#pages) {
                if (defined $rules{"$pages[$j]|$pages[$i]"}) {
                    $ok = 0;
                    ($pages[$i], $pages[$j]) = ($pages[$j], $pages[$i]);
                }
            }
        }
        if ($ok) {
            $part1 += $pages[$#pages/2];
        } else {
            $part2 += $pages[$#pages/2];
        }
    }
}

say "Part 1: $part1";
say "Part 2: $part2";
