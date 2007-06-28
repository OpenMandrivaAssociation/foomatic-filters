%define name foomatic-filters
%define version 3.0.2
%define releasedate 20070627
%define release %mkrel 1.%{releasedate}.1

##### GENERAL DEFINITIONS

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:        Foomatic filters needed to run print queues with Foomatic PPDs
License:        GPL
Group:          System/Servers
Url:            http://www.linuxprinting.org/
Requires:       mpage
%ifarch x86_64
Conflicts:	cups < 1.2.0-0.5361.0mdk
%endif
Obsoletes:	foomatic
Provides:	foomatic
BuildArchitectures: noarch

##### BUILDREQUIRES

BuildRequires:	autoconf
BuildRequires:	perl-devel file libxml2-devel mpage
%ifarch x86_64
BuildRequires:	cups >= 1.2.0-0.5361.0mdk
%else
BuildRequires:	cups >= 1.2.0
%endif

##### SOURCES

# Foomatic packages
Source:	http://www.linuxprinting.org/download/foomatic/%{name}-3.0-%{releasedate}.tar.gz

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
 
The site http://www.linuxprinting.org/ is based on this database.

This package contains the filters needed to run print queues based on
Foomatic PPD files.



%prep
##### FOOMATIC

# Source trees for installation
%setup -q -n %{name}-3.0-%{releasedate}
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
%configure
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

