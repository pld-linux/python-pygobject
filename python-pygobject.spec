#
%define		module	pygobject
#
Summary:	Python bindings for GObject library
Summary(pl):	Wi±zania Pythona do biblioteki GObject
Name:		python-%{module}
Version:	2.12.3
Release:	1
License:	LGPL
Group:		Libraries/Python
Source0:	http://ftp.gnome.org/pub/gnome/sources/pygobject/2.12/%{module}-%{version}.tar.bz2
# Source0-md5:	009986021225b7ea6e0ba848707785af
Patch0:		%{name}-pc.patch
URL:		http://www.pygtk.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.7
BuildRequires:	glib2-devel >= 1:2.12.4
BuildRequires:	libtool
BuildRequires:	libxslt-progs >= 1.1.17
BuildRequires:	python-devel >= 1:2.3.5
%pyrequires_eq	python-modules
BuildRequires:	rpm-pythonprov
Requires:	glib2 >= 1:2.12.4
Conflicts:	python-pygtk < 1:1.0
Obsoletes:	python-pygtk-glarea
Obsoletes:	python-pygtk-gobject
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for GObject library.

%description -l pl
Wi±zania Pythona do biblioteki GObject.

%package devel
Summary:	Python bindings for GObject library
Summary(pl):	Wi±zania Pythona do biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.12.4
Requires:	python-devel >= 1:2.3.5

%description devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%description devel -l pl
Pakiet zawiera pliki wymagane do zbudowania funkcji do biblioteki
GObject, tak by mog³y te biblioteki kooperowaæ z wi±zaniami Pythona.

%package examples
Summary:	Example programs for GObject library
Summary(pl):	Programy przyk³adowe dla biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	python-pygtk

%description examples
This package contains example programs for GObject library.

%description examples -l pl
Ten pakiet zawiera przyk³adowe programy dla biblioteki GObject.

%package apidocs
Summary:	pygobject API documentation
Summary(pl):	Dokumentacja API pygobject
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
pygobject API documentation.

%description apidocs -l pl
Dokumentacja API pygobject.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTMLdir='%{_gtkdocdir}/%{module}'

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*/{*.la,*/*.la}
rm -f $RPM_BUILD_ROOT%{py_sitedir}/{*.py,*/*.py,*/*/*.py}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{py_sitedir}/gtk-2.0/gobject/*.so
%dir %{py_sitedir}/gtk-2.0
%dir %{py_sitedir}/gtk-2.0/gobject
%{py_sitedir}/gtk-2.0/gobject/*.py[co]
%{py_sitedir}/gtk-2.0/*.py[co]
%{py_sitedir}/*.py[co]
%{py_sitedir}/pygtk.pth
%dir %{_datadir}/%{module}
%dir %{_datadir}/%{module}/xsl

%files devel
%defattr(644,root,root,755)
%{_includedir}/pygtk-2.0
%{_pkgconfigdir}/*.pc
%{_datadir}/%{module}/xsl/*.py
%{_datadir}/%{module}/xsl/*.xsl

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{module}
