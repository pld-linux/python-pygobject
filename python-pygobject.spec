#
%bcond_without	python2
%bcond_without	python3
#
%define		module	pygobject
#
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Name:		python-%{module}
Version:	2.28.1
Release:	1
License:	LGPL v2+
Group:		Libraries/Python
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/%{module}-%{version}.tar.bz2
# Source0-md5:	0afd773a7d62e9e1c146f99929599985
Patch0:		%{name}-pc.patch
Patch1:		%{name}-pyc.patch
Patch2:		gio.patch
URL:		http://www.pygtk.org/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.7
BuildRequires:	glib2-devel >= 1:2.22.4
BuildRequires:	gobject-introspection-devel >= 0.10.2
BuildRequires:	libffi-devel >= 3.0
BuildRequires:	libtool
BuildRequires:	libxslt-progs >= 1.1.22
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-devel >= 1:2.5.2
BuildRequires:	python-pycairo-devel >= 1.0.2
%pyrequires_eq	python-modules
%endif
%if %{with python3}
BuildRequires:	python3
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-pycairo-devel >= 1.8.10
%endif
Requires:	glib2 >= 1:2.22.4
Requires:	gobject-introspection >= 0.9.5
Provides:	python-pygtk-gobject
Obsoletes:	python-pygtk-glarea
Obsoletes:	python-pygtk-gobject
Conflicts:	python-pygtk < 1:1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# python provides Py* and _Py* symbols at runtime
%define		skip_post_check_so	libpyglib-2.0-python3?.so.*

%description
Python bindings for GObject library.

%description -l pl.UTF-8
Wiązania Pythona do biblioteki GObject.

%package devel
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.22.4
Requires:	libffi-devel >= 3.0
Requires:	python-devel >= 1:2.5.2

%description devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%description devel -l pl.UTF-8
Pakiet zawiera pliki wymagane do zbudowania funkcji do biblioteki
GObject, tak by mogły te biblioteki kooperować z wiązaniami Pythona.

%package -n python3-pygobject
Summary:	Python 3.x bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona 3.x do biblioteki GObject
Group:		Libraries/Python

%description -n python3-pygobject
Python 3.x bindings for GObject library.

%description -n python3-pygobject -l pl.UTF-8
Wiązania Pythona 3.x do biblioteki GObject.

%package -n python3-pygobject-devel
Summary:	Python bindings for GObject library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki GObject
Group:		Development/Languages/Python
Requires:	glib2-devel >= 1:2.22.4
Requires:	libffi-devel >= 3.0
Requires:	python3-devel
Requires:	python3-pygobject = %{version}-%{release}

%description -n python3-pygobject-devel
This package contains files required to build wrappers for GObject
addon libraries so that they interoperate with Python bindings.

%description -n python3-pygobject-devel -l pl.UTF-8
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
%if %{with python3}
mkdir py3
cd py3
../%configure \
	PYTHON=/usr/bin/python3 \
	--disable-silent-rules
%{__make}
cd ..
%endif
%if %{with python2}
mkdir py2
cd py2
../%configure \
	PYTHON=%{__python} \
	--disable-silent-rules
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with python3}
cd py3
%{__make} -j 1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	TARGET_DIR=%{_gtkdocdir}/%{module}
cd ..
%endif
%if %{with python2}
cd py2
%{__make} -j 1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	TARGET_DIR=%{_gtkdocdir}/%{module}
cd ..
%endif

cp -a examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/{gtk-2.0/,}*/*.la \
	$RPM_BUILD_ROOT%{py3_sitedir}/*/*.la \
	$RPM_BUILD_ROOT%{_libdir}/*.la

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{_datadir}/%{module}/2.0/codegen
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{module}/2.0/codegen
%py_postclean %{_datadir}/%{module}/2.0/codegen
%endif
%if %{with python3}
%py3_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%if %{with python2}
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
%dir %{py_sitedir}/gi
%dir %{py_sitedir}/gi/overrides
%{py_sitedir}/gi/overrides/*.py[co]
%dir %{py_sitedir}/gi/repository
%{py_sitedir}/gi/repository/*.py[co]
%{py_sitedir}/gi/*.py[co]
%attr(755,root,root) %{py_sitedir}/gi/_gi.so
%attr(755,root,root) %{py_sitedir}/gi/_gi_cairo.so
%dir %{py_sitedir}/glib
%attr(755,root,root) %{py_sitedir}/glib/_glib.so
%{py_sitedir}/glib/*.py[co]
%dir %{py_sitedir}/gobject
%attr(755,root,root) %{py_sitedir}/gobject/_gobject.so
%{py_sitedir}/gobject/*.py[co]
%{py_sitedir}/gtk-2.0/*.py[co]
%{py_sitedir}/pygtk.py[co]
%{py_sitedir}/pygtk.pth
%dir %{_datadir}/%{module}
%dir %{_datadir}/%{module}/xsl

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pygobject-codegen-2.0
%attr(755,root,root) %{_libdir}/libpyglib-2.0-python.so
%{_includedir}/pygtk-2.0
%{_pkgconfigdir}/pygobject-2.0.pc
%dir %{_datadir}/%{module}/2.0
%dir %{_datadir}/%{module}/2.0/codegen
%{_datadir}/%{module}/2.0/codegen/*.py[co]
%dir %{_datadir}/%{module}/2.0/defs
%{_datadir}/%{module}/2.0/defs/*.defs
%{_datadir}/%{module}/2.0/defs/*.override
%{_datadir}/%{module}/xsl/*.py
%{_datadir}/%{module}/xsl/*.xsl
%endif

%if %{with python3}
%files -n python3-pygobject
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libpyglib-2.0-python3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpyglib-2.0-python3.so.0
%dir %{py3_sitedir}/gtk-2.0
%dir %{py3_sitedir}/gtk-2.0/gio
%{py3_sitedir}/gtk-2.0/gio/*.py[co]
%dir %{py3_sitedir}/gi
%dir %{py3_sitedir}/gi/overrides
%{py3_sitedir}/gi/overrides/*.py[co]
%dir %{py3_sitedir}/gi/repository
%{py3_sitedir}/gi/repository/*.py[co]
%{py3_sitedir}/gi/*.py[co]
%attr(755,root,root) %{py3_sitedir}/gi/_gi.so
%attr(755,root,root) %{py3_sitedir}/gi/_gi_cairo.so
%dir %{py3_sitedir}/glib
%attr(755,root,root) %{py3_sitedir}/glib/_glib.so
%{py3_sitedir}/glib/*.py[co]
%dir %{py3_sitedir}/gobject
%attr(755,root,root) %{py3_sitedir}/gobject/_gobject.so
%{py3_sitedir}/gobject/*.py[co]
%{py3_sitedir}/gtk-2.0/*.py[co]
%{py3_sitedir}/pygtk.py[co]
%{py3_sitedir}/pygtk.pth

%files -n python3-pygobject-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpyglib-2.0-python3.so
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{module}
