from omnitools import IS_WIN32, def_template
from subprocess import run, PIPE
import threadwrapper
import shadowwalker
import threading
import requests
import time
import json
import os


def ping(host):
    output = run("chcp 65001 && ping -{} 1{} {}".format(
        "n" if IS_WIN32 else "c",
        " -w 500" if IS_WIN32 else " -W 1",
        host
    ), shell=True, stdout=PIPE, stderr=PIPE, close_fds=not IS_WIN32)
    if IS_WIN32:
        try:
            # print(output.stdout.decode())
            # print(output.stdout.decode().splitlines()[3].split("ms")[0].split("=")[-1])
            return float(output.stdout.decode().splitlines()[3].split("ms")[0].split("=")[-1])
        except:
            return 999
    else:
        try:
            return float(output.stdout.decode().splitlines()[-1].split(" ")[-2].split("/")[0])
        except:
            return 999


def benchmark(_10MB_file=None):
    _sw = shadowwalker.ShadowWalker()
    proxies = _sw.proxies
    sws = [None]*len(proxies)
    sws[0] = _sw
    bench = {}
    tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**3))
    for i, proxy in enumerate(proxies):
        def job(i, proxy):
            if not sws[i]:
                if sws[i-1].clash_port > 65000:
                    sws[i-1].clash_port = 7890
                sws[i] = sws[i-1].clone()
            sw = sws[i]
            p = threading.Thread(target=lambda: sw.start(proxy=proxy))
            p.daemon = True
            p.start()
            start = time.time()
            print(i + 1, len(sws))
            state = 0
            max_time = 10 if _10MB_file else 20

            def job2():
                nonlocal state
                link = _10MB_file
                if not link:
                    import megadownloader
                    md = megadownloader.MegaDownloader(proxies=[sw.proxy], db_i=i)
                    link = md.client.get_file_link("https://mega.nz/file/L8diRATC#Juh2xd4AduwyPBv9TW5UTLtrimRisNHEa0xYkWszfuQ")
                    md.stop()
                    os.remove("db_{}.db".format(i))
                r = requests.get(link, proxies={"all": sw.proxy}, timeout=max_time)
                if len(r.content) == 10 * 1024 * 1024:
                    state = 1

            p2 = threading.Thread(target=job2)
            p2.daemon = True
            p2.start()
            d = 10
            for j in range(0, max_time*d):
                time.sleep(1/d)
                if state:
                    break
            host = "{}:{}".format(proxy["server"], proxy["port"])
            bench[host] = [state, time.time() - start]
            print(i + 1, len(sws), *bench[host])
            open("bench.json", "wb").write(json.dumps(dict(sorted(bench.items(), key=lambda x: x[1][1]))).encode())
            sw.stop()
        tw.add(job=def_template(job, i, proxy))
    tw.wait()


def gse_availability():
    sw = shadowwalker.ShadowWalker()
    gse = []
    for i, proxy in enumerate(sw.proxies):
        sw.stop()
        time.sleep(1)
        p = threading.Thread(target=lambda: sw.start(proxy=proxy))
        p.daemon = True
        p.start()
        print(i + 1, len(sw.proxies))
        state = 0

        def job():
            nonlocal state
            r = requests.get("https://google.com/search?q=foxe6", proxies={"all": sw.proxy}, timeout=2)
            if b"foxe6.kozow.com" in r.content:
                state = 1

        p2 = threading.Thread(target=job)
        p2.daemon = True
        p2.start()
        for j in range(0, 2*20):
            time.sleep(2/20)
            if state:
                break
        host = "{}:{}".format(proxy["server"], proxy["port"])
        if state:
            gse.append(host)
        print(i + 1, len(sw.proxies), state)
        open("gse.json", "wb").write(json.dumps(gse).encode())
        sw.stop()

