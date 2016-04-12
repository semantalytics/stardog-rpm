%define __spec_install_post %{nill}
%define   debug_package %{nill}

Name: Stardog
Version: 4.0.5
Release: 1%{?dist}
Summary:	

Group:	
License: Stardog
URL:		
Source0:	

BuildRequires:	
Requires:	

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

