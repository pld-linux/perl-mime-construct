#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
Summary:	mime-construct - construct and optionally mail MIME messages
Summary(pl):	mime-construct - tworzenie i opcjonalnie wysy³anie wiadomo¶ci MIME
Name:		perl-mime-construct
Version:	1.9
Release:	1
Vendor:		Roderick Schertler <roderick@argon.org>
License:	GPL v2+
Group:		Applications/Mail
Source0:	http://search.cpan.org/CPAN/authors/id/R/RO/ROSCH/mime-construct-%{version}.tar.gz
# Source0-md5:	727a5b622fae6e2800caffae9b034f24
URL:		http://search.cpan.org/dist/mime-construct/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
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

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README debian/changelog
%attr(755,root,root) %{_bindir}/mime-construct
%{_mandir}/man1/mime-construct.1*
