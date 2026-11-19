# make-fun-news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Ktktkte/make-fun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Ktktkte/make-fun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026,
built as a newspaper front page:

- **Masthead** — the date, big: THURSDAY 19 NOVEMBER 2026.
- **Lead story** — Trump, Xi and Putin meet in Shenzhen: the first
  three-way summit of the three leaders, on the sidelines of APEC.
- **Culture** — Grand Theft Auto VI rolls out worldwide at midnight,
  market by market, starting in New Zealand after a 13-year wait.
- **Middle East** — the Gulf war widens to Kuwait: Iran strikes a US
  base; Kuwait and Bahrain say they repelled overnight drone attacks.
- **US politics** — House Democrats nominate Hakeem Jeffries for
  Speaker, 251–11, in line to be the first Black Speaker.
- **Weather** — Cyclone Akvan nears India's east coast, landfall due
  between Narsapur and Puri by noon Friday.
- **Europe** — the EU proposes a €45bn loan for Ukraine, repaid only
  once Russia pays war reparations.
- **Briefs** — Nvidia halts H-chip shipments to China; Voyager 1 is
  one light-day from Earth.

The three scene illustrations were drawn for this entry with a
Python/PIL script (see the build session); every fact on the page was
checked against wire-report digests of 19 November 2026 (Reuters, AP,
BBC, CNN, The Hindu, IMD, NASA). `main.ts` copies `entry.png`
byte-for-byte to the output directory, so both runs write identical
bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=md2m7pb0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
