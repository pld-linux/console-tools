Summary:     Linux console utilities
Summary(pl): Narzêdzia do obs³ugi konsoli
Name:	     console-tools
%define      date 1998.08.11 
Version:     1
Release:     2
Copyright:   GPL
Group:	     Utilities/Console
Group(pl):   Narzêdzia/Konsola
Vendor:	     Yann Dirson <dirson@debian.org>
Source:	     ftp://sunsite.unc.edu/pub/Linux/system/keyboards/console-tools-%{date}.tar.gz
Source1:     console-init.tar.gz
Patch:	     %{name}-ndebug.patch
Prereq:	     /sbin/chkconfig
Obsoletes:   kbd
Provides:    kbd
BuildRoot:   /tmp/%{name}-%{version}-root

%description
console-tools are utilities for handling console fonts and keyboard
maps. The package includes various fonts and keymaps.

It is derived from kbd-0.96a.tar.gz, with many bug-fixes and
enhancements.

%description -l pl
Console-tools to narzêdzia zajmuj±ce siê fontami i mapami klawiatury 
na konsoli. Do pakietu s± do³±czone ró¿ne fonty i mapy klawiatury.

Pakiet wywodzi siê z kbd-0.96a.tar.gz, poprawiaj±c wiele b³êdów
i wprowadzaj±c rozszerzenia.

%package devel
Summary:     Header files
Summary(pl): Pliki nag³ówkowe
Group:	     Utilities/Console
Requires:    %{name} = %{version}

%description devel
Console-tools header files for console-tools

%description devel -l pl
Pliki nag³ówkowe do console-tools.

%package static
Summary:     Static libraries
Summary(pl): Biblioteki statyczne
Group:	     Utilities/Console
Requires:    %{name}-devel = %{version}

%description static
Console-tools static libraries.

%description static -l pl
Biblioteki statyczne console-tools.

%prep
%setup -q -a1 -n %{name}-%{date}
%patch -p1

grep -v "Alt " data/keymaps/i386/qwerty/pl.kmap > \
data/keymaps/i386/qwerty/pl1.kmap

%build
CFLAGS=$RPM_OPT_FLAGS LDFLAGS=-s ./configure --enable-kbd-compat
make 

%install
rm -rf $RPM_BUILD_ROOT

make install prefix=$RPM_BUILD_ROOT/usr

cp -a etc $RPM_BUILD_ROOT

for i in loadunimap mapscrn saveunimap savefont; do
 rm -f $RPM_BUILD_ROOT/usr/man/man8/$i.8
 echo .so kbd-compat.8 > $RPM_BUILD_ROOT/usr/man/man8/$i.8
done

%post
/sbin/chkconfig --add console

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del console
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc README NEWS BUGS
%attr(700,root,root) %config /etc/rc.d/init.d/console
%config %verify(not size mtime md5) /etc/sysconfig/console
%attr(755,root,root) /etc/profile.d/console.sh
%attr(755, root, root) /usr/bin/*
%attr(755, root, root) /usr/lib/lib*.so.*
%attr(644, root,  man) /usr/man/man[1458]/*

/usr/share/consolefonts
/usr/share/consoletrans
/usr/share/keymaps
/usr/share/videomodes

%files devel
%defattr(644, root, root, 755)
%doc doc/*.html
/usr/include/lct

%attr(755, root, root) /usr/lib/*.so

%files static
%attr(644, root, root) /usr/lib/*.a

%changelog
* Thu Sep 24 1998 Marcin 'Qrczak' Kowalczyk <qrczak@knm.org.pl>
- Spec generally rewritten
- Qrczak's fonts removed from the package (they were not a part of
  console-tools and now are in a separate package called fonty)
- Added SysV-like init scripts
- Added pl1.kmap with diacritics under AltGr only (will be included
  in the next version of console-tools)
- Added --enable-kbd-compat (wrappers emulating kbd's syntax)
  and Provides: kbd

* Sat Jul 25 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- initial RPM release
