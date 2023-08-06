#!/bin/bash
#

set -e

APK_VERSION="2.3.3"


cd "$(dirname "$0")"

#if test -f apk_version.txt -a "$APK_VERSION" = "$(cat apk_version.txt)"
#then
#	echo "apk version $APK_VERSION, already downloaded, exit"
#	exit
#fi

function download(){
	VERSION=$1
	NAME=$2
	URL="https://hmddevicerts.hmdglobal.com/hmd_uiautomator/$VERSION/$NAME"
	echo "$URL"
	curl -L "$URL" --output "$NAME"
}

download "$APK_VERSION" "app-release.apk"
download "$APK_VERSION" "app-debug-androidTest.apk"

unzip -tq app-uiautomator.apk && echo "$APK_VERSION" > apk_version.txt
