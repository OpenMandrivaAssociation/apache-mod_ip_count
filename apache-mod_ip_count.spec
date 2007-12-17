#Module-Specific definitions
%define mod_name mod_ip_count
%define mod_conf A34_%{mod_name}.conf
%define mod_so %{mod_name}.so

%define svn_rev r353

Summary:	Mod_ip_count is a DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	2.0
Release:	%mkrel 6
License:	Apache License
Group:		System/Servers
# http://feh.holsman.net
#URL:		http://svn.zilbo.com/svn/mod_ip_count/trunk/
URL:		http://www.zilbo.com/
Source0: 	%{mod_name}-%{version}-%{svn_rev}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
#BuildRequires:	apr_memcache-devel
Epoch:		1

%description
mod_ip_count is a DoS prevention apache module. It works by
restricting the number of requests that a given client can issue
to a server pool.

%prep

%setup -q -n %{mod_name}

%build

sh ./autogen.sh

%configure2_5x \
    --with-apxs=%{_sbindir}/apxs

#%{_sbindir}/apxs -I. -I%{_includedir}/apr_memcache-0 -lapr_memcache -c %{mod_name}.c 

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README LICENSE
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


