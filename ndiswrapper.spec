#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace tools
%bcond_without	smp		# don't build SMP module
%bcond_without	up		# don't build UP module
#
Summary:	Tools to "wrap around" NDIS drivers
Summary(pl):	Narzêdzia "opakowuj±ce" sterowniki NDIS
Name:		ndiswrapper
Version:	0.12rc3
%define		_rel   1	
Release:	%{_rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	25d3607f23a870c555a90337a8abf3a9
URL:		http://ndiswrapper.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.8}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
ExclusiveArch:	%{ix86}
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
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel}
Requires:	dev >= 2.7.7-10
Requires:	%{name} = %{version}-%{_rel}

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
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel-smp}
Requires:	dev >= 2.7.7-10
Requires:	%{name} = %{version}-%{_rel}

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

%build
%if %{with userspace}
CFLAGS="%{rpmcflags}" %{__make} -C utils    
%endif

%if %{with kernel}
cd driver
# kernel module(s)
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
    if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
	exit 1
    fi
    rm -rf include
    install -d include/{linux,config}
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
    touch include/config/MARKER
    %{__make} gen_exports
    %{__make} -C %{_kernelsrcdir} clean \
	RCS_FIND_IGNORE="-name '*.ko' -o" \
	M=$PWD O=$PWD \
	%{?with_verbose:V=1}
    %{__make} -C %{_kernelsrcdir} modules \
	M=$PWD O=$PWD \
	%{?with_verbose:V=1}
    mv ndiswrapper{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT{/sbin,%{_sysconfdir}/ndiswrapper}
install utils/{ndiswrapper,loadndisdriver} \
	$RPM_BUILD_ROOT/sbin
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
