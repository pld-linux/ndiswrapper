# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%bcond_without	smp		# don't build SMP module
%bcond_without	up		# don't build UP module
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		pname	ndiswrapper
Summary:	Tools to "wrap around" NDIS drivers
Summary(pl.UTF-8):	Narzędzia "opakowujące" sterowniki NDIS
Name:		%{pname}%{_alt_kernel}
Version:	1.15
Release:	64
Epoch:		1
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ndiswrapper/%{pname}-%{version}.tar.gz
# Source0-md5:	0ca5bcab8e9b7b0d40f2e886f1fbaa45
Patch0:		%{name}-2.6.20.patch
URL:		http://ndiswrapper.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 2.6.8}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

The main package contains the userspace tools for ndiswrapper kernel
module.

%description -l pl.UTF-8
Niektórzy producenci bezprzewodowych kart sieciowych nie udostępniają
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
niż Microsoft Windows. Projekt ndiswrapper umożliwia użycie takiego
sprzętu w systemie Linux, dostarczając moduł jądra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

Główny pakiet zawiera narzędzia przestrzeni użytkownika dla
ndiswrappera.

%package -n kernel%{_alt_kernel}-net-ndiswrapper
Summary:	Loadable Linux kernel module that "wraps around" NDIS drivers
Summary(pl.UTF-8):	Moduł jądra Linuksa "owijający" sterowniki NDIS
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}(vermagic) = %{_kernel_ver}}
# loose dep intentional
Requires:	%{pname} = %{epoch}:%{version}
Requires:	dev >= 2.7.7-10

%description -n kernel%{_alt_kernel}-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

This package contains Linux kernel module.

%description -n kernel%{_alt_kernel}-net-ndiswrapper -l pl.UTF-8
Niektórzy producenci bezprzewodowych kart sieciowych nie udostępniają
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
niż Microsoft Windows. Projekt ndiswrapper umożliwia użycie takiego
sprzętu w systemie Linux, dostarczając moduł jądra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

Ten pakiet zawiera moduł jądra Linuksa.

%package -n kernel%{_alt_kernel}-smp-net-ndiswrapper
Summary:	Loadable Linux SMP kernel module that "wraps around" NDIS drivers
Summary(pl.UTF-8):	Moduł jądra Linuksa SMP "owijający" sterowniki NDIS
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}-smp(vermagic) = %{_kernel_ver}}
# loose dep intentional
Requires:	%{pname} = %{epoch}:%{version}
Requires:	dev >= 2.7.7-10

%description -n kernel%{_alt_kernel}-smp-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

This package contains Linux SMP kernel module.

%description -n kernel%{_alt_kernel}-smp-net-ndiswrapper -l pl.UTF-8
Niektórzy producenci bezprzewodowych kart sieciowych nie udostępniają
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
niż Microsoft Windows. Projekt ndiswrapper umożliwia użycie takiego
sprzętu w systemie Linux, dostarczając moduł jądra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

Ten pakiet zawiera moduł jądra Linuksa SMP.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%{__sed} -i -e 's,CFLAGS = -g,CFLAGS = $(OPTFLAGS),' utils/Makefile

%build
%if %{with userspace}
%{__make} -C utils \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"
%endif

%if %{with kernel}
cd driver

%{__make} gen_exports \
%ifarch %{x8664}
	x86_64_stubs \
	CONFIG_X86_64=y \
%endif
	KBUILD="%{_kernelsrcdir}"

%build_kernel_modules -m ndiswrapper \
	KBUILD="%{_kernelsrcdir}" \
%ifarch %{x8664}
	CONFIG_X86_64=y \
%endif
	KVERS="%{_kernel_ver}"

%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT{/sbin,%{_sysconfdir}/ndiswrapper,%{_sbindir}}
install utils/loadndisdriver \
	$RPM_BUILD_ROOT/sbin
install utils/{ndiswrapper,ndiswrapper-buginfo} \
	$RPM_BUILD_ROOT%{_sbindir}
%endif

%if %{with kernel}
%install_kernel_modules -m driver/ndiswrapper -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-ndiswrapper
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-ndiswrapper
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-ndiswrapper
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-net-ndiswrapper
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README
%dir %{_sysconfdir}/ndiswrapper
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_sbindir}/*
%endif

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-net-ndiswrapper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/ndiswrapper.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-ndiswrapper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/ndiswrapper.ko*
%endif
%endif
