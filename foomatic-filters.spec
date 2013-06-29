Summary:	Foomatic filters needed to run print queues with Foomatic PPDs
Name:		foomatic-filters
Version:	4.0.17
Release:	3
License:	GPLv2
Group:		System/Servers
Url:		http://www.openprinting.org
Source0:	http://www.openprinting.org/download/foomatic/%{name}-%{version}.tar.gz

BuildRequires:	cups
BuildRequires:	file
BuildRequires:	mpage
BuildRequires:	libgs-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libxml-2.0)
Requires:	mpage
Provides:	foomatic

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
%setup -q

%build
%configure2_5x
make

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_mandir}/man1

make \
	PREFIX=%{_prefix} \
	DESTDIR=%{buildroot} \
	install

# Remove superfluous file
rm -f %{buildroot}/etc/foomatic/filter.conf.sample

# Link to make Foomatic 2.0.x CUPS queues working with Foomatic 3.0.x
ln -s ../../../bin/foomatic-rip %{buildroot}%{_prefix}/lib/cups/filter/cupsomatic

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

%files
%doc README USAGE TODO ChangeLog
%{_bindir}/*
%{_prefix}/lib/cups/filter/*
%{_prefix}/lib/cups/backend/*
%{_prefix}/lib/ppr/interfaces/*
%{_prefix}/lib/ppr/lib/*
%{_mandir}/man1/*
%dir %config(noreplace) %{_sysconfdir}/foomatic
%dir %config(noreplace) %{_sysconfdir}/foomatic/direct
%config(noreplace) %{_sysconfdir}/foomatic/filter.conf

