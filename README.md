# 浪日誌 WaveLog（PWA 版）

記錄自己每一次下水的衝浪日誌。單一 HTML 的 PWA，手機加入主畫面即可使用。

- **線上網址**：https://vanessachuchu.github.io/wavelog-web/
- **資料**：全部存手機本機（IndexedDB），並可同步到私人 repo [`wavelog-data`](https://github.com/vanessachuchu/wavelog-data)（記錄 JSON＋照片影片）。這個公開 repo 只有 app 本體，沒有任何個人資料。
- **預報**：Open-Meteo 海象 API（免費）自動帶入浪高/週期/風；app 內嵌 Windy 浪圖與 Swelleye 預報（座標式內嵌頁，非官方嵌入服務，失效時僅該區塊無法顯示）；浪點可外連 Swelleye。
- **AI 分析**：把當天照片（含影片抽格）＋預報快照＋心得送給 Claude，分析預報準不準（Anthropic API key 只存本機）。

## 開發

沒有 build step。改 `index.html` 直接 push 就是部署；`sw.js` 是 network-first，重新整理即拿到新版。

Icon 來源是 `icons/illustration.svg`（手繪衝浪插圖）。改插圖後重產 PNG：
```bash
qlmanage -t -s 512 -o /tmp icons/illustration.svg
cp /tmp/illustration.svg.png icons/icon-512.png
sips -z 192 192 icons/icon-512.png --out icons/icon-192.png
sips -z 180 180 icons/icon-512.png --out icons/apple-touch-icon.png
```
（`scripts/make-icons.py` 是舊版幾何 icon 產生器，已不再使用。）
