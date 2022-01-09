# TODO:
# - topkg-care (BR: fmt, logs, bos >= 0.1.5, cmdliner >= 1.0.0, webbrowser, opam-format >= 2.0.0)
# - docs (BR ocaml-odoc)
#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	Topkg - the transitory OCaml software packager
Summary(pl.UTF-8):	Topkg - przejściowe narzędzie do pakowania oprogramowania w OCamlu
Name:		ocaml-topkg
Version:	1.0.3
Release:	1
License:	ISC
Group:		Libraries
Source0:	https://erratique.ch/software/topkg/releases/topkg-%{version}.tbz
# Source0-md5:	e285f7a296d77ee7d831ba9a6bfb396f
URL:		https://erratique.ch/software/topkg/
BuildRequires:	ocaml >= 1:4.03.0
BuildRequires:	ocaml-findlib >= 1.6.1
BuildRequires:	ocaml-ocamlbuild
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
Topkg is a packager for distributing OCaml software. It provides an
API to describe the files a package installs in a given build
configuration and to specify information about the package's
distribution, creation and publication procedures.

%description -l pl.UTF-8
Topkg to narzędzie do pakowania, przeznaczone do dystrybucji
oprogramowania w OCamlu. Udostępnia API do opisu plików instalowanych
przez pakiet w danych konfiguracjach budowania oraz przekazania
informacji o procedurze dystrybucji, tworzenia i publikacji pakietu.

%package devel
Summary:	Topkg - the transitory OCaml software packager - development part
Summary(pl.UTF-8):	Topkg - przejściowe narzędzie do pakowania oprogramowania w OCamlu - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
topkg library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki topkg.

%prep
%setup -q -n topkg-%{version}

%build
ocaml pkg/pkg.ml build \
	--pkg-name topkg

# CLI tool
%if %{with ocaml_opt}
ocamlbuild topkg.native
%else
ocamlbuild topkg.byte
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml/topkg}

cp -p _build/topkg.opam $RPM_BUILD_ROOT%{_libdir}/ocaml/topkg/opam
cp -p _build/pkg/META $RPM_BUILD_ROOT%{_libdir}/ocaml/topkg
cp -p _build/src/*.{cma,cmi,cmt,cmti,mli} $RPM_BUILD_ROOT%{_libdir}/ocaml/topkg
%if %{with ocaml_opt}
cp -p _build/src/*.{a,cmx,cmxa,cmxs} $RPM_BUILD_ROOT%{_libdir}/ocaml/topkg
%endif

%if %{with ocaml_opt}
install _build/src/topkg.native $RPM_BUILD_ROOT%{_bindir}/topkg
%else
install _build/src/topkg.byte $RPM_BUILD_ROOT%{_bindir}/topkg
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.md README.md
%attr(755,root,root) %{_bindir}/topkg
%dir %{_libdir}/ocaml/topkg
%{_libdir}/ocaml/topkg/META
%{_libdir}/ocaml/topkg/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/topkg/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/topkg/*.cmi
%{_libdir}/ocaml/topkg/*.cmt
%{_libdir}/ocaml/topkg/*.cmti
%{_libdir}/ocaml/topkg/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/topkg/*.a
%{_libdir}/ocaml/topkg/*.cmx
%{_libdir}/ocaml/topkg/*.cmxa
%endif
%{_libdir}/ocaml/topkg/opam
