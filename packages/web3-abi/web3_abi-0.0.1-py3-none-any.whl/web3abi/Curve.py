def _load_json(file_path):
    import json
    import pkg_resources

    ifile = pkg_resources.resource_stream(__name__, file_path)
    d = json.load(ifile)
    return d


CURVE_TRICRYPTO_ABI = _load_json("json/Curve_tricrypto.json")
CURVE_TRICRYPTO_MATH_ABI = _load_json("json/Curve_tricrypto_math.json")
CURVE_TRICRYPTO_VIEW_ABI = _load_json("json/Curve_tricrypto_view.json")
