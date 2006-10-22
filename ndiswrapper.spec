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
Version:	1.27
#%define		bver	rc2
%define		_rel	0.1
Release:	%{_rel}
Epoch:		1
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ndiswrapper/%{name}-%{version}.tar.gz
# Source0-md5:	f93aa94ec9733837fd75432bd7e4c72b
URL:		http://ndiswrapper.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.8}
BuildRequires:	rpmbuild(macros) >= 1.217
%endif
BuildRequires:	gcc >= 5:3.4.0
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

%package -n kernel-net-ndiswrapper
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

%description -n kernel-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

This package contains Linux kernel module.

%description -n kernel-net-ndiswrapper -l pl
Niektórzy producenci bezprzewodowych kart sieciowych nie udostêpniaj±
specyfikacji lub sterowników dla swoich produktów, dla systemów innych
ni¿ Microsoft Windows. Projekt ndiswrapper umo¿liwia u¿ycie takiego
sprzêtu w systemie Linux, dostarczaj±c modu³ j±dra który "owija"
sterowniki NDIS (API sterowników sieciowych w Windows).

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-net-ndiswrapper
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

%description -n kernel-smp-net-ndiswrapper
Some wireless LAN vendors refuse to release hardware specifications or
drivers for their products for operating systems other than Microsoft
Windows. The ndiswrapper project makes it possible to use such
hardware with Linux by means of a loadable kernel module that "wraps
around" NDIS (Windows network driver API) drivers.

This package contains Linux SMP kernel module.

%description -n kernel-smp-net-ndiswrapper -l pl
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
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts \
		KVERS="%{_kernel_ver}" \

	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o \
		KVERS="%{_kernel_ver}" \
		%{?with_verbose:V=1}

	%{__make} KBUILD=%{_kernelsrcdir} \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o \
		KVERS="%{_kernel_ver}" \
%ifarch %{x8664}
		CONFIG_X86_64=y \
%endif
		%{?with_verbose:V=1}
	 mv ndiswrapper{,-$cfg}.ko
done
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
cd driver
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install ndiswrapper-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ndiswrapper.ko
%if %{with smp} && %{with dist_kernel}
install ndiswrapper-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ndiswrapper.ko
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-net-ndiswrapper
%depmod %{_kernel_ver}

%postun	-n kernel-net-ndiswrapper
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-ndiswrapper
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-ndiswrapper
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
%files -n kernel-net-ndiswrapper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/ndiswrapper.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-ndiswrapper
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/ndiswrapper.ko*
%endif
%endif
