require('dotenv').config();
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));

// ✅ Load required headers from environment
const _userAgent = process.env.USER_AGENT;
const _xIgAppId = process.env.X_IG_APP_ID;

if (!_userAgent || !_xIgAppId) {
  console.error("❌ Missing USER_AGENT or X_IG_APP_ID in .env file");
  process.exit(1);
}

// ✅ Extract IG shortcode from URL
const getId = (url) => {
  const regex = /instagram\.com\/(?:[A-Za-z0-9_.]+\/)?(p|reels?|stories)\/([A-Za-z0-9-_]+)/;
  const match = url.match(regex);
  return match && match[2] ? match[2] : null;
};

// ✅ Fetch IG GraphQL data
const getInstagramGraphqlData = async (url) => {
  const igId = getId(url);
  if (!igId) return "❌ Invalid Instagram Reel/Post URL";

  const graphql = new URL("https://www.instagram.com/api/graphql");
  graphql.searchParams.set("variables", JSON.stringify({ shortcode: igId }));
  graphql.searchParams.set("doc_id", "10015901848480474");
  graphql.searchParams.set("lsd", "AVqbxe3J_YA");

  try {
  const response = await fetch(graphql, {
    method: "POST",
    headers: {
      "User-Agent": _userAgent,
      "Content-Type": "application/x-www-form-urlencoded",
      "X-IG-App-ID": _xIgAppId,
      "X-FB-LSD": "AVqbxe3J_YA",
      "X-ASBD-ID": "129477",
      "Sec-Fetch-Site": "same-origin"
    }
  });

  const json = await response.json();
    const items = json?.data?.xdt_shortcode_media;

    if (!items) {
      console.log("❌ No media data found in response");
      return "❌ Could not parse media data";
    }

    // Return custom json object with all available data
  return {
      __typename: items?.__typename,
      shortcode: items?.shortcode,
      dimensions: items?.dimensions,
      display_url: items?.display_url,
      display_resources: items?.display_resources,
      has_audio: items?.has_audio,
      video_url: items?.video_url,
      video_view_count: items?.video_view_count,
      video_play_count: items?.video_play_count,
      is_video: items?.is_video,
      caption: items?.edge_media_to_caption?.edges[0]?.node?.text,
      is_paid_partnership: items?.is_paid_partnership,
      location: items?.location,
      owner: items?.owner,
      product_type: items?.product_type,
      video_duration: items?.video_duration,
      thumbnail_src: items?.thumbnail_src,
      clips_music_attribution_info: items?.clips_music_attribution_info,
      sidecar: items?.edge_sidecar_to_children?.edges,
    };
  } catch (error) {
    console.error("❌ Error:", error);
    return "❌ Error fetching data: " + error.message;
  }
};

// ✅ MAIN FUNCTION
(async () => {
  const inputUrl = process.argv[2]; // Get from command line
  if (!inputUrl) {
    console.error("❌ Please pass a reel/post URL as an argument.");
    console.error("Example: node instagram_scraper_v2.js https://www.instagram.com/reel/CtjoC2BNsB2");
    process.exit(1);
  }

  const result = await getInstagramGraphqlData(inputUrl);
  console.log("✅ Scraped Data:\n", JSON.stringify(result, null, 2));
})();
