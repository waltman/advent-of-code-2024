#!/usr/bin/env perl
use v5.40;
use List::Util qw(sum zip);

my (@list1, @list2);

while (<<>>) {
    chomp;
    my @toks = split '   ';
    push @list1, $toks[0];
    push @list2, $toks[1];
}

say "Part 1: ", sum map {abs $_->[0] - $_->[1]} zip [sort {$a<=>$b} @list1], [sort {$a<=>$b} @list2];

my $sum = 0;
for my $l1 (@list1) {
    $sum += $l1 * grep {$_ == $l1} @list2;
}
say "Part 2: $sum";
