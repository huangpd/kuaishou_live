from DrissionPage import ChromiumPage, ChromiumOptions
import time
import requests
import threading

index = 0


def get_live_info(eid):
    co = ChromiumOptions()
    # co.set_user_agent(
    #     'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1')
    co.set_user_agent(
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1')
    # co.set_proxy('ip:port') #设置代理非常重要
    co.set_argument('--no-sandbox')  # 无沙盒模式
    co.incognito(True)
    # co.auto_port()
    page = ChromiumPage(addr_or_opts=co)

    try:
        page.listen.start('livev.m.chenzhongtech.com/rest/k/live/byUser?kpn=GAME_ZONE&kpf=')

        page.get(f'https://live.kuaishou.com/u/{eid}')
        time.sleep(3)
        # print(page.html)
        if 'captcha' in page.url:
            print('验证码')
            page.close()
            page.quit()
            while True:

                global index
                print(index)

                index += 1
                if index == 6:
                    break
                return get_live_info(eid)

        for _ in range(2):
            # page.refresh()
            if page.url == f'https://live.kuaishou.com/u/{eid}' or 'captcha' in page.url:
                page.quit()
                return get_live_info(eid)

            res = page.listen.wait()
            time.sleep(2)
            # print(res)
            # print(res.response.body)
            if res.response.body:
                data = res.response.body
                print(data)
                if data.get('error_msg') == '操作太快了，请稍微休息一下':
                    page.close()
                    page.quit()
                    return get_live_info(eid)

                liveStreamId = data['liveStream']['liveStreamId']
                kwaiId = data['liveStream']['userEid']
                token = data['token']
                webSocketAddresses = data['webSocketAddresses'][0]
                page.quit()
                return liveStreamId, kwaiId, token, webSocketAddresses

    except:
        page.quit()
