%define __spec_install_post %{nill}
%define   debug_package %{nill}

Name: Stardog
Version: @build.ver@
Release: 1%{?dist}
Summary: Stardog database

Group: Applications/Databases
License: Stardog
URL: http://www.stardog.com
Source0: ${name}-${version}.zip
BuildArch: noarch

BuildRequires:	
Requires:	java >= @java.version@

%description


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
%make_install


%files
%doc



%changelog

