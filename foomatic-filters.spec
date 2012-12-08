%define name foomatic-filters
%define version 4.0.17
%define releasedate 0
%if %{releasedate}
%define release %mkrel 0.%{releasedate}.1
%define tarname %{name}-%{version}-%{releasedate}
%else
%define release %mkrel 1
%define tarname %{name}-%{version}
%endif

##### GENERAL DEFINITIONS

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:        Foomatic filters needed to run print queues with Foomatic PPDs
License:        GPLv2
Group:          System/Servers
Url:            http://www.linuxprinting.org/
Requires:       mpage
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif
Obsoletes:	foomatic
Provides:	foomatic

##### BUILDREQUIRES

BuildRequires:	autoconf
BuildRequires:	perl-devel file libxml2-devel mpage
BuildRequires:	libgs-devel
BuildRequires:	dbus-devel
%ifarch x86_64
BuildRequires:	cups >= 1.2.0-0.5361.0mdk
%else
BuildRequires:	cups >= 1.2.0
%endif

##### SOURCES

# Foomatic packages
Source0:	http://www.openprinting.org/download/foomatic/%{name}-%{version}.tar.gz

##### BUILD ROOT

BuildRoot:	%_tmppath/%name-%version-%release-root

##### PACKAGE DESCRIPTION

%description
Foomatic is a comprehensive, spooler-independent database of printers,
printer drivers, and driver descriptions. It contains utilities to
generate PPD (Postscript Printer Description) files and printer queues
for CUPS, LPD, GNUlpr, LPRng, PPR, and PDQ using the database. There
is also the possibility to read the PJL options out of PJL-capable
laser printers and take them into account at the driver description
file generation.

There are spooler-independent command line interfaces to manipulate
queues (foomatic-configure) and to print files/manipulate jobs
(foomatic printjob).
 
This package contains the filters needed to run print queues based on
Foomatic PPD files.



%prep
##### FOOMATIC

# Source trees for installation
%setup -q -n %{tarname}
%if 0
# Modifications to make package building on 64-bit-systems
perl -p -i -e 's:\blib\b:\$LIB:g' configure.ac
perl -p -i -e 's!(AC_PROG_MAKE_SET)!$1

AC_PROG_CC

host_os=`uname -s`
host_cpu=`uname -m`

case \$host_os in
*Linux*)
  # Test if the compiler is 64bit
  echo "int i;" > conftest.\$ac_ext
  foomatic_cv_cc_64bit_output=no
  if AC_TRY_EVAL(ac_compile); then
    case `/usr/bin/file conftest.\$ac_objext` in
    *"ELF 64"*)
      foomatic_cv_cc_64bit_output=yes
      ;;
    esac
  fi
  rm -rf conftest*
  ;;
esac

case \$host_cpu:\$foomatic_cv_cc_64bit_output in
ppc64:yes | s390x:yes | sparc64:yes | x86_64:yes)
  LIB="lib64"
  ;;
*:*)
  LIB="lib"
  ;;
esac!' configure.ac
%endif

%build

# Makefile generation ("./make_configure" for CVS snapshots)
./make_configure
%configure2_5x
# Do not use "make" macro, as parallelized build of Foomatic does not
# work.
make

%install

rm -rf %{buildroot}

# Make directories
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_mandir}/man1

# Install program files
make	PREFIX=%{_prefix} \
        DESTDIR=%buildroot \
        install

# Remove superfluous file
rm -f %buildroot/etc/foomatic/filter.conf.sample

# Link to make Foomatic 2.0.x CUPS queues working with Foomatic 3.0.x
ln -s ../../../bin/foomatic-rip %buildroot%{_prefix}/lib/cups/filter/cupsomatic

##### GENERAL STUFF

%post
# Restart the CUPS daemon when it is running, but do not start it when it
# is not running. The restart of the CUPS daemon updates the CUPS-internal
# backend index
/sbin/service cups condrestart > /dev/null 2>/dev/null || :

%postun
# Restart the CUPS daemon when it is running, but do not start it when it
# is not running. The restart of the CUPS daemon updates the CUPS-internal
# backend index
/sbin/service cups condrestart > /dev/null 2>/dev/null || :

##### CLEAN UP

%clean
rm -rf %{buildroot}

##### FILES

%files
%defattr(-,root,root)
%doc README USAGE TODO ChangeLog
%_bindir/*
%_prefix/lib/cups/filter/*
%_prefix/lib/cups/backend/*
%_prefix/lib/ppr/interfaces/*
%_prefix/lib/ppr/lib/*
%{_mandir}/man1/*
%dir %config(noreplace) %{_sysconfdir}/foomatic
%dir %config(noreplace) %{_sysconfdir}/foomatic/direct
%config(noreplace) %{_sysconfdir}/foomatic/filter.conf



%changelog
* Thu Jul 19 2012 Alexander Khrukin <akhrukin@mandriva.org> 4.0.17-1mdv2012.0
+ Revision: 810172
- version update 4.0.17

* Wed Jun 27 2012 Alexander Khrukin <akhrukin@mandriva.org> 4.0.16-1
+ Revision: 807192
- version update 4.0.16

* Tue Mar 27 2012 Alexander Khrukin <akhrukin@mandriva.org> 4.0.15-1
+ Revision: 787132
- version update 4.0.15

* Thu Mar 08 2012 Alexander Khrukin <akhrukin@mandriva.org> 4.0.12-1
+ Revision: 783418
- version update 4.0.12

* Sun Aug 14 2011 Oden Eriksson <oeriksson@mandriva.com> 4.0.9-1
+ Revision: 694525
- 4.0.9 (fixes CVE-2011-2964)

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 4.0.7-1
+ Revision: 664405
- 4.0.7
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 4.0.5-1mdv2011.0
+ Revision: 605916
- 4.0.5
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 4.0.3-2mdv2010.1
+ Revision: 519000
- rebuild

* Wed Oct 14 2009 Oden Eriksson <oeriksson@mandriva.com> 4.0.3-1mdv2010.0
+ Revision: 457368
- 4.0.3

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 4.0.1-1mdv2010.0
+ Revision: 424475
- rebuild

* Mon Apr 20 2009 Gustavo De Nardin <gustavodn@mandriva.com> 4.0.1-1mdv2009.1
+ Revision: 368244
- new official version 4.0.1, only a few fixes more than previous 4.0-20090408

* Thu Apr 09 2009 Gustavo De Nardin <gustavodn@mandriva.com> 4.0-0.20090408.1mdv2009.1
+ Revision: 365300
- new "snapshot" 20090408, with fixes for custom page size handling

* Mon Mar 16 2009 Frederik Himpe <fhimpe@mandriva.org> 4.0-0.20090316.1mdv2009.1
+ Revision: 355837
- Update to 20090316 snapshot of 4.0 branch (important bug fixes)

* Sun Feb 08 2009 Frederik Himpe <fhimpe@mandriva.org> 4.0-0.20090208.1mdv2009.1
+ Revision: 338502
- Update to version 4.0 20090208 snapshot
- BuildRequires libgs-devel
- Package is not noarch anymore

* Sat Jan 03 2009 Frederik Himpe <fhimpe@mandriva.org> 3.0.2-2.20090103.1mdv2009.1
+ Revision: 323844
- Update to new version 20090103

* Mon Dec 29 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.2-2.20080810.2mdv2009.1
+ Revision: 321107
- rebuild

* Sun Aug 10 2008 Frederik Himpe <fhimpe@mandriva.org> 3.0.2-2.20080810.1mdv2009.0
+ Revision: 270353
- Update to new version 20080810

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 3.0.2-2.20080518.1mdv2009.0
+ Revision: 264480
- rebuild early 2009.0 package (before pixel changes)

* Sun May 18 2008 Frederik Himpe <fhimpe@mandriva.org> 3.0.2-1.20080518.1mdv2009.0
+ Revision: 208619
- New version
- Adapt to new license policy

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - fix description

* Thu Dec 20 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 3.0.2-1.20071218.1mdv2008.1
+ Revision: 135812
- New upstream: 20071218

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 3.0.2-1.20070820.1mdv2008.1
+ Revision: 125180
- kill re-definition of %%buildroot on Pixel's request

* Thu Aug 30 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 3.0.2-1.20070820.1mdv2008.0
+ Revision: 75929
- New upstream: 20070820.

* Thu Jun 28 2007 Adam Williamson <awilliamson@mandriva.org> 3.0.2-1.20070627.1mdv2008.0
+ Revision: 45340
- new snapshot 20070627, clean spec, rebuild for 2008
- Import foomatic-filters

