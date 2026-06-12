from androguard.core.apk import APK


class APKScanner:

    def scan(self, apk_path):

        try:

            apk = APK(apk_path)

            return {
                "app_name": apk.get_app_name(),
                "package": apk.get_package(),
                "version": apk.get_androidversion_name(),
                "permissions": apk.get_permissions()
            }

        except Exception as e:

            return {
                "error": str(e)
            }