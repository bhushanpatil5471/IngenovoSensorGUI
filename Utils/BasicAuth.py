import os
import requests  # pip install requests==2.25.1


if __name__ == '__main__':
    # Send GET request to endpoint of choice with Basic Auth authentication.

    key=os.getenv('DT_SERVICE_ACCOUNT_KEY_ID','c3dfdtb531lg009b6bng')
    value=os.environ.get('DT_SERVICE_ACCOUNT_SECRET','665df80c49544406974a9a3d7905d351')
    # print(key)
    # print(value)

    device_listing = requests.get(
        url='https://api.d21s.com/v2/projects',
        auth=(
            key,
            value,
        )
    )

    # Print response contents.
    print(device_listing.json())
