#
%define		module	pygobject
#
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Name:		python-%{module}
Version:	2.20.0
Release:	5
License:	LGPL v2+
Group:		Libraries/Python
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.20/%{module}-%{version}.tar.bz2
# Source0-md5:	10e1fb79be3d698476a28b1e1b0c5640
Patch0:		%{name}-pc.patch
Patch1:		%{name}-pyc.patch
Patch2:		gobject-introspection.patch
URL:		http://www.pygtk.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.7
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gobject-introspection-devel >= 0.6.3
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	libtool
BuildRequires:	libxslt-progs >= 1.1.22
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.3.5
%pyrequires_eq	python-modules
BuildRequires:	rpm-pythonprov
Requires:	glib2 >= 1:2.16.0
Provides:	python-pygtk-gobject
Obsoletes:	python-pygtk-glarea
Obsoletes:	python-pygtk-gobject
Conflicts:	python-pygtk < 1:1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for GObject library.

%description -l pl.UTF-8
Wiązania Pythona do biblioteki GObject.

%package devel
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.16.0
Requires:	libffi-devel >= 3.0
Requires:	python-devel >= 1:2.3.5

%description devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%description devel -l pl.UTF-8
Pakiet zawiera pliki wymagane do zbudowania funkcji do biblioteki
GObject, tak by mogły te biblioteki kooperować z wiązaniami Pythona.

%package examples
Summary:	Example programs for GObject library
Summary(pl.UTF-8):	Programy przykładowe dla biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	python-pygtk

%description examples
This package contains example programs for GObject library.

%description examples -l pl.UTF-8
Ten pakiet zawiera przykładowe programy dla biblioteki GObject.

%package apidocs
Summary:	pygobject API documentation
Summary(pl.UTF-8):	Dokumentacja API pygobject
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
pygobject API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API pygobject.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

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
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	TARGET_DIR=%{_gtkdocdir}/%{module}

cp -a examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/*/{*.la,*/*.la}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{module}/2.0/codegen
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{module}/2.0/codegen
%py_postclean %{_datadir}/%{module}/2.0/codegen

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libpyglib-2.0-python.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpyglib-2.0-python.so.0
%dir %{py_sitedir}/gtk-2.0
%dir %{py_sitedir}/gtk-2.0/gio
%attr(755,root,root) %{py_sitedir}/gtk-2.0/gio/_gio.so
%attr(755,root,root) %{py_sitedir}/gtk-2.0/gio/unix.so
%{py_sitedir}/gtk-2.0/gio/*.py[co]
%dir %{py_sitedir}/gtk-2.0/girepository
%dir %{py_sitedir}/gtk-2.0/girepository/overrides
%{py_sitedir}/gtk-2.0/girepository/overrides/*.py[co]
%attr(755,root,root) %{py_sitedir}/gtk-2.0/girepository/repo.so
%{py_sitedir}/gtk-2.0/girepository/*.py[co]
%dir %{py_sitedir}/gtk-2.0/glib
%attr(755,root,root) %{py_sitedir}/gtk-2.0/glib/_glib.so
%{py_sitedir}/gtk-2.0/glib/*.py[co]
%dir %{py_sitedir}/gtk-2.0/gobject
%attr(755,root,root) %{py_sitedir}/gtk-2.0/gobject/_gobject.so
%{py_sitedir}/gtk-2.0/gobject/*.py[co]
%{py_sitedir}/gtk-2.0/*.py[co]
%{py_sitedir}/*.py[co]
%{py_sitedir}/pygtk.pth
%dir %{_datadir}/%{module}
%dir %{_datadir}/%{module}/xsl

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pygobject-codegen-2.0
%attr(755,root,root) %{_libdir}/libpyglib-2.0-python.so
%{_libdir}/libpyglib-2.0-python.la
%{_includedir}/pygobject
%{_includedir}/pygtk-2.0
%{_pkgconfigdir}/*.pc
%dir %{_datadir}/%{module}/2.0
%dir %{_datadir}/%{module}/2.0/codegen
%{_datadir}/%{module}/2.0/codegen/*.py[co]
%dir %{_datadir}/%{module}/2.0/defs
%{_datadir}/%{module}/2.0/defs/*.defs
%{_datadir}/%{module}/2.0/defs/*.override
%{_datadir}/%{module}/xsl/*.py
%{_datadir}/%{module}/xsl/*.xsl

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{module}
