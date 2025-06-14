const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

const username = process.argv[2];
if (!username) {
  console.error('❌ Please provide an Instagram username as an argument.');
  console.error('Example: node get_recent_reels.js nasa');
  process.exit(1);
}

const REELS_URL = `https://www.instagram.com/${username}/reels/`;

(async () => {
  try {
    const res = await fetch(REELS_URL, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html',
      },
    });
    const html = await res.text();
    // Find the window._sharedData or window.__additionalDataLoaded JSON
    const jsonMatch = html.match(/<script type="application\/ld\+json">(.*?)<\/script>/s);
    let shortcodes = [];
    if (jsonMatch) {
      // Try to parse the ld+json block (not always present)
      try {
        const ldJson = JSON.parse(jsonMatch[1]);
        if (ldJson && ldJson.mainEntity && Array.isArray(ldJson.mainEntity.itemListElement)) {
          shortcodes = ldJson.mainEntity.itemListElement
            .map(item => item.url)
            .filter(url => url && url.includes('/reel/'))
            .map(url => url.split('/reel/')[1].replace(/\/$/, ''));
        }
      } catch {}
    }
    // Fallback: look for shortcodes in the page source
    if (shortcodes.length === 0) {
      const shortcodeMatches = [...html.matchAll(/"shortcode":"([A-Za-z0-9_-]{8,})"/g)];
      shortcodes = shortcodeMatches.map(m => m[1]);
    }
    // Remove duplicates and limit to 12
    const uniqueShortcodes = [...new Set(shortcodes)].slice(0, 12);
    const reelUrls = uniqueShortcodes.map(sc => `https://www.instagram.com/reel/${sc}/`);
    console.log(JSON.stringify(reelUrls, null, 2));
  } catch (err) {
    console.error('❌ Error fetching or parsing reels:', err.message);
    process.exit(1);
  }
})(); 