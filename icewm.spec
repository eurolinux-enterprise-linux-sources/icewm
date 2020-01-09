%define withimlib 1

Name:		icewm
Version:	1.2.37
Release:	1.2
Obsoletes:	icewm-common <= 1.2.2
Summary:	Fast and small X11 window manager
Group:		User Interface/Desktops
License:	LGPL
URL:		http://www.icewm.org/
Packager:       Troy Dawson <dawson@fnal.gov>
Source:		http://ftp.sourceforge.net/icewm/%{name}-%{version}.tar.gz
Source1: 	icewm.desktop
Source2: 	icewm-toolbar
Source3: 	icewm-menu
Source4: 	icewm-icons.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gettext-devel
BuildRequires:	freetype-devel
BuildRequires:	libX11-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libICE-devel
BuildRequires:	libXinerama
BuildRequires:	libXinerama-devel
BuildRequires:	libXft-devel
BuildRequires:	libXp-devel
BuildRequires:	libXpm-devel
BuildRequires:  libSM-devel libXext-devel libXrandr-devel libungif-devel kdelibs libpng-devel xorg-x11-font-utils imlib-devel
%if %{withimlib}
BuildRequires:	imlib-devel
%else
BuildRequires:	libXpm-devel
%endif

%define pkgdata %{_datadir}/%{name}

%description
A lightweight window manager for the X Window System. Optimized for
"feel" and speed, not looks. Features multiple workspaces, opaque
move/resize, task bar, window list, clock, mailbox, CPU, Network, APM
status. 

%package l10n
Group:		%{group}
Summary:        Message translations for icewm
Requires:       icewm = %{version}

%description l10n
Message translations for icewm.


%prep
%setup

%build
  CXXFLAGS="$RPM_OPT_FLAGS" ./configure \
     --prefix=%{_prefix} \
%if %{withimlib}
     --with-imlib=/usr/bin \
%else
     --with-xpm=%{_prefix} \
%endif
     --exec-prefix=%{_exec_prefix} \
     --datadir=%{_datadir} \
     --sysconfdir=%{_sysconfdir} \
     --with-docdir=%{_docdir}
  make

%install
  mkdir -p $RPM_BUILD_ROOT/etc/icewm
  make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p %{buildroot}%{_datadir}/apps/switchdesk
cat > %{buildroot}%{_datadir}/apps/switchdesk/Xclients.%{name} << EOF
#!/bin/sh
exec %{_bindir}/%{name}
EOF
mkdir -p %{buildroot}/etc/X11/gdm/Sessions
cat > %{buildroot}/etc/X11/gdm/Sessions/Icewm << EOF
#!/bin/sh
exec /etc/X11/xdm/Xsession %{name}
EOF


# Install the desktop entry
install -m 644 -D %{SOURCE1} %{buildroot}%{_datadir}/xsessions/icewm.desktop

# Install the customizations
install -m 644 -D %{SOURCE2} %{buildroot}%{pkgdata}/toolbar
install -m 644 -D %{SOURCE3} %{buildroot}%{pkgdata}/menu
cd %{buildroot}%{pkgdata}
tar xfz %{SOURCE4}

#%clean
#  test -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING AUTHORS CHANGES BUGS doc/*.html doc/icewm.sgml
%doc icewm.lsm
%{_datadir}/xsessions/%{name}.desktop
%attr(755, root, root) %{_datadir}/apps/switchdesk/Xclients.%{name}
%attr(755, root, root) /etc/X11/gdm/Sessions/Icewm

%config %{pkgdata}/keys
%config %{pkgdata}/menu
%config %{pkgdata}/preferences
%config %{pkgdata}/toolbar
%config %{pkgdata}/winoptions

%dir /etc/icewm

%dir %{pkgdata}/icons
%dir %{pkgdata}/ledclock
%dir %{pkgdata}/mailbox
%dir %{pkgdata}/taskbar
%dir %{pkgdata}/themes

%{_bindir}/*
%{pkgdata}/icons/*
%{pkgdata}/ledclock/*
%{pkgdata}/mailbox/*
%{pkgdata}/taskbar/*
%{pkgdata}/themes/*

%files l10n
%dir %{_datadir}/locale
%{_datadir}/locale/*

%changelog
* Fri Jan 15 2010 Nick Soms <nsoms at linux-ink.ru> 1.2.37-1.2
- Added missed build requirements

* Mon Oct 12 2009 Troy Dawson <dawson@fnal.gov> 1.2.37-1.1
- Scaled background (added imlib build requirements which replaces libXpm-devel)
  Spec file patch provided by Oleg Sadov

* Mon Feb 09 2009 Troy Dawson <dawson@fnal.gov> 1.2.37-1
- Updated to 1.2.37
- Added ooffice icons
- Changed menu and toolbar entries to be ooffice instead of soffice

* Mon Jun 09 2008 Troy Dawson <dawson@fnal.gov> 1.2.35-1
- Updated to 1.2.35

* Wed Nov 14 2007 Troy Dawson <dawson@fnal.gov> 1.2.33-1
- Updated to 1.2.33

* Wed Mar 28 2007 Troy Dawson <dawson@fnal.gov> 1.2.30-3
- Added BuildRequires so that it would build in a moch enviroment

* Mon Jan 22 2007 Troy Dawson <dawson@fnal.gov> 1.2.30-2
- Changed the exec from icewm to icewm-session

* Mon Jan 22 2007 Troy Dawson <dawson@fnal.gov> 1.2.30-1
- Updated to 1.2.30

* Mon Mar 14 2005 Troy Dawson <dawson@fnal.gov> 1.2.20-2
- Modified toolbar, menu, and added icons

* Fri Mar 11 2005 Troy Dawson <dawson@fnal.gov> 1.2.20-1
- Updated to 1.2.20

* Mon Mar 28 2004 Troy Dawson <dawson@fnal.gov>
1.2.13-3 - made it so you can select it from gdm

* Sun Feb 02 2003 Christian W. Zuckschwerdt <zany@triq.net>
1.2.6 - Switched to rpm build in macros.

* Sun Dec 15 2002 Marko Macek <marko.macek@gmx.net>
1.2.3pre2 - Completely rewritten and simplified packaging.

