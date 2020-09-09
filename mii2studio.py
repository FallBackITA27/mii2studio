import sys
from struct import pack
from binascii import hexlify

if len(sys.argv) < 4:
    print("Usage: python mii2studio.py <input switch mii file> <output studio mii file> <type (switch/wii/3ds/wiiu/miitomo)>")
    exit()

if sys.argv[3] == "wii":
    from gen1_wii import Gen1Wii
    orig_mii = Gen1Wii.from_file(sys.argv[1])
elif sys.argv[3] == "3ds" or sys.argv[3] == "wiiu" or sys.argv[3] == "miitomo":
    from gen2_wiiu_3ds_miitomo import Gen2Wiiu3dsMiitomo
    orig_mii = Gen2Wiiu3dsMiitomo.from_file(sys.argv[1])
elif sys.argv[3] == "switch":
    from gen3_switch import Gen3Switch
    orig_mii = Gen3Switch.from_file(sys.argv[1])

studio_mii = {}


def u8(data):
    return pack(">B", data)

makeup = {
    1: 1,
    2: 6,
    3: 9,
    9: 10
}

wrinkles = {
    4: 5,
    5: 2,
    6: 3,
    7: 7,
    8: 8,
    10: 9,
    11: 11
}

studio_mii["facial_hair_color"] = orig_mii.facial_hair_color
studio_mii["beard_goatee"] = orig_mii.facial_hair_beard
studio_mii["body_weight"] = orig_mii.body_weight
if sys.argv[3] == "wii":
    studio_mii["eye_stretch"] = 3
else:
    studio_mii["eye_stretch"] = orig_mii.eye_stretch
if sys.argv[3] != "switch":
    studio_mii["eye_color"] = orig_mii.eye_color + 8
else:
    studio_mii["eye_color"] = orig_mii.eye_color
studio_mii["eye_rotation"] = orig_mii.eye_rotation
studio_mii["eye_size"] = orig_mii.eye_size
studio_mii["eye_type"] = orig_mii.eye_type
studio_mii["eye_horizontal"] = orig_mii.eye_horizontal
studio_mii["eye_vertical"] = orig_mii.eye_vertical
if sys.argv[3] == "wii":
    studio_mii["eyebrow_stretch"] = 3
else:
    studio_mii["eyebrow_stretch"] = orig_mii.eyebrow_stretch
studio_mii["eyebrow_color"] = orig_mii.eyebrow_color
studio_mii["eyebrow_rotation"] = orig_mii.eyebrow_rotation
studio_mii["eyebrow_size"] = orig_mii.eyebrow_size
studio_mii["eyebrow_type"] = orig_mii.eyebrow_type
studio_mii["eyebrow_horizontal"] = orig_mii.eyebrow_horizontal
if sys.argv[3] != "switch":
    studio_mii["eyebrow_vertical"] = orig_mii.eyebrow_vertical
else:
    studio_mii["eyebrow_vertical"] = orig_mii.eyebrow_vertical + 3
studio_mii["face_color"] = orig_mii.face_color
if sys.argv[3] == "wii":
    if orig_mii.facial_feature in makeup:
        studio_mii["face_makeup"] = makeup[orig_mii.facial_feature]
    else:
        studio_mii["face_makeup"] = 0
else:
    studio_mii["face_makeup"] = orig_mii.face_makeup
studio_mii["face_type"] = orig_mii.face_type
if sys.argv[3] == "wii":
    if orig_mii.facial_feature in wrinkles:
        studio_mii["face_wrinkles"] = wrinkles[orig_mii.facial_feature]
    else:
        studio_mii["face_wrinkles"] = 0
else:
    studio_mii["face_wrinkles"] = orig_mii.face_wrinkles
studio_mii["favorite_color"] = orig_mii.favorite_color
studio_mii["gender"] = orig_mii.gender
studio_mii["glasses_color"] = orig_mii.glasses_color
studio_mii["glasses_size"] = orig_mii.glasses_size
studio_mii["glasses_type"] = orig_mii.glasses_type
studio_mii["glasses_vertical"] = orig_mii.glasses_vertical
studio_mii["hair_color"] = orig_mii.hair_color
studio_mii["hair_flip"] = orig_mii.hair_flip
studio_mii["hair_type"] = orig_mii.hair_type
studio_mii["body_height"] = orig_mii.body_height
studio_mii["mole_size"] = orig_mii.mole_size
studio_mii["mole_enable"] = orig_mii.mole_enable
studio_mii["mole_horizontal"] = orig_mii.mole_horizontal
studio_mii["mole_vertical"] = orig_mii.mole_vertical
if sys.argv[3] == "wii":
    studio_mii["mouth_stretch"] = 3
else:
    studio_mii["mouth_stretch"] = orig_mii.mouth_stretch
studio_mii["mouth_color"] = orig_mii.mouth_color
studio_mii["mouth_size"] = orig_mii.mouth_size
studio_mii["mouth_type"] = orig_mii.mouth_type
studio_mii["mouth_vertical"] = orig_mii.mouth_vertical
studio_mii["beard_size"] = orig_mii.facial_hair_size
studio_mii["beard_mustache"] = orig_mii.facial_hair_mustache
studio_mii["beard_vertical"] = orig_mii.facial_hair_vertical
studio_mii["nose_size"] = orig_mii.nose_size
studio_mii["nose_type"] = orig_mii.nose_type
studio_mii["nose_vertical"] = orig_mii.nose_vertical

with open(sys.argv[2], "wb") as f:
    mii_data = b""
    n = r = 256
    mii_data += hexlify(u8(0))
    for v in studio_mii.values():
        eo = (7 + (v ^ n)) % 256
        n = eo
        mii_data += hexlify(u8(eo))
        f.write(u8(v))

    f.close()

    print("https://studio.mii.nintendo.com/miis/image.png?data=" + mii_data.decode("utf-8") + "&type=face&width=512&instanceCount=1")
