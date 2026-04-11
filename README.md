# PermaDrop

**Archive every URL in your Word documents to [perma.cc](https://perma.cc)** — turning citations into permanent, tamper-proof links for legal scholarship.

**將 Word 文件中的每一個網址封存至 [perma.cc](https://perma.cc)** — 為法律學術寫作建立永久、不可篡改的引用連結。

🔗 **[permadrop.kirinchang.com](https://permadrop.kirinchang.com)**

---

## What it does / 功能說明

PermaDrop reads `.docx` files directly in your browser, extracts every URL from footnotes, endnotes, and body text, then archives them to perma.cc via the official API — inserting permanent perma.cc links back into a clean or redline copy of your document.

PermaDrop 在您的瀏覽器中直接讀取 `.docx` 檔案，從腳注、尾注與本文中擷取所有網址，透過 perma.cc 官方 API 進行封存，並將永久連結插回修改後的文件（提供乾淨版與修訂標記版）。

- ✅ Multiple files at once／支援同時上傳多個檔案
- ✅ Clean copy or Redline (Track Changes)／乾淨版或修訂標記版（Track Changes）
- ✅ CSV archive report／CSV 封存報告
- ✅ Existing perma.cc links detected and skipped／自動偵測並略過已有的 perma.cc 連結
- ✅ Wayback Machine fallback on capture failure／封存失敗時自動提供 Wayback Machine 備援
- ✅ Everything runs in your browser — no upload, no server／所有處理均在瀏覽器本地執行，不上傳、無伺服器

---

## Usage / 使用方式

1. Open [permadrop.kirinchang.com](https://permadrop.kirinchang.com)／開啟工具網址
2. Paste your [perma.cc API key](https://perma.cc/settings/tools)／貼上您的 perma.cc API 金鑰
3. Choose an archive folder／選擇封存資料夾
4. Upload your `.docx` file(s)／上傳 `.docx` 文件（可多檔）
5. Select URLs to archive → **Archive Selected**／勾選要封存的網址 → 按下封存
6. Download the modified document／下載修改後的文件

---

## Privacy / 隱私說明

Your documents and API key never leave your device. All processing happens client-side in JavaScript.

您的文件與 API 金鑰不會離開您的裝置。所有處理均於瀏覽器本地的 JavaScript 中執行。

---

## License / 授權

Copyright (C) 2026 [Kirin Chang](https://kirinchang.com)

Licensed under the [GNU Affero General Public License v3.0](LICENSE).

If you modify this tool and offer it as a network service, you must make your modified source code available under the same license.

本工具採用 [GNU Affero 通用公共授權條款第 3 版（AGPL-3.0）](LICENSE)。若您修改本工具並以網路服務形式提供，須以相同授權條款公開修改後的原始碼。
