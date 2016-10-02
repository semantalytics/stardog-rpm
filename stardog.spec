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
Stardog is an enterprise data unification platform built on smart graph technology: query, search, inference, and data virtualization.

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

