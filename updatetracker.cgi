#!/usr/bin/perl -w
# SPDX-License-Identifier: GPL-2.0-only
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

$p=~s/[^a-z0-9\@_.+-]//g; # sanitize untrusted input
#print "$m $action $p";
my @params = split("&", $ENV{QUERY_STRING});
my %params = ();
foreach(@params) {
    my ($k,$v) = split("=");
    $k =~ s/[^a-z0-9]//g; # sanitize untrusted input
    $v =~ s/[^a-z0-9]//g; # sanitize untrusted input
    $params{$k} = $v;
}

sub post_update()
{
    mkdir $cachedir;
    $p=~s/\.//g;
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
    if (my $b = $params{base}) {
        my $bv = $data{$b};
        foreach(keys %data) {
            $data{$_} -= $bv;
        }
    }
    print JSON->new->pretty->canonical->encode(\%data);
}
sub do_clear()
{
    for my $f (<$cachedir/*>) {
        unlink($f);
    }
}
sub do_send()
{
    my %whitelist=qw(
        bwiedemann+mailtest-imap-forward-at-suse.de 1
        mailmanautotest-at-suse.de 1
        schleuderautotest-at-suse.de 1
    );
    my($addr, $server)=split("@", $p);
    return unless $whitelist{$addr};
    $addr =~ s/-at-/\@/;
    $server ||= "mx2.suse.de";
    print "sending...\n";
    system(qw(swaks --server), $server, "--to", $addr);
    print "sent\n";
}

if($action eq "update") {
    if($m eq "POST") {
        post_update
    } else {
        get_update
    }
} elsif($action eq "clear") {
    do_clear;
} elsif($action eq "send" and $m eq "POST") {
    do_send;
}
