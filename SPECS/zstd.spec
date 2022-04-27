# enable asm implementations by default
%bcond_without asm

# enable .lz4 support by default
%bcond_without lz4

# enable .xz/.lzma support by default
%bcond_without lzma

# enable .gz support by default
%bcond_without zlib

%if 0%{?rhel} && 0%{?rhel} <= 6
# gcc-4.4 is currently too old to compile pzstd
%bcond_with pzstd
%else
%ifarch %{ix86} x86_64
%bcond_without pzstd
%else
# aarch64 and armv7hl at least currently segfault
# in ThreadPool test for the pzstd util
%bcond_with pzstd
%endif
%endif

Name:           zstd
Version:        1.5.2
Release:        1%{?dist}
Summary:        Zstd compression library

License:        BSD and GPLv2
URL:            https://github.com/facebook/zstd
Source0:        https://github.com/facebook/zstd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


BuildRequires:  make
BuildRequires:  gcc gtest-devel
%if %{with lz4}
BuildRequires:  lz4-devel
%endif
%if %{with lzma}
BuildRequires:  xz-devel
%endif
%if %{with pzstd}
BuildRequires:  gcc-c++
%endif
%if %{with zlib}
BuildRequires:  zlib-devel
%endif
BuildRequires:  prelink

%description
Zstd, short for Zstandard, is a fast lossless compression algorithm,
targeting real-time compression scenarios at zlib-level compression ratio.

%package -n lib%{name}
Summary:        Zstd shared library

%description -n lib%{name}
Zstandard compression shared library.

%package -n lib%{name}-devel
Summary:        Header files for Zstd library
Requires:       lib%{name}%{?_isa} = %{version}-%{release}

%package -n lib%{name}-static
Summary:        Static variant of the Zstd library
Requires:       lib%{name}-devel = %{version}-%{release}

%description -n lib%{name}-devel
Header files for Zstd library.

%description -n lib%{name}-static
Static variant of the Zstd library.

%prep
%setup -q
find -name .gitignore -delete

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"
export PREFIX="%{_prefix}"
export LIBDIR="%{_libdir}"
%make_build -C lib lib-mt %{!?with_asm:ZSTD_NO_ASM=1}
%make_build -C programs %{!?with_asm:ZSTD_NO_ASM=1}
%if %{with pzstd}
export CXXFLAGS="$RPM_OPT_FLAGS"
%make_build -C contrib/pzstd %{!?with_asm:ZSTD_NO_ASM=1}
%endif

%check
execstack lib/libzstd.so.1

export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="$RPM_LD_FLAGS"

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
%if %{with pzstd}
install -D -m755 contrib/pzstd/pzstd %{buildroot}%{_bindir}/pzstd
install -D -m644 programs/%{name}.1 %{buildroot}%{_mandir}/man1/p%{name}.1
%endif

%files
%doc CHANGELOG README.md
%{_bindir}/%{name}
%if %{with pzstd}
%{_bindir}/p%{name}
%{_mandir}/man1/p%{name}.1*
%endif
%{_bindir}/%{name}mt
%{_bindir}/un%{name}
%{_bindir}/%{name}cat
%{_bindir}/%{name}grep
%{_bindir}/%{name}less
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/un%{name}.1*
%{_mandir}/man1/%{name}cat.1*
%{_mandir}/man1/%{name}grep.1*
%{_mandir}/man1/%{name}less.1*
%license COPYING LICENSE

%files -n lib%{name}
%{_libdir}/libzstd.so.*
%license COPYING LICENSE

%files -n lib%{name}-devel
%{_includedir}/zdict.h
%{_includedir}/zstd.h
%{_includedir}/zstd_errors.h
%{_libdir}/pkgconfig/libzstd.pc
%{_libdir}/libzstd.so

%files -n lib%{name}-static
%{_libdir}/libzstd.a
