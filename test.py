import base64
from capstone_requests import *
# get the base64 encoding
with open("user-icon.png", "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())

# send the requests
image_req = Send_Image_Req()
#image_req.post_req(image_req.get_url(), image_req.create_payload("test", "test", "rami@email.com", b64_string.decode('utf-8')), Reqs.get_headers_noauth())
print(b64_string)
