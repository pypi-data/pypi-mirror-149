def export_rgp(meta, data):
    """
    Export data in JSON RGP format

    meta - is the info from the scans table
    data - is the drilling torques

    Todo: does the db contain all the info required to reconsitute the RGP file?
    """

    def time2dict(t):
        import arrow
        t = arrow.get(t)
        return {
            'dateYear': t.year,
            'dateMonth': t.month,
            'dateDay': t.day,
            'timeHour': t.hour,
            'timeMinute': t.minute,
            'timeSecond': t.second
        }

    # define a map from db to rgp
    db2json = {
        'instrument': lambda x: {'header':{'snrMachine': x}},
        'scanTime': lambda x: {'header': time2dict(x)},
        'scannedBy': (),
        'importTime': (),
        'importedBy': (),
        'importFilename': lambda x: {'provenance': '%s -> IMLresi db -> rgp.py::export_rgp()' % (x,)},
        'importComment': (),
        'resiId': lambda x: {'header': {'idNumber': x}},
        'resiComment': lambda x: {'header': {'remark': x}},
        'feedRate_cm1min-1': lambda x: {'header': {'speedFeed': x}},
        'rotationalSpeed_rpm': lambda x: {'header': {'speedDrill': x}},
        'pointSpacing_mm': lambda x: {'header': {'resolutionFeed': int((1./x))}},
        'npoints': (),
        'SNRelectronic': lambda x: {'header':{'snrElectronic': x}},
        'hardwareVersion': lambda x: {'header':{'verElectronic': x}},
        'rgpSHA256': (),
        'sampleType': (),
        "offsetFeed": lambda x: {'header':{'offsetFeed': x}},
        "offsetDrill": lambda x: {'header':{'offsetDrill': x}},
        "resolutionAmp": lambda x: {'header':{'resolutionAmp': x}},
    }

    def construct_rgp_v1(mapdict, meta, data):
        """
        mapdict maps from meta to rgp (*NOT* from rgp to meta!!!)

        data needs to have keys drill and feed
        """

        rgp = {
            "device": "0F02", # this is required to be present for read_json() to be happy
            #"version": 2, # ???
            "header": {
                #"snrMachine": "PD400-0000",
                #"verFirmware": "1.76",
                #"memoryId": "070920101407",
                #"number": 1,
                #"deviceLength": 40.15,
                #"depthMode": 0,
                #"depthPresel": 0.0,
                #"depthMsmt": 22.48,
                #"ampMaxFeed": 38.1,
                #"ampMaxDrill": 46.52,
                #"abortState": 3,
                #"feedOn": 0,
                #"ncOn": 0,
                #"ncState": 0,
                #"tiltOn": 0,
                #"tiltRelOn": 0,
                #"tiltRelAngle": 0.0,
                #"tiltAngle": 0.0,
                #"diameter": 0.0,
                #"wiInstalled": 0,
                #"wi": {}
            },
            "profile": {},
            #"wiPoleResult": {},
            #"app":{},
            #"assessment":{}
        }

        for k in ('drill','feed'):
            try:
                rgp[k] = list(map(float, data[k]))
            except KeyError:
                logging.warning("missing %s data" % k)

        for k in meta:
            if k not in mapdict: continue
            f = mapdict[k]
            if not f: continue
            rgp = dict_fmerge(rgp, f(meta[k]))
            #print(k, rgp)

        return rgp

    rgp = construct_rgp(db2json, meta, {'drill': data})

    import json
    return json.dumps(rgp, indent=2, sort_keys=True)


def export_txt(meta, data):
    """
    Export data in Resi ASCII format, e.g. for use with GeoffD software.
    """
    meta['date'] = meta['scanTime'].strftime('%d.%m.%Y')
    meta['time'] = meta['scanTime'].strftime('%H:%M:%S')
    meta['drillingDepth'] = int(meta['npoints']*meta['pointSpacing_mm'])
    meta['feedSpeed'] = meta['feedRate_cm1min-1']
    meta['needleSpeed'] = meta['rotationalSpeed_rpm']
    meta['firmwareVersion'] = 0.00
    meta['nSamplesPerMm'] = int(1./meta['pointSpacing_mm'])
    meta['maxDrillingDepthInstrument'] = '04013'
    meta['resolutionAmplitude'] = '10000'
    s = """{scanId:03d}
{firmwareVersion}
{instrument}
{SNRelectronic}
{hardwareVersion}
{resiId}
{date}
{time}
{nSamplesPerMm}
{resolutionAmplitude}
{maxDrillingDepthInstrument}
0
00000
{drillingDepth:05d}
{feedSpeed}
{needleSpeed}
0076
0319
02739
04565
3
0
0
0
0
0
+00,0
000,0
+00,0
000,0
0
0
0
0
0
000
00000
0
0
000
000
00000
0
0
0
000
00000


0
0
0
00000
000
00000
0
000
000
000
00000
00000
000
000
00000
000
000
00000
000
000
00000
0
0
0
00000
00000
000
000
00,0
000
000
000
00000
000
000
0
0
0
00000
000
00000
000
000
0
0
0
00000
00000
00000
00000
00000
00000
0
0
000
00000
000
0
000
00000
000
0
00000
000000




00000-00000:
00000-00000:
00000-00000:
00000-00000:
00000-00000:
00000-00000:
{resiComment}





""".format(**meta)
    for d in data:
        s += "%05i\n" % d
    return s
