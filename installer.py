import hashlib
import os
import requests
import subprocess

vlc_download_url = "https://get.videolan.org/vlc/3.0.16/win64/vlc-3.0.16-win64.exe"
EXPECTED_SHA256 = "2f2b7a0476d728528d7e45631c3f6ab4b6e4a10baa4b3c3e41e44a1635de5f5b"


def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)


def get_expected_sha256():
    response = requests.get(vlc_download_url + ".sha256")
    expected_sha256 = response.content.decode().split()[0]
    return expected_sha256


def download_installer():
    response = requests.get(vlc_download_url)
    installer_data = response.content
    return installer_data


def installer_ok(installer_data, expected_sha256):
    computed_sha256 = hashlib.sha256(installer_data).hexdigest()
    return computed_sha256 == expected_sha256


def save_installer(installer_data):
    installer_path = "vlc_installer.exe"
    with open(installer_path, "wb") as f:
        f.write(installer_data)
    return installer_path


def run_installer(installer_path):
    subprocess.call([installer_path, "/S"])


def delete_installer(installer_path):
    os.remove(installer_path)


if __name__ == "__main__":
    main()
