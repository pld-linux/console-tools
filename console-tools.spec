Summary:	Linux console utilities
Summary(pl):	Narzêdzia do obs³ugi konsoli
Name:		console-tools
Version:	0.2.0
Release:	2
Copyright:	GPL
Group:		Utilities/Console
Group(pl):	Narzêdzia/Konsola
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/keyboards/%{name}-%{version}.tar.gz
Source1:	console-init.tar.gz
Prereq:		/sbin/chkconfig
BuildPrereq:	sgml-tools
BuildPrereq:	jade
Obsoletes:	kbd
Provides:	kbd
BuildRoot:	/tmp/%{name}-%{version}-root

%description
console-tools are utilities for handling console fonts and keyboard
maps. 
It is derived from kbd-0.94.tar.gz, with many bug-fixes and
enhancements. 
The data files are now part of a new package (console-data).

%description -l pl
Console-tools to narzêdzia zajmuj±ce siê fontami i mapami klawiatury 
na konsoli. 
Pakiet wywodzi siê z kbd-0.94.tar.gz, poprawiaj±c wiele b³êdów
i wprowadzaj±c rozszerzenia. 
Pliki danych s± teraz czê¶ci± nowego pakietu (console-data).

%package devel
Summary:	Header files
Summary(pl):	Pliki nag³ówkowe
Group:		Development
Group(pl):	Programowanie
Requires:	%{name} = %{version}

%description devel
Console-tools header files for console-tools

%description devel -l pl
Pliki nag³ówkowe do console-tools.

%package static
Summary:	Static libraries
Summary(pl):	Biblioteki statyczne
Group:		Libraries
Group(pl):	Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Console-tools static libraries.

%description static -l pl
Biblioteki statyczne console-tools.

%prep
%setup -q -a1 

%build
%configure \
	--enable-kbd-compat
make 

%install
rm -rf $RPM_BUILD_ROOT

make install-strip prefix=$RPM_BUILD_ROOT/usr \
	bindir=$RPM_BUILD_ROOT/%{_bindir} \
	mandir=$RPM_BUILD_ROOT/%{_mandir} \
	libdir=$RPM_BUILD_ROOT/%{_libdir} \
	includedir=$RPM_BUILD_ROOT/%{_includedir}

cp -a etc $RPM_BUILD_ROOT

for i in loadunimap mapscrn saveunimap savefont setfont; do
	rm -f $RPM_BUILD_ROOT%{_mandir}/man8/$i.8
	echo .so kbd-compat.8 > $RPM_BUILD_ROOT%{_mandir}/man8/$i.8
done

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*so.*.*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	README NEWS BUGS doc/README.* doc/*.txt \
	doc/{dvorak,file-formats,contrib}/*

%find_lang %{name}

%post
/sbin/chkconfig --add console

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del console
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc {README,NEWS,BUGS}.gz doc/README.*
%doc doc/{dvorak,file-formats,contrib}

%attr(754,root,root) %config /etc/rc.d/init.d/console
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/console

%attr(755,root,root) /etc/profile.d/console.sh
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%{_mandir}/man[1458]/*

%files devel
%defattr(644,root,root,755)
%doc doc/*.html doc/*.txt.gz

%{_includedir}/lct
%attr(755,root,root) %{_libdir}/*.so

%files static
%defattr(644,root,root)
%{_libdir}/lib*.a
