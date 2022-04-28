# zstd-rpm

Building zstd RPMs on CentOS 7 or AlmaLinux 8 or RockyLinux 8



### Prerequsites


Install RPMBuild

    yum install rpm-build

Install zstd requirements

    yum install make gcc gtest-devel lz4-devel xz-devel gcc-c++ zlib-devel prelink


### Getting Ready

RPMBuild will create the following directories in /root

    ls -lF /root/rpmbuild/

    drwxr-xr-x. 4 root root 44 Apr 27 16:36 BUILD/
    drwxr-xr-x. 2 root root  6 Apr 27 16:37 BUILDROOT/
    drwxr-xr-x. 3 root root 20 Apr 27 16:37 RPMS/
    drwxr-xr-x. 2 root root 31 Apr 27 16:55 SOURCES/
    drwxr-xr-x. 2 root root 23 Apr 27 16:01 SPECS/
    drwxr-xr-x. 2 root root 38 Apr 27 16:37 SRPMS/


Inside the `SPECS` directory place `zstd.spec` from the `SPECS` folder of this repository

Inside the `SOURCES` directory download (wget) the `zstd-1.5.2.tar.gz` release

    wget https://github.com/facebook/zstd/releases/download/v1.5.2/zstd-1.5.2.tar.gz

#### Building zstd

Change diretory (cd) into the `SPECS` folder,

    cd SPECS

Then issue the build command with,

    rpmbuild -ba zstd.spec

The build RPM(s) will appear in the `RPMS/x86_64` folder as,

    -rw-r--r--. 1 root root  284256 Apr 27 16:37 libzstd-1.5.2-1.el7.x86_64.rpm
    -rw-r--r--. 1 root root   43648 Apr 27 16:37 libzstd-devel-1.5.2-1.el7.x86_64.rpm
    -rw-r--r--. 1 root root  277156 Apr 27 16:37 libzstd-static-1.5.2-1.el7.x86_64.rpm
    -rw-r--r--. 1 root root  433764 Apr 27 16:37 zstd-1.5.2-1.el7.x86_64.rpm
    -rw-r--r--. 1 root root 4000220 Apr 27 16:37 zstd-debuginfo-1.5.2-1.el7.x86_64.rpm

zstd-1.5.2-1.el7.x86_64.rpm is the most important file for us which can now be installed on other machines as needed.

Note,

- The `el7` part of the filename will change (possiblty) to `el8` or `el9` depending on your build platform/where you are building this RPM


#### References and more

- SPEC File was derived from: https://src.fedoraproject.org/rpms/zstd/blob/rawhide/f/zstd.spec
- Tests are disabled/removed
- PATCH-1 (pzstd.1.patch) and PATCH-2 (enable-CET.patch) have been removed as well