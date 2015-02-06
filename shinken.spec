%define major 0.5
%define minor 1

Name:       shinken
Version:    0.6
Release:    3
Summary:    TNagios(R) compatible monitoring tool
License:    AGPL
Group:      Networking/Other
URL:        http://shinken-monitoring.org
Source0:    http://shinken-monitoring.org/pub/shinken-%{version}.tar.gz
Source1:    shinken.init
BuildRequires:  python-setuptools
BuildArch:  noarch

%description
Shinken is a new, Nagios compatible monitoring tool, written in Python. The
main goal of Shinken is to allow users to have a fully flexible architecture
for their monitoring system that can easily scale to large environments. It’s
as simple as in all the marketing cloud computing slides, but here, it’s
real!

Shinken is backwards-compatible with the Nagios configuration standard and
plugins. It works on any operating system and architecture that supports
Python, which includes Windows and GNU/Linux.

%prep
%setup -q

perl -pi \
    -e 's|path=/usr/lib/nagios/plugins|path=%{_libdir}/nagios/plugins|' \
    setup_parameters.cfg

%build
python setup.py build

%install
python setup.py install --root=%{buildroot}

rm -f %{buildroot}%{_sysconfdir}/init.d/*
rm -f %{buildroot}%{_sysconfdir}/default/shinken

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/shinken

install -d -m 755 %{buildroot}%{_localstatedir}/log/shinken
install -d -m 755 %{buildroot}%{_localstatedir}/run/shinken

# move to an arch-neutral location
install -d -m 755 %{buildroot}%{_datadir}/shinken/plugins
mv %{buildroot}/usr/lib/shinken/plugins/check.sh \
    %{buildroot}%{_datadir}/shinken/plugins

%pre
%_pre_useradd shinken %{_localstatedir}/lib/shinken /bin/sh

%postun
%_postun_userdel shinken

%files
%doc README COPYING Changelog FROM_NAGIOS_TO_SHINKEN THANKS db doc
%config(noreplace) %{_sysconfdir}/shinken
%{_initrddir}/shinken
%{py_puresitedir}/shinken
%{py_puresitedir}/skonf
%{py_puresitedir}/Shinken-%{major}-py%{py_ver}.egg-info
%{_bindir}/shinken-arbiter
%{_bindir}/shinken-arbiter.py
%{_bindir}/shinken-broker
%{_bindir}/shinken-broker.py
%{_bindir}/shinken-poller
%{_bindir}/shinken-poller.py
%{_bindir}/shinken-discovery
%{_bindir}/shinken-reactionner
%{_bindir}/shinken-reactionner.py
%{_bindir}/shinken-receiver
%{_bindir}/shinken-receiver.py
%{_bindir}/shinken-scheduler
%{_bindir}/shinken-scheduler.py
%{_datadir}/shinken/plugins/check.sh
%attr(-,shinken,shinken) %{_localstatedir}/lib/shinken
%attr(-,shinken,shinken) %{_localstatedir}/log/shinken
%attr(-,shinken,shinken) %{_localstatedir}/run/shinken

