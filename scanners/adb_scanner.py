import subprocess

class ADBScanner:

    def scan(self):
        # 1. Check if adb is installed and available
        try:
            res = subprocess.run(["adb", "version"], capture_output=True, text=True, timeout=3)
            if res.returncode != 0:
                raise FileNotFoundError()
        except (FileNotFoundError, Exception):
            return {
                "status": "error",
                "message": "Android Debug Bridge (ADB) not found on host. To scan your connected Android device, please download ADB platform-tools, add it to your system PATH, and enable USB Debugging on your phone."
            }

        # 2. Check for connected devices
        try:
            res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=5)
            lines = res.stdout.strip().split("\n")
            devices = []
            for line in lines[1:]:
                if line.strip() and "device" in line and "devices" not in line:
                    devices.append(line.split()[0])
                    
            if not devices:
                return {
                    "status": "error",
                    "message": "No Android device detected over USB. Make sure USB Debugging is enabled on your phone and it is connected via cable."
                }
            device_id = devices[0] # Scan the first detected device
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed checking USB devices: {str(e)}"
            }

        # 3. Scan the device properties
        report = {"status": "success", "device_id": device_id}
        
        def get_prop(prop_name):
            try:
                res = subprocess.run(["adb", "-s", device_id, "shell", "getprop", prop_name], capture_output=True, text=True, timeout=3)
                return res.stdout.strip()
            except:
                return "Unknown"

        def get_setting(namespace, key):
            try:
                res = subprocess.run(["adb", "-s", device_id, "shell", "settings", "get", namespace, key], capture_output=True, text=True, timeout=3)
                val = res.stdout.strip()
                if "invalid" in val.lower() or "null" in val.lower():
                    return "0"
                return val
            except:
                return "0"

        # Device Identity
        brand = get_prop("ro.product.brand").upper()
        model = get_prop("ro.product.model").upper()
        release = get_prop("ro.build.version.release")
        patch = get_prop("ro.build.version.security_patch")
        
        report["device_info"] = {
            "brand": brand,
            "model": model,
            "android_version": release,
            "security_patch": patch
        }

        # Security Configurations
        report["security_config"] = {
            "usb_debugging": get_setting("global", "adb_enabled") == "1",
            "install_non_market_apps": get_setting("global", "install_non_market_apps") == "1",
            "mock_locations": get_setting("secure", "mock_location") == "1"
        }

        # Third Party Apps
        try:
            res = subprocess.run(["adb", "-s", device_id, "shell", "pm", "list", "packages", "-3"], capture_output=True, text=True, timeout=5)
            packages = []
            for line in res.stdout.strip().split("\n"):
                if line.strip() and line.startswith("package:"):
                    packages.append(line.replace("package:", "").strip())
            report["third_party_apps"] = {
                "count": len(packages),
                "list": packages[:15] # Return first 15 packages to keep payload clean
            }
        except:
            report["third_party_apps"] = {"count": 0, "list": []}

        return report
