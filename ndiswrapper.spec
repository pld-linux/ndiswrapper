#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%bcond_without	smp		# don't build SMP module
%bcond_without	up		# don't build UP module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	Tools to "wrap around" NDIS drivers
Summary(pl):	Narzêdzia "opakowuj±ce" sterowniki NDIS
Name:		ndiswrapper
Version:	1.29
#%define		bver	rc2
%define		_rel	0.1
Release:	%{_rel}
Epoch:		1
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ndiswrapper/%{name}-%{version}.tar.gz
# Source0-md5:	25264b9c71f68ddea24ab54b41ee7e60
URL:		http://ndiswrapper.sourceforge.net/
%if %{with kernel}
%ifarch %{ix86}
BuildRequires:	gcc >= 5:3.4
%endif
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.8}
BuildRequires:	rpmbuild(macros) >= 1.330
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

%description -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

G³ówny pakiet zawiera narzêdzia przestrzeni u¿ytkownika dla
ndiswrappera.

%package -n kernel%{_alt_kernel}-net-ndiswrapper
Summary:	Loadable Linux kernel module that "wraps around" NDIS drivers
Summary(pl):	Modu³ j±dra Linuksa "owijaj±cy" sterowniki NDIS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Requires:	%{name} = %{epoch}:%{version}-%{_rel}
Requires:	dev >= 2.7.7-10

%description -n kernel%{_alt_kernel}-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

This package contains Linux kernel module.

%description -n kernel%{_alt_kernel}-net-ndiswrapper -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel%{_alt_kernel}-smp-net-ndiswrapper
Summary:	Loadable Linux SMP kernel module that "wraps around" NDIS drivers
Summary(pl):	Modu³ j±dra Linuksa SMP "owijaj±cy" sterowniki NDIS
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Requires:	%{name} = %{epoch}:%{version}-%{_rel}
Requires:	dev >= 2.7.7-10

%description -n kernel%{_alt_kernel}-smp-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

This package contains Linux SMP kernel module.

%description -n kernel%{_alt_kernel}-smp-net-ndiswrapper -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q
%{__sed} -i -e 's#"loader.h"#"../driver/loader.h"#g' utils/loadndisdriver.c

%build
%if %{with userspace}
%{__make} -C utils \
%ifarch %{x8664}
	CONFIG_X86_64=y \
%endif
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -DUTILS_VERSION=\\\"\$(UTILS_VERSION)\\\""
%endif

%if %{with kernel}
cd driver
%{__make} win2lin_stubs.h gen_exports \
%ifarch %{x8664}
	CONFIG_X86_64=y \
%endif
	KBUILD="%{_kernelsrcdir}"

%build_kernel_modules -m ndiswrapper \
%ifarch %{x8664}
	CONFIG_X86_64=y \
%endif
	KBUILD="%{_kernelsrcdir}" \
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
%files -n kernel%{_alt_kernel}-net-ndiswrapper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/ndiswrapper.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-ndiswrapper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/ndiswrapper.ko*
%endif
%endif
