#Module-Specific definitions
%define mod_name mod_ip_count
%define mod_conf A34_%{mod_name}.conf
%define mod_so %{mod_name}.so

%define svn_rev r353

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	2.0
Release:	%mkrel 11
License:	Apache License
Group:		System/Servers
# http://feh.holsman.net
#URL:		http://svn.zilbo.com/svn/mod_ip_count/trunk/
URL:		http://www.zilbo.com/
Source0: 	%{mod_name}-%{version}-%{svn_rev}.tar.bz2
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
#BuildRequires:	apr_memcache-devel
BuildRequires:	apr-devel => 1:1.3.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_ip_count is a DoS prevention apache module. It works by restricting the
number of requests that a given client can issue to a server pool.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c %{mod_name}.c 

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LICENSE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
