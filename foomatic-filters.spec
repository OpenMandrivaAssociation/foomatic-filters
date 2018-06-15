Summary:	Foomatic filters needed to run print queues with Foomatic PPDs
Name:		foomatic-filters
Version:	4.0.17
Release:	17
License:	GPLv2
Group:		System/Servers
Url:		http://www.openprinting.org
Source0:	http://www.openprinting.org/download/foomatic/%{name}-%{version}.tar.gz
BuildArch:	noarch

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
%configure
%make

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_mandir}/man1

%make \
	PREFIX=%{_prefix} \
	DESTDIR=%{buildroot} \
	install-main install-cups

# Remove superfluous file
rm -f %{buildroot}/etc/foomatic/filter.conf.sample

# We get foomatic-rip from cups-filters these days
rm -f	%{buildroot}%{_bindir}/foomatic-rip \
	%{buildroot}%{_prefix}/lib/cups/filter/foomatic-rip \
	%{buildroot}%{_prefix}/lib/cups/backend/beh \
	%{buildroot}%{_mandir}/man1/foomatic-rip.1*

%post
# Restart the CUPS daemon when it is running, but do not start it when it
# is not running. The restart of the CUPS daemon updates the CUPS-internal
# backend index
%systemd_postun_with_restart cups

%postun
# Restart the CUPS daemon when it is running, but do not start it when it
# is not running. The restart of the CUPS daemon updates the CUPS-internal
# backend index
%systemd_postun

%files
%doc README USAGE TODO ChangeLog
%dir %config(noreplace) %{_sysconfdir}/foomatic
%dir %config(noreplace) %{_sysconfdir}/foomatic/direct
%config(noreplace) %{_sysconfdir}/foomatic/filter.conf

