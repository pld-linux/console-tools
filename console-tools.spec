Summary:	Linux console utilities
Summary(pl):	Narz�dzia do obs�ugi konsoli
Name:		console-tools
Version:	0.3.3
Release:	11
Epoch:		1
License:	GPL
Group:		Applications/Console
# ftp://ftp.sourceforge.net/pub/sourceforge/lct/ - but no 0.3.3 yet
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	dcb9a6fae481b20d77174bce06cbd00f
Source1:	console.init
Source2:	console.sysconfig
Source3:	console.sh
Patch0:		%{name}-man_compat.patch
Patch1:		%{name}-no_bash.patch
Patch2:		%{name}-acm.patch
Patch3:		%{name}-readacm.patch
Patch4:		%{name}-psfgettable.patch
Patch5:		%{name}-resizecons.patch
Patch6:		%{name}-amfix.patch
Patch7:		%{name}-et.patch
URL:		http://lct.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	jade
BuildRequires:	libtool
BuildRequires:	sgml-tools
Requires(post,preun):	/sbin/chkconfig
Requires:	console-data
Requires:	localedb-src
Provides:	kbd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	kbd

%description
console-tools are utilities for handling console fonts and keyboard
maps. It is derived from kbd-0.99.tar.gz, with many bug-fixes and
enhancements. The data files are now part of a new package
(console-data).

%description -l pl
Console-tools to narz�dzia zajmuj�ce si� fontami i mapami klawiatury
na konsoli. Pakiet wywodzi si� z kbd-0.99.tar.gz, poprawiaj�c wiele
b��d�w i wprowadzaj�c rozszerzenia. Pliki danych s� teraz cz�ci�
nowego pakietu (console-data).

%package devel
Summary:	Header files
Summary(pl):	Pliki nag��wkowe
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
Console-tools header files for console-tools

%description devel -l pl
Pliki nag��wkowe do console-tools.

%package static
Summary:	Static libraries
Summary(pl):	Biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
Console-tools static libraries.

%description static -l pl
Biblioteki statyczne console-tools.

%prep
%setup  -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p0

%build
mv po/et_EE.po po/et.po
mv po/et_EE.gmo po/et.gmo
rm -f missing
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-kbd-compat
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d,profile.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/console
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/console
install %{SOURCE3} $RPM_BUILD_ROOT/etc/profile.d

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add console

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del console
fi

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README NEWS BUGS doc/README.*
%doc doc/{dvorak,contrib}
%doc doc/*.txt

%attr(754,root,root) /etc/rc.d/init.d/console
%attr(755,root,root) /etc/profile.d/console.sh
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/console

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%{_mandir}/man[1458]/*

%files devel
%defattr(644,root,root,755)
%doc doc/file-formats/{TMPL,cp,cpi,psf,raw,xpsf-draft*}
%{_includedir}/lct
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a