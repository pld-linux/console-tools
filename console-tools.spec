Summary:	Linux console utilities
Summary(pl):	Narzêdzia do obs³ugi konsoli
Name:		console-tools
Version:	0.3.3
Release:	6
Serial:		1
License:	GPL
Group:		Utilities/Console
Group(pl):	Narzêdzia/Konsola
Source0:	http://altern.org/ydirson/soft/lct/dev/%{name}-%{version}.tar.gz
Source1:	console.init
Source2:	console.sysconfig
Source3:	console.sh
Patch0:		console-tools-man_compat.patch
Patch1:		console-tools-no_bash.patch
URL:		http://altern.org/ydirson/en/lct/
Prereq:		/sbin/chkconfig
BuildRequires:	sgml-tools
BuildRequires:	jade
BuildRequires:	gettext-devel
Requires:	console-data
Requires:	localedb-src
Obsoletes:	kbd
Provides:	kbd
BuildRoot:	/tmp/%{name}-%{version}-root

%description
console-tools are utilities for handling console fonts and keyboard maps.
It is derived from kbd-0.99.tar.gz, with many bug-fixes and enhancements.
The data files are now part of a new package (console-data).

%description -l pl
Console-tools to narzêdzia zajmuj±ce siê fontami i mapami klawiatury na
konsoli. Pakiet wywodzi siê z kbd-0.99.tar.gz, poprawiaj±c wiele b³êdów i
wprowadzaj±c rozszerzenia.  Pliki danych s± teraz czê¶ci± nowego pakietu
(console-data).

%package devel
Summary:	Header files
Summary(pl):	Pliki nag³ówkowe
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Console-tools header files for console-tools

%description devel -l pl
Pliki nag³ówkowe do console-tools.

%package static
Summary:	Static libraries
Summary(pl):	Biblioteki statyczne
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Console-tools static libraries.

%description static -l pl
Biblioteki statyczne console-tools.

%prep
%setup  -q 
%patch0 -p0
%patch1 -p1

%build
gettextize --copy --force
LDFLAGS="-s"; export LDFLAGS
%configure \
	--enable-kbd-compat
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d,profile.d}

make install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/console
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/console
install %{SOURCE3} $RPM_BUILD_ROOT/etc/profile.d

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*so.*.*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	README NEWS BUGS doc/README.* doc/*.txt \
	doc/{dvorak,file-formats,contrib}/*

%find_lang %{name}

%post
/sbin/chkconfig --add console
/sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del console
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc {README,NEWS,BUGS}.gz doc/README.*
%doc doc/{dvorak,contrib}
%doc doc/*.txt.gz

%attr(754,root,root) /etc/rc.d/init.d/console
%attr(755,root,root) /etc/profile.d/console.sh
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/console

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%{_mandir}/man[1458]/*

%files devel
%defattr(644,root,root,755)
%doc doc/file-formats/{TMPL,cp,cpi,psf,raw,xpsf-draft*}.gz
%{_includedir}/lct
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_libdir}/*.la

%files static
%attr(644,root,root) %{_libdir}/lib*.a
