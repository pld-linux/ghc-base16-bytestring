#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	base16-bytestring
Summary:	Fast base16 (hex) encoding and decoding for ByteStrings
Summary(pl.UTF-8):	Szybkie kodowanie i dekodowanie base16 (szesnastkowe) dla typu ByteString
Name:		ghc-%{pkgname}
Version:	0.1.1.6
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/base16-bytestring
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	b6aac9d679d7dd84c3cd23cbc143eb29
URL:		http://hackage.haskell.org/package/base16-bytestring
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-ghc-prim
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-ghc-prim-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 4
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-ghc-prim
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Fast base16 (hex) encoding and decoding for ByteStrings.

%description -l pl.UTF-8
Szybkie kodowanie i dekodowanie base16 (szesnastkowe) dla typu
ByteString.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-ghc-prim-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build

runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README.markdown %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base16
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base16/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base16/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteString/Base16/*.p_hi
%endif
