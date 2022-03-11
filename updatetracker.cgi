#!/usr/bin/perl -w
use strict;
use JSON;

our $cachedir="/tmp/updatetracker.cache";

print "Status: 200 OK\r\nContent-type: text/plain\r\n\r\n";

my $p = $ENV{PATH_INFO};
my $m = uc($ENV{REQUEST_METHOD});
my $action;
if($p =~ s!^/(\w+)/?!!) {
    $action = $1;
} else { die "no action" }

$p=~s/[^a-z0-9_-]//g; # sanitize untrusted input
#print "$m $action $p";

sub post_update()
{
    mkdir $cachedir;
    open(my $fd, ">", "$cachedir/$p") or die;
    print $fd time();
    close $fd;
}
sub get_update()
{
    my @list;
    if($p){@list="$cachedir/$p"}
    else  {@list=<$cachedir/*>}
    my %data=();
    for my $f (@list) {
        local $/;
        open(my $fd, "<", $f) or die;
        my $basename = $f;
        $basename =~s!.*/!!;
        $data{$basename} = <$fd>;
    }
    print JSON->new->pretty->canonical->encode(\%data);
}
sub do_clear()
{
    for my $f (<$cachedir/*>) {
        unlink($f);
    }
}

if($action eq "update") {
    if($m eq "POST") {
        post_update 
    } else {
        get_update
    }
} elsif($action eq "clear") {
    do_clear;
}
