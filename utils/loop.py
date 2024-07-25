def loop_z(zb: float, zt: float, dz: float):

    z = zt
    zp = None
    while True:
        z = max(z - dz, zb)
        if z == zp:
            break
        zp = z
        yield z
