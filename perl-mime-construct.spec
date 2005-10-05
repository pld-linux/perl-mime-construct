
%define filelist mime-construct-%{version}-filelist

Summary:	mime-construct - construct and optionally mail MIME messages
Summary(pl):	mime-construct - tworzenie i opcjonalnie wysy³anie wiadomo¶ci MIME
Name:		perl-mime-construct
Version:	1.9
Release:	1
Vendor:		Roderick Schertler <roderick@argon.org>
License:	Artistic
Group:		Applications/Mail
Source0:	http://search.cpan.org/CPAN/authors/id/R/RO/ROSCH/mime-construct-%{version}.tar.gz
URL:		http://search.cpan.org/dist/mime-construct/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mime-construct constructs and (by default) mails MIME messages. It
is entirely driven from the command line, it is designed to be used by
other programs, or people who act like programs.

%description -l pl
mime-construct tworzy i (domy¶lnie) wysy³a wiadomo¶ci MIME. Jest
sterowane ca³kowicie z linii poleceñ i zosta³o zaprojektowane z my¶l±
o u¿ywaniu przez inne programy lub ludzi zachowuj±cych siê jak
programy.

%prep
%setup -q -n mime-construct-%{version}
chmod -R u+w %{_builddir}/mime-construct-%{version}

%build
grep -rsl '^#!.*perl' . |
grep -v '.bak$' |xargs --no-run-if-empty \
%__perl -MExtUtils::MakeMaker -e 'MY->fixin(@ARGV)'
%{__perl} Makefile.PL `%{__perl} -MExtUtils::MakeMaker -e ' print qq|PREFIX=$RPM_BUILD_ROOT%{_prefix}| if \$ExtUtils::MakeMaker::VERSION =~ /5\.9[1-6]|6\.0[0-5]/ '`
%{__make}
%{__make} test

%install
mkdir -p $RPM_BUILD_ROOT
%{__make} `%{__perl} -MExtUtils::MakeMaker -e ' print \$ExtUtils::MakeMaker::VERSION <= 6.05 ? qq|PREFIX=$RPM_BUILD_ROOT%{_prefix}| : qq|DESTDIR=$RPM_BUILD_ROOT| '`

# remove special files
find $RPM_BUILD_ROOT -name "perllocal.pod" \
    -o -name ".packlist"                \
    -o -name "*.bs"                     \
    |xargs -i rm -f {}

%{__perl} -MFile::Find -le '
    find({ wanted => \&wanted, no_chdir => 1}, "$RPM_BUILD_ROOT");
    print "%defattr(-,root,root)";
    print "%doc  debian README";
    for my $x (sort @dirs, @files) {
        push @ret, $x unless indirs($x);
        }
    print join "\n", sort @ret;

    sub wanted {
        return if /auto$/;

        local $_ = $File::Find::name;
        my $f = $_; s|^$RPM_BUILD_ROOT||;
        return unless length;
        return $files[@files] = $_ if -f $f;

        $d = $_;
        /\Q$d\E/ && return for reverse sort @INC;
        $d =~ /\Q$_\E/ && return
for qw|%{_sysconfdir} %_prefix/man %_prefix/bin %_prefix/share|;

        $dirs[@dirs] = $_;
        }

    sub indirs {
        my $x = shift;
        $x =~ /^\Q$_\E\// && $x ne $_ && return 1 for @dirs;
        }
    ' > %filelist

[ -z %filelist ] && {
    echo "ERROR: empty %files listing"
    exit -1
    }

%files -f %filelist
%defattr(644,root,root,755)
