import asyncio

from prettytable import PrettyTable
from pyppeteer import launch
from pyppeteer.browser import Browser


async def songlist(driver: Browser, link: str):
    """
    歌单中歌曲列表
    :param driver:
    :param link: 歌单连接
    :return: 歌曲列表 {name,singer,album,link}
    """
    songlist = []
    page = await driver.newPage()
    await page.goto(link, options={"timeout": 0})
    try:
        while not await page.querySelector('.songlist-list-box'):
            await asyncio.sleep(1)
    except:
        pass

    list = await page.querySelectorAll('.songlist-item')
    for song in list:
        name = ''
        singer = ''
        album = ''
        link = ''

        namelink = await song.querySelector('div.songlist-inline.songlist-title > span > a')
        if namelink != None:
            nameProp = await namelink.getProperty('textContent')
            # 歌曲名称
            name = await nameProp.jsonValue()
            # 歌曲连接
            linkProp = await namelink.getProperty('href')
            link = await linkProp.jsonValue()

        singerlink = await song.querySelector(
            'div.songlist-inline.songlist-album.overdd.songlistheaderpercent > span > a')
        if singerlink != None:
            singerProp = await singerlink.getProperty('textContent')
            # 歌手
            singer = await singerProp.jsonValue()

        albumlink = await song.querySelector('a > div')
        if albumlink != None:
            albumProp = await albumlink.getProperty('textContent')
            # 专辑
            album = await albumProp.jsonValue()

        songlist.append({"name": str(name).strip().replace('\n','').replace(' ',''), "singer": str(singer).strip(), "album": str(album).strip(),
                         "link": str(link).strip()})
    await page.close()
    return songlist


async def start():
    """

    :return:
    """
    driver = await launch({'headless': False})
    page = await driver.newPage()
    await page.goto('https://www.baidu.com')
    print("等待点击右上方【新闻】按钮")
    await asyncio.sleep(1)
    ###自动点击
    newslink = await page.querySelector('#u1 > a:nth-child(1)')
    if newslink != None:
        await newslink.click()

    try:
        while not await page.querySelector('#channel-all'):
            await asyncio.sleep(1)
    except:
        pass

    print("等待点击上方【音乐】按钮")
    await asyncio.sleep(1)
    ###自动点击
    musiclink = await page.querySelector('#header-link-wrapper > li:nth-child(5) > a')
    if musiclink != None:
        await musiclink.click()

    try:
        while not await page.querySelector('.mod-hot-songlist'):
            await asyncio.sleep(1)
    except:
        pass

    print("到达音乐界面啦")

    # 获取热门歌单
    hot_songlist = await page.querySelectorAll(".to-2")
    for song in hot_songlist:
        a = await song.querySelector("a")
        hrefProp = await a.getProperty('href')
        href = await hrefProp.jsonValue()
        textProp = await a.getProperty('textContent')
        title = await textProp.jsonValue()
        list = await songlist(driver, href)
        print('===================================')
        print(href, title)
        table = PrettyTable(['歌曲名称', '歌手', '专辑', '链接'])
        for s in list:
            # print(s["name"], s["singer"], s["album"])
            table.add_row([s["name"], s["singer"], s["album"], s["link"]])
        print(table)

    await driver.close()


# 百度音乐热门歌单
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()
